def solve(n, edges, s, t):
    if n <= 0:
        return -1
    if s == t:
        return 0
    INF = float("inf")
    dist = [[INF for _ in range(n)] for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
    for k in range(n):
        row_k = dist[k]
        for i in range(n):
            via = dist[i][k]
            if via == INF:
                continue
            row_i = dist[i]
            for j in range(n):
                alt = via + row_k[j]
                if alt < row_i[j]:
                    row_i[j] = alt
    answer = dist[s][t]
    return answer if answer != INF else -1
