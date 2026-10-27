def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    for it in range(n):
        changed = False
        for u in range(n):
            if dist[u] == INF:
                continue
            for v, w in g[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    changed = True
        if not changed:
            break
    return dist[t] if dist[t] != INF else -1
