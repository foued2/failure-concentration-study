def solve(n, edges, s, t):
    min_w = {}
    for u, v, w in edges:
        key = (u, v)
        if key not in min_w or w < min_w[key]:
            min_w[key] = w
    adj = [[] for _ in range(n)]
    for (u, v), w in min_w.items():
        adj[u].append((v, w))
    dist = [float('inf')] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == t:
            return d
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
