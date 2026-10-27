def solve(n, edges, s, t):
    if s == t:
        return 0
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
    frontier = {s: 0}
    best = defaultdict(lambda: float('inf'))
    best[s] = 0
    while frontier:
        u, d = min(frontier.items(), key=lambda kv: kv[1])
        del frontier[u]
        for v, w in g[u]:
            nd = d + w
            if nd < best[v]:
                best[v] = nd
                frontier[v] = nd
        if u == t:
            return d
    return -1
