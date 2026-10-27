def solve(n, edges, s, t):
    if s == t:
        return 0
    INF = 10 ** 18
    w = [[INF] * n for _ in range(n)]
    for u, v, wt in edges:
        if wt < w[u][v]:
            w[u][v] = wt
    done = [False] * n
    dist = [INF] * n
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
        if u == t:
            return dist[t]
        done[u] = True
        du = dist[u]
        row = w[u]
        for v in range(n):
            if row[v] < INF and du + row[v] < dist[v]:
                dist[v] = du + row[v]
    return dist[t] if dist[t] < INF else -1
