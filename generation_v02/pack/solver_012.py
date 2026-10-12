"""Submission 012 (base body 4, replica 2)."""

def solve(n, edges, s, t):
    import heapq
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    visited = [False] * n
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        for v, w in g[u]:
            if not visited[v] and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return -1 if dist[t] == float("inf") else dist[t]
