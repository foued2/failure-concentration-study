#!/usr/bin/env python3
"""Artificial-only rank checks for the LC518-150 count bases.

No solver outcomes or study records are read. The maximum k_fail of 64 is
inferred only from the predeclared 64-record diagnostic-bank design.
"""
from __future__ import annotations
import json


def basis(k: int, knots: tuple[int, ...]) -> tuple[float, ...]:
    if k < 0:
        raise ValueError("k must be nonnegative")
    return (float(k), *(float(max(0, k - knot)) for knot in knots), float(k == 0))


def matrix_rank(rows: list[tuple[float, ...]], tol: float = 1e-12) -> int:
    a = [list(map(float, row)) for row in rows]
    m = len(a)
    n = len(a[0]) if m else 0
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, m) if abs(a[r][col]) > tol), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [x / scale for x in a[rank]]
        for r in range(m):
            if r != rank:
                factor = a[r][col]
                a[r] = [x - factor * y for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == m:
            break
    return rank


def main() -> None:
    low_k = list(range(5))
    old_knots = (1, 2, 4)
    primary_knots = (1, 2, 3, 4)
    sensitivity_knots = (1, 2, 3, 4, 8, 16, 32, 48)

    old_rows = [basis(k, old_knots) for k in low_k]
    primary_rows = [basis(k, primary_knots) for k in low_k]
    primary_transform = [list(row) for row in primary_rows]
    primary_transform.append([1.0] * (1 + len(primary_knots)) + [0.0])
    sensitivity_rows = [basis(k, sensitivity_knots) for k in range(65)]
    sensitivity_rank_points = [0, 1, 2, 3, 4, 8, 16, 32, 48, 49]
    sensitivity_square = [basis(k, sensitivity_knots) for k in sensitivity_rank_points]

    old_rank = matrix_rank(old_rows)
    primary_rank = matrix_rank(primary_rows)
    primary_full_rank = matrix_rank(primary_transform)
    sensitivity_rank = matrix_rank(sensitivity_rows)
    sensitivity_square_rank = matrix_rank(sensitivity_square)

    result = {
        "run_scope": "integer feature-basis algebra only; no study outcomes or solver data",
        "diagnostic_record_count": 64,
        "maximum_possible_k_fail": 64,
        "old_knots_1_2_4": {
            "knots": list(old_knots), "columns": len(old_rows[0]),
            "rank_on_k_0_to_4": old_rank,
            "saturated_on_k_0_to_4": old_rank == 5,
        },
        "primary_knots_1_2_3_4": {
            "knots": list(primary_knots), "columns": len(primary_rows[0]),
            "rank_on_k_0_to_4": primary_rank,
            "low_values_plus_tail_slope_rank": primary_full_rank,
            "saturated_before_regularization": primary_rank == 5,
        },
        "proposed_sensitivity_knots_1_2_3_4_8_16_32_48": {
            "knots": list(sensitivity_knots), "columns": len(sensitivity_rows[0]),
            "rank_on_all_integer_k_0_to_64": sensitivity_rank,
            "rank_on_selected_10_point_square_submatrix": sensitivity_square_rank,
            "selected_rank_points": sensitivity_rank_points,
            "full_column_rank_on_design_range": sensitivity_rank == 10,
        },
    }
    assert old_rank == 4
    assert primary_rank == 5
    assert primary_full_rank == 6
    assert sensitivity_rank == 10
    assert sensitivity_square_rank == 10
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
