def solve(n, edges, s, t):
    out = {i: [] for i in range(n)}
    for u, v, w in edges:
        out[u].append((w, v))
    best = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        for w, v in out[u]:
            nd = d + w
            if v not in best or nd < best[v]:
                best[v] = nd
                heapq.heappush(pq, (nd, v))
    return best.get(t, -1)
