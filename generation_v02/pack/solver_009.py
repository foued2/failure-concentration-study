"""Submission 009 (base body 3, replica 2)."""

def solve(n, edges, s, t):
    import heapq
    g = {}
    for u, v, w in edges:
        g.setdefault(u, []).append((v, w))
    best = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == t:
            return d
        for v, w in g.get(u, []):
            nd = d + w
            if nd < best.get(v, 10**18):
                best[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1 if t not in best else best[t]
