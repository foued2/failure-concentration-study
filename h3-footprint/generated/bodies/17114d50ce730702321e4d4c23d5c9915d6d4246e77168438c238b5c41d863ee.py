def solve(n, edges, s, t):
    graph = [dict() for _ in range(n)]
    for u, v, w in edges:
        if v not in graph[u] or w < graph[u][v]:
            graph[u][v] = w
    INF = float('inf')
    dist = [INF] * n
    done = [False] * n
    dist[s] = 0
    while True:
        u = -1
        best = INF
        for i in range(n):
            if not done[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        done[u] = True
        for v, w in graph[u].items():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist[t] if dist[t] != INF else -1
