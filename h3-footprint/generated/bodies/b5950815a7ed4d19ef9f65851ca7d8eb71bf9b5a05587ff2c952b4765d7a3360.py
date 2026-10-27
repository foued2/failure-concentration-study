def solve(n, edges, s, t):
    g = defaultdict(list)
    for a, b, c in edges:
        g[a].append((b, c))
    INF = float("inf")
    best = [INF] * n
    best[s] = 0
    frontier = [(0, s)]
    seen = set()
    while frontier:
        cost, node = heapq.heappop(frontier)
        if node == t:
            return int(cost)
        if node in seen:
            continue
        seen.add(node)
        for nxt, wt in g[node]:
            if cost + wt < best[nxt]:
                best[nxt] = cost + wt
                heapq.heappush(frontier, (best[nxt], nxt))
    return -1
