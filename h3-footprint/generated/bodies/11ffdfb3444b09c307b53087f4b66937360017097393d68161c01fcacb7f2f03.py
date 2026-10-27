def solve(n, edges, s, t):
    from collections import deque
    INF = float('inf')
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[s] = 0
    in_queue = [False] * n
    queue = deque([s])
    in_queue[s] = True
    while queue:
        u = queue.popleft()
        in_queue[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True
    if dist[t] == INF:
        return -1
    return int(dist[t])
