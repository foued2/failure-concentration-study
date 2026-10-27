def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [None] * n
    dist[s] = 0
    buckets = {0: [s]}
    pending = 1
    d = 0
    while pending:
        nodes = buckets.pop(d, None)
        if nodes is None:
            d += 1
            continue
        pending -= len(nodes)
        for u in nodes:
            if dist[u] != d:
                continue
            if u == t:
                return d
            for v, w in adj[u]:
                nd = d + w
                if dist[v] is None or nd < dist[v]:
                    dist[v] = nd
                    if nd in buckets:
                        buckets[nd].append(v)
                    else:
                        buckets[nd] = [v]
                    pending += 1
    return -1
