def solve(n, edges, s, t):
    import heapq

    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for u, v, w in edges:
        forward[u].append((v, w))
        backward[v].append((u, w))

    INF = float("inf")
    df = [INF] * n
    db = [INF] * n
    df[s] = 0
    db[t] = 0
    pf = [(0, s)]
    pb = [(0, t)]
    seen_f = [False] * n
    seen_b = [False] * n
    best = INF

    def heap_key(h):
        return h[0][0] if h else INF

    while True:
        if not pf and not pb:
            break
        if best < INF and heap_key(pf) + heap_key(pb) >= best:
            break
        if pf and (not pb or pf[0][0] <= pb[0][0]):
            d, u = heapq.heappop(pf)
            if seen_f[u] or d != df[u]:
                continue
            seen_f[u] = True
            if df[u] + db[u] < best:
                best = df[u] + db[u]
            for v, w in forward[u]:
                nd = d + w
                if nd < df[v]:
                    df[v] = nd
                    heapq.heappush(pf, (nd, v))
        else:
            d, u = heapq.heappop(pb)
            if seen_b[u] or d != db[u]:
                continue
            seen_b[u] = True
            if df[u] + db[u] < best:
                best = df[u] + db[u]
            for x, w in backward[u]:
                nd = d + w
                if nd < db[x]:
                    db[x] = nd
                    heapq.heappush(pb, (nd, x))
    return -1 if best == INF else int(best)
