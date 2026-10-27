def solve(n, edges, s, t):
    edges_from = [[] for _ in range(n)]
    for u, v, w in edges:
        edges_from[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    heap = []
    heapq.heappush(heap, (0, s))
    while len(heap) > 0:
        d, u = heapq.heappop(heap)
        if d == dist[u]:
            for v, w in edges_from[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(heap, (d + w, v))
            if u == t:
                return int(d)
    if dist[t] == INF:
        return -1
    return int(dist[t])
