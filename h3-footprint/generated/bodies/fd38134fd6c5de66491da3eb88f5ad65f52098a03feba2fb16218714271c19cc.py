def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    for lst in adj:
        lst.sort(key=lambda e: e[1])
    best = [None]
    sys.setrecursionlimit(max(1000, n + 1000))

    def dfs(u, d, onpath):
        if best[0] is not None and d >= best[0]:
            return
        if u == t:
            if best[0] is None or d < best[0]:
                best[0] = d
            return
        for v, w in adj[u]:
            if v not in onpath:
                onpath.add(v)
                dfs(v, d + w, onpath)
                onpath.discard(v)

    dfs(s, 0, {s})
    return best[0] if best[0] is not None else -1
