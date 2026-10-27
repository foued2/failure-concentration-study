def solve(n, edges, s, t):
    if s == t:
        return 0
    import heapq
    INF = float('inf')
    fwd = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for u, v, w in edges:
        fwd[u].append((v, w))
        rev[v].append((u, w))
    df = [INF] * n
    db = [INF] * n
    df[s] = 0
    db[t] = 0
    hf = [(0, s)]
    hb = [(0, t)]
    done_f = [False] * n
    done_b = [False] * n
    mu = INF
    while hf or hb:
        kf = hf[0][0] if hf else INF
        kb = hb[0][0] if hb else INF
        if kf + kb >= mu:
            break
        if hf and (not hb or kf <= kb):
            d, u = heapq.heappop(hf)
            if done_f[u] or d > df[u]:
                continue
            done_f[u] = True
            if db[u] != INF and d + db[u] < mu:
                mu = d + db[u]
            for v, w in fwd[u]:
                nd = d + w
                if nd < df[v]:
                    df[v] = nd
                    heapq.heappush(hf, (nd, v))
                    if db[v] != INF and nd + db[v] < mu:
                        mu = nd + db[v]
        else:
            d, u = heapq.heappop(hb)
            if done_b[u] or d > db[u]:
                continue
            done_b[u] = True
            if df[u] != INF and df[u] + d < mu:
                mu = df[u] + d
            for v, w in rev[u]:
                nd = d + w
                if nd < db[v]:
                    db[v] = nd
                    heapq.heappush(hb, (nd, v))
                    if df[v] != INF and df[v] + nd < mu:
                        mu = df[v] + nd
    if mu == INF:
        return -1
    return int(mu)
