def solve(n, edges, s, t):
    if s == t:
        return 0
    cap = 0
    for _, _, w in edges:
        cap += w
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    buckets = [[] for _ in range(cap + 1)]
    buckets[0].append(s)
    d = 0
    while d <= cap:
        while buckets[d]:
            u = buckets[d].pop()
            if dist[u] != d:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v] and nd <= cap:
                    dist[v] = nd
                    buckets[nd].append(v)
        d += 1
    if dist[t] == INF:
        return -1
    return dist[t]
