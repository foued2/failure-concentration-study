def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    max_w = 0
    for u, v, w in edges:
        if w >= 0:
            adj[u].append((v, w))
            if w > max_w:
                max_w = w
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    buckets = [deque() for _ in range(max_w + 1)]
    buckets[0].append(s)
    cur = 0
    limit = max_w
    while True:
        while cur <= limit and not buckets[cur]:
            cur += 1
        if cur > limit:
            break
        u = buckets[cur].popleft()
        if dist[u] < cur:
            continue
        if u == t:
            return cur
        for v, w in adj[u]:
            nd = cur + w
            if nd < dist[v]:
                dist[v] = nd
                if nd > limit:
                    limit = nd
                buckets[nd].append(v)
    return -1 if dist[t] == INF else dist[t]
