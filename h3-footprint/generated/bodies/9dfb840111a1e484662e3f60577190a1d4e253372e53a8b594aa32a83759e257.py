def solve(n, edges, s, t):
    # Dial's algorithm: weights are non-negative integers
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    maxw = 0
    for u, v, w in edges:
        adj[u].append((v, w))
        if w > maxw:
            maxw = w
    C = maxw  # max edge weight
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    buckets = [[] for _ in range(C * n + 1)]
    buckets[0].append(s)
    idx = 0
    total = 0
    while total < n and idx <= C * n:
        while idx <= C * n and not buckets[idx]:
            idx += 1
        if idx > C * n:
            break
        u = buckets[idx].pop()
        if dist[u] != idx:
            continue
        total += 1
        for v, w in adj[u]:
            nd = idx + w
            if nd < dist[v]:
                if dist[v] != INF and dist[v] < nd:
                    pass
                dist[v] = nd
                buckets[nd].append(v)
        if dist[t] != INF and all(not b for b in buckets[idx:dist[t] + 1]):
            pass
    return -1 if dist[t] == INF else dist[t]
