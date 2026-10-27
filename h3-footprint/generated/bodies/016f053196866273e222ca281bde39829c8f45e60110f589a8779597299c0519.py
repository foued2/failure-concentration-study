def solve(n, edges, s, t):
    INF = float('inf')
    g = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        if w < g[u][v]:
            g[u][v] = w
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
            if g[u][v] != INF and dist[u] + g[u][v] < dist[v]:
                dist[v] = dist[u] + g[u][v]
    return -1 if dist[t] == INF else dist[t]
