def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = None
    on_path = [False] * n

    def dfs(u, cost):
        nonlocal best
        if u == t:
            if best is None or cost < best:
                best = cost
            return
        if best is not None and cost >= best:
            return
        on_path[u] = True
        for v, w in adj[u]:
            if on_path[v]:
                continue
            nc = cost + w
            if best is None or nc < best:
                dfs(v, nc)
        on_path[u] = False

    dfs(s, 0)
    return best if best is not None else -1
