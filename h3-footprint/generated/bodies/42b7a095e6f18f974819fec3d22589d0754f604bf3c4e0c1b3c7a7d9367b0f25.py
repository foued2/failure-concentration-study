def solve(n, edges, s, t):
    adj = {}
    in_deg_from_s = 0
    for u, v, w in edges:
        if u not in adj:
            adj[u] = []
        adj[u].append((v, w))
    if s == t:
        return 0
    INF = float("inf")
    d = [INF] * n
    d[s] = 0
    h = [(0, s)]
    settled = set()
    while len(h) > 0:
        du, u = heapq.heappop(h)
        if u in settled or du > d[u]:
            continue
        settled.add(u)
        for (v, w) in adj.get(u, []):
            cand = du + w
            if cand < d[v]:
                d[v] = cand
                heapq.heappush(h, (cand, v))
    if t not in adj and d[t] == INF:
        return -1
    return d[t] if d[t] != INF else -1
