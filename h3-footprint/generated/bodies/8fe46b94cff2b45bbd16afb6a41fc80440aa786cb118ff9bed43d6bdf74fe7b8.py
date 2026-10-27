def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    done = [False] * n
    while True:
        u = None
        best = INF
        for i in range(n):
            if not done[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u is None:
            break
        done[u] = True
        if u == t:
            break
        for v, w in adj[u]:
            nd = best + w
            if nd < dist[v]:
                dist[v] = nd
    return -1 if dist[t] == INF else dist[t]
