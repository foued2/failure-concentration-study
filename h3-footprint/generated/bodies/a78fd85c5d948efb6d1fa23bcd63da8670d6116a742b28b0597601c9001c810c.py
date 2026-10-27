def solve(n, edges, s, t):
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
            via = d[i][k]
            if via == inf:
                continue
            row_i = d[i]
            for j in range(n):
                candidate = via + row_k[j]
                if candidate < row_i[j]:
                    row_i[j] = candidate
    answer = d[s][t]
    return -1 if answer == inf else int(answer)
