def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    for a in adj:
        a.sort(key=lambda p: p[1])
    best = [-1]
    on_path = [False] * n
    on_path[s] = True

    def dfs(u, cost):
        for v, w in adj[u]:
            nc = cost + w
            if best[0] != -1 and nc >= best[0]:
                continue
            if v == t:
                best[0] = nc
                continue
            if on_path[v]:
                continue
            on_path[v] = True
            dfs(v, nc)
            on_path[v] = False

    dfs(s, 0)
    return best[0]
