def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    dist[0][s] = 0
    heap = [(0, 0, s)]
    while heap:
        d, layer, u = heapq.heappop(heap)
        if d != dist[layer][u]:
            continue
        if u == t:
            return d
        if layer + 1 >= n:
            continue
        nd = d
        ndl = layer + 1
        if nd < dist[ndl][u]:
            dist[ndl][u] = nd
            heapq.heappush(heap, (nd, ndl, u))
        for v, w in adj[u]:
            ndv = d + w
            if ndv < dist[ndl][v]:
                dist[ndl][v] = ndv
                heapq.heappush(heap, (ndv, ndl, v))
    best = min(dist[layer][t] for layer in range(n))
    return -1 if best == INF else best
