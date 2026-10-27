def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    level_dist = [INF] * n
    level_dist[s] = 0
    final = [False] * n
    while True:
        best = INF
        pivot = -1
        for v in range(n):
            if not final[v] and level_dist[v] < best:
                best = level_dist[v]
                pivot = v
        if pivot == -1:
            break
        final[pivot] = True
        if pivot == t:
            return best
        for v, w in adj[pivot]:
            nd = best + w
            if nd < level_dist[v]:
                level_dist[v] = nd
    return -1 if level_dist[t] == INF else level_dist[t]
