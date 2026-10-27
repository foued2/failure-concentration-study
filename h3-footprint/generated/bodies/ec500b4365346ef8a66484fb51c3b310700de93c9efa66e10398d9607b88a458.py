def solve(n, edges, s, t):
    import heapq
    if s == t:
        return 0
    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for u, v, w in edges:
        forward[u].append((v, w))
        backward[v].append((u, w))
    inf = float("inf")

    def distances(start, graph):
        best = [inf] * n
        best[start] = 0
        heap = [(0, start)]
        while heap:
            d, u = heapq.heappop(heap)
            if d != best[u]:
                continue
            for v, w in graph[u]:
                nd = d + w
                if nd < best[v]:
                    best[v] = nd
                    heapq.heappush(heap, (nd, v))
        return best

    from_s = distances(s, forward)
    to_t = distances(t, backward)
    answer = inf
    for v in range(n):
        if from_s[v] != inf and to_t[v] != inf:
            total = from_s[v] + to_t[v]
            if total < answer:
                answer = total
    return -1 if answer == inf else int(answer)
