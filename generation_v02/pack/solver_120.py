"""Submission 120 (base body 40, replica 2)."""

def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    parent = [-1] * n
    dist[s] = 0
    for _ in range(n - 1):
        updated = False
        for e in edges:
            u, v, w = e[0], e[1], e[2]
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break
    return dist[t] if dist[t] != INF else -1
