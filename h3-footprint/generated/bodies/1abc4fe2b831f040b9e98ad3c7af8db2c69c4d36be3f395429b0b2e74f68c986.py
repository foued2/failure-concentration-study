def solve(n, edges, s, t):
    if s == t:
        return 0
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            graph[u].append((v, w))
        else:
            continue
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if u == t:
            return d
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return -1
