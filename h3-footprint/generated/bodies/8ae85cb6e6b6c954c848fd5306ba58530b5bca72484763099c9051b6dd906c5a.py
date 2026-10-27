def solve(n, edges, s, t):
    if s == t:
        return 0

    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0

    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] == inf:
                continue
            candidate = dist[u] + w
            if candidate < dist[v]:
                dist[v] = candidate
                changed = True
        if not changed:
            break

    if dist[t] == inf:
        return -1
    return int(dist[t])
