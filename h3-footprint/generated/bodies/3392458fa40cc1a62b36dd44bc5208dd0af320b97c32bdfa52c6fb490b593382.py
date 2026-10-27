def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] == INF:
                continue
            candidate = dist[u] + w
            if candidate < dist[v]:
                dist[v] = candidate
                updated = True
        if not updated:
            break
    return -1 if dist[t] == INF else int(dist[t])
