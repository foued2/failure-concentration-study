def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = [float("inf")]
    onpath = [False] * n
    onpath[s] = True
    sys.setrecursionlimit(max(10000, n * 4))

    def walk(u, cost):
        for v, w in adj[u]:
            nd = cost + w
            if nd < best[0]:
                if v == t:
                    best[0] = nd
                elif not onpath[v]:
                    onpath[v] = True
                    walk(v, nd)
                    onpath[v] = False

    walk(s, 0)
    return best[0] if best[0] != float("inf") else -1
