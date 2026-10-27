def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    heap = [(0, s)]

    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        if u == t:
            return d
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return -1 if dist[t] == INF else dist[t]
