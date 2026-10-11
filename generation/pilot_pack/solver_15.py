"""Directive: SPFA / queue-based relaxation."""
from collections import deque


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    inq = [False] * n
    dist[s] = 0
    q = deque([s])
    inq[s] = True
    while q:
        u = q.popleft()
        inq[u] = False
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if not inq[v]:
                    q.append(v)
                    inq[v] = True
    return dist[t] if dist[t] != INF else -1
