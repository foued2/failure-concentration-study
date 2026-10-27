def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    heap = [(0, s, 0)]
    steps = 0
    while heap:
        d, u, _ = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == t:
            return d
        steps += 1
        if steps > 4 * (n + len(edges) + 1):
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v, steps))
    return -1 if dist[t] == INF else dist[t]
