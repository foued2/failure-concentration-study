def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    inq = [False] * n
    dq = deque([s])
    inq[s] = True
    while dq:
        u = dq.popleft()
        inq[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not inq[v]:
                    dq.append(v)
                    inq[v] = True
    return -1 if dist[t] == INF else int(dist[t])
