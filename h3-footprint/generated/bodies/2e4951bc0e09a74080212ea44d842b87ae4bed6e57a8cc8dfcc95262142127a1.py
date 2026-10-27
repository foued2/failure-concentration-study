def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    if s == t:
        return 0
    INF = float('inf')
    df, dt = [INF] * n, [INF] * n
    df[s] = dt[t] = 0
    qf, qt = [(0, s)], [(0, t)]
    best = INF
    donef, donet = [False] * n, [False] * n
    while qf and qt:
        if qf[0][0] + qt[0][0] >= best:
            break
        if qf[0][0] <= qt[0][0]:
            d, u = heapq.heappop(qf)
            if d > df[u]:
                continue
            if donet[u]:
                best = min(best, d + dt[u])
            donef[u] = True
            for v, w in g[u]:
                nd = d + w
                if nd < df[v]:
                    df[v] = nd
                    heapq.heappush(qf, (nd, v))
                    if donet[v]:
                        best = min(best, nd + dt[v])
        else:
            d, u = heapq.heappop(qt)
            if d > dt[u]:
                continue
            if donef[u]:
                best = min(best, d + df[u])
            donet[u] = True
            for v, w in g[u]:
                nd = d + w
                if nd < dt[v]:
                    dt[v] = nd
                    heapq.heappush(qt, (nd, v))
                    if donef[v]:
                        best = min(best, nd + df[v])
    return best if best != INF else -1
