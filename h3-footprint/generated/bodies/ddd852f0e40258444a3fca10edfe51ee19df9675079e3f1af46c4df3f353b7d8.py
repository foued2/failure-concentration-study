def solve(n, edges, s, t):
    if n <= 0:
        return -1
    if s == t:
        return 0
    import heapq
    reverse = [[] for _ in range(n)]
    for u, v, w in edges:
        reverse[v].append((u, w))
    inf = float("inf")
    dist = [inf] * n
    dist[t] = 0
    heap = [(0, t)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        if u == s:
            return d
        for v, w in reverse[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return -1 if dist[s] == inf else dist[s]
