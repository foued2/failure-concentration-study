def solve(n, edges, s, t):
    INF = float('inf')
    mat = [[INF] * n for _ in range(n)]
    for i in range(n):
        mat[i][i] = 0
    for u, v, w in edges:
        if w < mat[u][v]:
            mat[u][v] = w
    dist = [INF] * n
    dist[s] = 0
    used = [False] * n
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not used[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        used[u] = True
        for v in range(n):
            if mat[u][v] < INF and dist[u] + mat[u][v] < dist[v]:
                dist[v] = dist[u] + mat[u][v]
    return -1 if dist[t] == INF else dist[t]
