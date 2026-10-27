def solve(n, edges, s, t):
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((w, v))
    dist = {}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in dist:
            continue
        dist[u] = d
        for w, v in adj[u]:
            if v not in dist:
                heapq.heappush(pq, (d + w, v))
    return dist.get(t, -1)
