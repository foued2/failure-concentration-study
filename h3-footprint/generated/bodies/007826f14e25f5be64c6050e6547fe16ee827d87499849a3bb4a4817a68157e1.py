def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    fixed = [False] * n
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not fixed[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        fixed[u] = True
        if u == t:
            break
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == INF else dist[t]
