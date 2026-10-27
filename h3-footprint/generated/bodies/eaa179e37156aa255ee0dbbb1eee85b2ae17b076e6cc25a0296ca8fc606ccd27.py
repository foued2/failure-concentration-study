def solve(n, edges, s, t):
    if s == t:
        return 0
    adj_f = [[] for _ in range(n)]
    adj_r = [[] for _ in range(n)]
    for u, v, w in edges:
        adj_f[u].append((v, w))
        adj_r[v].append((u, w))
    INF = float('inf')
    dist_f = [INF] * n
    dist_r = [INF] * n
    dist_f[s] = 0
    dist_r[t] = 0
    hf = [(0, s)]
    hr = [(0, t)]
    mu = INF
    while hf or hr:
        if hf and (not hr or hf[0][0] <= hr[0][0]):
            df, u = heapq.heappop(hf)
            if df > dist_f[u]:
                continue
            if df >= mu:
                break
            for v, w in adj_f[u]:
                nd = df + w
                if nd < dist_f[v]:
                    dist_f[v] = nd
                    heapq.heappush(hf, (nd, v))
            if dist_r[u] != INF:
                mu = min(mu, dist_f[u] + dist_r[u])
        else:
            dr, u = heapq.heappop(hr)
            if dr > dist_r[u]:
                continue
            if dr >= mu:
                break
            for v, w in adj_r[u]:
                nd = dr + w
                if nd < dist_r[v]:
                    dist_r[v] = nd
                    heapq.heappush(hr, (nd, v))
            if dist_f[u] != INF:
                mu = min(mu, dist_f[u] + dist_r[u])
    return -1 if mu == INF else mu
