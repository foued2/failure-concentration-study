def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [None] * n
    pq = [(0, s)]
    dist = {s: 0}
    while pq:
        d, u = heapq.heappop(pq)
        if u == t:
            return d
        if d > dist.get(u, float('inf')):
            continue
        for v, w in adj[u]:
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
