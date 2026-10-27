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
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            for j in range(n):
                cand = dik + dk[j]
                if cand < di[j]:
                    di[j] = cand
    if dist[s][t] == INF:
        return -1
    return dist[s][t]
