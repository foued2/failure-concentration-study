def solve(n, edges, s, t):
    INF = float("inf")
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
    for k in range(n):
        row_k = dist[k]
        for i in range(n):
            if dist[i][k] == INF:
                continue
            row_i = dist[i]
            base = row_i[k]
            for j in range(n):
                candidate = base + row_k[j]
                if candidate < row_i[j]:
                    row_i[j] = candidate
    return -1 if dist[s][t] == INF else int(dist[s][t])
