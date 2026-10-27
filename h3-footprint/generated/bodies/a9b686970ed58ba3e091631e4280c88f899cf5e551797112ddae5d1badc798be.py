def solve(n, edges, s, t):
    from collections import deque
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                if dist[v] == INF:
                    q.appendleft(v)
                else:
                    q.append(v)
                dist[v] = dist[u] + w
    return -1 if dist[t] == INF else dist[t]
