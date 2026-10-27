def solve(n, edges, s, t):
    if s == t:
        return 0
    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
        rg[v].append((u, w))
    INF = float('inf')
    df = [INF] * n
    db = [INF] * n
    df[s] = 0
    db[t] = 0
    pf = [(0, s)]
    pb = [(0, t)]
    mu = INF
    while pf or pb:
        if pf and (not pb or pf[0][0] <= pb[0][0]):
            d, u = heapq.heappop(pf)
            if d != df[u]:
                continue
            if d >= mu:
                pf = []
                continue
            for v, w in g[u]:
                nd = d + w
                if nd < df[v]:
                    df[v] = nd
                    heapq.heappush(pf, (nd, v))
                    cand = nd + db[v]
                    if cand < mu:
                        mu = cand
        else:
            d, u = heapq.heappop(pb)
            if d != db[u]:
                continue
            if d >= mu:
                pb = []
                continue
            for v, w in rg[u]:
                nd = d + w
                if nd < db[v]:
                    db[v] = nd
                    heapq.heappush(pb, (nd, v))
                    cand = df[v] + nd
                    if cand < mu:
                        mu = cand
    best = mu
    for v in range(n):
        cand = df[v] + db[v]
        if cand < best:
            best = cand
    return -1 if best == INF else int(best)
