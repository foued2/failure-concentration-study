def solve(n, edges, s, t):
    import heapq
    if s == t:
        return 0
    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for u, v, w in edges:
        forward[u].append((v, w))
        backward[v].append((u, w))

    INF = float("inf")

    def dijkstra(graph, source):
        dist = [INF] * n
        dist[source] = 0
        pq = [(0, source)]
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            for v, w in graph[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    from_s = dijkstra(forward, s)
    to_t = dijkstra(backward, t)
    best = INF
    for v in range(n):
        if from_s[v] != INF and to_t[v] != INF:
            candidate = from_s[v] + to_t[v]
            if candidate < best:
                best = candidate
    return best if best != INF else -1
