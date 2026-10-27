def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    queued = [False] * n
    dist[s] = 0
    q = deque([s])
    queued[s] = True
    while q:
        u = q.popleft()
        queued[u] = False
        du = dist[u]
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not queued[v]:
                    q.append(v)
                    queued[v] = True
    return dist[t] if dist[t] != INF else -1
