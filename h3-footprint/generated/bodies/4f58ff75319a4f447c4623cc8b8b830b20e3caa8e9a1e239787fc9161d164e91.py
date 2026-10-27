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

    from_s = distances(s, forward)
    to_t = distances(t, backward)

    answer = inf
    for i in range(n):
        if from_s[i] != inf and to_t[i] != inf:
            candidate = from_s[i] + to_t[i]
            if candidate < answer:
                answer = candidate

    return answer if answer != inf else -1
