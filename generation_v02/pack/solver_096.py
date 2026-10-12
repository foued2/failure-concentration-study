"""Submission 096 (base body 32, replica 2)."""

def solve(n, edges, s, t):
    import heapq
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    gsc = {s: 0}
    pq = [(0, 0, s)]
    while pq:
        _, cost, u = heapq.heappop(pq)
        if cost > gsc.get(u, float("inf")):
            continue
        if u == t:
            return cost
        for v, w in g[u]:
            ng = cost + w
            if ng < gsc.get(v, float("inf")):
                gsc[v] = ng
                heapq.heappush(pq, (ng, ng, v))
    return -1
