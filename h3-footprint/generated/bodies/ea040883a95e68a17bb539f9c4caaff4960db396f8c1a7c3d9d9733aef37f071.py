def solve(n, edges, s, t):
    import heapq
    dist = [float("inf")] * n
    dist[s] = 0
    queue = [(0, s)]
    while queue:
        d, u = heapq.heappop(queue)
        if d > dist[u]:
            continue
        for a, v, w in edges:
            if a == u:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(queue, (nd, v))
    return -1 if dist[t] == float("inf") else int(dist[t])
