"""LC518-150 production-generator candidate for frozen C9 revision 2.6.

This file is deliberately fail-closed. It contains the implementation, but its
entry point refuses bank generation until a separate execution protocol pins
an exact interpreter and output directory and a distinct bank-generation GO is
recorded. The acceptance suite uses synthetic trace/input fixtures only.

No candidate solver source is imported, constructed, or executed here.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Protocol

# Frozen C9 literals.
SEED_HELDOUT = 20261101
SEED_DIAGNOSTIC = 11052026
MAX_INT32 = 2_147_483_647
MAX_WHOLE_CANDIDATE_ATTEMPTS = 1000
MAX_COIN_SLOT_ATTEMPTS = 1000

# Protocol v1 proposal: CPython 3.13.5 is the in-script version guard.
# The launcher independently verifies the exact binary fingerprint and full
# sys.version/platform record. OUTPUT_DIR remains unset until the owner chooses
# a concrete absolute run path. The production generator reads no environment
# variables, command-line arguments, or configuration files.
EXPECTED_PYTHON_VERSION = (3, 13, 5)
OUTPUT_DIR: str | None = "/home/z/lc518_run/bank"
BANK_GENERATION_AUTHORIZED = True

JSON_KW = dict(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

QUOTAS = {
    "D1": 8, "D2": 8, "D3": 8, "D4": 8, "D5": 8, "D6": 8, "D7": 8, "D8": 8,
    "H1": 12, "H2": 12, "H3": 8, "H4": 8, "H5": 10, "H6": 10, "H7": 8, "H8": 12,
}

REJECTION_REASONS = {
    "MIN_COIN_ONE", "GCD_DIVIDES_AMOUNT", "D4_GCD_NOT_ONE",
    "D5_GREEDY_EQUALS_MINIMUM", "H2_MATCH_AMOUNT_BELOW_13",
    "H2_ORACLE_BELOW_TWO", "H4_MATCH_AMOUNT_BELOW_20",
    "H8_ORACLE_BELOW_TWO", "INT32_OVERFLOW",
    "WITHIN_BANK_CANONICAL_COLLISION", "CROSS_BANK_COLLISION",
    "IDENTITY_PERMUTATION",
}


class GeneratorDefect(RuntimeError):
    """A defect in the frozen design or generator implementation."""


class CoinSlotBudgetExhausted(GeneratorDefect):
    """A coin-array slot exceeded its 1,000 randrange-attempt budget."""


@dataclass(frozen=True)
class RawRecord:
    amount: int
    coins: tuple[int, ...]  # as-given order
    stratum: str
    rule_params: dict[str, Any]


@dataclass(frozen=True)
class Candidate:
    records: tuple[RawRecord, ...]  # one record, or original + permutation
    candidate_id: str
    stratum: str
    early_reject_reason: str | None = None

    @property
    def key(self) -> tuple[int, tuple[int, ...]]:
        first = self.records[0]
        return canonical_key(first.amount, first.coins)

    @property
    def is_pair(self) -> bool:
        return len(self.records) == 2


class RandomLike(Protocol):
    def randrange(self, start: int, stop: int | None = None) -> int: ...
    def shuffle(self, x: list[Any]) -> None: ...


def canonical_key(amount: int, coins: Iterable[int]) -> tuple[int, tuple[int, ...]]:
    return (amount, tuple(sorted(coins)))


def canonical_id(amount: int, coins: Iterable[int]) -> str:
    payload = {"amount": amount, "coins": list(sorted(coins))}
    raw = json.dumps(payload, **JSON_KW).encode("utf-8")
    return "C-" + hashlib.sha256(raw).hexdigest()


def compact_json_bytes(value: Any) -> bytes:
    return json.dumps(value, **JSON_KW).encode("utf-8") + b"\n"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def combinations_count(amount: int, coins: Iterable[int]) -> int:
    """LC518 unbounded combinations oracle, order-independent over denominations."""
    if type(amount) is not int or amount < 0:
        raise GeneratorDefect("amount must be a nonnegative exact int")
    denoms = tuple(sorted(coins))
    if any(type(c) is not int or c <= 0 for c in denoms):
        raise GeneratorDefect("denominations must be positive exact ints")
    if len(set(denoms)) != len(denoms):
        raise GeneratorDefect("denominations must be distinct")
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in denoms:
        for total in range(coin, amount + 1):
            dp[total] += dp[total - coin]
    return dp[amount]


def no_reuse_subset_count(amount: int, coins: Iterable[int]) -> int:
    """N0: 0/1 subset count, each distinct denomination used at most once."""
    if type(amount) is not int or amount < 0:
        raise GeneratorDefect("amount must be a nonnegative exact int")
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in sorted(coins):
        if type(coin) is not int or coin <= 0:
            raise GeneratorDefect("denominations must be positive exact ints")
        for total in range(amount, coin - 1, -1):
            dp[total] += dp[total - coin]
    return dp[amount]


def greedy_count(amount: int, coins: Iterable[int]) -> int:
    remaining = amount
    used = 0
    for coin in sorted(coins, reverse=True):
        q, remaining = divmod(remaining, coin)
        used += q
    return used if remaining == 0 else math.inf  # type: ignore[return-value]


def minimum_coin_count(amount: int, coins: Iterable[int]) -> int | float:
    best: list[int | float] = [math.inf] * (amount + 1)
    best[0] = 0
    for total in range(1, amount + 1):
        best[total] = min((best[total - c] + 1 for c in coins if c <= total), default=math.inf)
    return best[amount]


def _draw(rng: RandomLike, label: str, lo: int, hi: int, trace: list[tuple[str, Any]] | None) -> int:
    if lo > hi:
        raise GeneratorDefect(f"invalid inclusive range for {label}: [{lo}, {hi}]")
    if lo == hi:
        raise GeneratorDefect(f"degenerate random range forbidden for {label}: [{lo}, {hi}]")
    if trace is not None:
        trace.append((label, (lo, hi)))
    return rng.randrange(lo, hi + 1)


def draw_unique(
    rng: RandomLike,
    count: int,
    lo: int,
    hi: int,
    *,
    already: Iterable[int] = (),
    label: str = "coin",
    trace: list[tuple[str, Any]] | None = None,
) -> list[int]:
    """Full-interval rejection sampling, with 1,000 attempts per slot per candidate."""
    used = set(already)
    result: list[int] = []
    for slot in range(1, count + 1):
        for attempt in range(1, MAX_COIN_SLOT_ATTEMPTS + 1):
            value = _draw(rng, f"{label}[{slot}]", lo, hi, trace)
            if value not in used:
                used.add(value)
                result.append(value)
                break
        else:
            raise CoinSlotBudgetExhausted(
                f"{label}[{slot}] exceeded {MAX_COIN_SLOT_ATTEMPTS} randrange attempts"
            )
    return result


def _gcd_all(values: Iterable[int]) -> int:
    result = 0
    for value in values:
        result = math.gcd(result, value)
    return result


def _single(
    amount: int,
    coins: Iterable[int],
    stratum: str,
    params: dict[str, Any],
    early_reject_reason: str | None = None,
) -> Candidate:
    return Candidate((RawRecord(amount, tuple(coins), stratum, params),), "", stratum, early_reject_reason)


def draw_raw_candidate(
    stratum: str,
    k: int,
    rng: RandomLike,
    *,
    trace: list[tuple[str, Any]] | None = None,
) -> Candidate:
    """Draw one record-slot candidate (or one whole D6/H6 pair candidate).

    This function performs only the exact prescribed draws. It does not validate,
    call the LC518 oracle, accept/reject, assign final IDs, or write files.
    It is also used by the synthetic draw-order trace tests.
    """
    if stratum not in QUOTAS or not 1 <= k <= QUOTAS[stratum]:
        raise ValueError(f"invalid stratum/record index: {stratum} {k}")

    if stratum == "D1":
        n = _draw(rng, "n", 1, 4, trace)
        coins = draw_unique(rng, n, 1, 20, label="coins", trace=trace)
        c_min = min(coins)
        amount = [0, 1, 2, c_min - 1, c_min, c_min + 1, 2 * c_min, 2 * c_min + 1][k - 1]
        return _single(amount, coins, stratum, {"c_min": c_min, "pattern_index": k - 1})

    if stratum == "D2":
        m = _draw(rng, "m", 1, 4, trace)
        c_star = _draw(rng, "c_star", 1, 5000, trace)
        distractors = draw_unique(rng, m, 1, 5000, already=(c_star,), label="distractors", trace=trace)
        return _single(c_star, [c_star, *distractors], stratum, {"match_coin": c_star})

    if stratum == "D3":
        if k <= 4:
            n = _draw(rng, "n", 2, 6, trace)
            coins = draw_unique(rng, n, 1, 5000, label="coins", trace=trace)
            c_min = min(coins)
            if c_min == 1:
                # The stratum rule rejects before amount exists or is drawn.
                return _single(0, coins, stratum, {"mechanism": "min-coin"}, "MIN_COIN_ONE")
            amount = 1 if c_min == 2 else _draw(rng, "amount", 1, c_min - 1, trace)
            return _single(amount, coins, stratum, {"mechanism": "min-coin"})
        g = _draw(rng, "g", 2, 10, trace)
        n = _draw(rng, "n", 2, 6, trace)
        t = draw_unique(rng, n, 1, 5000 // g, label="t", trace=trace)
        amount = _draw(rng, "amount", 1, 5000, trace)
        return _single(amount, [g * x for x in t], stratum, {"mechanism": "gcd", "g": g})

    if stratum == "D4":
        n = _draw(rng, "n", 2, 6, trace)
        if k <= 4:
            t = draw_unique(rng, n, 1, 2500, label="t", trace=trace)
            coins = [2 * x - 1 for x in t]
            if k <= 2:
                amount = 2 * _draw(rng, "amount_half", 0, 2500, trace)
                mechanism = "odd-even-amt"
            else:
                amount = 2 * _draw(rng, "amount_half", 0, 2499, trace) + 1
                mechanism = "odd-odd-amt"
            return _single(amount, coins, stratum, {"mechanism": mechanism})
        t = draw_unique(rng, n, 1, 2500, label="t", trace=trace)
        if _gcd_all(t) != 1:
            # The whole record is rejected from its n draw; amount is not drawn.
            return _single(0, [2 * x for x in t], stratum, {"mechanism": "gcd2"}, "D4_GCD_NOT_ONE")
        amount = 2 * _draw(rng, "amount_half", 0, 2499, trace) + 1
        return _single(amount, [2 * x for x in t], stratum, {"mechanism": "gcd2"})

    if stratum == "D5":
        if k == 1:
            return _single(8, [1, 4, 5, 6, 9], stratum, {"exemplar_id": "D5-E1"})
        if k == 2:
            return _single(9, [1, 2, 4, 5, 6], stratum, {"exemplar_id": "D5-E2"})
        n = _draw(rng, "n", 3, 5, trace)
        coins = [1, *draw_unique(rng, n - 1, 2, 9, already=(1,), label="further_coins", trace=trace)]
        amount = _draw(rng, "amount", 5, 30, trace)
        return _single(amount, coins, stratum, {"coin_1_fixed": True})

    if stratum == "D6":
        if k not in (1, 3, 5, 7):
            raise ValueError("D6 slots are addressed by original record indices 1,3,5,7")
        pair_no = (k + 1) // 2
        pair_id = f"D6-P{pair_no:02d}"
        amount = _draw(rng, "amount", 10, 200, trace)
        n = _draw(rng, "n", 3, 8, trace)
        coins = draw_unique(rng, n, 1, 200, label="coins", trace=trace)
        shuffled = list(coins)
        if trace is not None:
            trace.append(("shuffle", "permutation"))
        rng.shuffle(shuffled)
        original = RawRecord(amount, tuple(coins), stratum, {"pair_id": pair_id, "ordering": "original"})
        permuted = RawRecord(amount, tuple(shuffled), stratum, {"pair_id": pair_id, "ordering": "permutation"})
        return Candidate((original, permuted), pair_id, stratum)

    if stratum == "D7":
        amount = _draw(rng, "amount", 50, 500, trace)
        n = _draw(rng, "n", 50, 300, trace)
        coins = draw_unique(rng, n, 1, 5000, label="coins", trace=trace)
        return _single(amount, coins, stratum, {})

    if stratum == "D8":
        amount = _draw(rng, "amount", 2000, 5000, trace)
        n = _draw(rng, "n", 3, 30, trace)
        coins = draw_unique(rng, n, 1, 5000, label="coins", trace=trace)
        return _single(amount, coins, stratum, {})

    if stratum == "H1":
        if k == 4:
            return _single(12, [2, 3], stratum, {"edge": False, "repeated_use_witness": True})
        amount = _draw(rng, "amount", 0, 1, trace) if k <= 3 else _draw(rng, "amount", 2, 12, trace)
        n = _draw(rng, "n", 1, 4, trace)
        coins = draw_unique(rng, n, 1, 20, label="coins", trace=trace)
        return _single(amount, coins, stratum, {"edge": k <= 3, "repeated_use_witness": False})

    if stratum == "H2":
        if k == 5:
            return _single(60, [2, 58], stratum, {"forced_coin_1": False, "match_amount": False, "repeated_use_witness": True})
        if k <= 4:
            n = _draw(rng, "n", 2, 6, trace)
            rest = draw_unique(rng, n - 1, 2, 60, already=(1,), label="remaining_coins", trace=trace)
            coins = [1, *rest]
            if k == 1:
                amount = max(coins)
            else:
                amount = _draw(rng, "amount", 13, 60, trace)
            return _single(amount, coins, stratum, {"forced_coin_1": True, "match_amount": k == 1, "repeated_use_witness": False})
        n = _draw(rng, "n", 2, 6, trace)
        coins = draw_unique(rng, n, 1, 60, label="coins", trace=trace)
        amount = _draw(rng, "amount", 13, 60, trace)
        return _single(amount, coins, stratum, {"forced_coin_1": False, "match_amount": False, "repeated_use_witness": False})

    if stratum == "H3":
        if k == 1:
            return _single(100, [50], stratum, {"repeated_use_witness": True})
        amount = _draw(rng, "amount", 0, 5000, trace)
        coin = _draw(rng, "coin", 1, 50, trace)
        return _single(amount, [coin], stratum, {"repeated_use_witness": False})

    if stratum == "H4":
        if k <= 2:
            coins = draw_unique(rng, 2, 1, 5000, label="coins", trace=trace)
            return _single(max(coins), coins, stratum, {"match_amount": True, "repeated_use_witness": False})
        if k == 3:
            return _single(100, [4, 96], stratum, {"match_amount": False, "repeated_use_witness": True})
        amount = _draw(rng, "amount", 20, 5000, trace)
        coins = draw_unique(rng, 2, 1, 5000, label="coins", trace=trace)
        return _single(amount, coins, stratum, {"match_amount": False, "repeated_use_witness": False})

    if stratum == "H5":
        amount = _draw(rng, "amount", 100, 2000, trace)
        n = _draw(rng, "n", 30, 120, trace)
        coins = draw_unique(rng, n, 1, 5000, label="coins", trace=trace)
        return _single(amount, coins, stratum, {})

    if stratum == "H6":
        if k <= 6:
            amount = _draw(rng, "amount", 3500, 5000, trace)
            n = _draw(rng, "n", 5, 40, trace)
            coins = draw_unique(rng, n, 1, 5000, label="coins", trace=trace)
            return _single(amount, coins, stratum, {"singleton": True})
        if k not in (7, 9):
            raise ValueError("H6 pair slots are addressed by original record indices 7 and 9")
        pair_no = 1 if k == 7 else 2
        pair_id = f"H6-P{pair_no:02d}"
        amount = _draw(rng, "amount", 3500, 5000, trace)
        n = _draw(rng, "n", 5, 40, trace)
        coins = draw_unique(rng, n, 1, 5000, label="coins", trace=trace)
        shuffled = list(coins)
        if trace is not None:
            trace.append(("shuffle", "permutation"))
        rng.shuffle(shuffled)
        original = RawRecord(amount, tuple(coins), stratum, {"pair_id": pair_id, "ordering": "original"})
        permuted = RawRecord(amount, tuple(shuffled), stratum, {"pair_id": pair_id, "ordering": "permutation"})
        return Candidate((original, permuted), pair_id, stratum)

    if stratum == "H7":
        if k <= 4:
            n = _draw(rng, "n", 2, 6, trace)
            coins = draw_unique(rng, n, 1, 5000, label="coins", trace=trace)
            c_min = min(coins)
            if c_min == 1:
                # The stratum rule rejects before amount exists or is drawn.
                return _single(0, coins, stratum, {"mechanism": "min-coin"}, "MIN_COIN_ONE")
            amount = 1 if c_min == 2 else _draw(rng, "amount", 1, c_min - 1, trace)
            return _single(amount, coins, stratum, {"mechanism": "min-coin"})
        g = _draw(rng, "g", 2, 10, trace)
        n = _draw(rng, "n", 2, 6, trace)
        t = draw_unique(rng, n, 1, 5000 // g, label="t", trace=trace)
        amount = _draw(rng, "amount", 1, 5000, trace)
        return _single(amount, [g * x for x in t], stratum, {"mechanism": "gcd", "g": g})

    if stratum == "H8":
        if k == 7:
            return _single(6, [1, 3, 4], stratum, {"anchor": "1-3-4", "anchor_fixed": True})
        if k <= 6:
            anchor = [1, 2, 3]
            n = _draw(rng, "n", 3, 8, trace)
            further = draw_unique(rng, n - 3, 4, 5000, already=anchor, label="further_coins", trace=trace)
            amount = _draw(rng, "amount", 6, 800, trace)
            return _single(amount, [*anchor, *further], stratum, {"anchor": "1-2-3", "anchor_fixed": True})
        anchor = [1, 3, 4]
        n = _draw(rng, "n", 3, 8, trace)
        further = draw_unique(rng, n - 3, 2, 5000, already=anchor, label="further_coins", trace=trace)
        amount = _draw(rng, "amount", 6, 800, trace)
        return _single(amount, [*anchor, *further], stratum, {"anchor": "1-3-4", "anchor_fixed": True})

    raise AssertionError("unreachable stratum")


def fixed_candidates() -> tuple[dict[str, Candidate], dict[str, Candidate]]:
    """Return exact deterministic records, with a guard against accidental draws."""
    class NoDrawRandom:
        def randrange(self, *args):
            raise GeneratorDefect("a fixed record attempted to consume RNG state")
        def shuffle(self, values):
            raise GeneratorDefect("a fixed record attempted to shuffle")
    no_rng = NoDrawRandom()
    d = {
        "D5:1": draw_raw_candidate("D5", 1, no_rng),
        "D5:2": draw_raw_candidate("D5", 2, no_rng),
    }
    h = {
        "H1:4": draw_raw_candidate("H1", 4, no_rng),
        "H2:5": draw_raw_candidate("H2", 5, no_rng),
        "H3:1": draw_raw_candidate("H3", 1, no_rng),
        "H4:3": draw_raw_candidate("H4", 3, no_rng),
        "H8:7": draw_raw_candidate("H8", 7, no_rng),
    }
    return d, h


def fixed_key_preflight() -> tuple[set[tuple[int, tuple[int, ...]]], set[tuple[int, tuple[int, ...]]]]:
    d_candidates, h_candidates = fixed_candidates()
    d_keys = [c.key for c in d_candidates.values()]
    h_keys = [c.key for c in h_candidates.values()]
    if len(d_keys) != len(set(d_keys)) or len(h_keys) != len(set(h_keys)):
        raise GeneratorDefect("fixed canonical identities are not unique within a bank")
    if set(d_keys) & set(h_keys):
        raise GeneratorDefect("fixed canonical identities overlap across banks")
    return set(d_keys), set(h_keys)


def validate_d5_structural_exclusion() -> dict[str, bool]:
    """Test the design-time D5-vs-held-out exclusion witnesses from C9 item 3d."""
    d, _ = fixed_candidates()
    exemplars = [next(iter(c.records)) for c in d.values()]
    results: dict[str, bool] = {}
    for h_stratum in (f"H{i}" for i in range(1, 9)):
        checks = []
        for rec in exemplars:
            a, cs = rec.amount, set(rec.coins)
            n = len(cs)
            if h_stratum == "H1": checks.append(n > 4)
            elif h_stratum == "H2": checks.append(a < 13)
            elif h_stratum == "H3": checks.append(n != 1)
            elif h_stratum == "H4": checks.append(n != 2)
            elif h_stratum == "H5": checks.append(n < 30)
            elif h_stratum == "H6": checks.append(a < 3500)
            elif h_stratum == "H7": checks.append(combinations_count(a, cs) != 0)
            elif h_stratum == "H8": checks.append(not ({1, 2, 3} <= cs or {1, 3, 4} <= cs))
        results[h_stratum] = all(checks)
    if not all(results.values()):
        raise GeneratorDefect(f"D5 structural exclusion proof failed: {results}")
    return results


def record_slot_plan(stratum: str) -> list[tuple[str, tuple[int, ...]]]:
    """Slot IDs in generation order; paired slots are represented once."""
    if stratum == "D6": return [(f"D6-P{i:02d}", (2*i-1, 2*i)) for i in range(1, 5)]
    if stratum == "H6": return [(f"H6-{i:03d}", (i,)) for i in range(1, 7)] + [(f"H6-P{i:02d}", (7+2*(i-1), 8+2*(i-1))) for i in range(1, 3)]
    return [(f"{stratum}:{i}", (i,)) for i in range(1, QUOTAS[stratum] + 1)]


def planned_input_id(bank: str, stratum: str, record_index: int) -> str:
    prefix = "D" if bank == "diagnostic" else "H" if bank == "heldout" else None
    if prefix is None:
        raise ValueError(f"unknown bank: {bank}")
    order = [f"{prefix}{i}" for i in range(1, 9)]
    offset = sum(QUOTAS[x] for x in order[:order.index(stratum)])
    return f"{prefix}{offset + record_index:03d}"


def planned_candidate_id(bank: str, stratum: str, record_indices: tuple[int, ...]) -> str:
    if len(record_indices) == 2:
        pair_number = (record_indices[0] + 1) // 2 if stratum == "D6" else (record_indices[0] - 5) // 2
        return f"{stratum}-P{pair_number:02d}"
    return planned_input_id(bank, stratum, record_indices[0])


def validate_basic(record: RawRecord) -> None:
    if type(record.amount) is not int or not 0 <= record.amount <= 5000:
        raise GeneratorDefect("amount outside contract or not exact int")
    if not 1 <= len(record.coins) <= 300:
        raise GeneratorDefect("coin count outside contract")
    if any(type(c) is not int or not 1 <= c <= 5000 for c in record.coins):
        raise GeneratorDefect("coin denomination outside contract or not exact int")
    if len(set(record.coins)) != len(record.coins):
        raise GeneratorDefect("duplicate denomination in one record")


def evaluate_candidate(candidate: Candidate) -> tuple[int, str | None]:
    """Run the common pipeline through stratum and pair predicates exactly once."""
    if candidate.early_reject_reason is not None:
        if candidate.early_reject_reason not in REJECTION_REASONS:
            raise GeneratorDefect("undeclared early rejection reason")
        return 0, candidate.early_reject_reason
    for raw in candidate.records:
        validate_basic(raw)
    first = candidate.records[0]
    answer = combinations_count(first.amount, first.coins)
    if answer > MAX_INT32:
        return answer, "INT32_OVERFLOW"
    reason = rejection_reason(candidate, answer)
    if reason is None and candidate.is_pair and candidate.records[0].coins == candidate.records[1].coins:
        reason = "IDENTITY_PERMUTATION"
    return answer, reason


def rejection_reason(candidate: Candidate, oracle: int) -> str | None:
    """Return the one C9 sidecar reason, preserving item 3 pipeline precedence."""
    first = candidate.records[0]
    s, k, p = first.stratum, first.coins, first.rule_params
    if s in ("D3", "H7") and p.get("mechanism") == "min-coin" and min(k) == 1:
        return "MIN_COIN_ONE"
    if s in ("D3", "H7") and p.get("mechanism") == "gcd":
        # The frozen rule rejects whenever the drawn g divides amount,
        # irrespective of whether a larger gcd would also make the answer zero.
        if first.amount % p["g"] == 0:
            return "GCD_DIVIDES_AMOUNT"
    if s == "D4" and p.get("mechanism") == "gcd2":
        if _gcd_all([c // 2 for c in k]) != 1:
            return "D4_GCD_NOT_ONE"
    if s == "D5" and "exemplar_id" not in p:
        if greedy_count(first.amount, k) == minimum_coin_count(first.amount, k):
            return "D5_GREEDY_EQUALS_MINIMUM"
    if s == "H2":
        if p.get("match_amount") and first.amount < 13:
            return "H2_MATCH_AMOUNT_BELOW_13"
        if oracle < 2:
            return "H2_ORACLE_BELOW_TWO"
    if s == "H4" and p.get("match_amount") and first.amount < 20:
        return "H4_MATCH_AMOUNT_BELOW_20"
    if s == "H8" and oracle < 2:
        return "H8_ORACLE_BELOW_TWO"
    if s == "D4" and p.get("mechanism") == "gcd2" and first.amount % 2 == 0:
        raise GeneratorDefect("D4 gcd2 odd-amount invariant failed")
    if s == "H1" and first.amount == 0 and oracle != 1:
        raise GeneratorDefect("H1 amount-zero answer-1 assertion failed")
    return None


def classify_collision(
    bank: str,
    key: tuple[int, tuple[int, ...]],
    own_reserved_and_accepted: set[tuple[int, tuple[int, ...]]],
    frozen_heldout: set[tuple[int, tuple[int, ...]]],
    fixed_d5: set[tuple[int, tuple[int, ...]]],
) -> tuple[str | None, bool]:
    """Return (reason, fatal). Held-out-vs-F_D is fatal, not retried."""
    if bank == "heldout" and key in fixed_d5:
        return "CROSS_BANK_COLLISION", True
    if key in own_reserved_and_accepted:
        return "WITHIN_BANK_CANONICAL_COLLISION", False
    if bank == "diagnostic" and key in frozen_heldout:
        return "CROSS_BANK_COLLISION", False
    return None, False


def make_sidecar_row(attempt: int, bank: str, candidate_id: str, reason: str, stratum: str) -> dict[str, Any]:
    if reason not in REJECTION_REASONS:
        raise GeneratorDefect(f"undeclared sidecar reason: {reason}")
    return {"attempt": attempt, "bank": bank, "candidate_id": candidate_id, "reason": reason, "stratum": stratum}


def _record_to_dict(
    raw: RawRecord,
    input_id: str,
    guard: dict[str, Any],
    oracle_output_file_sha256: str,
) -> dict[str, Any]:
    cid = canonical_id(raw.amount, raw.coins)
    rec: dict[str, Any] = {
        "input_id": input_id,
        "amount": raw.amount,
        "coins": list(raw.coins),
        "canonical_id": cid,
        "stratum": raw.stratum,
        "rule_id": raw.stratum,
        "rule_params": raw.rule_params,
        "int32_guard": dict(guard),
        "oracle_output_file_sha256": oracle_output_file_sha256,
    }
    # C9 item 5's serialized schema carries pair_id and ordering only inside
    # the hashed rule_params object. No top-level duplicate fields are emitted.
    return rec


def record_hash_payload(record: dict[str, Any]) -> dict[str, Any]:
    # C9 item 5 explicitly defines this closed payload. Pair metadata is stored
    # only inside rule_params, which is included in this exact payload.
    keys = (
        "input_id", "amount", "coins", "canonical_id", "stratum", "rule_id",
        "rule_params", "int32_guard", "oracle_output_file_sha256",
    )
    return {key: record[key] for key in keys}


RECORD_FIELDS_BEFORE_HASH = {
    "input_id", "amount", "coins", "canonical_id", "stratum", "rule_id",
    "rule_params", "int32_guard", "oracle_output_file_sha256",
}
RECORD_FIELDS_AFTER_HASH = RECORD_FIELDS_BEFORE_HASH | {"record_sha256"}


def validate_serialized_records(records: list[dict[str, Any]], bank_prefix: str) -> None:
    """Validate exact C9 schema and D6/H6 pair invariants.

    Pair metadata appears only inside the hashed rule_params object. Serialized
    records must not contain top-level pair_id or ordering fields.
    """
    if bank_prefix not in {"D", "H"}:
        raise GeneratorDefect("bank prefix must be D or H")
    expected_strata = {f"{bank_prefix}{i}" for i in range(1, 9)}
    expected_count = 64 if bank_prefix == "D" else 80
    if len(records) != expected_count:
        raise GeneratorDefect(f"{bank_prefix} bank has {len(records)} records, expected {expected_count}")

    for index, record in enumerate(records, start=1):
        if set(record) not in (RECORD_FIELDS_BEFORE_HASH, RECORD_FIELDS_AFTER_HASH):
            extra = sorted(set(record) - RECORD_FIELDS_AFTER_HASH)
            missing = sorted(RECORD_FIELDS_BEFORE_HASH - set(record))
            raise GeneratorDefect(f"{bank_prefix} record schema mismatch; extra={extra}, missing={missing}")
        expected_id = f"{bank_prefix}{index:03d}"
        if record.get("input_id") != expected_id:
            raise GeneratorDefect(f"record ordinal mismatch: expected {expected_id}")
        stratum = record.get("stratum")
        if stratum not in expected_strata or record.get("rule_id") != stratum:
            raise GeneratorDefect(f"{expected_id}: stratum/rule_id mismatch")
        if not isinstance(record.get("rule_params"), dict):
            raise GeneratorDefect(f"{expected_id}: rule_params must be an object")
        if record.get("canonical_id") != canonical_id(record["amount"], record["coins"]):
            raise GeneratorDefect(f"{expected_id}: canonical_id mismatch")
        if not isinstance(record.get("oracle_output_file_sha256"), str) or len(record["oracle_output_file_sha256"]) != 64:
            raise GeneratorDefect(f"{expected_id}: oracle output digest malformed")
        guard = record.get("int32_guard")
        if not isinstance(guard, dict) or set(guard) != {"status", "redraws"}:
            raise GeneratorDefect(f"{expected_id}: int32_guard schema mismatch")
        if type(guard["redraws"]) is not int or guard["redraws"] < 0:
            raise GeneratorDefect(f"{expected_id}: invalid int32 redraw count")
        if guard["status"] not in {"accepted", "redrawn"}:
            raise GeneratorDefect(f"{expected_id}: invalid int32 guard status")
        if (guard["redraws"] == 0) != (guard["status"] == "accepted"):
            raise GeneratorDefect(f"{expected_id}: int32 guard status/redraw count disagree")
        if "record_sha256" in record:
            expected_hash = sha256_bytes(json.dumps(record_hash_payload(record), **JSON_KW).encode("utf-8"))
            if record["record_sha256"] != expected_hash:
                raise GeneratorDefect(f"{expected_id}: record_sha256 mismatch")

    expected_pair_ids = {f"{bank_prefix}6-P{i:02d}" for i in range(1, 5 if bank_prefix == "D" else 3)}
    observed_pair_ids: set[str] = set()
    observed_pair_sequence: list[str] = []
    i = 0
    while i < len(records):
        record = records[i]
        stratum = record["stratum"]
        rp = record["rule_params"]
        has_pair_id = "pair_id" in rp
        has_ordering = "ordering" in rp
        if has_pair_id != has_ordering:
            raise GeneratorDefect(f"{record['input_id']}: pair_id/ordering must appear together in rule_params")
        is_pair_record = has_pair_id
        if is_pair_record and stratum != f"{bank_prefix}6":
            raise GeneratorDefect(f"{record['input_id']}: pair metadata outside D6/H6")
        if stratum == f"{bank_prefix}6" and bank_prefix == "D" and not is_pair_record:
            raise GeneratorDefect(f"{record['input_id']}: every D6 record must be part of a pair")
        if stratum == f"{bank_prefix}6" and bank_prefix == "H" and not is_pair_record:
            if rp != {"singleton": True}:
                raise GeneratorDefect(f"{record['input_id']}: H6 singleton metadata mismatch")
            i += 1
            continue
        if not is_pair_record:
            i += 1
            continue
        if rp.get("ordering") == "permutation":
            raise GeneratorDefect(f"{record['input_id']}: permutation row has no immediately preceding original")
        if rp.get("ordering") != "original" or set(rp) != {"pair_id", "ordering"}:
            raise GeneratorDefect(f"{record['input_id']}: pair original metadata invalid")
        if i + 1 >= len(records):
            raise GeneratorDefect(f"{record['input_id']}: missing adjacent permutation record")
        mate = records[i + 1]
        mate_rp = mate["rule_params"]
        pair_id = rp.get("pair_id")
        if not isinstance(pair_id, str) or pair_id not in expected_pair_ids or pair_id in observed_pair_ids:
            raise GeneratorDefect(f"{record['input_id']}: invalid or duplicate pair_id")
        if mate["stratum"] != f"{bank_prefix}6" or set(mate_rp) != {"pair_id", "ordering"}:
            raise GeneratorDefect(f"{pair_id}: pair records are not adjacent in the same stratum")
        if mate_rp.get("pair_id") != pair_id or mate_rp.get("ordering") != "permutation":
            raise GeneratorDefect(f"{pair_id}: permutation metadata mismatch")
        if mate["input_id"] != f"{bank_prefix}{i + 2:03d}":
            raise GeneratorDefect(f"{pair_id}: pair input IDs are not consecutive")
        if record["amount"] != mate["amount"]:
            raise GeneratorDefect(f"{pair_id}: pair amounts differ")
        if sorted(record["coins"]) != sorted(mate["coins"]):
            raise GeneratorDefect(f"{pair_id}: sorted denomination sets differ")
        if record["coins"] == mate["coins"]:
            raise GeneratorDefect(f"{pair_id}: identity permutation")
        if record["canonical_id"] != mate["canonical_id"]:
            raise GeneratorDefect(f"{pair_id}: canonical_id mismatch")
        if record["int32_guard"] != mate["int32_guard"]:
            raise GeneratorDefect(f"{pair_id}: int32_guard differs within pair")
        observed_pair_ids.add(pair_id)
        observed_pair_sequence.append(pair_id)
        i += 2

    expected_pair_sequence = [f"{bank_prefix}6-P{i:02d}" for i in range(1, 5 if bank_prefix == "D" else 3)]
    if observed_pair_ids != expected_pair_ids or observed_pair_sequence != expected_pair_sequence:
        raise GeneratorDefect(
            f"{bank_prefix} pair IDs/order mismatch: observed={observed_pair_sequence}, expected={expected_pair_sequence}"
        )

def attach_record_hashes(records: list[dict[str, Any]]) -> None:
    for record in records:
        record["record_sha256"] = sha256_bytes(json.dumps(record_hash_payload(record), **JSON_KW).encode("utf-8"))


def oracle_output_rows(
    records: list[dict[str, Any]],
    cached_answers: dict[tuple[int, tuple[int, ...]], int] | None = None,
) -> list[dict[str, Any]]:
    """Build attachment rows in first-occurrence order from canonical tuples.

    Production supplies the answers already computed by the common candidate
    pipeline. The optional uncached mode is retained for isolated fixture tests.
    A SHA-256 identifier collision between distinct mathematical inputs fails
    closed rather than merging two canonical instances.
    """
    seen_keys: set[tuple[int, tuple[int, ...]]] = set()
    id_to_key: dict[str, tuple[int, tuple[int, ...]]] = {}
    rows: list[dict[str, Any]] = []
    for record in records:
        key = canonical_key(record["amount"], record["coins"])
        cid = canonical_id(*key)
        if record["canonical_id"] != cid:
            raise GeneratorDefect("record canonical_id does not match its mathematical identity")
        previous_key = id_to_key.setdefault(cid, key)
        if previous_key != key:
            raise GeneratorDefect("SHA-256 canonical_id collision between distinct mathematical inputs")
        if key in seen_keys:
            continue
        seen_keys.add(key)
        coins = list(key[1])
        if cached_answers is None:
            answer = combinations_count(key[0], coins)
        else:
            try:
                answer = cached_answers[key]
            except KeyError as exc:
                raise GeneratorDefect(f"missing cached oracle answer for {cid}") from exc
        rows.append({
            "canonical_id": cid,
            "amount": key[0],
            "coins": coins,
            "oracle_answer": answer,
        })
    return rows


def sidecar_bytes(events: list[dict[str, Any]]) -> bytes:
    return b"".join(json.dumps(event, **JSON_KW).encode("utf-8") + b"\n" for event in events)


def emit_structured_stderr(tag: str, payload: dict[str, Any]) -> None:
    """Write a tagged, machine-parseable audit event and flush immediately."""
    if not tag or any(ch.isspace() for ch in tag):
        raise GeneratorDefect("invalid structured log tag")
    print(f"{tag} {json.dumps(payload, **JSON_KW)}", file=sys.stderr, flush=True)


def intersection_report_rows(
    diagnostic: list[dict[str, Any]], heldout: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    def grouped(rows: list[dict[str, Any]]) -> dict[tuple[int, tuple[int, ...]], list[dict[str, Any]]]:
        out: dict[tuple[int, tuple[int, ...]], list[dict[str, Any]]] = {}
        id_to_key: dict[str, tuple[int, tuple[int, ...]]] = {}
        for row in rows:
            key = canonical_key(row["amount"], row["coins"])
            cid = canonical_id(*key)
            if row["canonical_id"] != cid:
                raise GeneratorDefect("record canonical_id does not match its mathematical identity")
            previous_key = id_to_key.setdefault(cid, key)
            if previous_key != key:
                raise GeneratorDefect("SHA-256 canonical_id collision between distinct mathematical inputs")
            out.setdefault(key, []).append(row)
        return out
    dg, hg = grouped(diagnostic), grouped(heldout)
    common = set(dg) & set(hg)
    items = []
    for key in sorted(common, key=lambda item: canonical_id(*item)):
        r = dg[key][0]
        items.append({
            "canonical_id": canonical_id(*key),
            "amount": key[0],
            "coins": list(key[1]),
            "diagnostic_input_ids": [x["input_id"] for x in dg[key]],
            "heldout_input_ids": [x["input_id"] for x in hg[key]],
        })
    return items


def collision_counts(events_d: list[dict[str, Any]], events_h: list[dict[str, Any]]) -> dict[str, int]:
    counts = {f"D{i}": 0 for i in range(1, 9)} | {f"H{i}": 0 for i in range(1, 9)}
    for event in (*events_d, *events_h):
        if event["reason"] == "CROSS_BANK_COLLISION":
            counts[event["stratum"]] += 1
    return counts


def write_all_bytes(path: Path, data: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def preflight_output_directory(output_dir: Path) -> None:
    staging = Path(str(output_dir) + ".staging")
    if os.path.lexists(output_dir) or os.path.lexists(staging):
        raise GeneratorDefect("final output and staging directory entries must be absent before either RNG stream is consumed")


def atomic_publish_fixture_or_bank_package(
    output_dir: Path,
    diagnostic_bytes: bytes,
    heldout_bytes: bytes,
    diagnostic_oracle_bytes: bytes,
    heldout_oracle_bytes: bytes,
    diagnostic_sidecar: bytes,
    heldout_sidecar: bytes,
    diagnostic_rows: list[dict[str, Any]],
    heldout_rows: list[dict[str, Any]],
    events_d: list[dict[str, Any]],
    events_h: list[dict[str, Any]],
    *,
    fixture_prefix: str | None = None,
) -> dict[str, Any]:
    """Atomic item-8 publication implementation; caller supplies bytes in memory.

    The acceptance tests call it only with artificial `fixture_*` filenames and
    records. Production filenames are passed only by the blocked future runner.
    """
    staging = Path(str(output_dir) + ".staging")
    if os.path.lexists(output_dir) or os.path.lexists(staging):
        raise GeneratorDefect("final output and staging directory entries must be absent at preflight")
    intersection = intersection_report_rows(diagnostic_rows, heldout_rows)
    counts = collision_counts(events_d, events_h)
    if any(counts[f"H{i}"] for i in range(1, 9)):
        raise GeneratorDefect("CROSS_BANK_COLLISION: held-out/F_D structural contradiction was logged; item-8 publication must not proceed")
    staging.parent.mkdir(parents=True, exist_ok=True)
    staging.mkdir()
    if not intersection:
        prefix = fixture_prefix or ""
        files = {
            f"{prefix}diagnostic_oracle_outputs.json": diagnostic_oracle_bytes,
            f"{prefix}heldout_oracle_outputs.json": heldout_oracle_bytes,
            f"{prefix}diagnostic_bank.json": diagnostic_bytes,
            f"{prefix}heldout_bank.json": heldout_bytes,
            f"{prefix}diagnostic_bank.rejections.jsonl": diagnostic_sidecar,
            f"{prefix}heldout_bank.rejections.jsonl": heldout_sidecar,
        }
        for filename, data in files.items():
            write_all_bytes(staging / filename, data)
        artifacts = [{"filename": name, "sha256": sha256_bytes(data)} for name, data in sorted(files.items())]
        status = "PASS"
    else:
        prefix = fixture_prefix or ""
        files = {
            f"{prefix}diagnostic_bank.rejections.jsonl": diagnostic_sidecar,
            f"{prefix}heldout_bank.rejections.jsonl": heldout_sidecar,
        }
        for filename, data in files.items():
            write_all_bytes(staging / filename, data)
        artifacts = [{"filename": name, "sha256": sha256_bytes(data)} for name, data in sorted(files.items())]
        status = "FAIL"
    for item in artifacts:
        if sha256_bytes((staging / item["filename"]).read_bytes()) != item["sha256"]:
            raise GeneratorDefect("staged artifact digest verification failed")
    report = {
        "schema": "lc518-canonical-disjointness-v1",
        "status": status,
        "diagnostic_record_count": len(diagnostic_rows),
        "diagnostic_unique_canonical_count": len({r["canonical_id"] for r in diagnostic_rows}),
        "heldout_record_count": len(heldout_rows),
        "heldout_unique_canonical_count": len({r["canonical_id"] for r in heldout_rows}),
        "cross_bank_collision_counts_by_stratum": counts,
        "intersection": intersection,
        "artifacts": artifacts,
    }
    temp_report = staging / "canonical_disjointness_report.json.tmp"
    write_all_bytes(temp_report, compact_json_bytes(report))
    os.replace(temp_report, staging / "canonical_disjointness_report.json")
    os.replace(staging, output_dir)
    return report


PREDICATE_EXPECTED_COUNTS = {"H1": 12, "H2": 12, "H3": 8, "H4": 8}


def validate_predicate_records(
    predicate_records: list[dict[str, Any]],
    heldout_records: list[dict[str, Any]] | None = None,
    *,
    require_complete: bool = True,
) -> dict[str, int]:
    """Validate predicate accounting, optionally against accepted H-bank rows.

    For an early abort, callers use require_complete=False and preserve the
    partial counts. A completed generation must have exactly 40 unique rows.
    """
    counts = dict.fromkeys(PREDICATE_EXPECTED_COUNTS, 0)
    seen: set[str] = set()
    for item in predicate_records:
        required = {
            "input_id", "stratum", "amount", "coins", "oracle_answer", "N0",
            "repeated_use_predicate",
        }
        if set(item) != required:
            raise GeneratorDefect("predicate log record has missing or undeclared fields")
        input_id = item["input_id"]
        stratum = item["stratum"]
        if stratum not in counts or input_id in seen:
            raise GeneratorDefect(f"duplicate or out-of-scope predicate record: {input_id}")
        if type(item["amount"]) is not int or type(item["oracle_answer"]) is not int or type(item["N0"]) is not int:
            raise GeneratorDefect(f"predicate record numeric fields must be exact integers: {input_id}")
        if item["repeated_use_predicate"] is not (item["oracle_answer"] > item["N0"]):
            raise GeneratorDefect(f"predicate value does not equal oracle_answer > N0: {input_id}")
        seen.add(input_id)
        counts[stratum] += 1
    if require_complete and (len(seen) != 40 or counts != PREDICATE_EXPECTED_COUNTS):
        raise GeneratorDefect(f"repeated-use predicate accounting incomplete: {counts}")

    if heldout_records is not None:
        held_by_id = {row["input_id"]: row for row in heldout_records}
        for item in predicate_records:
            row = held_by_id.get(item["input_id"])
            if row is None or (row["amount"], row["coins"], row["stratum"]) != (
                item["amount"], item["coins"], item["stratum"]
            ):
                raise GeneratorDefect(f"predicate log does not match accepted held-out record: {item['input_id']}")
    return counts


class ProductionGenerator:
    """Full C9 generator. The only production entry point is intentionally disabled."""

    def __init__(self) -> None:
        self.fixed_d, self.fixed_h = fixed_key_preflight()
        validate_d5_structural_exclusion()
        self.heldout: list[dict[str, Any]] = []
        self.diagnostic: list[dict[str, Any]] = []
        self.events_h: list[dict[str, Any]] = []
        self.events_d: list[dict[str, Any]] = []
        self.accepted_h: set[tuple[int, tuple[int, ...]]] = set(self.fixed_h)
        self.accepted_d: set[tuple[int, tuple[int, ...]]] = set(self.fixed_d)
        self.oracle_answers_h: dict[tuple[int, tuple[int, ...]], int] = {}
        self.oracle_answers_d: dict[tuple[int, tuple[int, ...]], int] = {}
        self.repeated_use_log: list[dict[str, Any]] = []

    @staticmethod
    def _is_fixed(stratum: str, indices: tuple[int, ...]) -> bool:
        return len(indices) == 1 and (
            (stratum == "D5" and indices[0] in (1, 2))
            or (stratum == "H1" and indices[0] == 4)
            or (stratum == "H2" and indices[0] == 5)
            or (stratum == "H3" and indices[0] == 1)
            or (stratum == "H4" and indices[0] == 3)
            or (stratum == "H8" and indices[0] == 7)
        )

    def _append_accepted(
        self, bank: str, candidate: Candidate, indices: tuple[int, ...], ordinal: int,
        guard: dict[str, Any],
    ) -> None:
        target = self.heldout if bank == "heldout" else self.diagnostic
        output_sha_placeholder = "0" * 64  # replaced after oracle attachments are serialized
        for j, raw in enumerate(candidate.records):
            input_id = ("H" if bank == "heldout" else "D") + f"{ordinal + j:03d}"
            target.append(_record_to_dict(raw, input_id, guard, output_sha_placeholder))

    def _stream_rejection(self, bank: str, event: dict[str, Any]) -> None:
        events = self.events_h if bank == "heldout" else self.events_d
        events.append(event)
        emit_structured_stderr("REJECTION_EVENT", event)

    def _accept_one_slot(self, bank: str, stratum: str, indices: tuple[int, ...], rng: random.Random) -> None:
        is_fixed = self._is_fixed(stratum, indices)
        candidate_id = planned_candidate_id(bank, stratum, indices)
        slot_no = indices[0]
        prefix = "D" if bank == "diagnostic" else "H"
        ordinal = sum(QUOTAS[f"{prefix}{i}"] for i in range(1, int(stratum[1:])) ) + slot_no
        attempts = 1
        int32_redraws = 0
        max_attempts = 1 if is_fixed else MAX_WHOLE_CANDIDATE_ATTEMPTS
        while attempts <= max_attempts:
            candidate = draw_raw_candidate(stratum, slot_no, rng)
            first = candidate.records[0]
            answer, reason = evaluate_candidate(candidate)
            if reason is None and not is_fixed:
                own = self.accepted_h if bank == "heldout" else self.accepted_d
                collision, fatal = classify_collision(bank, candidate.key, own, self.accepted_h, self.fixed_d)
                reason = collision
                if fatal:
                    event = make_sidecar_row(attempts, bank, candidate_id, "CROSS_BANK_COLLISION", stratum)
                    self._stream_rejection(bank, event)
                    raise GeneratorDefect(
                        "CROSS_BANK_COLLISION: held-out candidate matched a reserved D5 fixed key; "
                        "fatal structural preflight contradiction, not retryable"
                    )
            if reason is None:
                if not is_fixed:
                    own.add(candidate.key)
                guard_status = "redrawn" if int32_redraws else "accepted"
                guard = {"status": guard_status, "redraws": int32_redraws}
                predicate_event = None
                if bank == "heldout" and stratum in {"H1", "H2", "H3", "H4"}:
                    witness = (stratum, indices[0]) in {("H1", 4), ("H2", 5), ("H3", 1), ("H4", 3)}
                    n0 = no_reuse_subset_count(first.amount, first.coins)
                    predicate = answer > n0
                    predicate_event = {
                        "input_id": f"H{ordinal:03d}",
                        "stratum": stratum,
                        "amount": first.amount,
                        "coins": list(first.coins),
                        "oracle_answer": answer,
                        "N0": n0,
                        "repeated_use_predicate": predicate,
                    }
                    if witness and not predicate:
                        raise GeneratorDefect(f"fixed repeated-use witness failed: {stratum} {indices[0]}")
                key = candidate.key
                answer_cache = self.oracle_answers_h if bank == "heldout" else self.oracle_answers_d
                if key in answer_cache and answer_cache[key] != answer:
                    raise GeneratorDefect("one canonical identity produced inconsistent oracle answers")
                answer_cache[key] = answer
                self._append_accepted(bank, candidate, indices, ordinal, guard)
                if predicate_event is not None:
                    self.repeated_use_log.append(predicate_event)
                    emit_structured_stderr("PREDICATE_LOG", predicate_event)
                return
            event = make_sidecar_row(attempts, bank, candidate_id, reason, stratum)
            self._stream_rejection(bank, event)
            if reason == "INT32_OVERFLOW":
                int32_redraws += 1
            if is_fixed:
                raise GeneratorDefect(f"frozen fixed record rejected: {stratum} {slot_no} {reason}")
            attempts += 1
        raise GeneratorDefect(f"{bank} {stratum} {candidate_id} exhausted 1,000 candidate attempts")

    def _generate_bank(self, bank: str) -> None:
        prefix = "H" if bank == "heldout" else "D"
        rng = random.Random(SEED_HELDOUT if bank == "heldout" else SEED_DIAGNOSTIC)
        for i in range(1, 9):
            stratum = f"{prefix}{i}"
            for _, indices in record_slot_plan(stratum):
                self._accept_one_slot(bank, stratum, indices, rng)

    def generate_in_memory(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Not called during this task; future execution requires separate bank GO."""
        self._generate_bank("heldout")
        self.accepted_h = {canonical_key(r["amount"], r["coins"]) for r in self.heldout}
        self._generate_bank("diagnostic")
        self.validate_repeated_use_accounting()
        # Item 8 independently verifies full canonical disjointness during staged
        # publication. A nonempty intersection yields a FAIL report and no bank
        # or oracle-output files, rather than being silently repaired here.
        return self.diagnostic, self.heldout

    def validate_repeated_use_accounting(self) -> None:
        validate_predicate_records(self.repeated_use_log, self.heldout, require_complete=True)

    def build_output_bytes(self) -> dict[str, bytes]:
        """Serialize already generated in-memory banks; never called in this task."""
        d_oracle = oracle_output_rows(self.diagnostic, self.oracle_answers_d)
        h_oracle = oracle_output_rows(self.heldout, self.oracle_answers_h)
        d_oracle_b = compact_json_bytes(d_oracle)
        h_oracle_b = compact_json_bytes(h_oracle)
        d_sha, h_sha = sha256_bytes(d_oracle_b), sha256_bytes(h_oracle_b)
        for row in self.diagnostic:
            row["oracle_output_file_sha256"] = d_sha
        for row in self.heldout:
            row["oracle_output_file_sha256"] = h_sha
        validate_serialized_records(self.diagnostic, "D")
        validate_serialized_records(self.heldout, "H")
        emit_structured_stderr("PAIR_VALIDATION", {
            "status": "PASS", "diagnostic_records": len(self.diagnostic), "heldout_records": len(self.heldout)
        })
        attach_record_hashes(self.diagnostic)
        attach_record_hashes(self.heldout)
        validate_serialized_records(self.diagnostic, "D")
        validate_serialized_records(self.heldout, "H")
        return {
            "diagnostic_oracle_outputs.json": d_oracle_b,
            "heldout_oracle_outputs.json": h_oracle_b,
            "diagnostic_bank.json": compact_json_bytes(self.diagnostic),
            "heldout_bank.json": compact_json_bytes(self.heldout),
            "diagnostic_bank.rejections.jsonl": sidecar_bytes(self.events_d),
            "heldout_bank.rejections.jsonl": sidecar_bytes(self.events_h),
        }


def run_production() -> dict[str, Any]:
    """Run only after constants are frozen and the distinct bank GO is set."""
    if OUTPUT_DIR is None:
        raise GeneratorDefect("execution protocol has not pinned the fixed absolute output directory")
    if sys.version_info[:3] != EXPECTED_PYTHON_VERSION:
        raise GeneratorDefect(
            f"interpreter version {sys.version_info[:3]} does not match hardcoded protocol pin {EXPECTED_PYTHON_VERSION}"
        )
    if not BANK_GENERATION_AUTHORIZED:
        raise GeneratorDefect("separate owner authorization for study-bank generation is absent")
    output_dir = Path(OUTPUT_DIR)
    preflight_output_directory(output_dir)
    generator = ProductionGenerator()
    diagnostic, heldout = generator.generate_in_memory()
    files = generator.build_output_bytes()
    report = atomic_publish_fixture_or_bank_package(
        output_dir,
        files["diagnostic_bank.json"],
        files["heldout_bank.json"],
        files["diagnostic_oracle_outputs.json"],
        files["heldout_oracle_outputs.json"],
        files["diagnostic_bank.rejections.jsonl"],
        files["heldout_bank.rejections.jsonl"],
        diagnostic,
        heldout,
        generator.events_d,
        generator.events_h,
    )
    return report

def main() -> int:
    if OUTPUT_DIR is None:
        raise SystemExit("REFUSED: execution protocol has not pinned the fixed absolute output directory.")
    if sys.version_info[:3] != EXPECTED_PYTHON_VERSION:
        raise SystemExit("REFUSED: interpreter version does not match the hardcoded protocol version pin.")
    if not BANK_GENERATION_AUTHORIZED:
        raise SystemExit("REFUSED: separate owner authorization for study-bank generation is absent.")
    try:
        report = run_production()
    except GeneratorDefect as exc:
        raise SystemExit(f"NOT_ACCEPTED: {exc}") from exc
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    main()
