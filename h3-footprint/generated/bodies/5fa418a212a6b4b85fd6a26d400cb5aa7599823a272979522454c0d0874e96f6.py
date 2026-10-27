def solve(n, edges, s, t):
    dist = [None] * n
    dist[s] = 0

    for _ in range(n):
        updated = False
        for u, v, w in edges:
            if dist[u] is not None:
                candidate = dist[u] + w
                if dist[v] is None or candidate < dist[v]:
                    dist[v] = candidate
                    updated = True
        if not updated:
            break

    return -1 if dist[t] is None else dist[t]
