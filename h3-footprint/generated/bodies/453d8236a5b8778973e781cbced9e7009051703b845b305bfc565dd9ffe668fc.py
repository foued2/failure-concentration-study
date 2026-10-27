def solve(n, edges, s, t):
    if s == t:
        return 0

    import heapq

    reverse_graph = [[] for _ in range(n)]
    for u, v, w in edges:
        reverse_graph[v].append((u, w))

    INF = float("inf")
    dist = [INF] * n
    dist[t] = 0
    heap = [(0, t)]

    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        if u == s:
            return d

        for v, w in reverse_graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return -1
