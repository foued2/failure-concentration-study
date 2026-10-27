def solve(n, edges, s, t):
    import heapq
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))
    dist = {s: 0}
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist.get(u):
            continue
        if u == t:
            return int(d)
        for v, w in adj.get(u, ()):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return -1
