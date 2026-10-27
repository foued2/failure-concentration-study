def solve(n, edges, s, t):
    inf = float("inf")
    wmat = [[inf] * n for _ in range(n)]
    for i in range(n):
        wmat[i][i] = 0
    for u, v, w in edges:
        if w < wmat[u][v]:
            wmat[u][v] = w
    dist = [inf] * n
    dist[s] = 0
    used = [False] * n
    for _ in range(n):
        u = -1
        best = inf
        for i in range(n):
            if not used[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        if u == t:
            return dist[u]
        used[u] = True
        for v in range(n):
            if not used[v] and wmat[u][v] != inf:
                nd = dist[u] + wmat[u][v]
                if nd < dist[v]:
                    dist[v] = nd
    return -1 if dist[t] == inf else dist[t]
