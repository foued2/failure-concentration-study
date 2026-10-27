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
    buckets = [[] for _ in range(max_w + 1)]
    buckets[0].append(s)
    cur = 0
    visited_count = 0
    while True:
        while cur < len(buckets) and not buckets[cur]:
            cur += 1
        if cur >= len(buckets):
            break
        u = buckets[cur].pop()
        if cur > dist[u]:
            continue
        if u == t:
            return dist[u]
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                buckets[nd].append(v)
    return -1 if dist[t] == INF else dist[t]
