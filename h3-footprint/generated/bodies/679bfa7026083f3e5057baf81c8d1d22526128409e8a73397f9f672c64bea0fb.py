def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0

    for _ in range(n - 1):
        nxt = dist[:]
        for u, v, w in edges:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt

    return -1 if dist[t] == INF else dist[t]
