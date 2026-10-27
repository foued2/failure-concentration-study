def solve(n, edges, start, goal):
    if start == goal:
        return 0
    neighbors = {}
    for u, v, w in edges:
        if u not in neighbors:
            neighbors[u] = []
        neighbors[u].append((w, v))
    dist = {start: 0}
    queue = [(0, start)]
    while len(queue) > 0:
        (_, cur) = heapq.heappop(queue)
        for (w, nxt) in neighbors.get(cur, []):
            nd = dist[cur] + w
            if nxt not in dist or nd < dist[nxt]:
                dist[nxt] = nd
                heapq.heappush(queue, (nd, nxt))
    return dist.get(goal, -1)
