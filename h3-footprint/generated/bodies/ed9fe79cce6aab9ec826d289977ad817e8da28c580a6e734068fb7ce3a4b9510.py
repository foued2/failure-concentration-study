def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [None] * n
    dist[s] = 0
    pq = [(0, s)]
    seen = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if v not in seen and (dist[v] is None or nd < dist[v]):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
