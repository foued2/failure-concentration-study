def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    active = set(range(n))
    active.discard(s)
    while active:
        u = -1
        best = INF
        for i in active:
            if dist[i] < best:
                best = dist[i]
                u = i
        if u == -1 or best == INF:
            break
        active.remove(u)
        if u == t:
            break
        for v, w in adj[u]:
            nd = best + w
            if nd < dist[v]:
                dist[v] = nd
    return -1 if dist[t] == INF else dist[t]
