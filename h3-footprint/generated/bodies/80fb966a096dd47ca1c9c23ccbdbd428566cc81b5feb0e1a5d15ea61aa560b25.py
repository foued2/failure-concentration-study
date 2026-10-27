def solve(n, edges, s, t):
    from collections import deque
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
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
                    if dq and dist[dq[0]] < nd:
                        dq.append(v)
                    else:
                        dq.appendleft(v)
                    in_queue[v] = True
    return dist[t] if dist[t] != INF else -1
