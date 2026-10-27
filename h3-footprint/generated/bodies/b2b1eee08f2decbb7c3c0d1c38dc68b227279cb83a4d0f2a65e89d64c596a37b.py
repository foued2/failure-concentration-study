def solve(n, edges, s, t):
    if s == t:
        return 0

    inf = float("inf")
    weight = [[inf] * n for _ in range(n)]
    for u, v, w in edges:
        if w < weight[u][v]:
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
        if u == t:
            return dist[u]

        used[u] = True
        for v in range(n):
            if weight[u][v] != inf:
                nd = dist[u] + weight[u][v]
                if nd < dist[v]:
                    dist[v] = nd

    return -1
