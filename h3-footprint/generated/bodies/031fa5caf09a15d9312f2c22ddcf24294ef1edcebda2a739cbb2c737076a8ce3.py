def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = [float('inf')] * n
    best[s] = 0
    found = [False]
    result = [None]

    def dfs(u, acc):
        if acc >= best[u]:
            return
        best[u] = acc
        if u == t:
            found[0] = True
            result[0] = acc
            return
        for v, w in adj[u]:
            dfs(v, acc + w)
            if found[0]:
                return

    dfs(s, 0)
    return result[0] if found[0] else -1
