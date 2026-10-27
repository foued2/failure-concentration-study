def solve(n, edges, s, t):
    import heapq

    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    reverse = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
        reverse[v].append((u, w))

    INF = float("inf")
    dist_s = [INF] * n
    dist_t = [INF] * n
    done_s = [False] * n
    done_t = [False] * n
    dist_s[s] = 0
    dist_t[t] = 0
    heap_s = [(0, s)]
    heap_t = [(0, t)]
    best = INF

    while heap_s and heap_t:
        while heap_s and heap_s[0][0] != dist_s[heap_s[0][1]]:
            heapq.heappop(heap_s)
        while heap_t and heap_t[0][0] != dist_t[heap_t[0][1]]:
            heapq.heappop(heap_t)
        if not heap_s or not heap_t:
            break
        if heap_s[0][0] + heap_t[0][0] >= best:
            break

        if heap_s[0][0] <= heap_t[0][0]:
            d, u = heapq.heappop(heap_s)
            if done_s[u]:
                continue
            done_s[u] = True
            if dist_t[u] < INF:
                if d + dist_t[u] < best:
                    best = d + dist_t[u]
            for v, w in graph[u]:
                nd = d + w
                if nd < dist_s[v]:
                    dist_s[v] = nd
                    heapq.heappush(heap_s, (nd, v))
        else:
            d, u = heapq.heappop(heap_t)
            if done_t[u]:
                continue
            done_t[u] = True
            if dist_s[u] < INF:
                if d + dist_s[u] < best:
                    best = d + dist_s[u]
            for v, w in reverse[u]:
                nd = d + w
                if nd < dist_t[v]:
                    dist_t[v] = nd
                    heapq.heappush(heap_t, (nd, v))

    return -1 if best == INF else best
