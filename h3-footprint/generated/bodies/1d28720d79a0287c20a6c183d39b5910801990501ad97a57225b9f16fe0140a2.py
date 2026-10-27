def solve(n, edges, s, t):
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    heap = [(0, s)]

    while heap:
        d, u = heapq.heappop(heap)

        if d != dist[u]:
            continue

        if u == t:
            return d

        for a, b, w in edges:
            if a != u:
                continue

            nd = d + w
            if nd < dist[b]:
                dist[b] = nd
                heapq.heappush(heap, (nd, b))

    return -1
