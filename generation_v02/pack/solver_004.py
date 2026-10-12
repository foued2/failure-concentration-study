"""Submission 004 (base body 2, replica 0)."""

def solve(n, edges, s, t):
    import heapq
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == t:
            return d
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
