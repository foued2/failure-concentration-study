def solve(n, edges, s, t):
    import bisect

    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    inf = float("inf")
    best = [inf] * n
    best[s] = 0
    queue = [(0, s)]
    while queue:
        d, u = queue.pop(0)
        if d != best[u]:
            continue
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < best[v]:
                best[v] = nd
                bisect.insort(queue, (nd, v))
    return -1
