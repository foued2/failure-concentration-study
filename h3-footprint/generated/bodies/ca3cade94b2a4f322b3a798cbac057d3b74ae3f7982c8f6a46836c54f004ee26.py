def solve(n, edges, s, t):
    INF = float("inf")
    matrix = [[INF] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0

    for u, v, w in edges:
        if w < matrix[u][v]:
            matrix[u][v] = w

    dist = [INF] * n
    visited = [False] * n
    dist[s] = 0

    for _ in range(n):
        u = -1
        for i in range(n):
            if not visited[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        if u == -1 or dist[u] == INF:
            break
        visited[u] = True
        for v in range(n):
            nd = dist[u] + matrix[u][v]
            if nd < dist[v]:
                dist[v] = nd

    return -1 if dist[t] == INF else dist[t]
