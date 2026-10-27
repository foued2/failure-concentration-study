def solve(n, edges, s, t):
    if s == t:
        return 0

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

    hf = [(0, s)]
    hb = [(0, t)]
    done_f = [False] * n
    done_b = [False] * n
    best = INF

    while hf and hb:
        while hf and (done_f[hf[0][1]] or hf[0][0] != df[hf[0][1]]):
            heapq.heappop(hf)
        while hb and (done_b[hb[0][1]] or hb[0][0] != db[hb[0][1]]):
            heapq.heappop(hb)

        if not hf or not hb:
            break

        if hf[0][0] + hb[0][0] >= best:
            break

        if hf[0][0] <= hb[0][0]:
            d, u = heapq.heappop(hf)
            if d != df[u] or done_f[u]:
                continue

            done_f[u] = True
            if db[u] != INF:
                candidate = d + db[u]
                if candidate < best:
                    best = candidate

            for v, w in forward[u]:
                nd = d + w
                if nd < df[v]:
                    df[v] = nd
                    heapq.heappush(hf, (nd, v))
        else:
            d, u = heapq.heappop(hb)
            if d != db[u] or done_b[u]:
                continue

            done_b[u] = True
            if df[u] != INF:
                candidate = df[u] + d
                if candidate < best:
                    best = candidate

            for v, w in backward[u]:
                nd = d + w
                if nd < db[v]:
                    db[v] = nd
                    heapq.heappush(hb, (nd, v))

    return -1 if best == INF else best
