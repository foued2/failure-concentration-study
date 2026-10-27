def solve(n, edges, s, t):
    dist = [None] * n
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] is None:
                continue
            nd = dist[u] + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                changed = True
        if not changed:
            break
    return -1 if dist[t] is None else dist[t]
