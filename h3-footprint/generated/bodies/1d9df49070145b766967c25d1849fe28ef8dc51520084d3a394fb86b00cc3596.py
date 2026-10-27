def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = {s: 0}
    while True:
        changed = False
        for u in list(dist.keys()):
            for v, w in adj[u]:
                nd = dist[u] + w
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    changed = True
        if not changed:
            break
    return dist.get(t, -1)
