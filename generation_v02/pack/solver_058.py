"""Submission 058 (base body 20, replica 0)."""

def solve(n, edges, s, t):
    # natural defect: treats weights as hop counts (sums weights on BFS tree)
    from collections import deque
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v, w in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                q.append(v)
    return dist[t]
