def solve(n, edges, s, t):
    if s == t:
        return 0
    graph = [[] for _ in range(n)]
    max_w = 0
    for u, v, w in edges:
        graph[u].append((v, w))
        if w > max_w:
            max_w = w
    C = max_w + 1
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    buckets = [deque() for _ in range(C)]
    buckets[0].append(s)
    curr = 0
    empty = 0
    processed = 0
    while processed < n and empty < C:
        if not buckets[curr]:
            empty += 1
            curr += 1
            if curr == C:
                curr = 0
            continue
        empty = 0
        u = buckets[curr].popleft()
        if dist[u] != curr:
            continue
        processed += 1
        if u == t:
            return curr
        for v, w in graph[u]:
            nd = curr + w
            if nd < dist[v]:
                dist[v] = nd
                buckets[nd % C].append(v)
        curr += 1
        if curr == C:
            curr = 0
    return -1 if dist[t] == INF else int(dist[t])
