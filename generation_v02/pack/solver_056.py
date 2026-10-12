"""Submission 056 (base body 19, replica 1)."""

def solve(n, edges, s, t):
    from collections import deque
    g = {}
    for u, v, _ in edges:
        g.setdefault(u, []).append(v)
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in g.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist.get(t, -1)
