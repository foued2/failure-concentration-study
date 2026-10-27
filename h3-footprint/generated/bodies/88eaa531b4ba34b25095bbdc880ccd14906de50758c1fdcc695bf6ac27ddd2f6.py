def solve(n, edges, s, t):
    fwd = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for u, v, w in edges:
        if w >= 0:
            fwd[u].append((v, w))
            rev[v].append((u, w))
    INF = float("inf")
    df = [INF] * n
    dr = [INF] * n
    df[s] = 0
    dr[t] = 0
    hf = [(0, s)]
    hr = [(0, t)]
    mu = INF
    while hf or hr:
        if hf:
            df_u, u = heapq.heappop(hf)
            if df_u == df[u]:
                if df_u + dr[u] < mu:
                    mu = df_u + dr[u]
                for v, w in fwd[u]:
                    nd = df_u + w
                    if nd < df[v]:
                        df[v] = nd
                        heapq.heappush(hf, (nd, v))
        if hr:
            dr_u, u = heapq.heappop(hr)
            if dr_u == dr[u]:
                if df[u] + dr_u < mu:
                    mu = df[u] + dr_u
                for v, w in rev[u]:
                    nd = dr_u + w
                    if nd < dr[v]:
                        dr[v] = nd
                        heapq.heappush(hr, (nd, v))
        if (not hf or hf[0][0] >= mu) and (not hr or hr[0][0] >= mu):
            break
    return -1 if mu == INF else mu
