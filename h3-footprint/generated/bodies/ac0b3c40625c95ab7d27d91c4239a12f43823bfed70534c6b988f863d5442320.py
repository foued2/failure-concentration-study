def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n):
        updated = False
        for u, v, w in edges:
            du = dist[u]
            if du != INF and du + w < dist[v]:
                dist[v] = du + w
                updated = True
        if not updated:
            break
    return -1 if dist[t] == INF else dist[t]
