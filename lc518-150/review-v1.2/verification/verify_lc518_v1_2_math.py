#!/usr/bin/env python3
"""Independent, solver-free checks for LC518-150 v1.2 mathematics.

Checks only the G22 reference recurrence and per-input E1 bounds algebra.
Does not generate banks, construct candidate solvers, import candidate solver
code, execute candidate solvers, or run the study pipeline.
"""
from bisect import bisect_left
from itertools import combinations, product


def oracle_change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for value in range(coin, amount + 1):
            dp[value] += dp[value - coin]
    return dp[amount]


def g22_change(amount, coins):
    ordered = sorted(coins, reverse=True)
    n = len(ordered)
    if amount == 0:
        return 1, set()
    first_usable = [n] * (amount + 1)
    j = 0
    for value in range(amount, 0, -1):
        while j < n and ordered[j] > value:
            j += 1
        first_usable[value] = j
    memo = {}
    def solve(i, remaining):
        if remaining == 0:
            return 1
        i = max(i, first_usable[remaining])
        key = (i, remaining)
        if key in memo:
            return memo[key]
        if i == n:
            result = 0
        else:
            result = solve(i + 1, remaining)
            if remaining >= ordered[i]:
                result += solve(i, remaining - ordered[i])
        memo[key] = result
        return result
    return solve(0, amount), set(memo)


def test_g22_exhaustive_distinct():
    cases = 0
    for n in range(1, 6):
        for coins in combinations(range(1, 11), n):
            for amount in range(0, 31):
                got, keys = g22_change(amount, coins)
                expected = oracle_change(amount, coins)
                assert got == expected, (coins, amount, got, expected)
                if amount > 0:
                    upper = (min(n, amount) + 1) * amount
                    assert len(keys) <= upper, (coins, amount, len(keys), upper)
                cases += 1
    return cases


def test_threshold_sweep_against_bisect():
    cases = 0
    for n in range(1, 7):
        for coins in product(range(1, 7), repeat=n):
            ordered = sorted(coins, reverse=True)
            table = [n] * 13
            j = 0
            for amount in range(12, 0, -1):
                while j < n and ordered[j] > amount:
                    j += 1
                table[amount] = j
            negated = [-coin for coin in ordered]
            for amount in range(1, 13):
                assert table[amount] == bisect_left(negated, -amount)
                cases += 1
    return cases


LOSSES = {"PASS": (0,), "FAIL": (1,), "UNRESOLVED": (0, 1)}


def test_single_contrast_bounds():
    cases = 0
    for baseline_status, patched_status in product(LOSSES, repeat=2):
        feasible = [
            patched - baseline
            for patched in LOSSES[patched_status]
            for baseline in LOSSES[baseline_status]
        ]
        true_min, true_max = min(feasible), max(feasible)
        if baseline_status != "UNRESOLVED" and patched_status != "UNRESOLVED":
            exact = LOSSES[patched_status][0] - LOSSES[baseline_status][0]
            calculated = (exact, exact)
        else:
            max_is_one = (
                baseline_status in ("PASS", "UNRESOLVED")
                and patched_status in ("FAIL", "UNRESOLVED")
            )
            min_is_minus_one = (
                baseline_status in ("FAIL", "UNRESOLVED")
                and patched_status in ("PASS", "UNRESOLVED")
            )
            calculated = (-int(min_is_minus_one), int(max_is_one))
        assert calculated == (true_min, true_max), (
            baseline_status, patched_status, calculated, (true_min, true_max)
        )
        cases += 1
    return cases


def test_interaction_bounds():
    cases = 0
    for s0, sa, sb, sab in product(LOSSES, repeat=4):
        low = (
            min(LOSSES[sab]) - max(LOSSES[sa])
            - max(LOSSES[sb]) + min(LOSSES[s0])
        )
        high = (
            max(LOSSES[sab]) - min(LOSSES[sa])
            - min(LOSSES[sb]) + max(LOSSES[s0])
        )
        feasible = [
            y_sab - y_sa - y_sb + y_s0
            for y_s0, y_sa, y_sb, y_sab in product(
                LOSSES[s0], LOSSES[sa], LOSSES[sb], LOSSES[sab]
            )
        ]
        assert (low, high) == (min(feasible), max(feasible))
        cases += 1
    return cases


def test_unique_interaction_extremes():
    outcomes = (0, 1)
    values = [
        (sab - sa - sb + s0, (s0, sa, sb, sab))
        for s0, sa, sb, sab in product(outcomes, repeat=4)
    ]
    maximum = max(value for value, _ in values)
    minimum = min(value for value, _ in values)
    max_patterns = [pattern for value, pattern in values if value == maximum]
    min_patterns = [pattern for value, pattern in values if value == minimum]
    assert maximum == 2 and max_patterns == [(1, 0, 0, 1)]
    assert minimum == -2 and min_patterns == [(0, 1, 1, 0)]
    return len(values)


if __name__ == "__main__":
    results = {
        "g22_distinct_correctness_and_state_bound_cases": test_g22_exhaustive_distinct(),
        "threshold_sweep_vs_bisect_cases": test_threshold_sweep_against_bisect(),
        "single_contrast_status_pairs": test_single_contrast_bounds(),
        "interaction_status_quadruples": test_interaction_bounds(),
        "binary_interaction_patterns": test_unique_interaction_extremes(),
    }
    print("ALL_CHECKS_PASSED")
    for name, count in results.items():
        print(f"{name}={count}")
