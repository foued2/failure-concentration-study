def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    stack = [s]
    while stack:
        u = stack.pop()
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                stack.append(v)
    return -1 if dist[t] == INF else dist[t]
