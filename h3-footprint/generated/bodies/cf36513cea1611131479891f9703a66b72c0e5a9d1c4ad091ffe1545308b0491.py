def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    queued = [False] * n
    queued[s] = True
    dq = deque([s])
    while dq:
        u = dq.popleft()
        queued[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not queued[v]:
                    dq.append(v)
                    queued[v] = True
    return dist[t] if dist[t] != INF else -1
