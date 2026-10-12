"""Submission 029 (base body 10, replica 1)."""

def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 2):  # natural defect: one iteration short
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == INF else dist[t]
