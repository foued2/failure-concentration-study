def solve(n, edges, s, t):
    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    buckets = {0: [s]}
    settled = [False] * n

    while buckets:
        d = min(buckets)
        layer = buckets.pop(d)
        for u in layer:
            if settled[u] or dist[u] != d:
                continue
            settled[u] = True
            if u == t:
                return d
            for v, w in graph[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets.setdefault(nd, []).append(v)

    return -1
