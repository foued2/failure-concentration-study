def solve(n, edges, s, t):
    INF = float("inf")
    adj = {}
    for u, v, w in edges:
        row = adj.setdefault(u, {})
        if v not in row or w < row[v]:
            row[v] = w
    dist = {s: 0}
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, INF):
            continue
        if u == t:
            return d
        for v, w in adj.get(u, {}).items():
            nd = d + w
            if nd < dist.get(v, INF):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return -1
