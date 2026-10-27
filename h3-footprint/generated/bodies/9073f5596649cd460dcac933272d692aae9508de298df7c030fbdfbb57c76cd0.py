def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    max_w = 1
    for u, v, w in edges:
        adj[u].append((v, w))
        if w > max_w:
            max_w = w
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    C = max_w + 1
    buckets = [deque() for _ in range(C)]
    buckets[0].append(s)
    pending = 1
    cur = 0
    while pending:
        while not buckets[cur % C]:
            cur += 1
        u = buckets[cur % C].popleft()
        pending -= 1
        if dist[u] != cur:
            continue
        if u == t:
            return cur
        for v, w in adj[u]:
            nd = cur + w
            if nd < dist[v]:
                dist[v] = nd
                buckets[nd % C].append(v)
                pending += 1
    return -1 if dist[t] is INF or dist[t] == INF else dist[t]
