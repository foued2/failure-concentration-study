def solve(n, edges, s, t):
    from heapq import heappush, heappop
    if n <= 0:
        return -1
    if s == t:
        return 0
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    best = [float("inf")] * n
    best[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heappop(heap)
        if d != best[u]:
            continue
        if u == t:
            return d
        for v, w in graph[u]:
            nd = d + w
            if nd < best[v]:
                best[v] = nd
                heappush(heap, (nd, v))
    return -1
