def solve(n, edges, s, t):
    import heapq
    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for u, v, w in edges:
        forward[u].append((v, w))
        backward[v].append((u, w))
    ds = [None] * n
    dt = [None] * n
    ds[s] = 0
    dt[t] = 0
    done_s = [False] * n
    done_t = [False] * n
    heap_s = [(0, s)]
    heap_t = [(0, t)]
    best = None
    while heap_s or heap_t:
        if heap_s and (not heap_t or heap_s[0][0] <= heap_t[0][0]):
            d, u = heapq.heappop(heap_s)
            if done_s[u]:
                continue
            done_s[u] = True
            if dt[u] is not None:
                cand = d + dt[u]
                if best is None or cand < best:
                    best = cand
            for v, w in forward[u]:
                nd = d + w
                if ds[v] is None or nd < ds[v]:
                    ds[v] = nd
                    heapq.heappush(heap_s, (nd, v))
        else:
            d, u = heapq.heappop(heap_t)
            if done_t[u]:
                continue
            done_t[u] = True
            if ds[u] is not None:
                cand = d + ds[u]
                if best is None or cand < best:
                    best = cand
            for v, w in backward[u]:
                nd = d + w
                if dt[v] is None or nd < dt[v]:
                    dt[v] = nd
                    heapq.heappush(heap_t, (nd, v))
    return -1 if best is None else best
