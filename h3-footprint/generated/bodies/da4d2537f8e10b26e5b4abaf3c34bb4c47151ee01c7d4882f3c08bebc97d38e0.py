def solve(n, edges, s, t):
    import heapq

    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == t:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1 if dist[t] == INF else int(dist[t])
