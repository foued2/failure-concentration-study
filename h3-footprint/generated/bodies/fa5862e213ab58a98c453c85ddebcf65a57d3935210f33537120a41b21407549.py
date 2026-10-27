def solve(n, edges, s, t):
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0

    for _ in range(n):
        updated = dist[:]
        for u, v, w in edges:
            if dist[u] != inf and dist[u] + w < updated[v]:
                updated[v] = dist[u] + w

        if updated == dist:
            break

        dist = updated

    return -1 if dist[t] == inf else int(dist[t])
