"""Submission 099 (base body 33, replica 2)."""

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
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
                if v == t:
                    return nd  # natural defect: exit on first sight, not pop
    return -1
