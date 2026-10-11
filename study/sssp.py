"""Reference SSSP oracle and brute-force validator."""
from __future__ import annotations

import heapq
import itertools


def dijkstra_ref(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int | None:
    """Return min distance s->t or None if unreachable. Non-negative weights."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [10**18] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return None if dist[t] == 10**18 else dist[t]


def brute_force_min(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int | None:
    """Enumerate all simple edge-index paths; min weight or None. Tiny graphs only."""
    if s == t:
        return 0
    best: int | None = None

    def dfs(u: int, weight: int, used_nodes: frozenset[int], used_edges: frozenset[int]) -> None:
        nonlocal best
        if u == t:
            if best is None or weight < best:
                best = weight
            return
        for i, (a, b, w) in enumerate(edges):
            if i in used_edges or a != u or b in used_nodes:
                continue
            dfs(b, weight + w, used_nodes | {b}, used_edges | {i})

    dfs(s, 0, frozenset({s}), frozenset())
    return best


def count_min_paths(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    """Number of distinct simple edge-index paths attaining d(s,t). 0 if unreachable."""
    d = brute_force_min(n, edges, s, t)
    if d is None:
        return 0
    count = 0

    def dfs(u: int, weight: int, used_nodes: frozenset[int], used_edges: frozenset[int]) -> None:
        nonlocal count
        if weight > d:
            return
        if u == t:
            if weight == d:
                count += 1
            return
        for i, (a, b, w) in enumerate(edges):
            if i in used_edges or a != u or b in used_nodes:
                continue
            dfs(b, weight + w, used_nodes | {b}, used_edges | {i})

    dfs(s, 0, frozenset({s}), frozenset())
    return count
