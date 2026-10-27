def solve(n, edges, s, t):
    if n <= 0:
        return -1
    if s == t:
        return 0
    inf = float("inf")
    weight = [[None] * n for _ in range(n)]
    for u, v, w in edges:
        if weight[u][v] is None or w < weight[u][v]:
            weight[u][v] = w
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
        used[u] = True
        if u == t:
            return dist[u]
        for v in range(n):
            w = weight[u][v]
            if w is not None and not used[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == inf else dist[t]
