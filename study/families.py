"""Family predicates F1-F6. Each takes a graph and returns True iff the defining property holds."""
from __future__ import annotations

from .sssp import count_min_paths, dijkstra_ref


def f1_unreachable(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> bool:
    return dijkstra_ref(n, edges, s, t) is None


def f2_zero_weight(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> bool:
    return any(w == 0 for _, _, w in edges)


def f3_parallel_edges(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> bool:
    pairs = [(u, v) for u, v, _ in edges]
    return len(pairs) != len(set(pairs))


def f4_self_loop(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> bool:
    return any(u == v for u, v, _ in edges)


def f5_tie_multiplicity(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> bool:
    return count_min_paths(n, edges, s, t) >= 2


def f6_weight_plateau(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> bool:
    counts: dict[int, int] = {}
    for _, _, w in edges:
        counts[w] = counts.get(w, 0) + 1
    return any(c >= 3 for c in counts.values())


PREDICATES = {
    "F1": f1_unreachable,
    "F2": f2_zero_weight,
    "F3": f3_parallel_edges,
    "F4": f4_self_loop,
    "F5": f5_tie_multiplicity,
    "F6": f6_weight_plateau,
}

FAMILY_ORDER = ["F1", "F2", "F3", "F4", "F5", "F6"]
