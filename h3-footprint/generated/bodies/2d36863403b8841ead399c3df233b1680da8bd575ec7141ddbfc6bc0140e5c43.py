def solve(n, edges, s, t):
    import heapq
    if s == t:
        return 0
    adjacency = {i: [] for i in range(n)}
    for u, v, w in edges:
        adjacency[u].append((v, w))
    best = {s: 0}
    heap = [(0, s)]
    closed = set()
    while heap:
        cost, u = heapq.heappop(heap)
        if u in closed:
            continue
        closed.add(u)
        if u == t:
            return cost
        for v, w in adjacency[u]:
            candidate = cost + w
            if v not in closed and candidate < best.get(v, float("inf")):
                best[v] = candidate
                heapq.heappush(heap, (candidate, v))
    return -1
