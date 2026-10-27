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
    while hf and hr:
        if hf[0][0] + hr[0][0] >= best:
            break
        if hf[0][0] <= hr[0][0]:
            d, u = heapq.heappop(hf)
            if d > df[u]:
                continue
            if dr[u] < INF and d + dr[u] < best:
                best = d + dr[u]
            for v, w in fwd[u]:
                nd = d + w
                if nd < df[v]:
                    df[v] = nd
                    heapq.heappush(hf, (nd, v))
                    if dr[v] < INF and nd + dr[v] < best:
                        best = nd + dr[v]
        else:
            d, u = heapq.heappop(hr)
            if d > dr[u]:
                continue
            if df[u] < INF and df[u] + d < best:
                best = df[u] + d
            for v, w in rev[u]:
                nd = d + w
                if nd < dr[v]:
                    dr[v] = nd
                    heapq.heappush(hr, (nd, v))
                    if df[v] < INF and df[v] + nd < best:
                        best = df[v] + nd
    return -1 if best == INF else int(best)
