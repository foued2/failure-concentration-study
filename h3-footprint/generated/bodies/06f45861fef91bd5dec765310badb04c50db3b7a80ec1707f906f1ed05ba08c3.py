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
    dist_f = [inf] * n
    dist_b = [inf] * n
    dist_f[s] = 0
    dist_b[t] = 0

    heap_f = [(0, s)]
    heap_b = [(0, t)]
    done_f = [False] * n
    done_b = [False] * n
    best = inf

    while heap_f and heap_b:
        while heap_f and (done_f[heap_f[0][1]] or heap_f[0][0] != dist_f[heap_f[0][1]]):
            heapq.heappop(heap_f)

        while heap_b and (done_b[heap_b[0][1]] or heap_b[0][0] != dist_b[heap_b[0][1]]):
            heapq.heappop(heap_b)

        if not heap_f or not heap_b:
            break

        if heap_f[0][0] + heap_b[0][0] >= best:
            break

        if heap_f[0][0] <= heap_b[0][0]:
            d, u = heapq.heappop(heap_f)
            if done_f[u] or d != dist_f[u]:
                continue

            done_f[u] = True

            if dist_b[u] != inf:
                candidate = d + dist_b[u]
                if candidate < best:
                    best = candidate

            for v, w in forward[u]:
                nd = d + w
                if nd < dist_f[v]:
                    dist_f[v] = nd
                    heapq.heappush(heap_f, (nd, v))
        else:
            d, u = heapq.heappop(heap_b)
            if done_b[u] or d != dist_b[u]:
                continue

            done_b[u] = True

            if dist_f[u] != inf:
                candidate = dist_f[u] + d
                if candidate < best:
                    best = candidate

            for v, w in backward[u]:
                nd = d + w
                if nd < dist_b[v]:
                    dist_b[v] = nd
                    heapq.heappush(heap_b, (nd, v))

    for i in range(n):
        if dist_f[i] != inf and dist_b[i] != inf:
            candidate = dist_f[i] + dist_b[i]
            if candidate < best:
                best = candidate

    return best if best != inf else -1
