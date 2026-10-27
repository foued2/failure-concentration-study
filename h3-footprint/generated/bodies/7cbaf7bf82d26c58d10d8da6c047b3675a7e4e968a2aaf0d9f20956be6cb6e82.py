def solve(n, edges, s, t):
    neighbors = {}
    for u, v, w in edges:
        neighbors.setdefault(u, []).append((v, w))
    best = {s: 0}
    frontier = [(0, s)]
    while frontier:
        cost, node = heapq.heappop(frontier)
        if node == t:
            return cost
        if cost > best.get(node, float('inf')):
            continue
        for nxt, wt in neighbors.get(node, []):
            total = cost + wt
            if total < best.get(nxt, float('inf')):
                best[nxt] = total
                heapq.heappush(frontier, (total, nxt))
    return -1
