def solve(n, edges, s, t):
    import heapq

    INF = float("inf")
    forward = [[] for _ in range(n)]
    reverse = [[] for _ in range(n)]
    for u, v, w in edges:
        forward[u].append((v, w))
        reverse[v].append((u, w))

    h = [INF] * n
    h[t] = 0
    rq = [(0, t)]
    while rq:
        d, u = heapq.heappop(rq)
        if d > h[u]:
            continue
        for x, w in reverse[u]:
            nd = d + w
            if nd < h[x]:
                h[x] = nd
                heapq.heappush(rq, (nd, x))

    if h[s] == INF:
        return -1

    g = [INF] * n
    g[s] = 0
    open_list = [(h[s], s)]
    while open_list:
        f, u = heapq.heappop(open_list)
        if f > g[u] + h[u]:
            continue
        if u == t:
            return int(g[u])
        for v, w in forward[u]:
            if h[v] == INF:
                continue
            ng = g[u] + w
            if ng < g[v]:
                g[v] = ng
                heapq.heappush(open_list, (ng + h[v], v))
    return -1
