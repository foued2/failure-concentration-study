def solve(n, edges, s, t):
    head = [[] for _ in range(n)]
    tail = [[] for _ in range(n)]
    for u, v, w in edges:
        head[u].append((v, w))
        tail[v].append((u, w))
    INF = float("inf")
    df = [INF] * n
    db = [INF] * n
    df[s] = 0
    db[t] = 0
    hf = [(0, s)]
    hb = [(0, t)]
    lockedf = [False] * n
    lockedb = [False] * n
    best = INF
    while hf or hb:
        tf = hf[0][0] if hf else INF
        tb = hb[0][0] if hb else INF
        if tf >= best and tb >= best:
            break
        if tf <= tb:
            d, u = heapq.heappop(hf)
            if lockedf[u]:
                continue
            lockedf[u] = True
            if db[u] != INF and df[u] + db[u] < best:
                best = df[u] + db[u]
            for v, w in head[u]:
                nd = d + w
                if nd < df[v]:
                    df[v] = nd
                    heapq.heappush(hf, (nd, v))
        else:
            d, u = heapq.heappop(hb)
            if lockedb[u]:
                continue
            lockedb[u] = True
            if df[u] != INF and df[u] + db[u] < best:
                best = df[u] + db[u]
            for v, w in tail[u]:
                nd = d + w
                if nd < db[v]:
                    db[v] = nd
                    heapq.heappush(hb, (nd, v))
    return best if best != INF else -1
