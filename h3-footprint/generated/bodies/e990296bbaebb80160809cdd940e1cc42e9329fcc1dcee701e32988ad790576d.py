def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        radj[v].append((u, w))
    INF = float('inf')
    dist_f = [INF] * n
    dist_b = [INF] * n
    dist_f[s] = 0
    dist_b[t] = 0
    pq_f = [(0, s)]
    pq_b = [(0, t)]
    mu = INF
    while pq_f or pq_b:
        if pq_f and (not pq_b or pq_f[0][0] <= pq_b[0][0]):
            d, u = heapq.heappop(pq_f)
            if d != dist_f[u]:
                continue
            if d >= mu:
                break
            for v, w in adj[u]:
                nd = d + w
                if nd < dist_f[v]:
                    dist_f[v] = nd
                    heapq.heappush(pq_f, (nd, v))
                if nd + dist_b[v] < mu:
                    mu = nd + dist_b[v]
        else:
            d, u = heapq.heappop(pq_b)
            if d != dist_b[u]:
                continue
            if d >= mu:
                break
            for v, w in radj[u]:
                nd = d + w
                if nd < dist_b[v]:
                    dist_b[v] = nd
                    heapq.heappush(pq_b, (nd, v))
                if nd + dist_f[v] < mu:
                    mu = nd + dist_f[v]
    return -1 if mu == INF else mu
