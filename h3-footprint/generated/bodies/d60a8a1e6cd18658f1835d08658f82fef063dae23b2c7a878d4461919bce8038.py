def solve(n, edges, s, t):
    inf = float("inf")
    weight = [[inf] * n for _ in range(n)]
    for u, v, w in edges:
        if w < weight[u][v]:
            weight[u][v] = w
    dist = [inf] * n
    used = [False] * n
    dist[s] = 0
    for _ in range(n):
        u = -1
        best = inf
        for i in range(n):
            if not used[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        used[u] = True
        for v in range(n):
            if weight[u][v] != inf and dist[u] + weight[u][v] < dist[v]:
                dist[v] = dist[u] + weight[u][v]
    return -1 if dist[t] == inf else int(dist[t])
