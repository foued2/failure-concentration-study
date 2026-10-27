def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    total = 0
    for u, v, w in edges:
        adj[u].append((v, w))
        total += w
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    limit = total + 1
    buckets = [[] for _ in range(limit)]
    buckets[0].append(s)
    for d in range(limit):
        for u in buckets[d]:
            if dist[u] != d:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets[nd].append(v)
    return dist[t] if dist[t] != INF else -1
