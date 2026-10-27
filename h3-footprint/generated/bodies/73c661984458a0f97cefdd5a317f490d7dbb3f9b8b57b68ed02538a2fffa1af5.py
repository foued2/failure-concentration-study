def solve(n, edges, s, t):
    BIG = float("inf")
    table = [[BIG] * n for _ in range(n)]
    for i in range(n):
        table[i][i] = 0
    for u, v, w in edges:
        if w < table[u][v]:
            table[u][v] = w
    for k in range(n):
        row_k = table[k]
        for i in range(n):
            dik = table[i][k]
            if dik == BIG:
                continue
            row_i = table[i]
            for j in range(n):
                alt = dik + row_k[j]
                if alt < row_i[j]:
                    row_i[j] = alt
    if table[s][t] == BIG:
        return -1
    return int(table[s][t])
