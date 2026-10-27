def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    inside = [False] * n
    queue = deque([s])
    inside[s] = True
    while queue:
        u = queue.popleft()
        inside[u] = False
        base = dist[u]
        for v, w in adj[u]:
            nd = base + w
            if nd < dist[v]:
                dist[v] = nd
                if not inside[v]:
                    queue.append(v)
                    inside[v] = True
    return dist[t] if dist[t] != INF else -1
