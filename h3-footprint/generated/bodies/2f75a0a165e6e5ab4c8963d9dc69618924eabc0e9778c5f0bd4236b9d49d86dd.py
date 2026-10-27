def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    on = [False] * n
    on[s] = True
    q = deque([s])
    while q:
        u = q.popleft()
        on[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not on[v]:
                    q.append(v)
                    on[v] = True
    return -1 if dist[t] == INF else dist[t]
