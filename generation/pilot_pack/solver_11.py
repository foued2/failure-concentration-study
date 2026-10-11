"""Directive: BFS counting edge weight as hop count."""
from collections import deque


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                q.append(v)
    return dist[t]
