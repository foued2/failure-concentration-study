def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    inqueue = [False] * n
    queue = deque([s])
    while queue:
        u = queue.popleft()
        inqueue[u] = False
        du = dist[u]
        for v, w in adj[u]:
            if du + w < dist[v]:
                dist[v] = du + w
                if not inqueue[v]:
                    inqueue[v] = True
                    queue.append(v)
    return dist[t] if dist[t] < INF else -1
