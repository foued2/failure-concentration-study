def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    seen = set()
    for u, v, w in edges:
        if u not in seen:
            g[u] = []
            seen.add(u)
        g[u].append((v, w))
    heap = []
    dist = {}
    dist[s] = 0
    heap.append((0, s))
    heapq.heapify(heap)
    visited = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if u == t:
            return d
        for v, w in g.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return -1
