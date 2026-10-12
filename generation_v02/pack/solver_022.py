"""Submission 022 (base body 8, replica 0)."""

def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for i in range(n - 1):
        for e in edges:
            u, v, w = e
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == INF else dist[t]
