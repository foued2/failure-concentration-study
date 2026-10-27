def solve(n, edges, s, t):
    maxw = 0
    for _, _, w in edges:
        if w > maxw:
            maxw = w
    INF = float('inf')
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[s] = 0
    buckets = [[] for _ in range(n * (maxw + 1) + 1)]
    buckets[0].append(s)
    for d in range(len(buckets)):
        while buckets[d]:
            u = buckets[d].pop()
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets[nd].append(v)
    return -1 if dist[t] == INF else dist[t]
