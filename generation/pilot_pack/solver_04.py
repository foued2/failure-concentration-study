"""Directive: BFS assuming unit weights."""
from collections import deque


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, _ in edges:
        adj[u].append(v)
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist[t]
