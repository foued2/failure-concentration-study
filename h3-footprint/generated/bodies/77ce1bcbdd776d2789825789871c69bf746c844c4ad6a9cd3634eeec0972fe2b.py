def solve(n, edges, s, t):
    out = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            out[u].append((v, w))
    infinity = 10 ** 18
    d = [infinity] * n
    d[s] = 0
    h = [(0, s)]
    while h:
        du, u = heapq.heappop(h)
        if du != d[u]:
            continue
        if u == t:
            return du
        for v, w in out[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(h, (d[v], v))
    return -1
