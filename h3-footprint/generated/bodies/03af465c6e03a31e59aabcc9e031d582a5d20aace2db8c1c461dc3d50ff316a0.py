def solve(n, edges, s, t):
    if s == t:
        return 0

    import heapq

    fwd = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for u, v, w in edges:
        fwd[u].append((v, w))
        rev[v].append((u, w))

    INF = float("inf")
    df = [INF] * n
    db = [INF] * n
    df[s] = 0
    db[t] = 0
    pf = [(0, s)]
    pb = [(0, t)]
    done_f = [False] * n
    done_b = [False] * n
    best = INF
    last_f = 0
    last_b = 0

    while pf or pb:
        if last_f + last_b >= best:
            break
        if pf and (not pb or pf[0][0] <= pb[0][0]):
            d, u = heapq.heappop(pf)
            if done_f[u] or d != df[u]:
                continue
            done_f[u] = True
            last_f = d
            for v, w in fwd[u]:
                nd = d + w
                if nd < df[v]:
                    df[v] = nd
                    heapq.heappush(pf, (nd, v))
                if db[v] < INF and nd + db[v] < best:
                    best = nd + db[v]
        else:
            d, u = heapq.heappop(pb)
            if done_b[u] or d != db[u]:
                continue
            done_b[u] = True
            last_b = d
            for v, w in rev[u]:
                nd = d + w
                if nd < db[v]:
                    db[v] = nd
                    heapq.heappush(pb, (nd, v))
                if df[v] < INF and nd + df[v] < best:
                    best = nd + df[v]

    if best < INF:
        return best
    return -1 if df[t] == INF else df[t]
