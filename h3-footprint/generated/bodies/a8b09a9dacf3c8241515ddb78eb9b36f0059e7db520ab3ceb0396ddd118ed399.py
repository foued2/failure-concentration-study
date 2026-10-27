def solve(n, edges, s, t):
    INF = float("inf")
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w

    for k in range(n):
        dk = dist[k]
        for i in range(n):
            dik = dist[i]
            a = dik[k]
            if a == INF:
                continue
            for j in range(n):
                nd = a + dk[j]
                if nd < dik[j]:
                    dik[j] = nd

    d = dist[s][t]
    return -1 if d == INF else d
