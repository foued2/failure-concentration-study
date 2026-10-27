def solve(n, edges, s, t):
    if n <= 0:
        return -1
    if s == t:
        return 0
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    for _ in range(n - 1):
        nxt = dist[:]
        for u in range(n):
            if dist[u] == inf:
                continue
            for v, w in graph[u]:
                nd = dist[u] + w
                if nd < nxt[v]:
                    nxt[v] = nd
        dist = nxt
    return -1 if dist[t] == inf else dist[t]
