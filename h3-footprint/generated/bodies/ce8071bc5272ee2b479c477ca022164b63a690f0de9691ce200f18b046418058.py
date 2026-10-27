def solve(n, edges, s, t):
    if s == t:
        return 0
    maxw = 0
    for _, _, w in edges:
        if w > maxw:
            maxw = w
    cap = maxw * n + n
    buckets = [[] for _ in range(cap + 1)]
    buckets[0].append(s)
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    d = 0
    while d <= cap:
        while buckets[d]:
            u = buckets[d].pop()
            if dist[u] != d:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    if nd <= cap:
                        buckets[nd].append(v)
        d += 1
        if dist[t] != INF and d > dist[t]:
            break
    return dist[t] if dist[t] != INF else -1
