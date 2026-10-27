def solve(n, edges, s, t):
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
    dist = {s: 0}
    visited = set()
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        for v, w in g[u]:
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist.get(t, -1)
