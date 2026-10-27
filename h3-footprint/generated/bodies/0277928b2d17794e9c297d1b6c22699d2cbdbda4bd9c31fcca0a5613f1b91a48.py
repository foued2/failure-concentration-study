def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [None] * n
    dist[s] = 0
    used = [False] * n
    for _ in range(n):
        u = -1
        best = None
        for i in range(n):
            if not used[i] and dist[i] is not None:
                if best is None or dist[i] < best:
                    best = dist[i]
                    u = i
        if u == -1:
            break
        used[u] = True
        if u == t:
            break
        for v, w in graph[u]:
            nd = best + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
    return -1 if dist[t] is None else dist[t]
