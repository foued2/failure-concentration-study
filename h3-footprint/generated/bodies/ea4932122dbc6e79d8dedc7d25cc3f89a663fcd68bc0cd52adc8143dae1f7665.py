def solve(n, edges, s, t):
    if s == t:
        return 0
    fwd = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for u, v, w in edges:
        fwd[u].append((v, w))
        rev[v].append((u, w))
    INF = float('inf')
    df = [INF] * n
    dr = [INF] * n
    df[s] = 0
    dr[t] = 0
    hf = [(0, s)]
    hr = [(0, t)]
    best = INF
    while hf or hr:
        if hf:
            d, u = heapq.heappop(hf)
            if d == df[u]:
                if dr[u] < INF:
                    best = min(best, d + dr[u])
                for v, w in fwd[u]:
                    nd = d + w
                    if nd < df[v]:
                        df[v] = nd
                        heapq.heappush(hf, (nd, v))
        if hr:
            d, u = heapq.heappop(hr)
            if d == dr[u]:
                if df[u] < INF:
                    best = min(best, d + df[u])
                for v, w in rev[u]:
                    nd = d + w
                    if nd < dr[v]:
                        dr[v] = nd
                        heapq.heappush(hr, (nd, v))
        bound = (hf[0][0] if hf else INF) + (hr[0][0] if hr else INF)
        if best <= bound:
            break
    return -1 if best == INF else int(best)
