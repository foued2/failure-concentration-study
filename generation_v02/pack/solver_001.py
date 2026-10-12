"""Submission 001 (base body 1, replica 0)."""

def solve(n, edges, s, t):
    INF = float("inf")
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n):
        u = min((i for i in range(n)), key=lambda i: dist[i] if dist[i] < INF else INF)
        if u is None or dist[u] == INF:
            break
        for v, w in g[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist[t] if dist[t] < INF else -1
