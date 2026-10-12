"""Submission 062 (base body 21, replica 1)."""

def solve(n, edges, s, t):
    from collections import deque
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    hops = [-1] * n
    hops[s] = 0
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v, w in g[u]:
            if hops[v] == -1:
                hops[v] = hops[u] + 1
                dist[v] = dist[u] + w
                q.append(v)
    return dist[t]
