def solve(n, edges, s, t):
    if s == t:
        return 0
    fwd = [[] for _ in range(n)]
    bwd = [[] for _ in range(n)]
    for u, v, w in edges:
        fwd[u].append((v, w))
        bwd[v].append((u, w))
    INF = float('inf')
    df = [INF] * n
    db = [INF] * n
    df[s] = 0
    db[t] = 0
    hf = [(0, s)]
    hb = [(0, t)]
    sfd = set()
    sbd = set()
    best = INF
    while hf or hb:
        if hf and hb and hf[0][0] + hb[0][0] >= best:
            break
        if not hb or (hf and hf[0][0] <= hb[0][0]):
            d, u = heapq.heappop(hf)
            if d > df[u]:
                continue
            if u in sbd and d + db[u] < best:
                best = d + db[u]
            sfd.add(u)
            for v, w in fwd[u]:
                nd = d + w
                if nd < df[v]:
                    df[v] = nd
                    heapq.heappush(hf, (nd, v))
                    if v in sbd and nd + db[v] < best:
                        best = nd + db[v]
        else:
            d, u = heapq.heappop(hb)
            if d > db[u]:
                continue
            if u in sfd and d + df[u] < best:
                best = d + df[u]
            sbd.add(u)
            for v, w in bwd[u]:
                nd = d + w
                if nd < db[v]:
                    db[v] = nd
                    heapq.heappush(hb, (nd, v))
                    if v in sfd and nd + df[v] < best:
                        best = nd + df[v]
    return -1 if best == INF else int(best)
