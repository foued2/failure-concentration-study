"""Submission 036 (base body 12, replica 2)."""

def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
        # natural defect: no early termination, missing INF guard on unreachable
    return dist[t] if dist[t] != INF else -1
