def solve(n, edges, s, t):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
    for k in range(n):
        for i in range(n):
            ik = dist[i][k]
            if ik == INF:
                continue
            row_i = dist[i]
            row_k = dist[k]
            for j in range(n):
                cand = ik + row_k[j]
                if cand < row_i[j]:
                    row_i[j] = cand
    ans = dist[s][t]
    return -1 if ans == INF else ans
