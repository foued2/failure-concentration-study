"""Rerun the calibration panel through the strict return-type adapter. No model calls."""
from __future__ import annotations

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
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PILOT))
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(PIPELINE))

import run_expression_pilot as pilot
import run_generated_smoke as suite_runner
from expression_mutants import VARIANT_ORDER, VARIANTS
from expression_task import FAMILY_ORDER
from source_policy import screen_source

BANKS = ROOT / "banks"
FREEZE = BANKS / "FREEZE.json"
DIAGNOSTIC = BANKS / "diagnostic.json"
EVALUATION = BANKS / "evaluation.json"
STRICT_PIPELINE = pilot.EXPRESSION_PIPELINE
AMENDMENT_03B = ROOT / "03B_OUTPUT_CONTRACT_AMENDMENT_2026-10-22.md"
LAUNCH_PRECONDITIONS_03C = ROOT / "03C_PILOT_LAUNCH_PRECONDITIONS_2026-10-22.md"
RUN = ROOT / f"calibration-strict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{uuid.uuid4().hex[:8]}"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def family_failures(rows: list[dict]) -> dict[str, int]:
    counts = {family: 0 for family in FAMILY_ORDER}
    for row in rows:
        if row["status"] != "pass":
            counts[row["family"]] += 1
    return counts


def main() -> None:
    if RUN.exists():
        raise FileExistsError(RUN)
    if not AMENDMENT_03B.is_file():
        raise FileNotFoundError(AMENDMENT_03B)
    if not LAUNCH_PRECONDITIONS_03C.is_file():
        raise FileNotFoundError(LAUNCH_PRECONDITIONS_03C)
    strict_adapter_sha256 = pilot.validate_strict_adapter()
    if not suite_runner.previous.SANDBOX.is_file() or not suite_runner.previous.PYTHON_BASE.is_dir():
        raise RuntimeError("Windows Sandbox or the Python runtime is unavailable")
    suite_runner.previous.check_no_running_sandbox()
    diagnostic, evaluation, freeze = pilot.load_frozen_banks()
    if pilot.load_preregistered_prompt() != pilot.PROMPT:
        raise RuntimeError("runner prompt does not match the preregistration")

    RUN.mkdir()
    (RUN / "guest-captures").mkdir()
    (RUN / "variants").mkdir()
    suite_runner.RUN = RUN
    suite_runner.PIPELINE = STRICT_PIPELINE

    panel = {
        "order": VARIANT_ORDER,
        "targets": {name: VARIANTS[name]["target_family"] for name in VARIANT_ORDER},
        "defects": {name: VARIANTS[name]["defect"] for name in VARIANT_ORDER},
        "sources": {name: VARIANTS[name]["source"] for name in VARIANT_ORDER},
    }
    write_json(RUN / "PANEL.json", panel)
    source_hashes = {
        "run_expression_calibration_strict.py": pilot.sha256_file(Path(__file__).resolve()),
        "run_expression_pilot.py": pilot.sha256_file(ROOT / "run_expression_pilot.py"),
        "expression_mutants.py": pilot.sha256_file(ROOT / "expression_mutants.py"),
        "expression_task.py": pilot.sha256_file(ROOT / "expression_task.py"),
        "build_expression_banks.py": pilot.sha256_file(ROOT / "build_expression_banks.py"),
        "freeze_expression_banks.py": pilot.sha256_file(ROOT / "freeze_expression_banks.py"),
        "pilot_tool.py": pilot.sha256_file(PILOT / "pilot_tool.py"),
        "source_policy.py": pilot.sha256_file(PILOT / "source_policy.py"),
        "run_generated_smoke.py": pilot.sha256_file(PILOT / "run_generated_smoke.py"),
        "integration_runner.py": pilot.sha256_file(PILOT / "integration_runner.py"),
        "pipeline_expression_strict/python_adapter.py": pilot.sha256_file(STRICT_PIPELINE / "python_adapter.py"),
        "pipeline_expression_strict/sandbox_suite_supervisor.ps1": pilot.sha256_file(
            STRICT_PIPELINE / "sandbox_suite_supervisor.ps1"),
        "banks/FREEZE.json": pilot.sha256_file(FREEZE),
        "banks/diagnostic.json": pilot.sha256_file(DIAGNOSTIC),
        "banks/evaluation.json": pilot.sha256_file(EVALUATION),
        "03_PILOT_PREREGISTRATION_2026-10-22.md": pilot.sha256_file(pilot.PROTOCOL_03),
        "03A_PREREGISTRATION_AMENDMENT_2026-10-22.md": pilot.sha256_file(pilot.AMENDMENT_03A),
        "03B_OUTPUT_CONTRACT_AMENDMENT_2026-10-22.md": pilot.sha256_file(AMENDMENT_03B),
        "03C_PILOT_LAUNCH_PRECONDITIONS_2026-10-22.md": pilot.sha256_file(LAUNCH_PRECONDITIONS_03C),
    }
    protocol = {
        "schema": 1,
        "run_id": RUN.name,
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "purpose": "strict return-type adapter calibration against the frozen banks",
        "no_model_calls": True,
        "model_calls": 0,
        "generation_attempts": 0,
        "prompt_sha256": pilot.sha256_text(pilot.PROMPT),
        "prompt_matches_preregistration": True,
        "output_contract": "exact int; type(value) is int",
        "wrong_return_type_scoring": "failed answer in the input family; not ineligible",
        "strict_adapter_sha256": strict_adapter_sha256,
        "bank_sizes": {"diagnostic": len(diagnostic), "evaluation": len(evaluation)},
        "input_hashes": {
            "FREEZE.json": pilot.sha256_file(FREEZE),
            "diagnostic.json": freeze["diagnostic"]["sha256"],
            "evaluation.json": freeze["evaluation"]["sha256"],
        },
        "source_hashes": source_hashes,
        "panel_sha256": pilot.sha256_text(json.dumps(panel, sort_keys=True, separators=(",", ":"))),
        "criteria": {
            "reference_control": "30/30 diagnostic passes and 30/30 evaluation correct",
            "faulty_target_diagnostic": "all five target-family probes fail",
            "faulty_target_evaluation": "all five target-family inputs fail",
            "cross_family": "no non-target family failures",
            "transport": "every row is tree-terminated and not timed out",
            "type_contract": "only exact int values pass",
        },
    }
    write_json(RUN / "PROTOCOL.json", protocol)

    records: list[dict] = []
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="fc-expression-strict-calibration-") as temporary:
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
                "source_sha256": pilot.sha256_text(source),
                "source_bytes": len(source.encode("utf-8")),
            }
            write_json(variant_dir / "source-screen.json", screen_record)
            if not screen.accepted:
                record = {
                    "variant": name,
                    "target_family": target,
                    "defect": VARIANTS[name]["defect"],
                    "screen": screen_record,
                    "status": "source_rejected",
                    "diagnostic": None,
                    "evaluation": None,
                    "target_diagnostic_failures": None,
                    "target_evaluation_failures": None,
                    "gate_pass": False,
                    "error": "source screen rejected the variant",
                }
                write_json(variant_dir / "variant-summary.json", record)
                records.append(record)
                continue

            try:
                host = pilot.execute_attempt(
                    variant_dir, temp, source, name, diagnostic, evaluation,
                    suite_runner.execute_suite, runtime,
                )
            except Exception as exc:
                record = {
                    "variant": name,
                    "target_family": target,
                    "defect": VARIANTS[name]["defect"],
                    "screen": screen_record,
                    "status": "execution_error",
                    "diagnostic": None,
                    "evaluation": None,
                    "target_diagnostic_failures": None,
                    "target_evaluation_failures": None,
                    "gate_pass": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }
                write_json(variant_dir / "variant-summary.json", record)
                records.append(record)
                continue

            diag = host["diagnostic"]
            ev = host["evaluation"]
            diag_family_failures = family_failures(diag["probe_rows"])
            eval_family_failures = family_failures(ev["probe_rows"])
            is_reference = name == "reference_parser"
            target_diag = 0 if is_reference else diag_family_failures[target]
            target_eval = 0 if is_reference else eval_family_failures[target]
            cross_diag = {
                family: count for family, count in diag_family_failures.items()
                if (is_reference or family != target) and count
            }
            cross_eval = {
                family: count for family, count in eval_family_failures.items()
                if (is_reference or family != target) and count
            }
            if is_reference:
                gate = (
                    host["eligible"]
                    and diag["failed"] == 0
                    and ev["correct_count"] == 30
                    and not cross_diag
                    and not cross_eval
                )
            else:
                gate = (
                    host["eligible"]
                    and target_diag == 5
                    and target_eval == 5
                    and diag["failed"] == 5
                    and not cross_diag
                    and not cross_eval
                )
            record = {
                "variant": name,
                "target_family": target,
                "defect": VARIANTS[name]["defect"],
                "screen": screen_record,
                "status": "executed",
                "diagnostic": diag,
                "evaluation": ev,
                "diag_family_failures": diag_family_failures,
                "eval_family_failures": eval_family_failures,
                "target_diagnostic_failures": target_diag,
                "target_evaluation_failures": target_eval,
                "cross_family_diagnostic": cross_diag,
                "cross_family_evaluation": cross_eval,
                "eligible": host["eligible"],
                "gate_pass": gate,
            }
            write_json(variant_dir / "variant-summary.json", record)
            records.append(record)

    total_seconds = time.perf_counter() - started
    reference = records[0]
    faulty = records[1:]
    all_passed = (
        reference.get("gate_pass") is True
        and len(faulty) == 6
        and all(record.get("gate_pass") is True for record in faulty)
    )
    result = {
        "schema": 1,
        "run_id": RUN.name,
        "started_utc": protocol["started_utc"],
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "PASS" if all_passed else "HOLD",
        "gate_pass": all_passed,
        "no_model_calls": True,
        "model_calls": 0,
        "generation_attempts": 0,
        "strict_adapter_sha256": strict_adapter_sha256,
        "reference_control": "PASS" if reference.get("gate_pass") is True else "FAIL",
        "protocol": protocol,
        "summary": {
            "executed_faulty_variants": sum(1 for record in faulty if record["status"] == "executed"),
            "faulty_variants": len(faulty),
            "target_family_gate_passes": [
                record["variant"] for record in faulty if record.get("gate_pass") is True
            ],
            "target_family_gate_failures": [
                record["variant"] for record in faulty if record.get("gate_pass") is not True
            ],
        },
        "variants": records,
        "scope": (
            "Strict return-type adapter calibration only. No model-generated solver was requested or executed. "
            "A pass supports only the claim that the strict path preserves the prespecified reference and mutant "
            "coverage on these frozen banks; it is not evidence of natural-solver concentration or predictive value."
        ),
        "total_wall_seconds": total_seconds,
    }
    write_json(RUN / "CALIBRATION_RESULT.json", result)
    lines = [
        "# Strict return-type calibration",
        "",
        f"Status: **{result['status']}**",
        "",
        f"Run: `{RUN.name}`.",
        f"Model calls: {result['model_calls']}; generation attempts: {result['generation_attempts']}.",
        f"Output contract: `{protocol['output_contract']}`.",
        "",
        "| Variant | Target | Diagnostic failures | Target failures | Evaluation target failures | Gate |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for record in records:
        diag_failed = record["diagnostic"]["failed"] if record["diagnostic"] else "n/a"
        lines.append(
            f"| {record['variant']} | {record['target_family'] or 'reference'} | "
            f"{diag_failed} | {record['target_diagnostic_failures']} | "
            f"{record['target_evaluation_failures']} | {record['gate_pass']} |"
        )
    lines += [
        "",
        "Frozen banks were not modified. This is a calibration rerun through the strict adapter, not a pilot attempt.",
        "",
    ]
    (RUN / "CALIBRATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "run_dir": str(RUN),
        "status": result["status"],
        "reference_control": result["reference_control"],
        "faulty_gate_passes": result["summary"]["target_family_gate_passes"],
        "faulty_gate_failures": result["summary"]["target_family_gate_failures"],
        "model_calls": result["model_calls"],
    }, indent=2), flush=True)
    if not all_passed:
        raise SystemExit("strict calibration did not pass")


if __name__ == "__main__":
    main()
