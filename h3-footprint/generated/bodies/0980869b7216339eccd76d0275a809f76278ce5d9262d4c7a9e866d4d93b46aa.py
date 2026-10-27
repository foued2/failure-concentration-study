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
    from_s = [inf] * n
    from_t = [inf] * n
    from_s[s] = 0
    from_t[t] = 0

    heap_s = [(0, s)]
    heap_t = [(0, t)]
    answer = inf

    while heap_s and heap_t:
        if heap_s[0][0] + heap_t[0][0] >= answer:
            break

        if heap_s[0][0] <= heap_t[0][0]:
            d, u = heapq.heappop(heap_s)
            if d != from_s[u]:
                continue

            if from_t[u] != inf:
                answer = min(answer, d + from_t[u])

            for v, w in forward[u]:
                nd = d + w
                if nd < from_s[v]:
                    from_s[v] = nd
                    heapq.heappush(heap_s, (nd, v))
                    if from_t[v] != inf:
                        answer = min(answer, nd + from_t[v])
        else:
            d, u = heapq.heappop(heap_t)
            if d != from_t[u]:
                continue

            if from_s[u] != inf:
                answer = min(answer, d + from_s[u])

            for v, w in backward[u]:
                nd = d + w
                if nd < from_t[v]:
                    from_t[v] = nd
                    heapq.heappush(heap_t, (nd, v))
                    if from_s[v] != inf:
                        answer = min(answer, nd + from_s[v])

    return -1 if answer == inf else int(answer)
