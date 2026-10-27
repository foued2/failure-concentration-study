def solve(n, edges, s, t):
    import heapq
    if s == t:
        return 0
    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for u, v, w in edges:
        forward[u].append((v, w))
        backward[v].append((u, w))

    def dijkstra(start, graph):
        inf = float("inf")
        dist = [inf] * n
        dist[start] = 0
        pq = [(0, start)]
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

    dist_from_s = dijkstra(s, forward)
    dist_to_t = dijkstra(t, backward)
    inf = float("inf")
    best = inf
    for i in range(n):
        if dist_from_s[i] != inf and dist_to_t[i] != inf:
            total = dist_from_s[i] + dist_to_t[i]
            if total < best:
                best = total
    return best if best != inf else -1
