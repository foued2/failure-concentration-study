def solve(n, edges, s, t):
    import bisect
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    queue = [(0, s)]
    settled = [False] * n
    while queue:
        d, u = queue.pop(0)
        if settled[u]:
            continue
        settled[u] = True
        if u == t:
            return int(d)
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                bisect.insort(queue, (nd, v))
    return -1
