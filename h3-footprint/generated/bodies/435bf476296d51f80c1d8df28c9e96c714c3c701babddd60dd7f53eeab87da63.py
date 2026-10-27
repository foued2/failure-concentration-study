def solve(n, edges, s, t):
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0

    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break

    return -1 if dist[t] == inf else int(dist[t])
