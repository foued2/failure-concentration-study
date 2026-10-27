def solve(n, edges, s, t):
    import heapq
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    heap = [(0, s)]
    done = [False] * n
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        if u == t:
            return int(d)
        for a, b, w in edges:
            if a == u:
                nd = d + w
                if nd < dist[b]:
                    dist[b] = nd
                    heapq.heappush(heap, (nd, b))
    return -1
