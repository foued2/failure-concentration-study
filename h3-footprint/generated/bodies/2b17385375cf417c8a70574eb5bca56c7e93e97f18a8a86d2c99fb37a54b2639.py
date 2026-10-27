def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    level = {s}
    while level:
        triggered = set()
        for u in level:
            base = dist[u]
            for v, w in adj[u]:
                nd = base + w
                if nd < dist[v]:
                    dist[v] = nd
                    triggered.add(v)
        level = triggered
    return dist[t] if dist[t] != INF else -1
