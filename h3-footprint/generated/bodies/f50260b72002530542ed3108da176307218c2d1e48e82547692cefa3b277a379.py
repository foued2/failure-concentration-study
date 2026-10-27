def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = [float('inf')]
    seen = [False] * n
    seen[s] = True

    def dfs(u, acc):
        if u == t:
            if acc < best[0]:
                best[0] = acc
            return
        for v, w in adj[u]:
            if not seen[v]:
                seen[v] = True
                dfs(v, acc + w)
                seen[v] = False

    dfs(s, 0)
    return -1 if best[0] == float('inf') else int(best[0])
