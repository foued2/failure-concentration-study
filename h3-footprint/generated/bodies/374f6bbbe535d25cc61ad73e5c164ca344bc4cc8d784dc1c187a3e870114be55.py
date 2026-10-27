def solve(n, edges, s, t):
    import heapq
    neighbours = [dict() for _ in range(n)]
    for u, v, w in edges:
        if v != u and (v not in neighbours[u] or w < neighbours[u][v]):
            neighbours[u][v] = w
    dist = {s: 0}
    frontier = [(0, s)]
    while frontier:
        _, node = heapq.heappop(frontier)
        if node == t:
            return dist[node]
        for nxt, wt in neighbours[node].items():
            cand = dist[node] + wt
            if cand < dist.get(nxt, cand + 1):
                dist[nxt] = cand
                heapq.heappush(frontier, (cand, nxt))
    return -1
