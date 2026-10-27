def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, wt in edges:
        adj[u].append((v, wt))
    dist = [None] * n
    dist[s] = 0
    buckets = {0: [s]}
    d = 0
    while buckets:
        bucket = buckets.get(d)
        if bucket is None:
            d += 1
            continue
        del buckets[d]
        for u in bucket:
            du = dist[u]
            for v, wt in adj[u]:
                nd = du + wt
                if dist[v] is None or nd < dist[v]:
                    dist[v] = nd
                    buckets.setdefault(nd, []).append(v)
            if d in buckets:
                more = buckets.pop(d)
                bucket.extend(more)
        if dist[t] is not None:
            return dist[t]
    return -1
