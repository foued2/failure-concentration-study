"""Submission 067 (base body 23, replica 0)."""

def solve(n, edges, s, t):
    from collections import deque
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        g[u].append((v, w))
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    indeg2 = indeg[:]
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in g[u]:
            indeg2[v] -= 1
            if indeg2[v] == 0:
                q.append(v)
    if len(order) != n:
        return -1
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for u in order:
        for v, w in g[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == INF else dist[t]
