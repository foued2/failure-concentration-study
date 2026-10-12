"""Submission 014 (base body 5, replica 1)."""

def solve(n, edges, s, t):
    import heapq
    if s == t:
        return 0
    g = [[] for _ in range(n)]
    for e in edges:
        u, v, w = e[0], e[1], e[2]
        g[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist[t] if dist[t] != float("inf") else -1
