def solve(n, edges, s, t):
    if s == t:
        return 0
    dist = [None] * n
    dist[s] = 0
    for _ in range(n - 1 if n > 0 else 0):
        changed = False
        for u, v, w in edges:
            du = dist[u]
            if du is None:
                continue
            nd = du + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                changed = True
        if not changed:
            break
    return -1 if dist[t] is None else dist[t]
