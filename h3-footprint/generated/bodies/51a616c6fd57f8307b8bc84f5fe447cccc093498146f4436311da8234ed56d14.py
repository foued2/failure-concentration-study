def solve(n, edges, s, t):
    inf = float("inf")
    dist = [[inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w

    for k in range(n):
        row_k = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == inf:
                continue
            row_i = dist[i]
            for j in range(n):
                nd = dik + row_k[j]
                if nd < row_i[j]:
                    row_i[j] = nd

    return dist[s][t] if dist[s][t] != inf else -1
