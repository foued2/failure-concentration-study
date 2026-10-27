def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    maxw = 0
    for u, v, w in edges:
        g[u].append((v, w))
        if w > maxw:
            maxw = w
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    buckets = [set() for _ in range(maxw * n + 1)]
    buckets[0].add(s)
    cur = 0
    total = maxw * n + 1
    while cur < total:
        if not buckets[cur]:
            cur += 1
            continue
        u = next(iter(buckets[cur]))
        buckets[cur].discard(u)
        if dist[u] != cur:
            continue
        for v, w in g[u]:
            nd = cur + w
            if nd < dist[v]:
                if dist[v] != INF:
                    buckets[dist[v]].discard(v)
                dist[v] = nd
                buckets[nd].add(v)
    return dist[t] if dist[t] != INF else -1
