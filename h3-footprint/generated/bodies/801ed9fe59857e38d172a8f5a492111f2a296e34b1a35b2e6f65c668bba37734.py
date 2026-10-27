def solve(n, edges, s, t):
    graph = {}
    for u, v, w in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
    heap = [(0, s)]
    seen = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u == t:
            return d
        if u in seen:
            continue
        seen.add(u)
        for v, w in graph.get(u, []):
            if v not in seen:
                heapq.heappush(heap, (d + w, v))
    return -1
