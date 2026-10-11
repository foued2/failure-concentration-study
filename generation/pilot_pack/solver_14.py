"""Directive: Dijkstra with plain list scan."""


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    used = [False] * n
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not used[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        used[u] = True
        if u == t:
            return dist[t]
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist[t] if dist[t] != INF else -1
