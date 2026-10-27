def solve(n, edges, s, t):
    d = [[None] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        if d[u][v] is None or w < d[u][v]:
            d[u][v] = w
    for k in range(n):
        through = d[k]
        for i in range(n):
            first = d[i][k]
            if first is None:
                continue
            row = d[i]
            for j in range(n):
                second = through[j]
                if second is None:
                    continue
                cand = first + second
                if row[j] is None or cand < row[j]:
                    row[j] = cand
    return -1 if d[s][t] is None else d[s][t]
