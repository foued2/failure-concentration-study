def solve(n, edges, s, t):
    import heapq

    if s == t:
        return 0
    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for u, v, w in edges:
        forward[u].append((v, w))
        backward[v].append((u, w))
    inf = float("inf")
    df = [inf] * n
    db = [inf] * n
    df[s] = 0
    db[t] = 0
    hf = [(0, s)]
    hb = [(0, t)]
    done_f = [False] * n
    done_b = [False] * n
    best = inf
    while hf and hb:
        if hf[0][0] + hb[0][0] >= best:
            break
        if hf[0][0] <= hb[0][0]:
            d, u = heapq.heappop(hf)
            if d != df[u] or done_f[u]:
                continue
            done_f[u] = True
            if db[u] != inf:
                best = min(best, df[u] + db[u])
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
            if df[u] != inf:
                best = min(best, df[u] + db[u])
            for v, w in backward[u]:
                nd = d + w
                if nd < db[v]:
                    db[v] = nd
                    heapq.heappush(hb, (nd, v))
    return -1 if best == inf else best
