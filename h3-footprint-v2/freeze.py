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
    "instrument.py",
    "generate.py",
    "run_gate.py",
    "probe_worker.py",
    "expected_values.json",
    "coherence_review.json",
    "validate_controls.py",
    "validation-report.json",
    "tests/test_harness.py",
    "tests/test_v2_controls.py",
    "freeze.py",
]
TAG = "h3-footprint-v2-freeze-2026-10-27"
THRESHOLDS = {
    "degeneracy_max": 0.80,
    "m_min": 4,
    "pass_cells": 3,
    "pass_k": 2,
    "pass_groups": 40,
    "weak_cells_max": 2,
}


def calculate(timestamp_override: str | None = None) -> dict:
    report = json.loads((ROOT / "validation-report.json").read_text(encoding="utf-8"))
    if report.get("status") != "PASS" or report.get("unit_tests_passed") is not True:
        raise SystemExit("Refusing freeze: validation report is not PASS.")
    if report.get("candidate_generation_performed") is not False or report.get("candidate_bodies_generated") != 0:
        raise SystemExit("Refusing pre-candidate freeze: candidate generation was recorded.")
    hashes = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in ARTIFACTS
    }
    return {
        "tag": TAG,
        "version": 2,
        "status": "PRE_CANDIDATE_HARNESS_FREEZE",
        "freeze_scope": "Corrected extraction and footprint gate harness; unchanged probe definitions.",
        "timestamp_utc": timestamp_override or datetime.now(timezone.utc).isoformat(),
        "artifact_hashes_sha256": hashes,
        "candidate_count_at_freeze": 0,
        "candidate_generation_performed": False,
        "model_calls_performed": 0,
        "generation_budget_batches": 400,
        "bodies_per_batch": 8,
        "requested_candidate_cap": 3200,
        "target_rejected_bodies": 150,
        "thresholds": THRESHOLDS,
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
