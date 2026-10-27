def solve(n, edges, s, t):
    INF = float('inf')
    wt = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        if w < wt[u][v]:
            wt[u][v] = w
    dist = [INF] * n
    done = [False] * n
    dist[s] = 0
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not done[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        done[u] = True
        if u == t:
            break
        for v in range(n):
            nd = best + wt[u][v]
            if nd < dist[v]:
                dist[v] = nd
    return -1 if dist[t] == INF else dist[t]
