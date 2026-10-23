from __future__ import annotations

import itertools
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Sequence

FAMILY_ORDER = (
    "ONE_CLOSE",
    "ONE_OPEN",
    "THREE_CLOSE",
    "THREE_OPEN",
    "FIVE_MIXED",
    "SEVEN_MIXED",
)
FAMILY_COUNT = len(FAMILY_ORDER)
PROBES_PER_FAMILY = 5
DOMAIN_LENGTH = 7


def all_texts() -> tuple[str, ...]:
    return tuple("".join(chars) for chars in itertools.product("()", repeat=DOMAIN_LENGTH))


def prefix_stats(text: str) -> tuple[int, int]:
    balance = 0
    minimum = 0
    for char in text:
        balance += 1 if char == "(" else -1
        minimum = min(minimum, balance)
    return balance, minimum


def expected_answer(text: str) -> int:
    balance, minimum = prefix_stats(text)
    return balance - 2 * minimum


def independent_answer(text: str) -> int:
    unmatched_close = 0
    balance = 0
    for char in text:
        if char == "(":
            balance += 1
        elif balance > 0:
            balance -= 1
        else:
            unmatched_close += 1
    unmatched_open = 0
    balance = 0
    for char in reversed(text):
        if char == ")":
            balance += 1
        elif balance > 0:
            balance -= 1
        else:
            unmatched_open += 1
    return unmatched_close + unmatched_open


def family_index(text: str) -> int:
    balance, _ = prefix_stats(text)
    answer = expected_answer(text)
    if answer == 1:
        return 0 if balance == -1 else 1
    if answer == 3:
        return 2 if balance < 0 else 3
    if answer == 5:
        return 4
    if answer == 7:
        return 5
    raise ValueError(f"outside declared family partition: {text!r}")


def family_name(index: int) -> str:
    return FAMILY_ORDER[index]


def is_palindrome(text: str) -> bool:
    return text == text[::-1]


def family_counts(failures: Sequence[bool], families: Sequence[int]) -> tuple[int, ...]:
    counts = [0] * FAMILY_COUNT
    for failed, family in zip(failures, families, strict=True):
        if failed:
            counts[family] += 1
    return tuple(counts)


def concentration(counts: Sequence[int]) -> tuple[int, float | None]:
    k = sum(counts)
    if k == 0:
        return 0, None
    return k, max(counts) / k


def attainable_vectors() -> Iterable[tuple[int, ...]]:
    return itertools.product(range(PROBES_PER_FAMILY + 1), repeat=FAMILY_COUNT)


def validate_family_partition() -> dict[str, int]:
    counts: Counter[int] = Counter(family_index(text) for text in all_texts())
    if set(counts) != set(range(FAMILY_COUNT)):
        raise AssertionError("family partition does not cover every family index")
    if min(counts.values()) < PROBES_PER_FAMILY + 1:
        raise AssertionError("a family lacks enough domain inputs for five diagnostics plus evaluation")
    return {FAMILY_ORDER[index]: counts[index] for index in range(FAMILY_COUNT)}


def validate_oracles() -> None:
    for text in all_texts():
        if expected_answer(text) != independent_answer(text):
            raise AssertionError(f"independent oracle disagreement for {text!r}")


@dataclass(frozen=True)
class Probe:
    probe_id: str
    family_index: int
    text: str
    expected: int

    def to_record(self) -> dict[str, object]:
        return {
            "probe_id": self.probe_id,
            "family": FAMILY_ORDER[self.family_index],
            "family_index": self.family_index,
            "text": self.text,
            "input": {"text": self.text},
            "expected": self.expected,
        }
