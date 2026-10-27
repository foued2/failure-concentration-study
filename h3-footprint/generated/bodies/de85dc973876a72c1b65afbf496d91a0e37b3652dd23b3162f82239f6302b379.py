def solve(n, edges, s, t):
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append(w)
        g[u].append(v)
    INF = float('inf')
    dist = {}
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if u == t:
            return d
        if d > dist.get(u, INF):
            continue
        row = g[u]
        for idx in range(0, len(row), 2):
            w, v = row[idx], row[idx + 1]
            nd = d + w
            cur = dist.get(v, INF)
            if nd < cur:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return -1
