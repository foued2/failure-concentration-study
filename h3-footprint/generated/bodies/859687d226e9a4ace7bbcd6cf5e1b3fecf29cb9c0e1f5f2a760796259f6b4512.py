def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    wmax = 0
    for u, v, w in edges:
        adj[u].append((v, w))
        if w > wmax:
            wmax = w
    max_dist = wmax * (n - 1)
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    buckets = [[] for _ in range(max_dist + 1)]
    buckets[0].append(s)
    d = 0
    while d <= max_dist:
        if not buckets[d]:
            d += 1
            continue
        u = buckets[d].pop()
        if dist[u] != d:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                buckets[nd].append(v)
    return -1 if dist[t] == INF else dist[t]
