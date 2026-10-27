def solve(n, edges, s, t):
    neighbors = defaultdict(list)
    for u, v, w in edges:
        neighbors[u].append((v, w))
    dist = {}
    frontier = [(0, s)]
    while frontier:
        d, u = heapq.heappop(frontier)
        if u == t:
            return d
        if u in dist and dist[u] < d:
            continue
        dist[u] = d
        for v, w in neighbors[u]:
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(frontier, (nd, v))
    return -1
