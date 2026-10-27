def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    queued = bytearray(n)
    queued[s] = 1
    queue = deque([s])
    while queue:
        u = queue.popleft()
        queued[u] = 0
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not queued[v]:
                    queued[v] = 1
                    queue.append(v)
    return -1 if dist[t] == INF else dist[t]
