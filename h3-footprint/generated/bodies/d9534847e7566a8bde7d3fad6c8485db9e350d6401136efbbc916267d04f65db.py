def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    maxw = 0
    for u, v, w in edges:
        adj[u].append((v, w))
        if w > maxw:
            maxw = w
    m = maxw + 1
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    buckets = [[] for _ in range(m)]
    buckets[0].append(s)
    for d in range(n * m):
        b = buckets[d % m]
        while b:
            u = b.pop()
            if dist[u] != d:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets[nd % m].append(v)
    return -1 if dist[t] == INF else int(dist[t])
