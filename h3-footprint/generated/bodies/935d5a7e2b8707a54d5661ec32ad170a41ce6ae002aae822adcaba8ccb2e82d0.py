def solve(n, edges, s, t):
    import heapq
    if s == t:
        return 0
    graph = {i: [] for i in range(n)}
    for u, v, w in edges:
        graph[u].append((v, w))
    best = {s: 0}
    queue = [(0, s)]
    done = set()
    while queue:
        cost, node = heapq.heappop(queue)
        if node in done:
            continue
        done.add(node)
        if node == t:
            return cost
        for nxt, weight in graph[node]:
            new_cost = cost + weight
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(queue, (new_cost, nxt))
    return -1
