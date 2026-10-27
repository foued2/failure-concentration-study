def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        radj[v].append((u, w))
    INF = float('inf')
    ds = [INF] * n
    dt = [INF] * n
    ds[s] = 0
    dt[t] = 0
    hs = [(0, s)]
    ht = [(0, t)]
    best = INF
    while hs or ht:
        if hs:
            du, u = heapq.heappop(hs)
            if du == ds[u]:
                if dt[u] < INF:
                    best = min(best, du + dt[u])
                for v, w in adj[u]:
                    if du + w < ds[v]:
                        ds[v] = du + w
                        heapq.heappush(hs, (ds[v], v))
        if ht:
            du, u = heapq.heappop(ht)
            if du == dt[u]:
                if ds[u] < INF:
                    best = min(best, du + ds[u])
                for v, w in radj[u]:
                    if du + w < dt[v]:
                        dt[v] = du + w
                        heapq.heappush(ht, (dt[v], v))
        if hs and ht and hs[0][0] + ht[0][0] >= best:
            break
    return -1 if best == INF else best
