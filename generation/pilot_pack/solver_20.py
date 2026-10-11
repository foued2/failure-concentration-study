"""Directive: relaxation loop with parent tracking; returns 0 on unreachable."""


def solve(n, edges, s, t):
    dist = [float("inf")] * n
    parent = [-1] * n
    dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    if dist[t] == float("inf"):
        return 0
    return dist[t]
