def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = None
    visited = [False] * n
    def dfs(u, total):
        nonlocal best
        if best is not None and total >= best:
            return
        if u == t:
            best = total
            return
        visited[u] = True
        for v, w in adj[u]:
            if not visited[v]:
                dfs(v, total + w)
        visited[u] = False
    sys.setrecursionlimit(10 ** 7)
    dfs(s, 0)
    return best if best is not None else -1
