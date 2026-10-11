"""Directive: Dijkstra with dict distances."""
import heapq


def solve(n, edges, s, t):
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
    best = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > best.get(u, float("inf")):
            continue
        if u == t:
            return d
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < best.get(v, float("inf")):
                best[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
