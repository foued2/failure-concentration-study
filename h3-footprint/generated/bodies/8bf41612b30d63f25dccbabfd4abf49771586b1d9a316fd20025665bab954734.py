def solve(n, edges, s, t):
    radj = [[] for _ in range(n)]
    for u, v, w in edges:
        radj[v].append((u, w))
    INF = float('inf')
    dist = [INF] * n
    dist[t] = 0
    heap = [(0, t)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == s:
            break
        for v, w in radj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist[s] if dist[s] < INF else -1
