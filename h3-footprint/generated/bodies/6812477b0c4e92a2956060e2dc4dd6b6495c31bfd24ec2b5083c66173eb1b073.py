def solve(n, edges, s, t):
    import heapq
    if s == t:
        return 0
    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for u, v, w in edges:
        forward[u].append((v, w))
        backward[v].append((u, w))
    INF = float("inf")
    dist_f = [INF] * n
    dist_b = [INF] * n
    dist_f[s] = 0
    dist_b[t] = 0
    heap_f = [(0, s)]
    heap_b = [(0, t)]
    best = INF
    while heap_f or heap_b:
        while heap_f and heap_f[0][0] != dist_f[heap_f[0][1]]:
            heapq.heappop(heap_f)
        while heap_b and heap_b[0][0] != dist_b[heap_b[0][1]]:
            heapq.heappop(heap_b)
        if not heap_f and not heap_b:
            break
        if not heap_b or (heap_f and heap_f[0][0] <= heap_b[0][0]):
            d, u = heapq.heappop(heap_f)
            if d + dist_b[u] < best:
                best = d + dist_b[u]
            for v, w in forward[u]:
                nd = d + w
                if nd < dist_f[v]:
                    dist_f[v] = nd
                    if nd + dist_b[v] < best:
                        best = nd + dist_b[v]
                    heapq.heappush(heap_f, (nd, v))
        else:
            d, u = heapq.heappop(heap_b)
            if d + dist_f[u] < best:
                best = d + dist_f[u]
            for v, w in backward[u]:
                nd = d + w
                if nd < dist_b[v]:
                    dist_b[v] = nd
                    if nd + dist_f[v] < best:
                        best = nd + dist_f[v]
                    heapq.heappush(heap_b, (nd, v))
    return -1 if best == INF else int(best)
