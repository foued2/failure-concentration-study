from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARTIFACTS = [
    "GATE.md",
    "README.md",
    "RUNBOOK.md",
    "instrument.py",
    "generate.py",
    "run_gate.py",
    "probe_worker.py",
    "isolation_probe.py",
    "isolation/fixtures/other_candidate.py",
    "isolation/windows-sandbox.wsb",
    "expected_values.json",
    "coherence_review.json",
    "validate_controls.py",
    "validation-report.json",
    "tests/test_harness.py",
    "tests/test_v2_controls.py",
    "tests/test_v3_controls.py",
    "tests/test_v4_classifier.py",
    "tests/test_v5_other_category.py",
    "tests/test_v6_integrity.py",
    "tests/test_v7_output_boundary.py",
    "tests/test_v8_low_integrity.py",
    "freeze.py",
]
TAG = "h3-footprint-v8-freeze-2026-10-27"
CORE_ARTIFACTS = ["run_gate.py", "probe_worker.py", "instrument.py", "expected_values.json"]
THRESHOLDS = {
    "saturation_max": 0.80,
    "m_min": 4,
    "pass_cells": 3,
    "pass_k": 2,
    "pass_groups": 40,
    "weak_cells_max": 2,
}
FUTILITY_CHECKPOINTS = {100: 10, 200: 20, 300: 30}


def calculate(timestamp_override: str | None = None) -> dict:
    report = json.loads((ROOT / "validation-report.json").read_text(encoding="utf-8"))
    if report.get("status") != "PASS" or report.get("unit_tests_passed") is not True:
        raise SystemExit("Refusing freeze: validation report is not PASS.")
    if report.get("candidate_generation_performed") is not False or report.get("candidate_bodies_generated") != 0:
        raise SystemExit("Refusing pre-candidate freeze: candidate generation was recorded.")
    # Hash canonical LF bytes so freeze hashes match repository blobs
    # independently of the checkout's line-ending conversion.
    hashes = {
        name: hashlib.sha256((ROOT / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        for name in ARTIFACTS
    }
    return {
        "tag": TAG,
        "version": 8,
        "status": "PRE_CANDIDATE_HARNESS_FREEZE",
        "freeze_scope": "Candidate-integrity revision: every probe worker drops to low integrity before loading candidate code, and each scratch directory is relabelled low. The output root remains at the normal integrity level and is also ACL-locked with pre-opened result handles. The probe requires a sys.modules->os lock-removal candidate (icacls/grant/reset, takeown, integrity lowering) to fail to remove the lock or change canaries, in addition to the V7 io.open and direct-write checks. Unchanged probes, generation frame, thresholds, and futility rule.",
        "timestamp_utc": timestamp_override or datetime.now(timezone.utc).isoformat(),
        "artifact_hashes_sha256": hashes,
        "core_integrity_artifacts": CORE_ARTIFACTS,
        "isolation_report_policy": "produced_by_pre_generation_isolation_probe_in_first_sandbox_session_exported_to_read_only_staging_outside_output_root_not_hashed_in_FREEZE",
        "candidate_integrity_policy": "probe_worker_drops_to_low_integrity_before_candidate_load; scratch_relabelled_low; output_root_normal_integrity",
        "candidate_count_at_freeze": 0,
        "candidate_generation_performed": False,
        "model_calls_performed": 0,
        "generation_budget_batches": 400,
        "generation_segment_batches": 100,
        "bodies_per_batch": 8,
        "requested_candidate_cap": 3200,
        "target_rejected_bodies": 150,
        "thresholds": THRESHOLDS,
        "futility_checkpoints": {str(k): v for k, v in FUTILITY_CHECKPOINTS.items()},
        "base_algorithm_classifier": "ast_structural_reachable_from_solve_v1",
        "other_category_policy": "reported_in_all_counts_but_excluded_from_supported_cells_and_pass_group_count",
        "validation": {
            "status": report["status"],
            "unit_test_count": report["unit_test_count"],
            "oracle_agreement_count": report["oracle_validation"]["oracle_agreement_count"],
            "control_suite": "Passed; expected-k controls are in validation-report.json.",
        },
        "scientific_status": "No H3 conclusion. No new candidate data generated.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = ROOT / "FREEZE.json"
    if args.verify:
        existing = json.loads(output.read_text(encoding="utf-8"))
        current = calculate(timestamp_override=existing.get("timestamp_utc"))
        if existing != current:
            raise SystemExit("FREEZE.json does not match current artifact hashes or configuration.")
        print("FREEZE_VERIFY=PASS")
    else:
        record = calculate()
        output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
