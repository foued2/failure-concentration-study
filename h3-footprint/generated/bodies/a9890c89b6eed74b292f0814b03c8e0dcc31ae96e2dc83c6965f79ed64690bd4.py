def solve(n, edges, s, t):
    import heapq
    reverse_graph = [[] for _ in range(n)]
    for u, v, w in edges:
        reverse_graph[v].append((u, w))
    inf = float("inf")
    dist = [inf] * n
    dist[t] = 0
    pq = [(0, t)]
    while pq:
        d, v = heapq.heappop(pq)
        if d != dist[v]:
            continue
        if v == s:
            return d
        for u, w in reverse_graph[v]:
            nd = d + w
            if nd < dist[u]:
                dist[u] = nd
                heapq.heappush(pq, (nd, u))
    return -1
