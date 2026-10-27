def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [None] * n
    dist[s] = 0
    queue = [(0, s)]
    while queue:
        d, u = heapq.heappop(queue)
        if d > dist[u]:
            continue
        if u == t:
            return d
        for v, w in graph[u]:
            nd = d + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(queue, (nd, v))
    return -1
