def solve(n, edges, s, t):
    if s == t:
        return 0
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    settled = [False] * n
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if settled[u]:
            continue
        settled[u] = True
        if u == t:
            return d
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
