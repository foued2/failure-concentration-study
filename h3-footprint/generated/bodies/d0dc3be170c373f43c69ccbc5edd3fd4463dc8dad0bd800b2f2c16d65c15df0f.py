def solve(n, edges, s, t):
    nbrs = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            nbrs[u].append((v, w))
        else:
            nbrs[u].append((v, w))
    dist = [float('inf')] * n
    dist[s] = 0
    frontier = [(0, s)]
    while frontier:
        d, u = heappop(frontier)
        if d > dist[u]:
            continue
        if u == t:
            return int(d)
        for v, w in nbrs[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heappush(frontier, (nd, v))
    return -1
