def solve(n, edges, s, t):
    import bisect
    if n <= 0:
        return -1
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    queue = [(0, s)]
    finished = [False] * n
    while queue:
        d, u = queue.pop(0)
        if finished[u] or d != dist[u]:
            continue
        finished[u] = True
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                bisect.insort(queue, (nd, v))
    return -1
