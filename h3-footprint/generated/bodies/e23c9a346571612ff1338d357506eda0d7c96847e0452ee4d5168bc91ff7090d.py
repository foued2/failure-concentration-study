def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    visited = [False] * n
    dist[s] = 0

    for _ in range(n):
        u = -1
        best = inf
        for i in range(n):
            if not visited[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        visited[u] = True
        if u == t:
            return best
        for v, w in graph[u]:
            nd = best + w
            if nd < dist[v]:
                dist[v] = nd

    return -1 if dist[t] == inf else dist[t]
