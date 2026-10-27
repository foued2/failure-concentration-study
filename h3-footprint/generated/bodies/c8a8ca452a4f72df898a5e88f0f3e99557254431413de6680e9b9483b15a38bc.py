def solve(n, edges, s, t):
    if s == t:
        return 0

    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0

    for _ in range(n - 1):
        next_dist = dist[:]
        changed = False

        for u, v, w in edges:
            if dist[u] != inf:
                candidate = dist[u] + w
                if candidate < next_dist[v]:
                    next_dist[v] = candidate
                    changed = True

        dist = next_dist

        if not changed:
            break

    return dist[t] if dist[t] != inf else -1
