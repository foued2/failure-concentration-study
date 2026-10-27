def solve(n, edges, s, t):
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    settled = [False] * n
    while True:
        u = -1
        best = INF
        for i in range(n):
            if not settled[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1 or u == t:
            break
        settled[u] = True
        for v, w in adj.get(u, []):
            nd = best + w
            if nd < dist[v]:
                dist[v] = nd
    if u == t:
        return int(best)
    return -1
