"""Validate the retained bug-detection coverage records."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

PILOT = Path(__file__).resolve().parent
REPO = PILOT.parent
PIPELINE = PILOT / "python-pipeline-integration"
sys.path.insert(0, str(PILOT))
sys.path.insert(0, str(REPO))

from bug_detection_variants import VARIANT_ORDER, VARIANTS
from study.families import FAMILY_ORDER
from study.features import concentration, family_counts


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def source_paths() -> dict[str, Path]:
    return {
        "run_bug_detection_check.py": PILOT / "run_bug_detection_check.py",
        "bug_detection_variants.py": PILOT / "bug_detection_variants.py",
        "source_policy.py": PILOT / "source_policy.py",
        "run_generated_smoke.py": PILOT / "run_generated_smoke.py",
        "integration_runner.py": PILOT / "integration_runner.py",
        "python_adapter.py": PIPELINE / "python_adapter.py",
        "sandbox_suite_supervisor.ps1": PIPELINE / "sandbox_suite_supervisor.ps1",
        "run_python_pipeline_integration.py": PIPELINE / "run_python_pipeline_integration.py",
        "protocol": PILOT / "BUG_DETECTION_CHECK_PROTOCOL_2026-10-21.md",
    }


def latest_run() -> Path:
    candidates = sorted(PILOT.glob("bug-detection-check-*"))
    if not candidates:
        raise FileNotFoundError("no bug-detection-check run found")
    return candidates[-1]


def validate(run: Path) -> dict:
    result = read_json(run / "BUG_DETECTION_RESULT.json")
    protocol = read_json(run / "PROTOCOL.json")
    assert isinstance(result, dict) and isinstance(protocol, dict)
    hash_checks: dict[str, bool] = {}

    paths = source_paths()
    for name, expected in protocol["source_hashes"].items():
        path = paths.get(name)
        hash_checks[f"source:{name}"] = bool(path and path.is_file() and sha256_file(path) == expected)
    hash_checks["protocol_sha256"] = sha256_file(PILOT / "BUG_DETECTION_CHECK_PROTOCOL_2026-10-21.md") == protocol["protocol_sha256"]

    diagnostic = read_json(PILOT / "diagnostic_battery.json")
    evaluation = read_json(PILOT / "evaluation_bank.json")
    hash_checks["input:diagnostic_battery.json"] = sha256_file(PILOT / "diagnostic_battery.json") == protocol["input_hashes"]["diagnostic_battery.json"]
    hash_checks["input:evaluation_bank.json"] = sha256_file(PILOT / "evaluation_bank.json") == protocol["input_hashes"]["evaluation_bank.json"]

    closure_integrity_path = PILOT / "natural-pilot-gemini-20261021T172103Z" / "INTEGRITY.json"
    closure_hashes_match = None
    if closure_integrity_path.is_file():
        closure = read_json(closure_integrity_path)
        closure_hashes_match = (
            protocol["input_hashes"]["diagnostic_battery.json"] == closure["sha256"]["diagnostic_battery"]
            and protocol["input_hashes"]["evaluation_bank.json"] == closure["sha256"]["evaluation_bank"]
        )
        hash_checks["inputs_match_closed_gemini_integrity"] = closure_hashes_match

    panel = {
        "order": VARIANT_ORDER,
        "defects": {name: VARIANTS[name]["defect"] for name in VARIANT_ORDER},
        "sources": {name: VARIANTS[name]["source"] for name in VARIANT_ORDER},
    }
    hash_checks["panel_sha256"] = sha256_text(json.dumps(panel, sort_keys=True, separators=(",", ":"))) == protocol["panel_sha256"]

    variant_records = result["variants"]
    variant_names = [record["variant"] for record in variant_records]
    variant_checks = variant_names == VARIANT_ORDER
    all_tree_terminated = True
    diagnostic_rows = 0
    evaluation_rows = 0
    reference_record = next((record for record in variant_records if record["variant"] == "reference_dijkstra"), None)
    for record in variant_records:
        name = record["variant"]
        variant_dir = run / "variants" / name
        source = (variant_dir / "source.py").read_text(encoding="utf-8")
        screen = read_json(variant_dir / "source-screen.json")
        diagnostic_record = read_json(variant_dir / "diagnostic.json")
        evaluation_record = read_json(variant_dir / "evaluation.json")
        summary = read_json(variant_dir / "variant-summary.json")
        if screen["source_sha256"] != sha256_text(source) or not screen["accepted"]:
            variant_checks = False
        diag_rows = diagnostic_record["probe_rows"]
        eval_rows = evaluation_record["probe_rows"]
        if diagnostic_record["rows"] != len(diag_rows) or evaluation_record["rows"] != len(eval_rows):
            variant_checks = False
        diagnostic_rows += len(diag_rows)
        evaluation_rows += len(eval_rows)
        if len(diag_rows) != 30 or len(eval_rows) != 20:
            variant_checks = False
        all_tree_terminated = all_tree_terminated and all(row["tree_terminated"] for row in diag_rows + eval_rows)
        failures = [not row["correct"] for row in diag_rows]
        counts = family_counts(failures)
        k, c = concentration(failures)
        eval_correct = sum(row["correct"] for row in eval_rows)
        if diagnostic_record["family_counts"] != counts or diagnostic_record["k"] != k or diagnostic_record["C"] != c:
            variant_checks = False
        if diagnostic_record["failed"] != sum(failures) or diagnostic_record["failed_probe_ids"] != [row["probe_id"] for row in diag_rows if not row["correct"]]:
            variant_checks = False
        if evaluation_record["correct"] != eval_correct or evaluation_record["failed"] != len(eval_rows) - eval_correct:
            variant_checks = False
        if evaluation_record["failed_probe_ids"] != [row["probe_id"] for row in eval_rows if not row["correct"]]:
            variant_checks = False
        if record["caught_by_diagnostic"] != (k > 0) or record["caught_by_evaluation"] != (eval_correct < len(eval_rows)):
            variant_checks = False
        if summary["caught_by_diagnostic"] != record["caught_by_diagnostic"] or summary["caught_by_evaluation"] != record["caught_by_evaluation"]:
            variant_checks = False
        if summary["diagnostic"]["k"] != k or summary["diagnostic"]["C"] != c or summary["evaluation"]["correct"] != eval_correct:
            variant_checks = False

    reference_ok = bool(
        reference_record
        and reference_record["diagnostic"]["failed"] == 0
        and reference_record["diagnostic"]["k"] == 0
        and reference_record["diagnostic"]["C"] == 0
        and reference_record["evaluation"]["correct"] == 20
    )
    faulty = [record for record in variant_records if record["variant"] != "reference_dijkstra"]
    caught_diag = [record["variant"] for record in faulty if record["caught_by_diagnostic"]]
    caught_eval = [record["variant"] for record in faulty if record["caught_by_evaluation"]]
    caught_either = [record["variant"] for record in faulty if record["caught_by_either"]]
    summary = result["summary"]
    summary_ok = (
        summary["faulty_variants"] == len(faulty)
        and summary["executed_faulty_variants"] == len(faulty)
        and summary["caught_by_diagnostic"] == caught_diag
        and summary["caught_by_evaluation"] == caught_eval
        and summary["caught_by_either"] == caught_either
        and summary["diagnostic_only"] == [name for name in caught_diag if name not in caught_eval]
        and summary["evaluation_only"] == [name for name in caught_eval if name not in caught_diag]
        and summary["caught_by_both"] == [name for name in caught_diag if name in caught_eval]
        and summary["missed_by_both"] == [record["variant"] for record in faulty if not record["caught_by_either"]]
    )
    capture_dirs = sorted(path for path in (run / "guest-captures").iterdir() if path.is_dir())
    captures_ok = len(capture_dirs) == 16 and all(
        [entry.name for entry in path.iterdir()] == ["capture.json"] for path in capture_dirs
    )
    essentials_ok = (
        result["status"] == "COMPLETE"
        and result["reference_control"] == "PASS"
        and result["no_model_calls"] is True
        and result["model_calls"] == 0
        and reference_ok
        and variant_checks
        and all_tree_terminated
        and summary_ok
        and captures_ok
        and diagnostic_rows == 240
        and evaluation_rows == 160
    )
    all_hash_checks = all(hash_checks.values())
    report = {
        "run_id": run.name,
        "checked_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hash_checks": hash_checks,
        "all_hashes_match": all_hash_checks,
        "variant_order_match": variant_names == VARIANT_ORDER,
        "variant_count": len(variant_records),
        "faulty_variant_count": len(faulty),
        "reference_control": "PASS" if reference_ok else "FAIL",
        "all_variants_executed": all(record["status"] == "executed" for record in variant_records),
        "all_sources_accepted": all(record["screen"]["accepted"] for record in variant_records),
        "all_tree_terminated": all_tree_terminated,
        "diagnostic_rows": diagnostic_rows,
        "evaluation_rows": evaluation_rows,
        "total_rows": diagnostic_rows + evaluation_rows,
        "capture_directories": len(capture_dirs),
        "capture_layout_valid": captures_ok,
        "summary_consistent": summary_ok,
        "no_model_calls": result["no_model_calls"] is True and result["model_calls"] == 0,
        "caught_by_diagnostic": caught_diag,
        "caught_by_evaluation": caught_eval,
        "caught_by_either": caught_either,
        "missed_by_both": summary["missed_by_both"],
        "evaluation_self_loop_inputs": sum(any(u == v for u, v, _ in item["input"]["edges"]) for item in evaluation),
        "diagnostic_self_loop_probes": sum(any(u == v for u, v, _ in item["input"]["edges"]) for item in diagnostic),
        "all_essentials_pass": essentials_ok,
        "status": "PASS" if all_hash_checks and essentials_ok else "FAIL",
    }
    (run / "INTEGRITY.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=None)
    args = parser.parse_args()
    report = validate(args.run or latest_run())
    print(json.dumps(report, indent=2, sort_keys=True), flush=True)
    if report["status"] != "PASS":
        raise SystemExit("bug-detection integrity validation failed")


if __name__ == "__main__":
    main()
