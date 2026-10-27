def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    max_w = 0
    for u, v, w in edges:
        adj[u].append((v, w))
        if w > max_w:
            max_w = w
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    buckets = deque()
    buckets.append(deque([s]))
    current_bucket = 0
    while buckets:
        while current_bucket < len(buckets) and not buckets[current_bucket]:
            buckets.popleft()
            current_bucket += 1
            if current_bucket == len(buckets):
                break
        if current_bucket == len(buckets):
            break
        u = buckets[current_bucket].popleft()
        if current_bucket != dist[u]:
            continue
        if u == t:
            break
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                if dist[v] != INF and dist[v] < len(buckets) and v in buckets[dist[v]]:
                    buckets[dist[v]].remove(v)
                dist[v] = nd
                if nd >= len(buckets):
                    buckets.extend(deque() for _ in range(nd - len(buckets) + 1))
                buckets[nd].append(v)
    return -1 if dist[t] == INF else dist[t]
