def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    def dij(start, rev):
        d = [INF] * n
        d[start] = 0
        pq = [(0, start)]
        while pq:
            du, u = heapq.heappop(pq)
            if du != d[u]:
                continue
            for v, w in adj[u]:
                if not rev:
                    if du + w < d[v]:
                        d[v] = du + w
                        heapq.heappush(pq, (d[v], v))
                else:
                    if du + w < d[v]:
                        d[v] = du + w
                        heapq.heappush(pq, (d[v], v))
        return d
    dist = [INF] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == t:
            break
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return -1 if dist[t] == INF else dist[t]
