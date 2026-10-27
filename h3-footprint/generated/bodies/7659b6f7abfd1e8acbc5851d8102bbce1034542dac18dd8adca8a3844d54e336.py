def solve(n, edges, s, t):
    from heapq import heappush, heappop
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((w, v))
    seen = [False] * n
    best = [None] * n
    heap = [(0, s)]
    while heap:
        d, u = heappop(heap)
        if seen[u]:
            continue
        seen[u] = True
        best[u] = d
        if u == t:
            return d
        for w, v in adj[u]:
            if not seen[v]:
                heappush(heap, (d + w, v))
    return -1
