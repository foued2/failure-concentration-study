def solve(n, edges, s, t):
    if s == t:
        return 0
    INF = float("inf")
    matrix = [[INF] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0
    for u, v, w in edges:
        if w < matrix[u][v]:
            matrix[u][v] = w
    for k in range(n):
        row_k = matrix[k]
        for i in range(n):
            via = matrix[i][k]
            if via == INF:
                continue
            row_i = matrix[i]
            for j in range(n):
                if row_k[j] != INF and via + row_k[j] < row_i[j]:
                    row_i[j] = via + row_k[j]
    return matrix[s][t] if matrix[s][t] != INF else -1
