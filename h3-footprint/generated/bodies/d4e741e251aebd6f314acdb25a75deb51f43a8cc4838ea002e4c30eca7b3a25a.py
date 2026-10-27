def solve(n, edges, s, t):
    from collections import deque
    if n <= 0:
        return -1
    if s == t:
        return 0
    out = [[] for _ in range(n)]
    for u, v, w in edges:
        out[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    queued = [False] * n
    dist[s] = 0
    q = deque([s])
    queued[s] = True
    while q:
        u = q.popleft()
        queued[u] = False
        base = dist[u]
        for v, w in out[u]:
            cand = base + w
            if cand < dist[v]:
                dist[v] = cand
                if not queued[v]:
                    queued[v] = True
                    q.append(v)
    return dist[t] if dist[t] != INF else -1
