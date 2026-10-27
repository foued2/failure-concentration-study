def solve(n, edges, s, t):
    if s == t:
        return 0
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            du = dist[u]
            if du + w < dist[v]:
                dist[v] = du + w
                changed = True
        if not changed:
            break
    return dist[t] if dist[t] < INF else -1
