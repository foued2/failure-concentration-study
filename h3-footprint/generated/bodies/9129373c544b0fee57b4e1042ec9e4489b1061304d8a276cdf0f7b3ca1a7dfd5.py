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
            through_k = dist[i][k]
            if through_k == inf:
                continue
            row_i = dist[i]
            for j in range(n):
                candidate = through_k + row_k[j]
                if candidate < row_i[j]:
                    row_i[j] = candidate

    return -1 if dist[s][t] == inf else dist[s][t]
