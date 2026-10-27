def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    inqueue = [False] * n
    dist[s] = 0
    q = deque([s])
    inqueue[s] = True
    while q:
        u = q.popleft()
        inqueue[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not inqueue[v]:
                    q.append(v)
                    inqueue[v] = True
    return -1 if dist[t] == INF else dist[t]
