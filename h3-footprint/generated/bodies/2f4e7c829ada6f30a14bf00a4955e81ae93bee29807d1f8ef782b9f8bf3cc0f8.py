def solve(n, edges, s, t):
    from collections import deque

    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    in_queue = [False] * n
    dq = deque([s])
    in_queue[s] = True
    while dq:
        u = dq.popleft()
        in_queue[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    dq.append(v)
                    in_queue[v] = True
    return -1 if dist[t] == INF else int(dist[t])
