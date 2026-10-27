def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((w, v))
    reached = set()
    best = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in reached:
            continue
        reached.add(u)
        if u == t:
            return d
        for w, v in adj.get(u, ()):
            if v not in reached:
                nd = d + w
                if nd < best.get(v, float("inf")):
                    best[v] = nd
                    heapq.heappush(pq, (nd, v))
    return -1
