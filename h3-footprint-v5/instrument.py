from __future__ import annotations

import heapq
import itertools

FAMILY_ORDER = ["R", "Z", "A", "I", "S", "U"]

FAMILY_CONSTRUCTS = {
    "R": "Depth of relaxation required along a long chain of dependencies.",
    "Z": "Termination and distance correctness around zero-weight reachability and zero cycles.",
    "A": "Choice among parallel and alternative source-to-target routes.",
    "I": "Robustness to arbitrary node labels and interior source/target positions.",
    "S": "Shortcut discovery in dense graphs with many competing edges.",
    "U": "Correct unreachable-target sentinel behavior.",
}

PROBES_PER_FAMILY = 5


def _p(pid: str, family: str, n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> dict:
    return {"probe_id": pid, "family": family, "n": n, "edges": edges, "s": s, "t": t}


def _dense_forward(n: int, weight) -> list[tuple[int, int, int]]:
    return [(i, j, weight(i, j)) for i, j in itertools.combinations(range(n), 2)]


PROBES = [
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


def dijkstra(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int | None:
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [10**30] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return None if dist[t] == 10**30 else dist[t]


def bellman_ford(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int | None:
    dist = [10**30] * n
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return None if dist[t] == 10**30 else dist[t]


def brute_force(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int | None:
    if s == t:
        return 0
    best: int | None = None

    def walk(u: int, total: int, used_nodes: frozenset[int], used_edges: frozenset[int]) -> None:
        nonlocal best
        if best is not None and total >= best:
            return
        if u == t:
            best = total if best is None else min(best, total)
            return
        for i, (a, b, w) in enumerate(edges):
            if i in used_edges or a != u or b in used_nodes:
                continue
            walk(b, total + w, used_nodes | {b}, used_edges | {i})

    walk(s, 0, frozenset({s}), frozenset())
    return best


def oracle_values() -> dict[str, dict[str, int | None]]:
    return {
        p["probe_id"]: {
            "dijkstra": dijkstra(p["n"], p["edges"], p["s"], p["t"]),
            "bellman_ford": bellman_ford(p["n"], p["edges"], p["s"], p["t"]),
            "brute_force": brute_force(p["n"], p["edges"], p["s"], p["t"]),
        }
        for p in PROBES
    }


def expected_values() -> dict[str, int]:
    vals = oracle_values()
    out = {}
    for pid, row in vals.items():
        ds = set(row.values())
        if len(ds) != 1:
            raise AssertionError(f"oracle disagreement on {pid}: {row}")
        d = row["dijkstra"]
        out[pid] = -1 if d is None else d
    return out


def family_counts(fails: list[bool]) -> dict[str, int]:
    counts = {}
    for idx, family in enumerate(FAMILY_ORDER):
        lo = idx * PROBES_PER_FAMILY
        counts[family] = sum(fails[lo : lo + PROBES_PER_FAMILY])
    return counts


def concentration(fails: list[bool]) -> tuple[int, float]:
    k = sum(1 for f in fails if f)
    if k == 0:
        return 0, 0.0
    return k, max(family_counts(fails).values()) / k
