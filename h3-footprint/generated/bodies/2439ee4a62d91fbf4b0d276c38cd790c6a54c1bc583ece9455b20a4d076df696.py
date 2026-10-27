def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                if v == t:
                    return dist[v]
                q.append(v)
            elif dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                q.appendleft(v)
    return dist[t]
