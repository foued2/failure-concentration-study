"""Submission 070 (base body 24, replica 0)."""

def solve(n, edges, s, t):
    # natural defect: returns -1 on any cycle (not just unreachable t)
    from collections import deque
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        g[u].append((v, w))
        indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    ind = indeg[:]
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in g[u]:
            ind[v] -= 1
            if ind[v] == 0:
                q.append(v)
    if len(order) != n:
        return -1
    dist = [10**18] * n
    dist[s] = 0
    for u in order:
        for v, w in g[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == 10**18 else dist[t]
