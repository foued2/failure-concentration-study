def solve(n, edges, s, t):
    adj = [[ ] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = pq.pop(0)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                bisect.insort(pq, (nd, v))
    return dist[t] if dist[t] != INF else -1
