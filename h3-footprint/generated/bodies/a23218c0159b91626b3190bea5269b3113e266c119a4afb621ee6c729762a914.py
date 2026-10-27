def solve(n, edges, s, t):
    import heapq
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    def heuristic(node):
        return 0

    g_score = [None] * n
    g_score[s] = 0
    frontier = [(heuristic(s), 0, s)]
    closed = [False] * n
    while frontier:
        _, g, u = heapq.heappop(frontier)
        if closed[u]:
            continue
        closed[u] = True
        if u == t:
            return g
        for v, w in graph[u]:
            tentative = g + w
            if g_score[v] is None or tentative < g_score[v]:
                g_score[v] = tentative
                heapq.heappush(frontier, (tentative + heuristic(v), tentative, v))
    return -1
