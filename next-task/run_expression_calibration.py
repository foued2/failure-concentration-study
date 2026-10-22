"""Run the frozen expression banks against the prespecified calibration panel."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import time
import uuid
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PILOT = REPO / "natural-feasibility-pilot"
PIPELINE = PILOT / "python-pipeline-integration"
EXPRESSION_PIPELINE = ROOT / "pipeline_expression"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PILOT))
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(PIPELINE))

import run_generated_smoke as suite_runner
from expression_mutants import VARIANT_ORDER, VARIANTS
from expression_task import FAMILY_ORDER, evaluate_ast, validate_bank
from integration_runner import CaptureRejected, parse_worker_scalar
from source_policy import screen_source

BANKS = ROOT / "banks"
DIAGNOSTIC = BANKS / "diagnostic.json"
EVALUATION = BANKS / "evaluation.json"
FREEZE = BANKS / "FREEZE.json"
MANIFEST = BANKS / "BUILD_MANIFEST.json"
PROTOCOL = ROOT / "CALIBRATION_PROTOCOL_2026-10-22.md"
RUN = ROOT / f"calibration-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{uuid.uuid4().hex[:8]}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def status_counts(rows: list[dict]) -> dict[str, int]:
    return dict(sorted(Counter(row["status"] for row in rows).items()))


def failure_counts(rows: list[dict]) -> dict[str, int]:
    counts = {family: 0 for family in FAMILY_ORDER}
    for row in rows:
        if row["status"] != "pass":
            counts[row["family"]] += 1
    return counts


def load_frozen_banks() -> tuple[list[dict], list[dict], dict]:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    if freeze.get("status") != "FROZEN_FOR_CALIBRATION":
        raise RuntimeError("expression banks are not frozen for calibration")
    if freeze.get("no_model_calls") is not True:
        raise RuntimeError("freeze record does not attest zero model calls")
    if freeze["manifest_sha256"] != sha256_file(MANIFEST):
        raise RuntimeError("bank manifest changed after freeze")
    diagnostic_doc = json.loads(DIAGNOSTIC.read_text(encoding="utf-8"))
    evaluation_doc = json.loads(EVALUATION.read_text(encoding="utf-8"))
    for doc, freeze_entry, id_key in (
        (diagnostic_doc, freeze["diagnostic"], "probe_id"),
        (evaluation_doc, freeze["evaluation"], "hid"),
    ):
        if doc.get("task_id") != freeze["task_id"]:
            raise RuntimeError("bank task identity does not match freeze record")
        if sha256_file(BANKS / "diagnostic.json") != freeze["diagnostic"]["sha256"]:
            raise RuntimeError("diagnostic bank changed after freeze")
        if sha256_file(BANKS / "evaluation.json") != freeze["evaluation"]["sha256"]:
            raise RuntimeError("evaluation bank changed after freeze")
        records = doc["records"]
        validate_bank(records, 5)
        ids = [record.get(id_key) for record in records]
        if len(ids) != 30 or None in ids or len(set(ids)) != 30:
            raise RuntimeError("bank record identities are not unique")
        if any(evaluate_ast(record["expr"]) != record["expected"] for record in records):
            raise RuntimeError("bank expected value disagrees with the AST oracle")
        counts = Counter(record["family"] for record in records)
        if set(counts) != set(FAMILY_ORDER) or set(counts.values()) != {5}:
            raise RuntimeError("bank is not five records per family")
    diagnostic = diagnostic_doc["records"]
    evaluation = evaluation_doc["records"]
    if {record["expr"] for record in diagnostic} & {record["expr"] for record in evaluation}:
        raise RuntimeError("diagnostic and evaluation expression strings overlap")
    return diagnostic, evaluation, freeze


def expression_outcome(raw: dict, entry: dict, phase: str) -> dict:
    expected = entry["expected"]
    parsed = None
    error = None
    correct = False
    if raw["status"] == "complete" and raw["exit_code"] == 0 and not raw["timed_out"]:
        try:
            parsed = parse_worker_scalar(raw)
            correct = type(parsed) is int and parsed == expected
        except CaptureRejected as exc:
            error = str(exc)
    else:
        error = raw["status"]
    status = "pass" if correct else "wrong" if parsed is not None else "invalid" if raw["status"] == "complete" else raw["status"]
    return {
        "phase": phase,
        "probe_id": entry["probe_id"],
        "family": entry["family"],
        "expr": entry["input"]["expr"],
        "expected": expected,
        "solver_output": parsed,
        "correct": correct,
        "status": status,
        "error": error,
        "raw_stdout_b64": raw["stdout_b64"],
        "raw_stderr_b64": raw["stderr_b64"],
        "exit_code": raw["exit_code"],
        "timed_out": raw["timed_out"],
        "tree_terminated": raw["tree_terminated"],
        "worker_elapsed_ms": raw.get("elapsed_ms"),
    }


def main() -> None:
    if RUN.exists():
        raise FileExistsError(RUN)
    if not PROTOCOL.is_file():
        raise FileNotFoundError(PROTOCOL)
    if not suite_runner.previous.SANDBOX.is_file() or not suite_runner.previous.PYTHON_BASE.is_dir():
        raise RuntimeError("Windows Sandbox or the Python runtime is unavailable")
    suite_runner.previous.check_no_running_sandbox()
    diagnostic, evaluation, freeze = load_frozen_banks()

    RUN.mkdir()
    (RUN / "guest-captures").mkdir()
    (RUN / "variants").mkdir()
    suite_runner.RUN = RUN
    suite_runner.PIPELINE = EXPRESSION_PIPELINE

    panel = {
        "order": VARIANT_ORDER,
        "targets": {name: VARIANTS[name]["target_family"] for name in VARIANT_ORDER},
        "defects": {name: VARIANTS[name]["defect"] for name in VARIANT_ORDER},
        "sources": {name: VARIANTS[name]["source"] for name in VARIANT_ORDER},
    }
    write_json(RUN / "PANEL.json", panel)
    source_hashes = {
        "run_expression_calibration.py": sha256_file(Path(__file__).resolve()),
        "expression_mutants.py": sha256_file(ROOT / "expression_mutants.py"),
        "expression_task.py": sha256_file(ROOT / "expression_task.py"),
        "build_expression_banks.py": sha256_file(ROOT / "build_expression_banks.py"),
        "freeze_expression_banks.py": sha256_file(ROOT / "freeze_expression_banks.py"),
        "calibration_protocol": sha256_file(PROTOCOL),
        "banks/FREEZE.json": sha256_file(FREEZE),
        "banks/diagnostic.json": sha256_file(DIAGNOSTIC),
        "banks/evaluation.json": sha256_file(EVALUATION),
        "run_generated_smoke.py": sha256_file(PILOT / "run_generated_smoke.py"),
        "source_policy.py": sha256_file(PILOT / "source_policy.py"),
        "integration_runner.py": sha256_file(PILOT / "integration_runner.py"),
        "python-pipeline-integration/python_adapter.py": sha256_file(PIPELINE / "python_adapter.py"),
        "python-pipeline-integration/sandbox_suite_supervisor.ps1": sha256_file(PIPELINE / "sandbox_suite_supervisor.ps1"),
        "pipeline_expression/python_adapter.py": sha256_file(EXPRESSION_PIPELINE / "python_adapter.py"),
        "pipeline_expression/sandbox_suite_supervisor.ps1": sha256_file(EXPRESSION_PIPELINE / "sandbox_suite_supervisor.ps1"),
    }
    started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    protocol_record = {
        "schema": 1,
        "run_id": RUN.name,
        "started_utc": started_utc,
        "purpose": "hand-built expression defect coverage check against the frozen banks",
        "no_model_calls": True,
        "model_calls": 0,
        "generation_attempts": 0,
        "bank_sizes": {"diagnostic": len(diagnostic), "evaluation": len(evaluation)},
        "input_hashes": {
            "diagnostic.json": freeze["diagnostic"]["sha256"],
            "evaluation.json": freeze["evaluation"]["sha256"],
            "FREEZE.json": sha256_file(FREEZE),
        },
        "source_hashes": source_hashes,
        "panel_sha256": sha256_text(json.dumps(panel, sort_keys=True, separators=(",", ":"))),
        "criteria": {
            "reference_control": "30/30 diagnostic passes and 30/30 evaluation inputs correct",
            "faulty_target_diagnostic": "all five target-family probes fail",
            "faulty_target_evaluation": "all five target-family inputs fail",
            "cross_family": "no non-target family failures",
            "transport": "every row is tree-terminated and not timed out",
        },
    }
    write_json(RUN / "PROTOCOL.json", protocol_record)

    diag_requests = [
        {
            "probe_id": record["probe_id"],
            "family": record["family"],
            "expected": record["expected"],
            "input": {"expr": record["expr"]},
        }
        for record in diagnostic
    ]
    eval_requests = [
        {
            "probe_id": record["hid"],
            "hid": record["hid"],
            "family": record["family"],
            "expected": record["expected"],
            "input": {"expr": record["expr"]},
        }
        for record in evaluation
    ]
    records: list[dict] = []
    started = time.perf_counter()

    with tempfile.TemporaryDirectory(prefix="fc-expression-calibration-") as temporary:
        temp = Path(temporary)
        runtime = temp / "python"
        shutil.copytree(
            suite_runner.previous.PYTHON_BASE,
            runtime,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

        for name in VARIANT_ORDER:
            source = VARIANTS[name]["source"]
            target = VARIANTS[name]["target_family"]
            screen = screen_source(source)
            variant_dir = RUN / "variants" / name
            variant_dir.mkdir()
            (variant_dir / "source.py").write_text(source, encoding="utf-8")
            screen_record = {
                "accepted": screen.accepted,
                "reasons": list(screen.reasons),
                "source_sha256": sha256_text(source),
                "source_bytes": len(source.encode("utf-8")),
            }
            write_json(variant_dir / "source-screen.json", screen_record)
            if not screen.accepted:
                records.append({
                    "variant": name,
                    "target_family": target,
                    "defect": VARIANTS[name]["defect"],
                    "screen": screen_record,
                    "status": "source_rejected",
                    "diagnostic": None,
                    "evaluation": None,
                    "target_diagnostic_failures": None,
                    "target_evaluation_failures": None,
                    "cross_family_diagnostic": None,
                    "cross_family_evaluation": None,
                    "all_tree_terminated": None,
                    "gate_pass": False,
                })
                continue

            diag_transport, diag_wall = suite_runner.execute_suite(
                temp,
                f"diagnostic-{name}",
                f"diagnostic_{name}",
                diag_requests,
                source,
                runtime,
            )
            diag_rows = [
                expression_outcome(raw, entry, "diagnostic")
                for raw, entry in zip(diag_transport["probe_rows"], diag_requests, strict=True)
            ]
            diag_failures = [row["status"] != "pass" for row in diag_rows]
            diag_counts = failure_counts(diag_rows)
            diag_record = {
                "probe_rows": diag_rows,
                "rows": len(diag_rows),
                "passed": len(diag_rows) - sum(diag_failures),
                "failed": sum(diag_failures),
                "family_order": FAMILY_ORDER,
                "family_counts": diag_counts,
                "status_counts": status_counts(diag_rows),
                "failed_probe_ids": [row["probe_id"] for row in diag_rows if row["status"] != "pass"],
                "all_tree_terminated": all(row["tree_terminated"] and not row["timed_out"] for row in diag_rows),
                "wall_seconds": diag_wall,
            }
            write_json(variant_dir / "diagnostic.json", diag_record)

            eval_transport, eval_wall = suite_runner.execute_suite(
                temp,
                f"evaluation-{name}",
                f"holdout_{name}",
                eval_requests,
                source,
                runtime,
            )
            eval_rows = [
                expression_outcome(raw, entry, "evaluation")
                for raw, entry in zip(eval_transport["probe_rows"], eval_requests, strict=True)
            ]
            eval_counts = failure_counts(eval_rows)
            eval_correct = sum(1 for row in eval_rows if row["correct"])
            eval_record = {
                "probe_rows": eval_rows,
                "rows": len(eval_rows),
                "correct": eval_correct,
                "failed": len(eval_rows) - eval_correct,
                "family_order": FAMILY_ORDER,
                "failed_family_counts": eval_counts,
                "status_counts": status_counts(eval_rows),
                "failed_probe_ids": [row["probe_id"] for row in eval_rows if not row["correct"]],
                "all_tree_terminated": all(row["tree_terminated"] and not row["timed_out"] for row in eval_rows),
                "wall_seconds": eval_wall,
            }
            write_json(variant_dir / "evaluation.json", eval_record)

            target_diag = diag_counts[target] if target else 0
            target_eval = eval_counts[target] if target else 0
            cross_diag = {family: count for family, count in diag_counts.items() if family != target and count}
            cross_eval = {family: count for family, count in eval_counts.items() if family != target and count}
            all_tree = diag_record["all_tree_terminated"] and eval_record["all_tree_terminated"]
            variant_gate = bool(
                target
                and target_diag == 5
                and target_eval == 5
                and not cross_diag
                and not cross_eval
                and all_tree
            )
            record = {
                "variant": name,
                "target_family": target,
                "defect": VARIANTS[name]["defect"],
                "screen": screen_record,
                "status": "executed",
                "diagnostic": diag_record,
                "evaluation": eval_record,
                "target_diagnostic_failures": target_diag,
                "target_evaluation_failures": target_eval,
                "cross_family_diagnostic": cross_diag,
                "cross_family_evaluation": cross_eval,
                "all_tree_terminated": all_tree,
                "caught_by_diagnostic": target_diag > 0,
                "caught_by_evaluation": target_eval > 0,
                "gate_pass": variant_gate,
            }
            write_json(variant_dir / "variant-summary.json", record)
            records.append(record)

    reference = next((record for record in records if record["variant"] == "reference_parser"), None)
    reference_ok = bool(
        reference
        and reference["status"] == "executed"
        and reference["diagnostic"]["failed"] == 0
        and reference["evaluation"]["correct"] == 30
        and reference["all_tree_terminated"]
    )
    faulty = [record for record in records if record["variant"] != "reference_parser"]
    executed_faulty = [record for record in faulty if record["status"] == "executed"]
    gaps: list[str] = []
    if not reference_ok:
        gaps.append("reference control is not clean on both banks")
    for record in faulty:
        if record["status"] != "executed":
            gaps.append(f"{record['variant']}: source_rejected or not executed")
            continue
        if record["target_diagnostic_failures"] != 5:
            gaps.append(f"{record['variant']}: target diagnostic failures {record['target_diagnostic_failures']}/5")
        if record["target_evaluation_failures"] != 5:
            gaps.append(f"{record['variant']}: target evaluation failures {record['target_evaluation_failures']}/5")
        if record["cross_family_diagnostic"]:
            gaps.append(f"{record['variant']}: cross-family diagnostic failures {record['cross_family_diagnostic']}")
        if record["cross_family_evaluation"]:
            gaps.append(f"{record['variant']}: cross-family evaluation failures {record['cross_family_evaluation']}")
        if not record["all_tree_terminated"]:
            gaps.append(f"{record['variant']}: non-terminated or timed-out transport")
    all_executed = len(executed_faulty) == len(faulty) == 6
    gate_pass = bool(reference_ok and all_executed and not gaps)
    status = "PASS" if gate_pass else "FAIL"
    finished_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    result = {
        "schema": 1,
        "run_id": RUN.name,
        "started_utc": started_utc,
        "finished_utc": finished_utc,
        "status": status,
        "gate_pass": gate_pass,
        "no_model_calls": True,
        "model_calls": 0,
        "generation_attempts": 0,
        "reference_control": "PASS" if reference_ok else "FAIL",
        "total_wall_seconds": time.perf_counter() - started,
        "protocol": protocol_record,
        "variants": records,
        "gaps": gaps,
        "summary": {
            "faulty_variants": len(faulty),
            "executed_faulty_variants": len(executed_faulty),
            "target_family_gate_passes": [record["variant"] for record in executed_faulty if record["gate_pass"]],
            "target_family_gate_failures": [record["variant"] for record in executed_faulty if not record["gate_pass"]],
        },
        "scope": (
            "Hand-built expression defect coverage only. No model-generated solver was requested "
            "or executed. A pass supports only the claim that these frozen banks detect the "
            "prespecified hand-built defects under the stated gate. It is not evidence that natural "
            "solvers concentrate failures, that C predicts correctness, or that the task is easy."
        ),
    }
    write_json(RUN / "CALIBRATION_RESULT.json", result)

    lines = [
        "# Expression task calibration",
        "",
        f"Status: **{status}**",
        "",
        "No model calls were made. The correct reference and six prespecified faulty",
        "implementations were run through the frozen 30-probe diagnostic bank and",
        "30-input evaluation bank using the existing Sandbox path.",
        "",
        f"Reference control: **{result['reference_control']}** "
        f"(diagnostic failures {reference['diagnostic']['failed'] if reference and reference['diagnostic'] else 'n/a'}, "
        f"evaluation correct {reference['evaluation']['correct'] if reference and reference['evaluation'] else 'n/a'}/30).",
        "",
        "| Variant | Target | Diag target failures | Eval target failures | Cross-family | Tree terminated | Gate |",
        "| --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for record in records:
        if record["status"] != "executed":
            lines.append(f"| `{record['variant']}` | {record['target_family'] or 'none'} | n/a | n/a | n/a | n/a | **FAIL** |")
            continue
        cross = bool(record["cross_family_diagnostic"] or record["cross_family_evaluation"])
        lines.append(
            f"| `{record['variant']}` | {record['target_family'] or 'none'} | "
            f"{record['target_diagnostic_failures']}/5 | {record['target_evaluation_failures']}/5 | "
            f"{'yes' if cross else 'no'} | {'yes' if record['all_tree_terminated'] else 'no'} | "
            f"{'PASS' if record['gate_pass'] else 'FAIL'} |"
        )
    lines += ["", "## Gate gaps", ""]
    lines += [f"- {gap}" for gap in gaps] or ["- None."]
    lines += [
        "",
        "## Scope",
        "",
        "This is a hand-built test-coverage check. It does not establish that the task is easy,",
        "that natural solvers concentrate failures, or that C predicts correctness. A pass only",
        "qualifies these frozen banks for the next review step; it does not authorize generation.",
        "",
    ]
    (RUN / "CALIBRATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "run_id": RUN.name,
        "status": status,
        "gate_pass": gate_pass,
        "reference_control": result["reference_control"],
        "summary": result["summary"],
        "gaps": gaps,
    }, indent=2), flush=True)
    if status != "PASS":
        raise SystemExit("expression calibration gate failed; see CALIBRATION_RESULT.json and CALIBRATION_REPORT.md")


if __name__ == "__main__":
    main()
