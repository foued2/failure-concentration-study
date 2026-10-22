"""Run the prespecified hand-built SSSP defect panel through both frozen banks."""
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

PILOT = Path(__file__).resolve().parent
REPO = PILOT.parent
PIPELINE = PILOT / "python-pipeline-integration"
sys.path.insert(0, str(PILOT))
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(PIPELINE))

import run_generated_smoke as suite_runner
from bug_detection_variants import VARIANT_ORDER, VARIANTS
from source_policy import screen_source
from study.families import FAMILY_ORDER
from study.features import concentration, family_counts

RUN = PILOT / f"bug-detection-check-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{uuid.uuid4().hex[:8]}"
PROTOCOL = PILOT / "BUG_DETECTION_CHECK_PROTOCOL_2026-10-21.md"
DIAGNOSTIC = PILOT / "diagnostic_battery.json"
EVALUATION = PILOT / "evaluation_bank.json"


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


def status_counts(records: list[dict]) -> dict[str, int]:
    return dict(sorted(Counter(record["status"] for record in records).items()))


def main() -> None:
    if RUN.exists():
        raise FileExistsError(RUN)
    if not PROTOCOL.is_file():
        raise FileNotFoundError(PROTOCOL)
    if not suite_runner.previous.SANDBOX.is_file() or not suite_runner.previous.PYTHON_BASE.is_dir():
        raise RuntimeError("Windows Sandbox or the Python runtime is unavailable")
    suite_runner.previous.check_no_running_sandbox()

    diagnostic = json.loads(DIAGNOSTIC.read_text(encoding="utf-8"))
    evaluation = json.loads(EVALUATION.read_text(encoding="utf-8"))
    if len(diagnostic) != 30 or len(evaluation) != 20:
        raise RuntimeError("frozen bank sizes are not 30 and 20")
    if len({item["input_id"] for item in diagnostic}) != 30:
        raise RuntimeError("diagnostic input IDs are not unique")
    if len({item["input_id"] for item in evaluation}) != 20:
        raise RuntimeError("evaluation input IDs are not unique")
    if {item["input_id"] for item in diagnostic} & {item["input_id"] for item in evaluation}:
        raise RuntimeError("diagnostic and evaluation banks overlap")

    RUN.mkdir()
    (RUN / "guest-captures").mkdir()
    (RUN / "variants").mkdir()
    suite_runner.RUN = RUN

    source_hashes = {
        "run_bug_detection_check.py": sha256_file(Path(__file__).resolve()),
        "bug_detection_variants.py": sha256_file(PILOT / "bug_detection_variants.py"),
        "source_policy.py": sha256_file(PILOT / "source_policy.py"),
        "run_generated_smoke.py": sha256_file(PILOT / "run_generated_smoke.py"),
        "integration_runner.py": sha256_file(PILOT / "integration_runner.py"),
        "python_adapter.py": sha256_file(PIPELINE / "python_adapter.py"),
        "sandbox_suite_supervisor.ps1": sha256_file(PIPELINE / "sandbox_suite_supervisor.ps1"),
        "run_python_pipeline_integration.py": sha256_file(PIPELINE / "run_python_pipeline_integration.py"),
        "protocol": sha256_file(PROTOCOL),
    }
    panel = {
        "order": VARIANT_ORDER,
        "defects": {name: VARIANTS[name]["defect"] for name in VARIANT_ORDER},
        "sources": {name: VARIANTS[name]["source"] for name in VARIANT_ORDER},
    }
    started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    protocol_record = {
        "schema": 1,
        "run_id": RUN.name,
        "started_utc": started_utc,
        "purpose": "hand-built SSSP defect coverage check against the frozen banks",
        "no_model_calls": True,
        "model_calls": 0,
        "input_hashes": {
            "diagnostic_battery.json": sha256_file(DIAGNOSTIC),
            "evaluation_bank.json": sha256_file(EVALUATION),
        },
        "bank_sizes": {"diagnostic": len(diagnostic), "evaluation": len(evaluation)},
        "source_hashes": source_hashes,
        "protocol_sha256": sha256_file(PROTOCOL),
        "panel_sha256": sha256_text(json.dumps(panel, sort_keys=True, separators=(",", ":"))),
        "criteria": {
            "diagnostic_caught": "k > 0",
            "evaluation_caught": "correct < 20",
            "reference_control": "30/30 diagnostic passes and 20/20 evaluation correctness",
        },
    }
    write_json(RUN / "PROTOCOL.json", protocol_record)

    diag_requests = [{"probe_id": item["probe_id"], "input": item["input"]} for item in diagnostic]
    eval_requests = [{"probe_id": item["hid"], "input": item["input"]} for item in evaluation]
    records: list[dict] = []
    started = time.perf_counter()

    with tempfile.TemporaryDirectory(prefix="fc-bug-check-") as temporary:
        temp = Path(temporary)
        runtime = temp / "python"
        shutil.copytree(
            suite_runner.previous.PYTHON_BASE,
            runtime,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

        for name in VARIANT_ORDER:
            source = VARIANTS[name]["source"]
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
                    "defect": VARIANTS[name]["defect"],
                    "screen": screen_record,
                    "status": "source_rejected",
                    "diagnostic": None,
                    "evaluation": None,
                    "caught_by_diagnostic": None,
                    "caught_by_evaluation": None,
                    "caught_by_either": None,
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
            diag_records = [
                suite_runner.outcome(raw, item, source, "diagnostic")
                for raw, item in zip(diag_transport["probe_rows"], diagnostic, strict=True)
            ]
            diag_failures = [record["status"] != "pass" for record in diag_records]
            diag_counts = family_counts(diag_failures)
            k, c = concentration(diag_failures)
            diag_record = {
                "rows": len(diag_records),
                "failed": sum(diag_failures),
                "family_order": FAMILY_ORDER,
                "family_counts": diag_counts,
                "k": k,
                "C": c,
                "status_counts": status_counts(diag_records),
                "failed_probe_ids": [record["probe_id"] for record in diag_records if record["status"] != "pass"],
                "wall_seconds": diag_wall,
            }
            write_json(variant_dir / "diagnostic.json", {"probe_rows": diag_records, **diag_record})

            eval_transport, eval_wall = suite_runner.execute_suite(
                temp,
                f"evaluation-{name}",
                f"evaluation_{name}",
                eval_requests,
                source,
                runtime,
            )
            eval_records = [
                suite_runner.outcome(raw, item, source, "evaluation")
                for raw, item in zip(eval_transport["probe_rows"], evaluation, strict=True)
            ]
            eval_correct = sum(record["correct"] for record in eval_records)
            eval_record = {
                "rows": len(eval_records),
                "correct": eval_correct,
                "failed": len(eval_records) - eval_correct,
                "status_counts": status_counts(eval_records),
                "failed_probe_ids": [record["probe_id"] for record in eval_records if not record["correct"]],
                "wall_seconds": eval_wall,
            }
            write_json(variant_dir / "evaluation.json", {"probe_rows": eval_records, **eval_record})

            caught_diag = k > 0
            caught_eval = eval_correct < len(eval_records)
            record = {
                "variant": name,
                "defect": VARIANTS[name]["defect"],
                "screen": screen_record,
                "status": "executed",
                "diagnostic": diag_record,
                "evaluation": eval_record,
                "caught_by_diagnostic": caught_diag,
                "caught_by_evaluation": caught_eval,
                "caught_by_either": caught_diag or caught_eval,
            }
            write_json(variant_dir / "variant-summary.json", record)
            records.append(record)

    reference = next((record for record in records if record["variant"] == "reference_dijkstra"), None)
    reference_ok = bool(
        reference
        and reference["status"] == "executed"
        and reference["diagnostic"]["k"] == 0
        and reference["diagnostic"]["failed"] == 0
        and reference["evaluation"]["correct"] == 20
    )
    faulty = [record for record in records if record["variant"] != "reference_dijkstra"]
    executed_faulty = [record for record in faulty if record["status"] == "executed"]
    caught_diag = [record["variant"] for record in executed_faulty if record["caught_by_diagnostic"]]
    caught_eval = [record["variant"] for record in executed_faulty if record["caught_by_evaluation"]]
    caught_either = [record["variant"] for record in executed_faulty if record["caught_by_either"]]
    missed_both = [record["variant"] for record in executed_faulty if not record["caught_by_either"]]
    both = [name for name in caught_diag if name in caught_eval]
    diagnostic_only = [name for name in caught_diag if name not in caught_eval]
    evaluation_only = [name for name in caught_eval if name not in caught_diag]
    all_executed = len(executed_faulty) == len(faulty) and bool(reference and reference["status"] == "executed")
    status = "COMPLETE" if reference_ok and all_executed else "HOLD"
    finished_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    result = {
        "schema": 1,
        "run_id": RUN.name,
        "started_utc": started_utc,
        "finished_utc": finished_utc,
        "status": status,
        "no_model_calls": True,
        "model_calls": 0,
        "reference_control": "PASS" if reference_ok else "FAIL",
        "total_wall_seconds": time.perf_counter() - started,
        "protocol": protocol_record,
        "variants": records,
        "summary": {
            "faulty_variants": len(faulty),
            "executed_faulty_variants": len(executed_faulty),
            "caught_by_diagnostic": caught_diag,
            "caught_by_evaluation": caught_eval,
            "caught_by_either": caught_either,
            "diagnostic_only": diagnostic_only,
            "evaluation_only": evaluation_only,
            "caught_by_both": both,
            "missed_by_both": missed_both,
        },
        "scope": (
            "Hand-built defect coverage only. No model-generated solver was requested or executed. "
            "A caught defect supports only the claim that these frozen banks detected this specific "
            "hand-built defect. It is not evidence that natural solvers concentrate failures or that "
            "C predicts correctness."
        ),
    }
    write_json(RUN / "BUG_DETECTION_RESULT.json", result)

    lines = [
        "# Bug-detection coverage check",
        "",
        f"Status: **{status}**",
        "",
        "No model calls were made. Seven prespecified faulty SSSP variants and one correct",
        "reference were run through the frozen 30-probe diagnostic battery and 20-input",
        "evaluation bank using the existing Sandbox path.",
        "",
        f"Reference control: **{result['reference_control']}** "
        f"(diagnostic failures {reference['diagnostic']['failed'] if reference and reference['diagnostic'] else 'n/a'}, "
        f"evaluation correct {reference['evaluation']['correct'] if reference and reference['evaluation'] else 'n/a'}/20).",
        "",
        "| Variant | Defect | Diag failures | k | C | Eval correct | Diag caught | Eval caught |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for record in records:
        diag = record["diagnostic"]
        evaluation = record["evaluation"]
        if record["status"] != "executed":
            lines.append(f"| `{record['variant']}` | {record['defect']} | n/a | n/a | n/a | n/a | n/a | n/a |")
            continue
        lines.append(
            f"| `{record['variant']}` | {record['defect']} | {diag['failed']}/30 | {diag['k']} | "
            f"{diag['C']:.2f} | {evaluation['correct']}/20 | "
            f"{'yes' if record['caught_by_diagnostic'] else 'no'} | "
            f"{'yes' if record['caught_by_evaluation'] else 'no'} |"
        )
    lines += [
        "",
        "## Coverage summary",
        "",
        f"- Caught by diagnostic: {', '.join(f'`{name}`' for name in caught_diag) or 'none'}",
        f"- Caught by evaluation: {', '.join(f'`{name}`' for name in caught_eval) or 'none'}",
        f"- Caught by both: {', '.join(f'`{name}`' for name in both) or 'none'}",
        f"- Diagnostic only: {', '.join(f'`{name}`' for name in diagnostic_only) or 'none'}",
        f"- Evaluation only: {', '.join(f'`{name}`' for name in evaluation_only) or 'none'}",
        f"- Missed by both: {', '.join(f'`{name}`' for name in missed_both) or 'none'}",
        "",
        "## Scope",
        "",
        "This is a hand-built test-coverage check. It does not establish that the task is easy,",
        "that the diagnostic battery is generally sufficient, or that concentration predicts",
        "correctness. A defect missed by both banks would be a documented coverage limitation;",
        "a defect caught by only one bank is evidence of complementary coverage for that defect.",
        "",
    ]
    (RUN / "BUG_DETECTION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "run_id": RUN.name,
        "status": status,
        "reference_control": result["reference_control"],
        "summary": result["summary"],
    }, indent=2), flush=True)
    if status != "COMPLETE":
        raise SystemExit("bug-detection check did not complete with a valid reference control")


if __name__ == "__main__":
    main()
