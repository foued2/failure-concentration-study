from __future__ import annotations

import json
import re
from datetime import datetime, timezone
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def validate_oracles() -> dict:
    sys.path.insert(0, str(ROOT))
    import instrument

    expected = json.loads((ROOT / "expected_values.json").read_text(encoding="utf-8"))
    values = instrument.oracle_values()
    if len(instrument.PROBES) != 30 or len(expected) != 30 or len(values) != 30:
        raise AssertionError("expected exactly 30 probes and expected values")
    if len({p["probe_id"] for p in instrument.PROBES}) != 30:
        raise AssertionError("probe IDs are not unique")
    family_counts = {
        family: sum(p["family"] == family for p in instrument.PROBES)
        for family in instrument.FAMILY_ORDER
    }
    if family_counts != {family: 5 for family in instrument.FAMILY_ORDER}:
        raise AssertionError(f"unexpected probe family counts: {family_counts}")
    for probe_id, oracle_row in values.items():
        if len(set(oracle_row.values())) != 1:
            raise AssertionError(f"oracle disagreement on {probe_id}: {oracle_row}")
        value = next(iter(oracle_row.values()))
        normalized = -1 if value is None else value
        if expected[probe_id] != normalized:
            raise AssertionError(f"frozen expected value mismatch on {probe_id}")
    review = json.loads((ROOT / "coherence_review.json").read_text(encoding="utf-8"))
    if len(review) != 30 or any(item.get("belongs") is not True for item in review):
        raise AssertionError("coherence review coverage is incomplete")
    return {
        "probe_count": 30,
        "family_counts": family_counts,
        "oracle_agreement_count": 30,
        "coherence_review_entries": len(review),
        "expected_values_match": True,
    }


def run_tests() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=str(ROOT), capture_output=True, text=True, timeout=180,
        encoding="utf-8", errors="replace",
    )
    output = proc.stdout + proc.stderr
    match = re.search(r"Ran (\d+) tests?", output)
    if proc.returncode != 0 or not match:
        raise AssertionError(
            "unit test suite failed or did not report a count\n"
            + output[-12000:]
        )
    return int(match.group(1)), output


def main() -> None:
    oracle = validate_oracles()
    test_count, test_output = run_tests()
    report = {
        "status": "PASS",
        "version": 2,
        "validated_at_utc": datetime.now(timezone.utc).isoformat(),
        "candidate_generation_performed": False,
        "model_calls_performed": 0,
        "candidate_bodies_generated": 0,
        "oracle_validation": oracle,
        "unit_test_count": test_count,
        "unit_tests_passed": True,
        "control_expectations": {
            "reference": {"k": 0},
            "unreachable_sentinel_bug": {"k": 5, "C": 1.0},
            "spread_bug_across_R_and_Z": {"k": 5, "family_counts": {"R": 2, "Z": 3}, "C": 0.6},
            "constant_zero": {"k": 29},
            "constant_minus_one": {"k": 25},
            "reachable_distance_plus_one": {"k": 25},
            "single_R1_failure": {"k": 1},
            "single_Z4_failure": {"k": 1},
            "runtime_exception": {"k": 30},
            "invalid_to_load": {"k": None},
            "undefined_global": {"k": None},
            "missing_solve": {"k": None},
            "syntax_error": {"k": None},
        },
        "limitations": [
            "Static undefined-name checking is a conservative warning; preflight loading remains mandatory.",
            "These are deterministic harness controls, not generated candidate results.",
            "No generation, model calls, held-out scoring, power estimate, or H3 inference was performed.",
        ],
        "test_output_tail": test_output[-3000:],
    }
    out = ROOT / "validation-report.json"
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "test_output_tail"}, indent=2, sort_keys=True))
    print("Wrote validation-report.json")


if __name__ == "__main__":
    main()
