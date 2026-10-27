def solve(n, edges, s, t):
    if s == t:
        return 0

    dist = [None] * n
    dist[s] = 0

    for _ in range(max(0, n - 1)):
        changed = False
        for u, v, w in edges:
            if dist[u] is None:
                continue
            candidate = dist[u] + w
            if dist[v] is None or candidate < dist[v]:
                dist[v] = candidate
                changed = True
        if not changed:
            break

    return -1 if dist[t] is None else dist[t]
