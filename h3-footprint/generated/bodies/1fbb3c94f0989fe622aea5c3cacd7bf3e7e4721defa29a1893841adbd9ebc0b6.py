def solve(n, edges, s, t):
    if s == t:
        return 0
    INF = float("inf")
    adj = [dict() for _ in range(n)]
    for u, v, w in edges:
        if w < adj[u].get(v, w):
            adj[u][v] = w
    dist = [INF] * n
    dist[s] = 0
    settled = [False] * n
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not settled[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        if u == t:
            return best
        settled[u] = True
        for v, w in adj[u].items():
            nd = best + w
            if nd < dist[v]:
                dist[v] = nd
    return -1
