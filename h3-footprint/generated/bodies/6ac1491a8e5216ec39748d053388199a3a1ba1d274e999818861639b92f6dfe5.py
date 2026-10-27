def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    stack = [s]
    on_stack = [False] * n
    on_stack[s] = True
    while stack:
        u = stack.pop()
        on_stack[u] = False
        du = dist[u]
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not on_stack[v]:
                    stack.append(v)
                    on_stack[v] = True
    return -1 if dist[t] == INF else int(dist[t])
