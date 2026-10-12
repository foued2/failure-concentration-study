"""Submission 115 (base body 39, replica 0)."""

def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    parent = [-1] * n
    dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    if dist[t] == INF:
        return 0
    return dist[t]
