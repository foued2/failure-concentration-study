def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    max_w = 0
    for u, v, w in edges:
        adj[u].append((v, w))
        if w > max_w:
            max_w = w
    INF = float("inf")
    limit = max_w * (n - 1) if n > 1 else 0
    dist = [INF] * n
    dist[s] = 0
    pending = 1
    buckets = {0: [s]}
    d = 0
    while pending and d <= limit:
        bucket = buckets.get(d)
        if not bucket:
            d += 1
            continue
        while bucket:
            u = bucket.pop()
            if dist[u] != d:
                continue
            pending -= 1
            if u == t:
                return d
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    if dist[v] == INF:
                        pending += 1
                    dist[v] = nd
                    buckets.setdefault(nd, []).append(v)
    return -1 if dist[t] == INF else dist[t]
