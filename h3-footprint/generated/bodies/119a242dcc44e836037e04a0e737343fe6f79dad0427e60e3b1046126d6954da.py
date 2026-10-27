def solve(n, edges, s, t):
    import heapq
    if n <= 0:
        return -1
    if s == t:
        return 0
    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for a, b, w in edges:
        forward[a].append((b, w))
        backward[b].append((a, w))
    INF = float("inf")
    dist_f = [INF] * n
    dist_b = [INF] * n
    dist_f[s] = 0
    dist_b[t] = 0
    heap_f = [(0, s)]
    heap_b = [(0, t)]
    settled_f = [False] * n
    settled_b = [False] * n
    answer = INF
    while heap_f and heap_b:
        if heap_f[0][0] >= answer or heap_b[0][0] >= answer:
            break
        if heap_f[0][0] <= heap_b[0][0]:
            d, u = heapq.heappop(heap_f)
            if settled_f[u] or d != dist_f[u]:
                continue
            settled_f[u] = True
            if u == t:
                return d
            if settled_b[u]:
                candidate = d + dist_b[u]
                if candidate < answer:
                    answer = candidate
            for v, w in forward[u]:
                nd = d + w
                if nd < dist_f[v]:
                    dist_f[v] = nd
                    heapq.heappush(heap_f, (nd, v))
        else:
            d, u = heapq.heappop(heap_b)
            if settled_b[u] or d != dist_b[u]:
                continue
            settled_b[u] = True
            if u == s:
                return d
            if settled_f[u]:
                candidate = d + dist_f[u]
                if candidate < answer:
                    answer = candidate
            for v, w in backward[u]:
                nd = d + w
                if nd < dist_b[v]:
                    dist_b[v] = nd
                    heapq.heappush(heap_b, (nd, v))
    return answer if answer != INF else -1
