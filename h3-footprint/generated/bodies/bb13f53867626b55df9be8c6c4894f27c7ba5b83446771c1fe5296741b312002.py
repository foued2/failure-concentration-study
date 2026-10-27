def solve(n, edges, s, t):
    if s == t:
        return 0
    F = [[] for _ in range(n)]
    R = [[] for _ in range(n)]
    for u, v, w in edges:
        F[u].append((v, w))
        R[v].append((u, w))
    INF = 10**30
    df = [INF] * n
    db = [INF] * n
    df[s] = 0
    db[t] = 0
    hf = [(0, s)]
    hb = [(0, t)]
    sf = [False] * n
    sb = [False] * n
    best = INF

    def top(h):
        return h[0][0] if h else INF

    while hf or hb:
        if top(hf) + top(hb) >= best:
            break
        if hf and top(hf) <= top(hb):
            d, u = heapq.heappop(hf)
            if sf[u]:
                continue
            sf[u] = True
            if db[u] < INF and d + db[u] < best:
                best = d + db[u]
            for v, w in F[u]:
                if d + w < df[v]:
                    df[v] = d + w
                    heapq.heappush(hf, (df[v], v))
        else:
            d, u = heapq.heappop(hb)
            if sb[u]:
                continue
            sb[u] = True
            if df[u] < INF and d + df[u] < best:
                best = d + df[u]
            for v, w in R[u]:
                if d + w < db[v]:
                    db[v] = d + w
                    heapq.heappush(hb, (db[v], v))
    return -1 if best == INF else best
