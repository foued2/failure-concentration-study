def solve(n, edges, s, t):
    adj = defaultdict(list)
    for u, v, w in edges:
        if u != v:
            adj[u].append((v, w))
    dist = {s: 0}
    frontier = [(0, s)]
    while frontier:
        d, u = heapq.heappop(frontier)
        if d > dist.get(u, d):
            continue
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(frontier, (nd, v))
    return -1
