def solve(n, edges, s, t):
    if s == t:
        return 0
    neighbors = {i: [] for i in range(n)}
    for (u, v, w) in edges:
        neighbors[u].append((v, w))
    best = {}
    pending = [(0, s)]
    while pending:
        cost, curr = heapq.heappop(pending)
        if curr in best:
            continue
        best[curr] = cost
        if curr == t:
            return cost
        for nxt, wt in neighbors[curr]:
            if nxt not in best:
                heapq.heappush(pending, (cost + wt, nxt))
    return -1
