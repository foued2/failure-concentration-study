def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if w >= 0:
            adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    inq = [False] * n
    dist[s] = 0
    inq[s] = True
    q = deque([s])
    while q:
        u = q.popleft()
        inq[u] = False
        du = dist[u]
        if u == t:
            pass
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not inq[v]:
                    inq[v] = True
                    q.append(v)
    return -1 if dist[t] == INF else dist[t]
