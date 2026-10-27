def solve(n, edges, s, t):
    from collections import deque
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    queued = [False] * n
    queued[s] = True
    q = deque([s])
    while q:
        u = q.popleft()
        queued[u] = False
        base = dist[u]
        for v, w in adj[u]:
            nd = base + w
            if nd < dist[v]:
                dist[v] = nd
                if not queued[v]:
                    queued[v] = True
                    q.append(v)
    return -1 if dist[t] == inf else int(dist[t])
