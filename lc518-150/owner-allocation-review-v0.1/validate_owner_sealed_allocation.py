#!/usr/bin/env python3
"""Read-only structural and synthetic-semantic validation for LC518 new allocation v0.1.

This script does NOT create candidate solver sources or execute any of the 150 planned
solver bodies. It validates the allocation matrix, orientation, S-extra balance,
family-incidence counts, C6 witness arithmetic, and test-only semantic mutation models
on synthetic inputs that satisfy the published D1-D8 stratum descriptions.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path
import unittest

OUT = Path(__file__).resolve().parent

FAMILY_RANGES = {
    "K1": range(1, 8),
    "K2": range(8, 16),
    "K3": range(16, 24),
    "K4": range(24, 29),
    "K5": range(29, 31),
}
PARENT_FAMILY = {f"G{i:02d}": fam for fam, ids in FAMILY_RANGES.items() for i in ids}
PARENT_TACTICS = {
    "G01":"K1 canonical list, given order", "G02":"K1 sorted ascending", "G03":"K1 sparse dict cells",
    "G04":"K1 filtered coins plus while-loop", "G05":"K1 sorted descending", "G06":"K1 double buffer per coin",
    "G07":"K1 bisect cutoff prefix", "G08":"K2 full table, row-wise", "G09":"K2 rolling two rows",
    "G10":"K2 full table, amount-outer fill", "G11":"K2 suffix-indexed reverse table", "G12":"K2 sparse dict rows",
    "G13":"K2 flat list with stride arithmetic", "G14":"K2 copy-then-extend row builder", "G15":"K2 sorted coins, skip-row compression",
    "G16":"K3 lru_cache top-down, use-first, given order", "G17":"K3 dict memo top-down, skip-first", "G18":"K3 explicit-stack iterative DFS",
    "G19":"K3 flat-array memo, sorted coins", "G20":"K3 largest-part-first suffix recursion", "G21":"K3 smallest-part-first suffix recursion, dict memo",
    "G22":"K3 bisect skip-run compaction", "G23":"K3 lru top-down, explicit depth-bound", "G24":"K4 geometric doubling, given order",
    "G25":"K4 geometric doubling, descending coins", "G26":"K4 residue-chain accumulation", "G27":"K4 residue-chain, sorted coins",
    "G28":"K4 doubling on sparse dict carrier", "G29":"K5 split plus Cauchy product, given-order split",
    "G30":"K5 split plus Cauchy product, sorted split",
}

# parent_id -> unordered pair, in M01..M08 numbering.
PAIR_BY_PARENT = {
    "G04": (1, 2), "G29": (1, 3), "G11": (1, 4), "G13": (1, 5),
    "G24": (1, 6), "G08": (1, 7), "G07": (1, 8), "G12": (2, 3),
    "G14": (2, 4), "G02": (2, 5), "G28": (2, 6), "G09": (2, 7),
    "G05": (2, 8), "G25": (3, 4), "G06": (3, 5), "G26": (3, 6),
    "G15": (3, 7), "G27": (3, 8), "G18": (4, 5), "G30": (4, 6),
    "G20": (4, 7), "G17": (4, 8), "G19": (5, 6), "G16": (5, 7),
    "G03": (5, 8), "G23": (6, 7), "G22": (6, 8), "G21": (7, 8),
    "G01": (3, 4), "G10": (1, 2),
}

# Exactly one S-extra mechanism per parent. No parent receives its S-extra mechanism
# again as SA or SB.
EXTRA_BY_PARENT = {
    "G01": 7, "G02": 6, "G03": 4, "G04": 5, "G05": 1, "G06": 2,
    "G07": 4, "G08": 2, "G09": 6, "G10": 8, "G11": 3, "G12": 1,
    "G13": 3, "G14": 5, "G15": 6, "G16": 3, "G17": 2, "G18": 7,
    "G19": 1, "G20": 8, "G21": 5, "G22": 4, "G23": 2, "G24": 3,
    "G25": 7, "G26": 5, "G27": 1, "G28": 4, "G29": 6, "G30": 8,
}

# Base tournament orientation. For the two replicated edges, the second occurrence is
# deliberately reversed, balancing every mechanism's SA/SB incidence.
BASE_A = {
    (1,2):1,(1,3):1,(1,4):1,(1,5):1,(1,6):6,(1,7):7,(1,8):8,
    (2,3):2,(2,4):2,(2,5):2,(2,6):6,(2,7):7,(2,8):8,
    (3,4):3,(3,5):3,(3,6):3,(3,7):3,(3,8):8,
    (4,5):4,(4,6):4,(4,7):4,(4,8):8,
    (5,6):5,(5,7):5,(5,8):5,(6,7):6,(6,8):6,(7,8):7,
}
REPEATED_PAIRS = {(1,2), (3,4)}
REPEAT_PARENT_IDS = {"G01", "G10"}

MECHANISMS = {
    1: {
        "id":"M01", "name":"Empty-combination identity set to zero",
        "definition":"Change the coefficient/base state for amount 0 from 1 to 0.",
        "trigger_condition":"The correct reference answer is positive; the incorrect zero identity then removes every derivation from the empty state.",
        "semantic_edit":"W(0,S): 1 -> 0",
        "strata":["D1","D2","D4","D5","D6","D7","D8"],
        "witness_strata":["D1","D2"],
        "reach":"D1 amount-zero/boundary and every reachable positive stratum D2, D4, D5, D6, D7 and D8. The wrong identity suppresses positive counts; D3 is unchanged because its reference count is zero.",
        "family_adapters":{"K1":"dp[0]=0; also change explicit amount==0 or empty-prefix returns from 1 to 0 (notably G04 and G07)","K2":"T[0][0]=0","K3":"f(i,0)=0","K4":"polynomial identity coefficient P[0]=0","K5":"one half-product identity coefficient P_L[0]=0"},
        "risk":"A direct base-state fault; should be localized in each family."
    },
    2: {
        "id":"M02", "name":"Unbounded multiplicity reduced to one use",
        "definition":"Replace unlimited reuse of each denomination by at-most-one use per denomination.",
        "trigger_condition":"At least one valid combination requires using some denomination at least twice, and the at-most-once count is lower than the unbounded count.",
        "semantic_edit":"Unbounded recurrence -> 0/1 recurrence",
        "strata":["D1","D2","D4","D5","D6","D7","D8"],
        "witness_strata":["D1","D5"],
        "reach":"D1/D2 boundary and exact-match cases, D4 modular cases, D5 non-greedy cases, and D6-D8 where a valid representation requires repeated use. D3 remains unchanged because restricting a solution set cannot make an unreachable target reachable.",
        "family_adapters":{"K1":"in-place parents: descending amount update; double-buffer G06: use previous-row value prev[a-c] rather than same-pass cur[a-c]","K2":"use branch reads previous row T[i-1][a-c_i]","K3":"use branch advances to f(i+1,a-c_i)","K4":"replace each geometric factor by (1+x^c); doubling variants retain only the one-use factor","K5":"use finite-use factor updates in each half-product"},
        "risk":"Same intended semantic error, translated to each recurrence."
    },
    3: {
        "id":"M03", "name":"Largest denomination omitted",
        "definition":"Remove the maximum denomination before evaluating the otherwise unchanged parent.",
        "trigger_condition":"At least one valid combination uses the maximum denomination, so removing it changes the answer.",
        "semantic_edit":"coins := coins without max(coins)",
        "strata":["D1","D2","D4","D5","D6","D7","D8"],
        "witness_strata":["D2","D5"],
        "reach":"D1, D2, D4-D8 when the largest denomination contributes to at least one valid representation. It cannot create a solution on D3 unreachable inputs.",
        "family_adapters":{"K1":"skip max denomination in outer coin loop","K2":"omit max-denomination row/factor","K3":"omit max denomination from recursion state","K4":"omit its generating-function factor","K5":"omit it from the appropriate half-product"},
        "risk":"Order-independent because max(coins) is determined by value, not input position."
    },
    4: {
        "id":"M04", "name":"First denomination processed twice",
        "definition":"Process the first input denomination twice as if the two occurrences were distinct coin types, despite the contract's distinct-denomination set semantics.",
        "trigger_condition":"The first input denomination participates in at least one representation, and treating it as two distinct types changes the combination count.",
        "semantic_edit":"duplicate first coin factor/iteration once",
        "strata":["D1","D2","D4","D5","D6","D7","D8"],
        "witness_strata":["D2","D5"],
        "reach":"D1, D2, D4-D8 whenever the first denomination participates in a representation; duplicating its type changes the count. It cannot make D3 reachable because denomination values are unchanged.",
        "family_adapters":{"K1":"repeat first coin's in-place update pass","K2":"add a duplicate first-coin row/factor","K3":"include first denomination twice as two recursion indices","K4":"multiply by the first geometric factor twice","K5":"include first denomination factor twice in its half-product"},
        "risk":"A localized repeated-iteration defect; preserve original input order when identifying the first denomination."
    },
    5: {
        "id":"M05", "name":"Target-equal denomination omitted",
        "definition":"Discard any denomination c equal to the target amount A before counting combinations, incorrectly treating an exact denomination match as unusable.",
        "trigger_condition":"A positive target denomination is present; removing it removes the singleton combination using that denomination.",
        "semantic_edit":"coins := [c for c in coins if c != amount]",
        "strata":["D1","D2","D4","D6","D7","D8"],
        "witness_strata":["D1","D2"],
        "reach":"D1/D2 exact-match boundaries and D4/D6-D8 inputs where a denomination equals the target. The fixed D5 {1,3,4}, amount 6/10 examples contain no target-equal denomination; D3 remains unchanged because its answer is zero.",
        "family_adapters":{"K1":"filter target-equal denomination before the coin loop","K2":"omit target-equal coin row","K3":"omit target-equal coin index from recursion state","K4":"omit target-equal factor from the generating-function product","K5":"omit target-equal factor before splitting and half-products"},
        "risk":"Distinct from M03: it removes only c=A, even when a larger denomination remains; the two coincide only when the target-equal denomination is also the maximum."
    },
    6: {
        "id":"M06", "name":"Unsorted prefix early-stop",
        "definition":"Before the parent performs any ordering/normalization, scan the original input sequence and stop at the first denomination greater than amount; retain only the prefix. No sort is performed before this test.",
        "trigger_condition":"A denomination greater than the target appears before a later denomination that contributes to a valid representation; the premature break then discards that useful suffix.",
        "semantic_edit":"coins := takewhile(c <= amount, original_coins)",
        "strata":["D1","D2","D4","D6","D7","D8"],
        "witness_strata":["D2","D6"],
        "reach":"D1, D2, D4, D6, D7 and D8 when an input ordering places a denomination greater than amount before a later useful denomination. The fixed D5 {1,3,4}, amount 6/10 examples contain no coin greater than amount; D3 remains zero either way.",
        "family_adapters":{"K1":"insert pre-normalization prefix filter","K2":"insert pre-normalization prefix filter","K3":"insert pre-normalization prefix filter","K4":"insert pre-normalization prefix filter","K5":"insert pre-normalization prefix filter"},
        "risk":"Must execute before all sorting/bisect/filtering in S0; otherwise it may be repaired by the parent normalization."
    },
    7: {
        "id":"M07", "name":"Minimum-denomination divisibility shortcut",
        "definition":"Incorrectly return zero whenever amount is not divisible by min(coins), treating divisibility by the smallest denomination as necessary for reachability.",
        "trigger_condition":"The target is not divisible by the minimum denomination, but the reference answer is positive because other denominations form a valid combination.",
        "semantic_edit":"if amount % min(coins) != 0: return 0",
        "strata":["D1","D2","D4","D6","D7","D8"],
        "witness_strata":["D2","D4"],
        "reach":"D1, D2, D4, D6, D7 and D8 when a reachable amount is not divisible by the smallest denomination. The fixed D5 examples contain denomination 1; D3 is correctly zero under this guard.",
        "family_adapters":{"K1":"pre-DP guard","K2":"pre-table guard","K3":"pre-recursion guard","K4":"pre-product guard","K5":"pre-convolution guard"},
        "risk":"This is deliberately a false-negative pruning rule; it does not alter inputs or the oracle."
    },
    8: {
        "id":"M08", "name":"Use-transition contribution doubled",
        "definition":"Multiply every non-empty use-transition contribution by two instead of one, overcounting denomination-use paths.",
        "trigger_condition":"The reference answer is positive; every non-empty transition path receives an extra multiplicity weight, changing the total.",
        "semantic_edit":"add 2*use_count instead of use_count",
        "strata":["D1","D2","D4","D5","D6","D7","D8"],
        "witness_strata":["D2","D5"],
        "reach":"D1, D2, D4-D8 whenever the correct answer includes at least one denomination-use transition; D3 remains zero and is unchanged.",
        "family_adapters":{"K1":"dp[a] += 2*dp[a-c]","K2":"T[i][a] = T[i-1][a] + 2*T[i][a-c]","K3":"f(i,a) = f(i+1,a) + 2*f(i,a-c)","K4":"residue-chain: new[a]=old[a]+2*new[a-c]; binary-doubling: replace each factor (1-x^c)^-1 by product_j(1+2^(2^j)*x^(2^j*c)); sparse carrier: coefficient at multiplicity t is weighted by 2^t","K5":"apply the same doubled geometric-factor coefficients in each half-product before the Cauchy product"},
        "risk":"A transition-weight fault distinct from duplicating one denomination: each positive multiplicity path is reweighted."
    },
}

# Synthetic, contract-valid examples. These show semantic realizability within the
# published stratum descriptions; they are NOT asserted to be rows in the frozen bank.
FIXTURES = {
    1: {"D1":[(0,[1,2]),(2,[1,2])], "D2":[(5,[2,5,7]),(9,[4,5,9])], "D7":[(100,list(range(1,51)))], "D8":[(2000,[1,3,4])]},
    2: {"D1":[(2,[1,2]),(3,[1,2])], "D5":[(6,[1,3,4]),(10,[1,3,4])], "D7":[(100,list(range(1,51)))], "D8":[(2000,[1,3,4])]},
    3: {"D2":[(9,[4,5,9]),(10,[2,7,10])], "D5":[(6,[1,3,4]),(10,[1,3,4])], "D7":[(100,list(range(1,51)))], "D8":[(2000,[1,3,4])]},
    4: {"D2":[(3,[1,2,3]),(4,[1,2,4])], "D5":[(6,[1,3,4]),(10,[1,3,4])], "D7":[(100,list(range(1,51)))], "D8":[(2000,[1,3,4])]},
    5: {"D1":[(2,[1,2]),(3,[2,3,5])], "D2":[(9,[4,5,9]),(5,[2,5,7])], "D7":[(100,list(range(1,50))+[100])], "D8":[(2000,[1,3,4,2000])]},
    6: {"D2":[(5,[7,5,2]),(6,[8,6,4,3])], "D6":[(5,[7,8,3,2]),(5,[2,8,7,3]),(5,[9,8,4,1]),(5,[1,8,9,4])], "D7":[(100,[5000]+list(range(1,50)))], "D8":[(2000,[2500,1000,500,1])]},
    7: {"D2":[(9,[2,4,9]),(10,[4,5,10])], "D4":[(8,[3,5]),(12,[5,7])], "D7":[(101,list(range(2,52)))], "D8":[(2000,[3,999,1001])]},
    8: {"D2":[(3,[1,2,3]),(4,[1,2,4])], "D5":[(6,[1,3,4]),(10,[1,3,4])], "D7":[(100,list(range(1,51)))], "D8":[(2000,[1,3,4])]},
}

# One negative-control input per proposed mechanism. The relevant trigger predicate is
# deliberately false, so the corresponding mutation must leave the exact answer intact.
NEGATIVE_CONTROLS = {
    1: (3, [2, 4]),             # unreachable: wrong zero identity remains observationally silent
    2: (5, [2, 3]),             # only representation uses each denomination once
    3: (6, [1, 2, 9]),          # largest denomination exceeds target and cannot contribute
    4: (4, [9, 1, 2]),          # duplicated first denomination is too large to contribute
    5: (6, [1, 3, 4]),          # no denomination equals target
    6: (5, [1, 2, 7]),           # all useful denominations precede the over-target suffix
    7: (6, [2, 3, 5]),          # target divisible by minimum denomination
    8: (3, [2, 4]),             # unreachable: no use transition exists to reweight
}


def oracle(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    return dp[amount]


def oracle_2d(amount: int, coins: list[int]) -> int:
    """Independent coin-index x amount use/skip table oracle."""
    table = [[0] * (amount + 1) for _ in range(len(coins) + 1)]
    table[0][0] = 1
    for i, coin in enumerate(coins, 1):
        for a in range(amount + 1):
            table[i][a] = table[i - 1][a]
            if a >= coin:
                table[i][a] += table[i][a - coin]
    return table[len(coins)][amount]


def oracle_exhaustive(amount: int, coins: list[int]) -> int:
    """Bounded multiplicity enumeration oracle for small synthetic inputs only."""
    def count_from(i: int, remaining: int) -> int:
        if i == len(coins):
            return int(remaining == 0)
        coin = coins[i]
        return sum(count_from(i + 1, remaining - used * coin)
                   for used in range(remaining // coin + 1))
    return count_from(0, amount)


def solve_family(family: str, amount: int, coins: list[int], *, base_identity: int = 1, unbounded: bool = True, weight_use: int = 1) -> int:
    """Five mathematically distinct LC518 formulations used only as synthetic test models."""
    n = len(coins)
    if family == "K1":
        dp = [0] * (amount + 1); dp[0] = base_identity
        for c in coins:
            if unbounded:
                for a in range(c, amount + 1): dp[a] += weight_use * dp[a-c]
            else:
                for a in range(amount, c-1, -1): dp[a] += weight_use * dp[a-c]
        return dp[amount]
    if family == "K2":
        table = [[0] * (amount + 1) for _ in range(n + 1)]
        table[0][0] = base_identity
        for i, c in enumerate(coins, 1):
            for a in range(amount + 1):
                eligible = a >= c
                if not eligible:
                    use = 0
                elif unbounded:
                    use = weight_use * table[i][a-c]
                else:
                    use = weight_use * table[i-1][a-c]
                table[i][a] = table[i-1][a] + use
        return table[n][amount]
    if family == "K3":
        # Explicit-stack memoized suffix recurrence. This is the frozen G18-style
        # K3 tactic, avoiding host recursion limits in the synthetic test harness.
        memo: dict[tuple[int,int], int] = {}
        stack: list[tuple[int,int,bool]] = [(0, amount, False)]
        while stack:
            i, rem, expanded = stack.pop()
            key = (i, rem)
            if key in memo: continue
            if rem == 0:
                memo[key] = base_identity; continue
            if i == n:
                memo[key] = 0; continue
            skip_key = (i+1, rem)
            use_ok = rem >= coins[i]
            use_key = (i if unbounded else i+1, rem-coins[i]) if use_ok else None
            if not expanded:
                stack.append((i, rem, True))
                if skip_key not in memo: stack.append((skip_key[0], skip_key[1], False))
                if use_key is not None and use_key not in memo: stack.append((use_key[0], use_key[1], False))
            else:
                value = memo[skip_key]
                if use_key is not None: value += weight_use * memo[use_key]
                memo[key] = value
        return memo[(0, amount)]
    if family == "K4":
        # Multiplicity-indexed generating-function product using residue chains.
        poly = [0] * (amount + 1); poly[0] = base_identity
        for c in coins:
            nxt = [0] * (amount + 1)
            for residue in range(min(c, amount + 1)):
                acc = 0
                for a in range(residue, amount + 1, c):
                    if not unbounded:
                        acc = poly[a] + (weight_use * poly[a-c] if a >= c else 0)
                    else:
                        acc = poly[a] + weight_use * acc
                    nxt[a] = acc
            poly = nxt
        return poly[amount]
    if family == "K5":
        # Split the coin set, build two half-products, then take one Cauchy product.
        mid = (n + 1) // 2
        left, right = coins[:mid], coins[mid:]
        def half(part: list[int]) -> list[int]:
            d = [0] * (amount + 1); d[0] = base_identity
            for c in part:
                if unbounded:
                    for a in range(c, amount + 1): d[a] += weight_use * d[a-c]
                else:
                    for a in range(amount, c-1, -1): d[a] += weight_use * d[a-c]
            return d
        lp, rp = half(left), half(right)
        return sum(lp[t] * rp[amount-t] for t in range(amount + 1))
    raise ValueError(f"Unknown family {family}")


def mutate_family(m: int, family: str, amount: int, coins: list[int]) -> int:
    """Apply one proposed semantic fault to one of the five family formulations."""
    if m == 1:
        return solve_family(family, amount, coins, base_identity=0)
    if m == 2:
        return solve_family(family, amount, coins, unbounded=False)
    if m == 3:
        reduced = list(coins); reduced.remove(max(reduced))
        return solve_family(family, amount, reduced)
    if m == 4:
        return solve_family(family, amount, coins + [coins[0]])
    if m == 5:
        return solve_family(family, amount, [c for c in coins if c != amount])
    if m == 6:
        prefix = []
        for c in coins:
            if c > amount: break
            prefix.append(c)
        return solve_family(family, amount, prefix)
    if m == 7:
        if amount != 0 and amount % min(coins) != 0: return 0
        return solve_family(family, amount, coins)
    if m == 8:
        return solve_family(family, amount, coins, weight_use=2)
    raise ValueError(m)



def mutate_pair(m_a: int, m_b: int, family: str, amount: int, coins: list[int]) -> int:
    """Compose two proposal mechanisms under the fixed v0.1 merge precedence.

    Order: duplicate the original first input denomination (M04); remove every
    occurrence of the original maximum (M03); remove target-equal denominations
    (M05); apply unsorted prefix break (M06); apply M07's divisibility guard against
    the original minimum; then combine recurrence modifiers M01/M02/M08.
    """
    mechanisms={m_a,m_b}
    original=list(coins)
    working=list(original)
    if 4 in mechanisms:
        working=[original[0]]+working
    if 3 in mechanisms:
        largest=max(original)
        working=[c for c in working if c != largest]
    if 5 in mechanisms:
        working=[c for c in working if c != amount]
    if 6 in mechanisms:
        prefix=[]
        for c in working:
            if c > amount: break
            prefix.append(c)
        working=prefix
    if 7 in mechanisms and amount != 0 and amount % min(original) != 0:
        return 0
    return solve_family(
        family, amount, working,
        base_identity=0 if 1 in mechanisms else 1,
        unbounded=(2 not in mechanisms),
        weight_use=2 if 8 in mechanisms else 1,
    )


def family_for(parent_id: str) -> str:
    return PARENT_FAMILY[parent_id]


def make_rows() -> list[dict]:
    # Preserve pair-map order in a stable, reviewable P01..P30 sequence.
    pair_order = list(PAIR_BY_PARENT.items())
    occurrences = Counter(tuple(sorted(pair)) for _, pair in pair_order)
    seen = Counter()
    rows = []
    for idx, (parent_id, pair) in enumerate(pair_order, 1):
        key = tuple(sorted(pair))
        seen[key] += 1
        if key in REPEATED_PAIRS and seen[key] == 2:
            a = BASE_A[key]
            a = key[0] if a == key[1] else key[1]
            repeat_status = "REPEAT-1"
        else:
            a = BASE_A[key]
            repeat_status = "BASE"
        b = key[0] if key[1] == a else key[1]
        rows.append({
            "pair_assignment_id": f"PAIR-{idx:02d}",
            "parent_id": parent_id,
            "family_id": family_for(parent_id),
            "pair": [f"M{x:02d}" for x in key],
            "SA_mutation_A": f"M{a:02d}",
            "SB_mutation_B": f"M{b:02d}",
            "pair_status": repeat_status,
            "S_extra": f"M{EXTRA_BY_PARENT[parent_id]:02d}",
            "parent_source_sha256": None,
            "opaque_solver_ids": None,
        })
    return rows


def incidence(rows: list[dict]) -> dict[str, dict[str, int]]:
    result = {fam: {f"M{i:02d}":0 for i in range(1,9)} for fam in FAMILY_RANGES}
    for row in rows:
        fam = row["family_id"]
        qset = set(row["pair"] + [row["S_extra"]])
        for q in qset:
            result[fam][q] += 1
    return result


def role_incidence(rows: list[dict]) -> dict[str, dict[str, dict[str, int]]]:
    result = {fam: {f"M{i:02d}": {"SA":0,"SB":0,"S-extra":0,"total":0} for i in range(1,9)} for fam in FAMILY_RANGES}
    for row in rows:
        fam=row["family_id"]
        result[fam][row["SA_mutation_A"]]["SA"] += 1
        result[fam][row["SB_mutation_B"]]["SB"] += 1
        result[fam][row["S_extra"]]["S-extra"] += 1
    for fam in result:
        for q in result[fam]:
            result[fam][q]["total"] = sum(result[fam][q][role] for role in ("SA","SB","S-extra"))
    return result


def make_witness_skeletons(rows: list[dict]) -> list[dict]:
    inc = incidence(rows)
    parent_sets = defaultdict(list)
    for row in rows:
        qset = set(row["pair"] + [row["S_extra"]])
        for q in qset:
            parent_sets[(q,row["family_id"])].append(row)
    out = []
    for m in range(1,9):
        q = f"M{m:02d}"
        s1,s2 = MECHANISMS[m]["witness_strata"]
        j1,j2 = int(s1[1:])-1, int(s2[1:])-1
        for fam in FAMILY_RANGES:
            eligible = sorted(parent_sets[(q,fam)], key=lambda r:r["parent_id"])
            if len(eligible) < 3:
                continue
            patterns = []
            for idx, row in enumerate(eligible[:3]):
                f = [0]*8; u=[0]*8
                if idx == 0:
                    f[j1]=2
                elif idx == 1:
                    f[j1]=1; f[j2]=1
                else:
                    f[j2]=2
                k=sum(f); ku=sum(u); cd=Fraction(max(f),k)
                patterns.append({
                    "parent_id":row["parent_id"],
                    "family_id":fam,
                    "mechanism_id":q,
                    "variant_role":("SA" if row["SA_mutation_A"]==q else "SB" if row["SB_mutation_B"]==q else "S-extra"),
                    "f":f,"u":u,"k_fail":k,"k_unresolved":ku,
                    "C_D":f"{cd.numerator}/{cd.denominator}",
                    "witness_status":"HYPOTHETICAL_SKELETON_NOT_ADMISSIBLE",
                })
            values={p["C_D"] for p in patterns}
            if all(all(fj+uj<=8 for fj,uj in zip(p["f"],p["u"])) for p in patterns) and len(values)>=2:
                out.append({
                    "mechanism_id":q,"family_id":fam,
                    "exact_cell":{"k_fail":2,"k_unresolved":0},
                    "strata_pair":[s1,s2],
                    "parent_witness_skeletons":patterns,
                    "cross_parent_C_D_difference_demonstrated_arithmetically":True,
                    "admission_limit":"No bank record IDs, parent source hashes, or source-line mechanism-reach citations are attached; these are not Rev 11-admissible witnesses or C6 PASS results."
                })
    return out


def make_parent_compatibility(rows: list[dict]) -> list[dict]:
    out=[]
    for row in rows:
        fam=row["family_id"]
        assigned=[row["SA_mutation_A"],row["SB_mutation_B"],row["S_extra"]]
        flags=[]
        if fam=="K1" and row["parent_id"] in {"G04","G07"} and "M01" in assigned:
            flags.append("M01 must also alter the parent's explicit amount-zero/empty-prefix return branch, not only dp[0].")
        if row["parent_id"]=="G06" and "M02" in assigned:
            flags.append("M02 must make the double-buffer recurrence read prev[a-c], not cur[a-c].")
        tactic=PARENT_TACTICS[row["parent_id"]].lower()
        if "sort" in tactic or "reverse" in tactic or "bisect" in tactic:
            if "M04" in assigned: flags.append("M04 must capture and duplicate the original first input denomination before sorting/reversing.")
            if "M06" in assigned: flags.append("M06 must run on the original input order before sorting/reversing/bisect normalization.")
        if fam=="K4" and "M08" in assigned:
            flags.append("M08 must use weighted geometric coefficients in the exact K4 tactic (residue-chain, binary-doubling, or sparse carrier).")
        if not flags:
            flags.append("No extra family-tactic exception identified by this coarse screen; exact source patch still requires review.")
        out.append({
            "parent_id":row["parent_id"],
            "family_id":fam,
            "parent_tactic_from_frozen_design":PARENT_TACTICS[row["parent_id"]],
            "specific_patch_flags":flags,
            "SA_mechanism":row["SA_mutation_A"],
            "SA_family_adapter":MECHANISMS[int(row["SA_mutation_A"][1:])]["family_adapters"][fam],
            "SB_mechanism":row["SB_mutation_B"],
            "SB_family_adapter":MECHANISMS[int(row["SB_mutation_B"][1:])]["family_adapters"][fam],
            "S_extra_mechanism":row["S_extra"],
            "S_extra_family_adapter":MECHANISMS[int(row["S_extra"][1:])]["family_adapters"][fam],
            "formulation_level_status":"PROPOSED_COMPATIBLE",
            "source_patch_status":"NOT_REVIEWED_NO_PARENT_SOURCE_BODY_EXISTS",
            "patch_boundary":"The mechanism must be introduced at the stated preprocessing or recurrence boundary without silently changing unrelated parent logic; source-specific patch location and diff are not established.",
        })
    return out


def build_package() -> dict:
    rows=make_rows()
    inc=incidence(rows)
    extra_counts=Counter(row["S_extra"] for row in rows)
    sa_counts=Counter(row["SA_mutation_A"] for row in rows)
    sb_counts=Counter(row["SB_mutation_B"] for row in rows)
    pair_counts=Counter(tuple(row["pair"]) for row in rows)
    support_cells=[{"mechanism_id":q,"family_id":fam,"parent_id_count":n}
                   for fam, vals in inc.items() for q,n in vals.items() if n>=3 and fam!="K5"]
    return {
        "document_id":"LC518_NEW_OWNER_SEALED_ALLOCATION_V0_1",
        "design_status":"PROPOSED_NEW_DESIGN_PENDING_INDEPENDENT_REVIEW_NOT_FROZEN",
        "design_date":"2026-11-25",
        "not_recovered_from_original_annex":True,
        "parent_design_source":{"commit":"3e9a29c9652a6ab4f6bab0919e386757280b2654","path":"lc518-150/glm-handoff/PARENT_DESIGN.md","git_blob_sha1":"fd15338bd511ba479e62efa50ada9d2d233e143a"},
        "fixed_parent_families":{"K1":"G01-G07","K2":"G08-G15","K3":"G16-G23","K4":"G24-G28","K5":"G29-G30"},
        "repeat_pairs_preselected":[["M01","M02"],["M03","M04"]],
        "orientation_rule":"Balanced base tournament orientation; the second occurrence of each repeated pair is reversed. The mechanism placed in SA is M01..M08 as recorded per row, not always the lower-numbered mechanism.",
        "SAB_composition_precedence":"For a combined pair, duplicate the original first denomination (M04), remove all occurrences of the original maximum (M03), remove denominations equal to amount (M05), apply the unsorted prefix break (M06), apply the M07 guard using the original minimum, then combine recurrence modifiers M01/M02/M08. This is an explicit proposal-level semantic merge rule; exact source-diff compatibility still requires review against each parent implementation.",
        "mutation_taxonomy":list(MECHANISMS.values()),
        "allocation_rows":rows,
        "parent_compatibility_matrix":make_parent_compatibility(rows),
        "summary":{
            "parent_count":len(rows),
            "unique_parent_ids":len({r['parent_id'] for r in rows}),
            "pair_assignment_count":len(rows),
            "unique_unordered_pairs":len(pair_counts),
            "repeated_pair_counts":{f"{a}-{b}":n for (a,b),n in pair_counts.items() if n==2},
            "SA_incidence_by_mechanism":dict(sorted(sa_counts.items())),
            "SB_incidence_by_mechanism":dict(sorted(sb_counts.items())),
            "S_extra_incidence_by_mechanism":dict(sorted(extra_counts.items())),
            "raw_parent_id_incidence_by_family":inc,
            "role_incidence_by_family":role_incidence(rows),
            "candidate_C6_parent_count_cells":support_cells,
            "candidate_C6_cell_count":len(support_cells),
            "C6_witness_skeletons":make_witness_skeletons(rows),
            "base_source_hash_status":"NOT YET AVAILABLE; C4 effective parent-group counts and duplicate-hash deduplication remain unverified",
            "solver_variant_ids_status":"NOT ASSIGNED; all S0/SA/SB/SAB/S-extra source bodies remain unbuilt",
        },
        "limits":[
            "The 50 synthetic trigger examples are valid examples under the published D1-D8 stratum descriptions; they are not verified records in the frozen 64-record diagnostic bank.",
            "The 48 C6 witness skeletons demonstrate arithmetic feasibility only; they are not admissible Rev 11 witnesses without parent source hashes, exact bank-record mapping, and mechanism-reach/joint-attainability citations.",
            "No 150 solver source bodies were created, imported, or executed.",
            "No runtime/memory failure, diagnostic outcome, held-out correctness outcome, or predictive result was produced.",
            "The publicly exposed held-out bank and diagnostic candidate-screening history remain provenance limitations to disclose in any later report.",
        ]
    }


class AllocationStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package=build_package(); cls.rows=cls.package["allocation_rows"]

    def test_exactly_30_unique_parent_rows(self):
        self.assertEqual(len(self.rows),30)
        self.assertEqual(len({r['parent_id'] for r in self.rows}),30)
        self.assertEqual({r['parent_id'] for r in self.rows},set(PARENT_FAMILY))

    def test_parent_family_mapping_matches_frozen_roster(self):
        for r in self.rows:self.assertEqual(r['family_id'],PARENT_FAMILY[r['parent_id']])

    def test_complete_28_plus_two_pair_schedule(self):
        counts=Counter(tuple(r['pair']) for r in self.rows)
        self.assertEqual(len(counts),28)
        self.assertTrue(all(v in (1,2) for v in counts.values()))
        self.assertEqual({p for p,v in counts.items() if v==2}, {("M01","M02"),("M03","M04")})
        self.assertEqual(sum(counts.values()),30)

    def test_sa_sb_orientation_is_complete_and_balanced(self):
        a=Counter(r['SA_mutation_A'] for r in self.rows)
        b=Counter(r['SB_mutation_B'] for r in self.rows)
        self.assertEqual(set(a),{f'M{i:02d}' for i in range(1,9)})
        self.assertEqual(set(b),{f'M{i:02d}' for i in range(1,9)})
        self.assertTrue(all(abs(a[q]-b[q])<=1 for q in a))
        self.assertEqual(sum(a.values()),30); self.assertEqual(sum(b.values()),30)

    def test_s_extra_balance_and_parent_nonduplication(self):
        counts=Counter(r['S_extra'] for r in self.rows)
        self.assertEqual(sorted(counts.values()),[3,3,4,4,4,4,4,4])
        for r in self.rows:self.assertNotIn(r['S_extra'],r['pair'])

    def test_all_40_incidence_cells_reported(self):
        inc=incidence(self.rows)
        self.assertEqual(sum(len(x) for x in inc.values()),40)
        self.assertTrue(all(len(inc[f])==8 for f in FAMILY_RANGES))

    def test_k5_cannot_meet_three_parent_floor(self):
        inc=incidence(self.rows)
        self.assertTrue(all(v<=2 for v in inc['K5'].values()))

    def test_sixteen_raw_id_candidate_support_cells(self):
        cells=[(f,q) for f,vals in incidence(self.rows).items() if f!="K5" for q,v in vals.items() if v>=3]
        self.assertEqual(len(cells),16)

    def test_c6_witness_skeletons_are_arithmetically_coherent(self):
        w=self.package['summary']['C6_witness_skeletons']
        self.assertEqual(len(w),16)
        for cell in w:
            ps=cell['parent_witness_skeletons']
            self.assertEqual(len(ps),3)
            self.assertEqual(len({p['parent_id'] for p in ps}),3)
            self.assertEqual({p['k_fail'] for p in ps},{2})
            self.assertEqual({p['k_unresolved'] for p in ps},{0})
            self.assertEqual(len({p['C_D'] for p in ps}),2)
            q=cell['mechanism_id']; fam=cell['family_id']
            eligible={r['parent_id'] for r in self.rows if r['family_id']==fam and q in r['pair']+[r['S_extra']]}
            self.assertTrue({p['parent_id'] for p in ps}.issubset(eligible))
            for p in ps:
                self.assertEqual(len(p['f']),8); self.assertEqual(len(p['u']),8)
                self.assertEqual(sum(p['f']),2); self.assertEqual(sum(p['u']),0)
                self.assertTrue(all(a+b<=8 for a,b in zip(p['f'],p['u'])))
                reach=set(MECHANISMS[int(q[1:])]['strata'])
                self.assertTrue(all(value==0 or f'D{j+1}' in reach for j,value in enumerate(p['f'])))
                expected=Fraction(max(p['f']),sum(p['f']))
                self.assertEqual(p['C_D'],f'{expected.numerator}/{expected.denominator}')
                self.assertEqual(p['witness_status'],'HYPOTHETICAL_SKELETON_NOT_ADMISSIBLE')

    def test_every_mechanism_has_family_adapter_for_all_five_formulations(self):
        expected=set(FAMILY_RANGES)
        for mechanism in MECHANISMS.values():
            self.assertEqual(set(mechanism["family_adapters"]),expected)
            self.assertTrue(all(mechanism["family_adapters"][f] for f in expected))

    def test_repeat_pair_occurrences_have_distinct_parent_families_and_reversed_roles(self):
        rows=self.rows
        for pair in REPEATED_PAIRS:
            matches=[r for r in rows if tuple(map(lambda s:int(s[1:]),r["pair"]))==pair]
            self.assertEqual(len(matches),2)
            self.assertNotEqual(matches[0]["family_id"],matches[1]["family_id"])
            self.assertEqual(matches[0]["SA_mutation_A"],matches[1]["SB_mutation_B"])
            self.assertEqual(matches[0]["SB_mutation_B"],matches[1]["SA_mutation_A"])

    def test_all_30_assigned_pair_compositions_are_defined_across_five_families(self):
        probe_amount=6
        probe_coins=[1,3,4]
        for row in self.rows:
            a=int(row["SA_mutation_A"][1:])
            b=int(row["SB_mutation_B"][1:])
            for family in FAMILY_RANGES:
                first=mutate_pair(a,b,family,probe_amount,probe_coins)
                second=mutate_pair(a,b,family,probe_amount,probe_coins)
                self.assertIs(type(first),int,(row["parent_id"],family))
                self.assertEqual(first,second,(row["parent_id"],family))

    def test_composition_precedence_handles_overlapping_coin_filters(self):
        # M03 and M05 both remove 8 when it is both the maximum and target denomination.
        for family in FAMILY_RANGES:
            out=mutate_pair(3,5,family,8,[8,3,5])
            self.assertIs(type(out),int)
        # M04 duplicates a first coin that M03 then removes as the maximum.
        for family in FAMILY_RANGES:
            out=mutate_pair(3,4,family,16,[8,4,5])
            self.assertIs(type(out),int)
        # M02 and M08 combine finite-use semantics with a doubled contribution weight.
        for family in FAMILY_RANGES:
            out=mutate_pair(2,8,family,6,[1,3,4])
            self.assertIs(type(out),int)

    def test_all_30_parent_compatibility_entries_are_explicitly_provisional(self):
        matrix=self.package["parent_compatibility_matrix"]
        self.assertEqual(len(matrix),30)
        self.assertEqual({r["parent_id"] for r in matrix},set(PARENT_FAMILY))
        for r in matrix:
            self.assertEqual(r["family_id"],PARENT_FAMILY[r["parent_id"]])
            self.assertEqual(r["formulation_level_status"],"PROPOSED_COMPATIBLE")
            self.assertEqual(r["source_patch_status"],"NOT_REVIEWED_NO_PARENT_SOURCE_BODY_EXISTS")
            self.assertTrue(r["SA_family_adapter"] and r["SB_family_adapter"] and r["S_extra_family_adapter"])

    def test_hashes_and_opaque_variant_ids_are_not_fabricated(self):
        self.assertTrue(all(r['parent_source_sha256'] is None for r in self.rows))
        self.assertTrue(all(r['opaque_solver_ids'] is None for r in self.rows))


# Test-only semantic models: not candidate solver sources and not imported/executed study
# bodies. All outputs are compared with the exact DP oracle on synthetic domain inputs.
class SyntheticMutationSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = build_package()["allocation_rows"]

    def test_each_mechanism_reaches_two_declared_strata(self):
        self.assertEqual(set(FIXTURES),set(range(1,9)))
        for m, by_stratum in FIXTURES.items():
            self.assertTrue(set(MECHANISMS[m]['witness_strata']).issubset(set(by_stratum)))
            self.assertTrue(set(by_stratum).issubset(set(MECHANISMS[m]['strata'])))
            self.assertTrue(all(len(by_stratum[stratum])>=2 for stratum in MECHANISMS[m]["witness_strata"]))
            self.assertTrue(all(len(v)>=1 for v in by_stratum.values()))

    def test_dp_oracles_agree_on_all_50_synthetic_inputs(self):
        all_inputs=[]
        for by_stratum in FIXTURES.values():
            for examples in by_stratum.values(): all_inputs.extend(examples)
        self.assertEqual(len(all_inputs),50)
        for amount,coins in all_inputs:
            self.assertEqual(oracle(amount,coins),oracle_2d(amount,coins),(amount,coins))

    def test_exhaustive_oracle_agrees_on_bounded_small_fixtures(self):
        small=[]
        for by_stratum in FIXTURES.values():
            for examples in by_stratum.values():
                small.extend((a,c) for a,c in examples if a<=10 and len(c)<=6)
        self.assertGreaterEqual(len(small),20)
        for amount,coins in small:
            self.assertEqual(oracle(amount,coins),oracle_exhaustive(amount,coins),(amount,coins))

    def test_all_declared_triggers_across_five_family_adapters(self):
        families = tuple(FAMILY_RANGES)
        tested = 0
        for m, by_stratum in FIXTURES.items():
            for stratum, examples in by_stratum.items():
                for amount, coins in examples:
                    self.assertGreaterEqual(len(coins),1)
                    self.assertLessEqual(len(coins),300)
                    self.assertTrue(all(type(c) is int and 1<=c<=5000 for c in coins))
                    self.assertEqual(len(coins),len(set(coins)), "coin denominations must be distinct")
                    self.assertTrue(0<=amount<=5000)
                    good=oracle(amount,coins)
                    for family in families:
                        baseline=solve_family(family,amount,coins)
                        self.assertEqual(baseline,good,("baseline",family,amount,coins,good,baseline))
                        bad=mutate_family(m,family,amount,coins)
                        self.assertIs(type(bad),int)
                        self.assertNotEqual(good,bad,(m,family,stratum,amount,coins,good,bad))
                        tested += 1
        self.assertEqual(tested,250)

    def test_negative_controls_do_not_activate_the_named_fault(self):
        for m,(amount,coins) in NEGATIVE_CONTROLS.items():
            expected=oracle(amount,coins)
            for family in FAMILY_RANGES:
                self.assertEqual(mutate_family(m,family,amount,coins),expected,("negative-control",m,family))

    def test_every_allocated_pair_has_a_composed_effect_on_at_least_one_declared_trigger_fixture(self):
        for row in self.rows:
            a=int(row["SA_mutation_A"][1:]); b=int(row["SB_mutation_B"][1:])
            candidates=[]
            for m in (a,b):
                for examples in FIXTURES[m].values(): candidates.extend(examples)
            for family in FAMILY_RANGES:
                changed=False
                for amount,coins in candidates:
                    baseline=solve_family(family,amount,coins)
                    combined=mutate_pair(a,b,family,amount,coins)
                    if combined != baseline:
                        changed=True; break
                self.assertTrue(changed,(row["parent_id"],a,b,family,"combined pair never changes any assigned trigger fixture"))

    def test_all_proposed_mechanisms_have_explicit_trigger_predicates(self):
        for m,spec in MECHANISMS.items():
            self.assertTrue(spec.get("trigger_condition"),m)
            self.assertTrue(spec.get("definition"),m)

    def test_d6_permutation_pair_exhibits_order_dependence_for_m06_in_all_families(self):
        amount=5
        a=[7,5,2]; b=[2,5,7]
        self.assertEqual(sorted(a),sorted(b))
        self.assertEqual(oracle(amount,a),oracle(amount,b))
        for family in FAMILY_RANGES:
            self.assertEqual(solve_family(family,amount,a),solve_family(family,amount,b))
            self.assertNotEqual(mutate_family(6,family,amount,a),mutate_family(6,family,amount,b))


def main() -> int:
    pkg=build_package()
    out=OUT/"OWNER_SEALED_NEW_ALLOCATION_v0.1.json"
    out.write_text(json.dumps(pkg,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    suite=unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(AllocationStructureTests),
        unittest.defaultTestLoader.loadTestsFromTestCase(SyntheticMutationSemanticsTests),
    ])
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report=[]
    report.append("LC518 NEW ALLOCATION v0.1 — SYNTHETIC STRUCTURAL VALIDATION")
    report.append(f"Tests run: {result.testsRun}")
    report.append(f"Failures: {len(result.failures)}")
    report.append(f"Errors: {len(result.errors)}")
    report.append(f"Pair assignments: {len(pkg['allocation_rows'])}; unique pairs: {pkg['summary']['unique_unordered_pairs']}; repeated pairs: {pkg['summary']['repeated_pair_counts']}")
    report.append(f"SA incidence: {pkg['summary']['SA_incidence_by_mechanism']}")
    report.append(f"SB incidence: {pkg['summary']['SB_incidence_by_mechanism']}")
    report.append(f"S-extra incidence: {pkg['summary']['S_extra_incidence_by_mechanism']}")
    n_fixtures=sum(len(examples) for by_stratum in FIXTURES.values() for examples in by_stratum.values())
    report.append(f"Synthetic positive-trigger inputs: {n_fixtures} (valid under published D1-D8 descriptions; not asserted to be frozen bank rows).")
    report.append(f"Family-semantic checks: {n_fixtures * len(FAMILY_RANGES)}; each baseline family result matched the independent DP oracle and each designated mutant changed its trigger fixture.")
    report.append(f"Negative-control checks: {len(NEGATIVE_CONTROLS) * len(FAMILY_RANGES)}; each named mutation was silent on its predeclared non-trigger case.")
    report.append(f"Pair-composition checks: {len(pkg['allocation_rows']) * len(FAMILY_RANGES)} assigned parent-pair/family compositions were deterministic; separate test confirms each pair changes at least one trigger fixture in each family model.")
    report.append("Oracle checks: independent 1-D and 2-D DPs agree on all 50 inputs; bounded exhaustive multiplicity enumeration also agrees on the small-input subset.")
    report.append("Compatibility scope: all 30 parent/tactic entries have proposed family-adapter mappings; no source-specific patch compatibility has been established.")
    report.append(f"Raw-ID candidate C6 cells (K1-K4): {pkg['summary']['candidate_C6_cell_count']}; 48 witness skeletons are arithmetic proposals only.")
    report.append("C6 status: NOT PASSED; source-specific joint attainability, bank-record mapping, and C4 source-hash deduplication are not established.")
    report.append("Parent source hashes: missing; C4 effective parent-group deduplication unverified.")
    report.append("Exact diagnostic bank record mapping: not tested; fixtures are synthetic.")
    report.append("Candidate solver source bodies: none created or executed.")
    report.append("Overall: PASS for listed structural and synthetic semantic checks only; NOT an A2 verdict.")
    report_path=OUT/"VALIDATION_REPORT.txt"
    report_path.write_text("\n".join(report)+"\n",encoding="utf-8")
    if not result.wasSuccessful():return 1
    print("\n".join(report))
    print(f"Wrote {out}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())