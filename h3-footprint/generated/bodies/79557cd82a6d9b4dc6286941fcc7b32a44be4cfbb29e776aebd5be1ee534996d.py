def solve(n, edges, s, t):
    if s == t:
        return 0
    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for u, v, w in edges:
        forward[u].append((v, w))
        backward[v].append((u, w))
    INF = float('inf')
    dist_f = [INF] * n
    dist_b = [INF] * n
    dist_f[s] = 0
    dist_b[t] = 0
    heap_f = [(0, s)]
    heap_b = [(0, t)]
    best = INF
    while heap_f and heap_b:
        if heap_f[0][0] + heap_b[0][0] >= best:
            break
        if heap_f[0][0] <= heap_b[0][0]:
            d, u = heapq.heappop(heap_f)
            if d > dist_f[u]:
                continue
            if dist_b[u] != INF and d + dist_b[u] < best:
                best = d + dist_b[u]
            for v, w in forward[u]:
                nd = d + w
                if nd < dist_f[v]:
                    dist_f[v] = nd
                    heapq.heappush(heap_f, (nd, v))
        else:
            d, u = heapq.heappop(heap_b)
            if d > dist_b[u]:
                continue
            if dist_f[u] != INF and d + dist_f[u] < best:
                best = d + dist_f[u]
            for v, w in backward[u]:
                nd = d + w
                if nd < dist_b[v]:
                    dist_b[v] = nd
                    heapq.heappush(heap_b, (nd, v))
    return -1 if best == INF else best
