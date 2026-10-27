def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = {s: 0}
    queue = [s]
    inq = {s}
    while queue:
        u = queue.pop(0)
        inq.discard(u)
        du = dist[u]
        for v, w in adj[u]:
            if du + w < dist.get(v, INF):
                dist[v] = du + w
                if v not in inq:
                    queue.append(v)
                    inq.add(v)
    return dist.get(t, -1)
