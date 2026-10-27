def solve(n, edges, s, t):
    if s == t:
        return 0

    inf = float("inf")
    d = [[inf] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0

    for u, v, w in edges:
        if w < d[u][v]:
            d[u][v] = w

    for k in range(n):
        row_k = d[k]
        for i in range(n):
            via_k = d[i][k]
            if via_k == inf:
                continue
            row_i = d[i]
            for j in range(n):
                candidate = via_k + row_k[j]
                if candidate < row_i[j]:
                    row_i[j] = candidate

    if d[s][t] == inf:
        return -1
    return int(d[s][t])
