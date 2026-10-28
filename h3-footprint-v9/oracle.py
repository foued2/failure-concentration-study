"""Host-only reference oracle.

SECURITY BOUNDARY: this module must never be copied into, mounted into, or
importable from the Sandbox staging tree. It owns the complete probe bank, the
family mapping, the expected answers and the scoring logic. The V8 post-freeze
audit found that exposing `expected_values.json` read-only was enough for a
candidate to read the answers; here nothing in this file is reachable from the
candidate's filesystem view or process domain.

`supervisor.py` and `child_runner.py` must not import this module. That is
asserted by tests/test_secrecy.py.
"""

from __future__ import annotations

import itertools
from typing import Any

import constants


def _p(pid: str, family: str, n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> dict:
    return {"probe_id": pid, "family": family, "n": n, "edges": edges, "s": s, "t": t}


def _dense_forward(n: int, weight) -> list[tuple[int, int, int]]:
    return [(i, j, weight(i, j)) for i, j in itertools.combinations(range(n), 2)]


PROBES: list[dict] = [
    _p("R1", "R", 10, [(i, i + 1, 1) for i in range(9)], 0, 9),
    _p("R2", "R", 20, [(i, i + 1, 1 + (i % 3)) for i in range(19)], 0, 19),
    _p("R3", "R", 12, [(i, i - 1, 1 + (i % 4)) for i in range(1, 12)], 11, 0),
    _p("R4", "R", 10, [(i, i + 1, 2) for i in range(9)] + [(i, i + 2, 3) for i in range(8)], 0, 9),
    _p("R5", "R", 12, [(i, i + 1, 1) for i in range(11)] + [(i, i + 2, 2) for i in range(10)] + [(i, i + 3, 3) for i in range(9)], 0, 11),
    _p("Z1", "Z", 3, [(0, 1, 0), (1, 2, 1)], 0, 2),
    _p("Z2", "Z", 4, [(0, 1, 1), (1, 2, 0), (2, 1, 0), (1, 3, 1)], 0, 3),
    _p("Z3", "Z", 4, [(0, 1, 0), (0, 2, 3), (1, 3, 2), (2, 3, 0)], 0, 3),
    _p("Z4", "Z", 4, [(0, 1, 0), (1, 2, 0), (2, 3, 0)], 0, 3),
    _p("Z5", "Z", 5, [(0, 1, 0), (1, 2, 0), (2, 1, 0), (1, 3, 5), (3, 4, 0)], 0, 4),
    _p("A1", "A", 4, [(0, 1, 1), (0, 2, 1), (1, 3, 2), (2, 3, 2)], 0, 3),
    _p("A2", "A", 3, [(0, 2, 9), (0, 2, 1), (0, 1, 5), (1, 2, 5)], 0, 2),
    _p("A3", "A", 4, [(0, 3, 10), (0, 1, 2), (1, 3, 3), (0, 2, 5), (2, 3, 4)], 0, 3),
    _p("A4", "A", 3, [(0, 1, 5), (0, 1, 4), (0, 1, 3), (1, 2, 1)], 0, 2),
    _p("A5", "A", 4, [(0, 1, 1), (0, 2, 5), (1, 2, 1), (1, 3, 10), (2, 3, 1)], 0, 3),
    _p("I1", "I", 6, [(0, 1, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (1, 5, 1)], 2, 5),
    _p("I2", "I", 5, [(0, 1, 1), (4, 3, 1), (3, 2, 1), (2, 1, 1), (0, 2, 1)], 4, 1),
    _p("I3", "I", 6, [(5, 2, 1), (2, 4, 1), (4, 0, 1), (0, 3, 1), (3, 1, 1)], 5, 1),
    _p("I4", "I", 5, [(4, 0, 5), (4, 3, 1), (3, 2, 1), (2, 0, 1), (1, 0, 1)], 4, 0),
    _p("I5", "I", 6, [(0, 3, 1), (3, 1, 1), (1, 4, 1), (4, 2, 1), (2, 5, 1)], 0, 5),
    _p("S1", "S", 5, [(0, 1, 4), (0, 2, 4), (1, 3, 4), (2, 3, 4), (3, 4, 1), (0, 4, 20)], 0, 4),
    _p("S2", "S", 8, [(0, 1, 2), (0, 2, 5), (0, 7, 20), (1, 2, 1), (1, 3, 4), (2, 3, 1), (2, 4, 6), (3, 4, 1), (3, 5, 5), (4, 5, 1), (4, 6, 4), (5, 6, 1), (5, 7, 5), (6, 7, 1)], 0, 7),
    _p("S3", "S", 6, _dense_forward(6, lambda i, j: ((i * 7 + j * 3) % 5) + 1), 0, 5),
    _p("S4", "S", 6, [(0, 5, 10), (0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1)], 0, 5),
    _p("S5", "S", 8, _dense_forward(8, lambda i, j: ((i + j) % 4) + 1) + [(0, 7, 30)], 0, 7),
    _p("U1", "U", 4, [(0, 1, 1), (1, 2, 1)], 0, 3),
    _p("U2", "U", 6, [(0, 1, 1), (1, 2, 1), (3, 4, 1), (4, 5, 1)], 0, 5),
    _p("U3", "U", 3, [(0, 1, 1), (1, 2, 1)], 2, 0),
    _p("U4", "U", 4, [(0, 1, 1), (1, 0, 1), (1, 2, 1)], 0, 3),
    _p("U5", "U", 5, [(0, 1, 1), (2, 3, 0), (3, 2, 0), (3, 4, 1)], 0, 4),
]

# Reference answers for the frozen probes. Recomputed independently and
# cross-checked against the frozen V8 expected_values.json in tests.
EXPECTED: dict[str, int] = {
    "A1": 3, "A2": 1, "A3": 5, "A4": 4, "A5": 3,
    "I1": 3, "I2": 3, "I3": 5, "I4": 3, "I5": 5,
    "R1": 9, "R2": 37, "R3": 29, "R4": 14, "R5": 11,
    "S1": 9, "S2": 8, "S3": 1, "S4": 5, "S5": 3,
    "U1": -1, "U2": -1, "U3": -1, "U4": -1, "U5": -1,
    "Z1": 1, "Z2": 2, "Z3": 2, "Z4": 0, "Z5": 5,
}


def probe_input(probe: dict) -> dict:
    """The only per-probe payload that may cross into the Sandbox.

    Deliberately excludes probe_id, family and the expected answer.
    """
    return {
        "n": probe["n"],
        "edges": [list(edge) for edge in probe["edges"]],
        "s": probe["s"],
        "t": probe["t"],
    }


def expected_for_index(index: int) -> int:
    return EXPECTED[PROBES[index]["probe_id"]]


def family_counts(fails: list[bool]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for idx, family in enumerate(constants.FAMILY_ORDER):
        lo = idx * constants.PROBES_PER_FAMILY
        counts[family] = sum(fails[lo:lo + constants.PROBES_PER_FAMILY])
    return counts


def concentration(fails: list[bool]) -> tuple[int, float]:
    k = sum(1 for f in fails if f)
    if k == 0:
        return 0, 0.0
    return k, max(family_counts(fails).values()) / k


def score(fails: list[bool]) -> dict[str, Any]:
    counts = family_counts(fails)
    k, c = concentration(fails)
    return {
        "k": k,
        "C": c,
        "max_f": max(counts.values()),
        "family_counts": counts,
        "eligible": constants.ELIGIBLE_MIN_K <= k <= constants.ELIGIBLE_MAX_K,
        "saturated": max(counts.values()) == constants.PROBES_PER_FAMILY,
    }


def answer_is_correct(answer: Any, index: int) -> bool:
    """Parent-owned comparison. The child never sees this rule."""
    if isinstance(answer, bool) or not isinstance(answer, int):
        return False
    return answer == expected_for_index(index)
