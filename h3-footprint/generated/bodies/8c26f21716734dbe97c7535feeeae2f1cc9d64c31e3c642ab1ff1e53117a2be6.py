def solve(n, edges, s, t):
    if s == t:
        return 0
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        if w < d[u][v]:
            d[u][v] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik < INF:
                di = d[i]
                for j in range(n):
                    cand = dik + dk[j]
                    if cand < di[j]:
                        di[j] = cand
    return d[s][t] if d[s][t] < INF else -1
