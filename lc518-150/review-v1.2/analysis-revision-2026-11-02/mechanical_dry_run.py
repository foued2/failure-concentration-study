#!/usr/bin/env python3
"""Artificial-only LC518-150 mechanics check.

This is a disposable test harness, not the study generator. It uses deliberately
out-of-contract sentinel values and independent test seeds. It creates no study
bank, solver body, oracle output, or candidate execution result.
"""
from __future__ import annotations

import json
import os
import random
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any


# Deliberately outside the LC518 input contract to prevent fixtures being
# mistaken for valid study records (amount > 5000, denominations > 5000).
SYNTHETIC_HELDOUT = [
    {"fixture_id": "H_FIX_001", "stratum": "H1_FIX", "amount": 900_013, "coins": [70_001, 80_003]},
]
SYNTHETIC_DIAGNOSTIC_CANDIDATES = [
    {"candidate_id": "D_FIX_001", "stratum": "D1_FIX", "records": [
        {"fixture_id": "D_FIX_001_A", "amount": 900_017, "coins": [90_001, 100_003]},
    ]},
    {"candidate_id": "D_FIX_002", "stratum": "D2_FIX", "records": [
        {"fixture_id": "D_FIX_002_A", "amount": 900_013, "coins": [80_003, 70_001]},
        {"fixture_id": "D_FIX_002_B", "amount": 900_019, "coins": [110_003, 120_011]},
    ]},
    {"candidate_id": "D_FIX_003", "stratum": "D3_FIX", "records": [
        {"fixture_id": "D_FIX_003_A", "amount": 900_023, "coins": [130_003, 140_009]},
    ]},
    {"candidate_id": "D_FIX_004", "stratum": "D6_FIX", "records": [
        {"fixture_id": "D_FIX_004_A", "amount": 900_029, "coins": [150_001, 160_001]},
        {"fixture_id": "D_FIX_004_B", "amount": 900_029, "coins": [160_001, 150_001]},
    ]},
]


def canonical_key(record: dict[str, Any]) -> tuple[int, tuple[int, ...]]:
    return int(record["amount"]), tuple(sorted(int(x) for x in record["coins"]))


def fixed_key_preflight(heldout_records: list[dict[str, Any]], fixed_d5_keys: set[tuple[int, tuple[int, ...]]]) -> None:
    """Raise a fatal contradiction if held-out records contain a fixed D5 key."""
    if {canonical_key(r) for r in heldout_records} & fixed_d5_keys:
        raise RuntimeError("FATAL_FIXED_D5_CROSS_BANK_CONTRADICTION")


def cd_from_stratum_failures(failures: list[int]) -> float:
    if len(failures) != 8 or any(x < 0 for x in failures):
        raise ValueError("expected eight nonnegative diagnostic-stratum failure counts")
    k_fail = sum(failures)
    return 0.0 if k_fail == 0 else max(failures) / k_fail


def k_spline_basis(k: int) -> tuple[float, float, float, float, float, float]:
    if k < 0:
        raise ValueError("k_fail must be nonnegative")
    return (
        float(k),
        float(max(0, k - 1)),
        float(max(0, k - 2)),
        float(max(0, k - 3)),
        float(max(0, k - 4)),
        float(k == 0),
    )


def make_family_indicators(train_families: list[str], heldout_family: str) -> dict[str, int]:
    """All-zero representation is the declared unseen-family handling."""
    known = sorted(set(train_families))
    return {f"Z:{family}": int(heldout_family == family) for family in known}


def run_collision_fixture_test() -> dict[str, Any]:
    # This test's canonical identity is a permutation-invariant synthetic key.
    # Candidate D_FIX_002 has two rows; one collides with H_FIX_001. The whole
    # candidate is rejected, including its otherwise non-colliding companion.
    heldout_keys = {canonical_key(r) for r in SYNTHETIC_HELDOUT}
    all_strata = [f"D{i}_FIX" for i in range(1, 9)] + [f"H{i}_FIX" for i in range(1, 9)]
    counts = Counter({stratum: 0 for stratum in all_strata})
    sidecar: list[dict[str, Any]] = []
    accepted: list[str] = []
    rejected: list[str] = []

    for candidate in SYNTHETIC_DIAGNOSTIC_CANDIDATES:
        collisions = sorted({canonical_key(r) for r in candidate["records"]} & heldout_keys)
        if collisions:
            rejected.append(candidate["candidate_id"])
            counts[candidate["stratum"]] += 1
            sidecar.append({
                "candidate_id": candidate["candidate_id"],
                "stratum": candidate["stratum"],
                "reason": "CROSS_BANK_COLLISION",
                "matched_key_count": len(collisions),
                "whole_candidate_rejected": True,
            })
        else:
            accepted.append(candidate["candidate_id"])

    # Reconcile each stratum's candidate rejection counter against one sidecar
    # row per rejected candidate. Include all eight strata, including zeroes.
    sidecar_counts = Counter(row["stratum"] for row in sidecar)
    reconciled = all(counts[s] == sidecar_counts[s] for s in all_strata)
    assert canonical_key(SYNTHETIC_HELDOUT[0]) == canonical_key(
        {"amount": 900_013, "coins": [70_001, 80_003]}
    )
    assert "D_FIX_002" in rejected and "D_FIX_002" not in accepted
    assert "D_FIX_004" in accepted  # Within-bank permutation pair is allowed.
    pair_keys = {canonical_key(r) for r in SYNTHETIC_DIAGNOSTIC_CANDIDATES[3]["records"]}
    assert len(pair_keys) == 1
    accepted_keys = {canonical_key(r) for c in SYNTHETIC_DIAGNOSTIC_CANDIDATES if c["candidate_id"] in accepted for r in c["records"]}
    assert not (accepted_keys & heldout_keys)
    assert len(sidecar) == 1 and sidecar[0]["whole_candidate_rejected"] is True
    assert reconciled

    # A held-out candidate matching a fixed D5 exemplar is a fatal preflight
    # contradiction, not a silent held-out redraw.
    fixed_d5_key = canonical_key({"amount": 900_031, "coins": [170_003, 180_001]})
    heldout_candidate = {"amount": 900_031, "coins": [180_001, 170_003]}
    try:
        fixed_key_preflight([heldout_candidate], {fixed_d5_key})
    except RuntimeError as exc:
        fatal_fixed_key_contradiction = str(exc) == "FATAL_FIXED_D5_CROSS_BANK_CONTRADICTION"
    else:
        fatal_fixed_key_contradiction = False
    assert fatal_fixed_key_contradiction

    # Prove fixtures are deliberately not valid LC518 records.
    assert all(r["amount"] > 5000 for r in SYNTHETIC_HELDOUT)
    assert all(all(c > 5000 for c in r["coins"]) for r in SYNTHETIC_HELDOUT)
    return {
        "status": "PASS",
        "heldout_key_count": len(heldout_keys),
        "accepted_candidate_ids": accepted,
        "rejected_candidate_ids": rejected,
        "whole_candidate_rejection_verified": True,
        "fixed_d5_preflight_collision_is_fatal": fatal_fixed_key_contradiction,
        "all_sixteen_strata_present_in_counters": list(counts.keys()) == all_strata,
        "within_bank_permutation_pair_permitted": True,
        "accepted_diagnostic_keys_disjoint_from_heldout": True,
        "counter_sidecar_reconciliation": reconciled,
        "rejection_counts": dict(counts),
        "sidecar_rows": sidecar,
        "fixtures_outside_lc518_contract": True,
    }


def run_rng_isolation_test() -> dict[str, Any]:
    # Disposable seeds only; no production bank seeds are imported or reused.
    heldout_seed = 73_019
    diagnostic_seed = 51_127

    reference_heldout_rng = random.Random(heldout_seed)
    reference_heldout_draws = [reference_heldout_rng.randrange(10**8, 10**9) for _ in range(12)]

    heldout_rng = random.Random(heldout_seed)
    diagnostic_rng = random.Random(diagnostic_seed)
    diagnostic_rejections = 0
    for _ in range(25):
        _candidate_token = diagnostic_rng.randrange(10**8, 10**9)
        # Simulate a variable number of diagnostic-side retries.
        if _candidate_token % 3 == 0:
            diagnostic_rejections += 1
            _retry_token = diagnostic_rng.randrange(10**8, 10**9)
    actual_heldout_draws = [heldout_rng.randrange(10**8, 10**9) for _ in range(12)]
    assert actual_heldout_draws == reference_heldout_draws
    return {
        "status": "PASS",
        "disposable_heldout_seed": heldout_seed,
        "disposable_diagnostic_seed": diagnostic_seed,
        "simulated_diagnostic_rejections": diagnostic_rejections,
        "heldout_stream_unchanged_by_diagnostic_retries": True,
    }


def run_cd_and_spline_math_test() -> dict[str, Any]:
    cd_cases = {
        "zero_failures": cd_from_stratum_failures([0] * 8),
        "one_failure": cd_from_stratum_failures([1, 0, 0, 0, 0, 0, 0, 0]),
        "two_all_same_stratum": cd_from_stratum_failures([2, 0, 0, 0, 0, 0, 0, 0]),
        "two_split_evenly": cd_from_stratum_failures([1, 1, 0, 0, 0, 0, 0, 0]),
        "three_all_same_stratum": cd_from_stratum_failures([3, 0, 0, 0, 0, 0, 0, 0]),
        "three_split_2_1": cd_from_stratum_failures([2, 1, 0, 0, 0, 0, 0, 0]),
        "three_split_1_1_1": cd_from_stratum_failures([1, 1, 1, 0, 0, 0, 0, 0]),
    }
    assert cd_cases["zero_failures"] == 0.0
    assert cd_cases["one_failure"] == 1.0
    assert cd_cases["two_all_same_stratum"] == 1.0
    assert cd_cases["two_split_evenly"] == 0.5
    assert cd_cases["three_all_same_stratum"] == 1.0
    assert abs(cd_cases["three_split_2_1"] - 2 / 3) < 1e-12
    assert abs(cd_cases["three_split_1_1_1"] - 1 / 3) < 1e-12

    # Demonstrate that the earlier {1, 2, 4} knot proposal is not saturated:
    # the 5x5 map over k=0..4 has rank 4, not the required rank 5.
    old_rows = [
        [float(k), float(max(0, k - 1)), float(max(0, k - 2)),
         float(max(0, k - 4)), float(k == 0)]
        for k in range(5)
    ]
    old_matrix = [row[:] for row in old_rows]
    old_rank = 0
    old_col = 0
    while old_rank < 5 and old_col < 5:
        pivot = next((r for r in range(old_rank, 5)
                      if abs(old_matrix[r][old_col]) > 1e-12), None)
        if pivot is None:
            old_col += 1
            continue
        old_matrix[old_rank], old_matrix[pivot] = old_matrix[pivot], old_matrix[old_rank]
        pv = old_matrix[old_rank][old_col]
        old_matrix[old_rank] = [v / pv for v in old_matrix[old_rank]]
        for r in range(5):
            if r != old_rank:
                factor = old_matrix[r][old_col]
                old_matrix[r] = [a - factor * b for a, b in zip(old_matrix[r], old_matrix[old_rank])]
        old_rank += 1
        old_col += 1
    assert old_rank == 4

    # Design matrix at k=0..4 has full rank: six coefficients encode five
    # arbitrary low-k fitted values plus the linear slope beyond k=4.
    rows = [k_spline_basis(k) for k in range(5)]
    # Gaussian-elimination rank check (stdlib only).
    matrix = [list(map(float, row)) for row in rows]
    rank = 0
    col = 0
    while rank < len(matrix) and col < 6:
        pivot = next((r for r in range(rank, len(matrix)) if abs(matrix[r][col]) > 1e-12), None)
        if pivot is None:
            col += 1
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pv = matrix[rank][col]
        matrix[rank] = [v / pv for v in matrix[rank]]
        for r in range(len(matrix)):
            if r != rank:
                factor = matrix[r][col]
                matrix[r] = [a - factor * b for a, b in zip(matrix[r], matrix[rank])]
        rank += 1
        col += 1
    assert rank == 5  # five distinct low-k rows, full row rank.

    # Add the post-k=4 slope functional. The 6x6 map from coefficients to
    # (g(0), g(1), g(2), g(3), g(4), tail_slope) must be invertible.
    transform = [list(map(float, row)) for row in rows]
    transform.append([1.0, 1.0, 1.0, 1.0, 1.0, 0.0])
    rank6 = 0
    col = 0
    while rank6 < 6 and col < 6:
        pivot = next((r for r in range(rank6, 6) if abs(transform[r][col]) > 1e-12), None)
        if pivot is None:
            col += 1
            continue
        transform[rank6], transform[pivot] = transform[pivot], transform[rank6]
        pv = transform[rank6][col]
        transform[rank6] = [v / pv for v in transform[rank6]]
        for r in range(6):
            if r != rank6:
                factor = transform[r][col]
                transform[r] = [a - factor * b for a, b in zip(transform[r], transform[rank6])]
        rank6 += 1
        col += 1
    assert rank6 == 6

    # Above k=4, every hinge is active; the increment is constant.
    beta = (0.7, -0.1, 0.25, 0.05, -0.02, 2.0)
    def fitted(k: int) -> float:
        return sum(a * b for a, b in zip(k_spline_basis(k), beta))
    increments = [fitted(k + 1) - fitted(k) for k in (4, 5, 6, 7)]
    assert max(increments) - min(increments) < 1e-12
    return {
        "status": "PASS",
        "cd_cases": cd_cases,
        "previous_1_2_4_knot_basis_low_count_rank": old_rank,
        "previous_1_2_4_knot_basis_is_not_saturated": old_rank < 5,
        "spline_basis_row_rank_at_k_0_to_4": rank,
        "spline_basis_column_count": 6,
        "low_count_values_plus_tail_slope_transform_rank": rank6,
        "spline_is_saturated_on_k_0_to_4": True,
        "spline_is_linear_above_k_4": True,
        "spline_knots_are_fixed_conventions_not_data_optimized": True,
    }


def run_unknown_family_test() -> dict[str, Any]:
    train_families = ["FAMILY_A", "FAMILY_A", "FAMILY_B"]
    known = make_family_indicators(train_families, "FAMILY_A")
    unknown = make_family_indicators(train_families, "FAMILY_C")
    assert known == {"Z:FAMILY_A": 1, "Z:FAMILY_B": 0}
    assert unknown == {"Z:FAMILY_A": 0, "Z:FAMILY_B": 0}
    # For a one-parent family, leave-that-parent-out makes the family absent;
    # all indicators are zero and there is no family-specific adjustment.
    singleton_train = make_family_indicators(["FAMILY_A", "FAMILY_A"], "FAMILY_SINGLETON")
    assert all(v == 0 for v in singleton_train.values())
    return {
        "status": "PASS",
        "known_family_encoding": known,
        "unseen_family_encoding": unknown,
        "singleton_family_leave_group_out_encoding": singleton_train,
        "unseen_family_effect_is_zero_not_average": True,
    }



def standardize_with_training_stats(train_values: list[float], test_values: list[float]) -> tuple[list[float], list[float]]:
    mean = sum(train_values) / len(train_values)
    variance = sum((x - mean) ** 2 for x in train_values) / len(train_values)
    scale = variance ** 0.5
    if scale == 0:
        return [0.0 for _ in train_values], [0.0 for _ in test_values]
    return ([(x - mean) / scale for x in train_values],
            [(x - mean) / scale for x in test_values])


def run_training_only_standardization_test() -> dict[str, Any]:
    train_scaled, test_scaled = standardize_with_training_stats([1.0, 2.0, 3.0], [1000.0])
    assert abs(sum(train_scaled)) < 1e-12
    # 1000 is transformed using training mean=2, sd=sqrt(2/3), not test stats.
    assert abs(test_scaled[0] - ((1000.0 - 2.0) / (2 / 3) ** 0.5)) < 1e-9
    const_train, const_test = standardize_with_training_stats([4.0, 4.0], [9.0])
    assert const_train == [0.0, 0.0] and const_test == [0.0]
    return {
        "status": "PASS",
        "training_only_statistics_used": True,
        "constant_training_column_maps_to_zero_in_train_and_test": True,
    }


def run_mse_weighting_test() -> dict[str, Any]:
    # Thirty groups x five bodies. Equal group averaging must equal pooled
    # body-level MSE because every parent group contributes exactly five bodies.
    squared_errors = [[(g + b + 1) ** 2 for b in range(5)] for g in range(30)]
    body_mse = sum(sum(group) for group in squared_errors) / 150
    group_mse_equal_weight = sum(sum(group) / 5 for group in squared_errors) / 30
    assert abs(body_mse - group_mse_equal_weight) < 1e-12
    return {
        "status": "PASS",
        "body_level_oof_mse_equals_equal_parent_group_mean": True,
        "bodies_per_group": 5,
        "parent_groups": 30,
        "effective_group_count_for_uncertainty_interpretation": 30,
    }


def run_atomic_publication_test() -> dict[str, Any]:
    # Test only in an auto-deleted temporary directory outside the study package.
    with tempfile.TemporaryDirectory(prefix="lc518_artificial_mech_") as tmp:
        root = Path(tmp)
        authoritative = root / "authoritative_PASS.json"
        staging = root / "staging.json"

        # Failed validation: no authoritative PASS file may appear.
        staging.write_text(json.dumps({"fixture": "bad", "valid": False}), encoding="utf-8")
        bad_payload = json.loads(staging.read_text(encoding="utf-8"))
        if bad_payload["valid"]:
            os.replace(staging, authoritative)
        assert not authoritative.exists()
        staging.unlink()

        # Successful validation: same-filesystem atomic replace publishes only
        # after the final predicate passes.
        staging.write_text(json.dumps({"fixture": "good", "valid": True}), encoding="utf-8")
        good_payload = json.loads(staging.read_text(encoding="utf-8"))
        if good_payload["valid"]:
            os.replace(staging, authoritative)
        assert authoritative.exists()
        assert json.loads(authoritative.read_text(encoding="utf-8"))["valid"] is True
    return {
        "status": "PASS",
        "failed_validation_publishes_no_authoritative_pass": True,
        "successful_validation_publishes_after_check": True,
        "temporary_directory_auto_deleted": True,
    }


def main() -> None:
    results = {
        "run_scope": "artificial fixtures only; not the study generator",
        "study_banks_created": False,
        "solver_bodies_created_or_executed": False,
        "private_annex_accessed": False,
        "predictive_model_fitted": False,
        "tests": {
            "cd_and_spline_math": run_cd_and_spline_math_test(),
            "unknown_family_encoding": run_unknown_family_test(),
            "training_only_standardization": run_training_only_standardization_test(),
            "mse_weighting": run_mse_weighting_test(),
            "canonical_collision_and_rejection_accounting": run_collision_fixture_test(),
            "separate_rng_streams": run_rng_isolation_test(),
            "atomic_pass_fail_publication": run_atomic_publication_test(),
        },
    }
    results["overall_status"] = "PASS" if all(v["status"] == "PASS" for v in results["tests"].values()) else "FAIL"
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()