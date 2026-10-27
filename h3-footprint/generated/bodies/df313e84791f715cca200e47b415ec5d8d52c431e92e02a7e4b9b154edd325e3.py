def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    layers = {0: [s]}
    while layers:
        d = min(layers)
        nodes = layers.pop(d)
        for u in nodes:
            if d != dist[u]:
                continue
            if u == t:
                return d
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    layers.setdefault(nd, []).append(v)
    return -1
