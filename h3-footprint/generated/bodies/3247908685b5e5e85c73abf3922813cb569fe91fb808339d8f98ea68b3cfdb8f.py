def solve(n, edges, s, t):
    if s == t:
        return 0
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((w, v))
    dist = {}
    heap = [(0, s)]
    while heap:
        d, node = heapq.heappop(heap)
        if node in dist:
            continue
        dist[node] = d
        if node == t:
            return d
        for w, nxt in g[node]:
            if nxt not in dist:
                heapq.heappush(heap, (d + w, nxt))
    return -1
