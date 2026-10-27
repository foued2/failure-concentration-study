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
    mu = INF
    while hf and hr:
        if hf[0][0] + hr[0][0] >= mu:
            break
        du, u = heapq.heappop(hf)
        if du == df[u]:
            for v, w in fwd[u]:
                nd = du + w
                if nd < df[v]:
                    df[v] = nd
                    heapq.heappush(hf, (nd, v))
                    if df[v] + dr[v] < mu:
                        mu = df[v] + dr[v]
        du, u = heapq.heappop(hr)
        if du == dr[u]:
            for v, w in rev[u]:
                nd = du + w
                if nd < dr[v]:
                    dr[v] = nd
                    heapq.heappush(hr, (nd, v))
                    if df[v] + dr[v] < mu:
                        mu = df[v] + dr[v]
    return -1 if mu == INF else mu
