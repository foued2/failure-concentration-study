def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                changed = True
        if not changed:
            break
    return -1 if dist[t] == INF else dist[t]
