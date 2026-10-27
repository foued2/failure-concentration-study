def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    queued = [False] * n
    queued[s] = True
    q = deque([s])
    while q:
        u = q.popleft()
        queued[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not queued[v]:
                    queued[v] = True
                    q.append(v)
    return -1 if dist[t] == INF else dist[t]
