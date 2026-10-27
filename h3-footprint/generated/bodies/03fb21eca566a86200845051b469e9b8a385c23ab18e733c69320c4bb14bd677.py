def solve(n, edges, s, t):
    if n <= 0:
        return -1
    if s == t:
        return 0
    from collections import defaultdict
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    buckets = defaultdict(list)
    buckets[0].append(s)
    while buckets:
        d = min(buckets)
        u = buckets[d].pop()
        if not buckets[d]:
            del buckets[d]
        if dist[u] != d:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                buckets[nd].append(v)
    return -1 if dist[t] == inf else dist[t]
