def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    buckets = defaultdict(list)
    keys = [0]
    buckets[0].append(s)
    while keys:
        d = heapq.heappop(keys)
        bucket = buckets.pop(d, None)
        if not bucket:
            continue
        while bucket:
            u = bucket.pop()
            if dist[u] != d:
                continue
            if u == t:
                return d
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    if nd not in buckets:
                        heapq.heappush(keys, nd)
                    buckets[nd].append(v)
    return -1 if dist[t] == INF else int(dist[t])
