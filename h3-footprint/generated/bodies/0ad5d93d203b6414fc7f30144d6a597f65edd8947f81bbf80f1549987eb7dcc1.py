def solve(n, edges, s, t):
    import bisect

    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    pq = [(0, s)]

    while pq:
        d, u = pq.pop(0)
        if d != dist[u]:
            continue
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                bisect.insort(pq, (nd, v))

    return -1
