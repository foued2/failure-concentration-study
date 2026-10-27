def solve(n, edges, s, t):
    adj = {node: [] for node in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))

    best = {node: float("inf") for node in range(n)}
    best[s] = 0
    queue = [(0, s)]

    while queue:
        d, u = heapq.heappop(queue)
        if d > best[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < best[v]:
                best[v] = nd
                heapq.heappush(queue, (nd, v))

    return -1 if best[t] == float("inf") else best[t]
