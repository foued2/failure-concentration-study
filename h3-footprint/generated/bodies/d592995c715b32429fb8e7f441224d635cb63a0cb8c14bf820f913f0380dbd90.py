def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = 1 << 62
    dist = [INF] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        du = dist[u]
        for v, w in adj[u]:
            if du + w < dist[v]:
                dist[v] = du + w
                q.append(v)
    return dist[t] if dist[t] < INF else -1
