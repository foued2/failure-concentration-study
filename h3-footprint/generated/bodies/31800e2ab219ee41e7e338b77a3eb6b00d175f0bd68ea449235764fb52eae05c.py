def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    in_q = [False] * n
    q = deque([s])
    in_q[s] = True
    while q:
        u = q.popleft()
        in_q[u] = False
        du = dist[u]
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not in_q[v]:
                    q.append(v)
                    in_q[v] = True
    return -1 if dist[t] == INF else int(dist[t])
