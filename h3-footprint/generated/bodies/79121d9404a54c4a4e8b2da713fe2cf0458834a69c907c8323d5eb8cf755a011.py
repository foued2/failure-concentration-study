def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    total = 0
    for u, v, w in edges:
        adj[u].append((v, w))
        total += w
    dist = [None] * n
    dist[s] = 0
    buckets = [deque() for _ in range(total + 1)]
    buckets[0].append(s)
    d = 0
    while d <= total:
        if dist[t] is not None and dist[t] <= d:
            return dist[t]
        bucket = buckets[d]
        d += 1
        while bucket:
            u = bucket.popleft()
            if dist[u] != d - 1:
                continue
            for v, w in adj[u]:
                nd = dist[u] + w
                if dist[v] is None or nd < dist[v]:
                    dist[v] = nd
                    buckets[nd].append(v)
    return -1 if dist[t] is None else dist[t]
