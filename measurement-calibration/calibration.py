"""Controlled fixture calibration through the repository's real diagnostic pipeline."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY))

from study.features import concentration, family_counts, run_probes
from study.probes import make_probe_suite
from study.sssp import dijkstra_ref

SEED = 20261021
FAMILY_ORDER = ["F1", "F2", "F3", "F4", "F5", "F6"]


def input_key(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> str:
    value = {"n": n, "edges": [list(e) for e in edges], "s": s, "t": t}
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def make_targeted_fixture(probes: list[dict], fail_ids: set[str], call_log: list[dict] | None = None):
    """Trusted test callable: correct by reference except on explicitly selected probes."""
    by_key = {}
    for probe in probes:
        key = input_key(probe["n"], probe["edges"], probe["s"], probe["t"])
        if key in by_key:
            raise ValueError("probe inputs are not unique; targeted fixture is ambiguous")
        by_key[key] = probe["probe_id"]
    known_ids = set(by_key.values())
    unknown = fail_ids - known_ids
    if unknown:
        raise ValueError(f"unknown failure probe IDs: {sorted(unknown)}")

    def solve(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
        key = input_key(n, edges, s, t)
        probe_id = by_key.get(key)
        expected = dijkstra_ref(n, edges, s, t)
        output = (0 if expected is None else expected + 1) if probe_id in fail_ids else (-1 if expected is None else expected)
        if call_log is not None:
            call_log.append({"input_id": key, "probe_id": probe_id, "solver_output": output})
        return output

    return solve


CASES = [
    {"case_id": "all_pass_reference", "fail_ids": set(), "expected_k": 0, "expected_C": 0.0},
    {"case_id": "k4_one_family", "fail_ids": {"F1_0", "F1_1", "F1_2", "F1_3"}, "expected_k": 4, "expected_C": 1.0},
    {"case_id": "k4_two_families", "fail_ids": {"F1_0", "F1_1", "F2_0", "F2_1"}, "expected_k": 4, "expected_C": 0.5},
    {"case_id": "k4_four_families", "fail_ids": {"F1_0", "F2_0", "F3_0", "F4_0"}, "expected_k": 4, "expected_C": 0.25},
]


def run_case(probes: list[dict], case: dict) -> dict:
    calls: list[dict] = []
    solve = make_targeted_fixture(probes, case["fail_ids"], calls)
    fails = run_probes(solve, probes)
    if len(calls) != 30:
        raise AssertionError(f"{case['case_id']}: expected 30 solver calls, got {len(calls)}")
    if any(calls[i]["probe_id"] != probes[i]["probe_id"] for i in range(30)):
        raise AssertionError(f"{case['case_id']}: probe execution order/identity mismatch")
    observed_fail_ids = {probes[i]["probe_id"] for i, failed in enumerate(fails) if failed}
    if observed_fail_ids != case["fail_ids"]:
        raise AssertionError(f"{case['case_id']}: intended {case['fail_ids']}, observed {observed_fail_ids}")
    counts = family_counts(fails)
    k, c = concentration(fails)
    if k != case["expected_k"] or c != case["expected_C"]:
        raise AssertionError(f"{case['case_id']}: observed (k,C)=({k},{c})")
    rows = []
    for probe, failed, call in zip(probes, fails, calls):
        expected = dijkstra_ref(probe["n"], probe["edges"], probe["s"], probe["t"])
        expected = -1 if expected is None else expected
        rows.append({
            "probe_id": probe["probe_id"], "family": probe["family"], "variant": probe["variant"],
            "input_id": call["input_id"], "expected_output": expected,
            "solver_output": call["solver_output"], "failed": bool(failed),
        })
    return {
        "case_id": case["case_id"], "controlled_failure_probe_ids": sorted(case["fail_ids"]),
        "family_counts": counts, "k": k, "C": c,
        "expected_k": case["expected_k"], "expected_C": case["expected_C"],
        "matches_expected": True, "probe_records": rows,
    }


def run_calibration() -> dict:
    probes = make_probe_suite(SEED)
    probe_keys = [input_key(p["n"], p["edges"], p["s"], p["t"]) for p in probes]
    if len(set(probe_keys)) != 30:
        raise AssertionError("diagnostic battery contains duplicate inputs")
    return {
        "status": "CONTROLLED_MEASUREMENT_CALIBRATION_ONLY",
        "seed": SEED,
        "instrument": "study.probes.make_probe_suite + study.features.run_probes/family_counts/concentration",
        "observation_type": "trusted hand-written targeted-failure software fixtures; not generated solvers",
        "predictive_analysis_performed": False,
        "natural_solver_evidence": False,
        "probe_count": len(probes),
        "cases": [run_case(probes, case) for case in CASES],
    }


def main() -> None:
    result = run_calibration()
    output = Path(__file__).resolve().parent / "calibration_records.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "probe_count": result["probe_count"],
                      "cases": [{k: c[k] for k in ("case_id", "family_counts", "k", "C", "matches_expected")}
                                for c in result["cases"]]}, indent=2))


if __name__ == "__main__":
    main()
