def solve(n, edges, s, t):
    if s == t:
        return 0

    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0

    for _ in range(max(0, n - 1)):
        next_dist = dist[:]
        changed = False
        for u, v, w in edges:
            if dist[u] == INF:
                continue
            candidate = dist[u] + w
            if candidate < next_dist[v]:
                next_dist[v] = candidate
                changed = True
        dist = next_dist
        if not changed:
            break

    return -1 if dist[t] == INF else dist[t]
