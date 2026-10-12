"""Submission 051 (base body 17, replica 2)."""

def solve(n, edges, s, t):
    from collections import deque
    g = [[] for _ in range(n)]
    for u, v, _ in edges:
        g[u].append(v)
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist[t]
