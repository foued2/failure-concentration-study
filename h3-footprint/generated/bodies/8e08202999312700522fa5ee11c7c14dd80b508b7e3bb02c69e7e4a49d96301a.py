def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [None] * n
    dist[s] = 0
    dq = deque([s])
    while dq:
        u = dq.popleft()
        if u == t:
            return dist[t]
        for v, w in adj[u]:
            nd = dist[u] + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                dq.append(v)
    return -1
