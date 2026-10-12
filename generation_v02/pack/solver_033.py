"""Submission 033 (base body 11, replica 2)."""

def solve(n, edges, s, t):
    from collections import deque
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    inq = [False] * n
    dist[s] = 0
    q = deque([s])
    inq[s] = True
    while q:
        u = q.popleft()
        inq[u] = False
        for v, w in g[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if not inq[v]:
                    q.append(v)
                    inq[v] = True
    return -1 if dist[t] == INF else dist[t]
