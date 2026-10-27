def solve(n, edges, s, t):
    if s == t:
        return 0
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    buckets = {0: [s]}
    while buckets:
        current = min(buckets)
        layer = buckets.pop(current)
        for u in layer:
            if dist[u] != current:
                continue
            if u == t:
                return int(current)
            for v, w in graph[u]:
                nd = current + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets.setdefault(nd, []).append(v)
    return -1 if dist[t] == INF else int(dist[t])
