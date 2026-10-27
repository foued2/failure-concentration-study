def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [None] * n
    dist[s] = 0
    in_queue = [False] * n
    in_queue[s] = True
    q = deque([s])
    while q:
        u = q.popleft()
        in_queue[u] = False
        for v, w in adj[u]:
            nd = dist[u] + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    q.append(v)
                    in_queue[v] = True
    return -1 if dist[t] is None else dist[t]
