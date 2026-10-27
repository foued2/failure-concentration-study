def solve(n, edges, s, t):
    inf = float("inf")
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = {s: 0}
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, inf):
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist.get(v, inf):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    if t in dist:
        return dist[t]
    return -1
