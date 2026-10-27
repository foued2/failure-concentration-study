def solve(n, edges, s, t):
    import heapq
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
    INF = float("inf")
    dist = {s: 0}
    done = set()
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist.get(u, INF):
            continue
        if u in done:
            continue
        done.add(u)
        if u == t:
            return d
        for v, w in graph.get(u, ()):
            nd = d + w
            if nd < dist.get(v, INF):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
