def solve(n, edges, s, t):
    import heapq
    if n <= 0:
        return -1
    if s == t:
        return 0
    links = [[] for _ in range(n)]
    for u, v, w in edges:
        links[u].append((v, w))
    INF = float("inf")
    g = [INF] * n
    g[s] = 0
    closed = [False] * n
    frontier = [(0, s)]
    while frontier:
        f, node = heapq.heappop(frontier)
        if closed[node]:
            continue
        if node == t:
            return g[node]
        closed[node] = True
        for nxt, cost in links[node]:
            tentative = g[node] + cost
            if tentative < g[nxt]:
                g[nxt] = tentative
                heapq.heappush(frontier, (tentative, nxt))
    return -1
