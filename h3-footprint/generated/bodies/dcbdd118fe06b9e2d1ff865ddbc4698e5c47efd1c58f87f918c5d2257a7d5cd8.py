def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [None] * n
    dist[s] = 0
    settled = [False] * n
    for _ in range(n):
        u = -1
        best = None
        for i in range(n):
            if not settled[i] and dist[i] is not None and (best is None or dist[i] < best):
                best = dist[i]
                u = i
        if u == -1:
            break
        settled[u] = True
        if u == t:
            return best
        for v, w in g[u]:
            nd = best + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
    return -1
