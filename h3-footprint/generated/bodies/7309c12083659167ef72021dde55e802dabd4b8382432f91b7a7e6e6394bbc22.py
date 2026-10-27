def solve(n, edges, s, t):
    import heapq
    from collections import defaultdict
    g = defaultdict(list)
    for a, b, c in edges:
        g[a].append((b, c))
    d = {s: 0}
    heap = [(0, s)]
    while heap:
        du, u = heapq.heappop(heap)
        if du > d[u]:
            continue
        for v, w in g[u]:
            nd = du + w
            if v not in d or nd < d[v]:
                d[v] = nd
                heapq.heappush(heap, (nd, v))
    return d.get(t, -1)
