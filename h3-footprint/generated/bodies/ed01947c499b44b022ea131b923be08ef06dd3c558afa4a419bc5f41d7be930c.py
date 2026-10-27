def solve(n, edges, s, t):
    graph = defaultdict(dict)
    for u, v, w in edges:
        if v not in graph[u] or w < graph[u][v]:
            graph[u][v] = w
    dist = {}
    heap = [(0, s)]
    while heap:
        d, node = heapq.heappop(heap)
        if node in dist:
            continue
        dist[node] = d
        for nb, w in graph[node].items():
            if nb not in dist:
                heapq.heappush(heap, (d + w, nb))
    return dist.get(t, -1)
