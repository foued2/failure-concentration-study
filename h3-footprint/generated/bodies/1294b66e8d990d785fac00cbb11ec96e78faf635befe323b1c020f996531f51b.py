def solve(n, edges, s, t):
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))
    if s == t:
        return 0
    dist = [None] * n
    dist[s] = 0
    heap = [(0, s)]
    seen = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        for v, w in adj.get(u, []):
            nd = d + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
        if dist[t] is not None and t in seen:
            return dist[t]
    return -1 if dist[t] is None else dist[t]
