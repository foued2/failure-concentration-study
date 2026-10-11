"""Directive: DP over topological order."""


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    from collections import deque

    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    indeg_copy = indeg[:]
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in adj[u]:
            indeg_copy[v] -= 1
            if indeg_copy[v] == 0:
                q.append(v)
    if len(order) != n:
        return -1
    dist = [float("inf")] * n
    dist[s] = 0
    for u in order:
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist[t] if dist[t] != float("inf") else -1
