def solve(n, edges, s, t):
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((w, v))
    best = {}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in best:
            continue
        best[u] = d
        if u == t:
            return d
        for w, v in adj[u]:
            if v not in best:
                heapq.heappush(pq, (d + w, v))
    return -1
