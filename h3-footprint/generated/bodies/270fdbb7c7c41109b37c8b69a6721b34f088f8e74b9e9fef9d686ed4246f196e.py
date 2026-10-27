def solve(n, edges, s, t):
    from collections import deque
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    buckets = {0: deque([s])}
    while buckets:
        d = min(buckets)
        q = buckets[d]
        while q:
            u = q.popleft()
            if dist[u] != d:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets.setdefault(nd, deque()).append(v)
        del buckets[d]
    return -1 if dist[t] == INF else dist[t]
