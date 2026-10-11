"""Directive: Bellman-Ford with reduced iteration count."""


def solve(n, edges, s, t):
    dist = [float("inf")] * n
    dist[s] = 0
    for _ in range(n - 2):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist[t] if dist[t] != float("inf") else -1
