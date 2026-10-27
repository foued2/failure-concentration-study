def solve(n, edges, s, t):
    import heapq

    graph = [[] for _ in range(n)]
    reverse = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
        reverse[v].append((u, w))

    inf = float("inf")
    dist_from_s = [inf] * n
    dist_to_t = [inf] * n
    dist_from_s[s] = 0
    dist_to_t[t] = 0
    heap_s = [(0, s)]
    heap_t = [(0, t)]
    done_s = [False] * n
    done_t = [False] * n
    answer = inf

    def settle(heap, dist, done):
        while heap:
            d, u = heapq.heappop(heap)
            if done[u] or d != dist[u]:
                continue
            done[u] = True
            return u, d
        return -1, inf

    while heap_s or heap_t:
        if heap_s:
            u, du = settle(heap_s, dist_from_s, done_s)
            if u != -1:
                if done_t[u]:
                    answer = min(answer, du + dist_to_t[u])
                for v, w in graph[u]:
                    nd = du + w
                    if nd < dist_from_s[v]:
                        dist_from_s[v] = nd
                        heapq.heappush(heap_s, (nd, v))

        if heap_t:
            u, du = settle(heap_t, dist_to_t, done_t)
            if u != -1:
                if done_s[u]:
                    answer = min(answer, du + dist_from_s[u])
                for v, w in reverse[u]:
                    nd = du + w
                    if nd < dist_to_t[v]:
                        dist_to_t[v] = nd
                        heapq.heappush(heap_t, (nd, v))

    return -1 if answer == inf else answer
