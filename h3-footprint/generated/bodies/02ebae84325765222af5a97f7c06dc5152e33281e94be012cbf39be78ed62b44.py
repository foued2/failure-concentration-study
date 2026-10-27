def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    best = [float("inf")]
    onpath = [False] * n

    def dfs(u, cost):
        if cost >= best[0]:
            return
        if u == t:
            best[0] = cost
            return
        for v, w in adj[u]:
            if not onpath[v]:
                onpath[v] = True
                dfs(v, cost + w)
                onpath[v] = False

    onpath[s] = True
    dfs(s, 0)
    return -1 if best[0] == float("inf") else best[0]
