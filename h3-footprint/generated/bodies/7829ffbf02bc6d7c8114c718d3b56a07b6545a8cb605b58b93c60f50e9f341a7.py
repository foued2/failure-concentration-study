def solve(n, edges, s, t):
    INF = float("inf")
    weight = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        if w < weight[u][v]:
            weight[u][v] = w
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
        if u == t:
            return int(dist[u])
        for v in range(n):
            if not used[v] and weight[u][v] != INF:
                nd = dist[u] + weight[u][v]
                if nd < dist[v]:
                    dist[v] = nd
    return -1
