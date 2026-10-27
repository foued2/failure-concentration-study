def solve(n, edges, s, t):
    dist = [None] * n
    dist[s] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            du = dist[u]
            if du is None:
                continue
            nd = du + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                updated = True
        if not updated:
            break
    return -1 if dist[t] is None else dist[t]
