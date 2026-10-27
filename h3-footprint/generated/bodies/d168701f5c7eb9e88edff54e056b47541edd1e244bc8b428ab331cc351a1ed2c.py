def solve(n, edges, s, t):
    import heapq
    fadj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    for u, v, w in edges:
        fadj[u].append((v, w))
        radj[v].append((u, w))
    INF = float('inf')
    fd = [INF] * n
    rd = [INF] * n
    fd[s] = 0
    rd[t] = 0
    fpq = [(0, s)]
    rpq = [(0, t)]
    best = INF
    while fpq or rpq:
        if fpq:
            d, u = heapq.heappop(fpq)
            if d == fd[u]:
                for v, w in fadj[u]:
                    if fd[u] + w < fd[v]:
                        fd[v] = fd[u] + w
                        heapq.heappush(fpq, (fd[v], v))
                        if rd[v] < INF:
                            cand = fd[v] + rd[v]
                            if cand < best:
                                best = cand
        if rpq:
            d, u = heapq.heappop(rpq)
            if d == rd[u]:
                for v, w in radj[u]:
                    if rd[u] + w < rd[v]:
                        rd[v] = rd[u] + w
                        heapq.heappush(rpq, (rd[v], v))
                        if fd[v] < INF:
                            cand = fd[v] + rd[v]
                            if cand < best:
                                best = cand
    return -1 if best == INF else best
