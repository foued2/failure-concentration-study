def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    buckets = {0: [s]}
    cur = 0
    while buckets:
        if cur not in buckets:
            cur += 1
            continue
        nodes = buckets.pop(cur)
        for u in nodes:
            if dist[u] < cur:
                continue
            for v, w in adj[u]:
                nd = cur + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets.setdefault(nd, []).append(v)
    return dist[t] if dist[t] != INF else -1
