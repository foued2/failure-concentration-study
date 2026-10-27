def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    inq = [False] * n
    q = deque([s])
    inq[s] = True
    while q:
        u = q.popleft()
        inq[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not inq[v]:
                    inq[v] = True
                    q.append(v)
    if dist[t] == INF:
        return -1
    return dist[t]
