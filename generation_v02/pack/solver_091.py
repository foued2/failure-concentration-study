"""Submission 091 (base body 31, replica 0)."""

def solve(n, edges, s, t):
    import heapq
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    gs = {s: 0}
    pq = [(0, s)]
    closed = set()
    while pq:
        f, u = heapq.heappop(pq)
        if u in closed:
            continue
        closed.add(u)
        if u == t:
            return gs[u]
        for v, w in g[u]:
            ng = gs[u] + w
            if ng < gs.get(v, float("inf")):
                gs[v] = ng
                heapq.heappush(pq, (ng, v))
    return -1
