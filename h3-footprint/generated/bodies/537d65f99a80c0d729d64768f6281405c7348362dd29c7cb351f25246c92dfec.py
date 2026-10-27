def solve(n, edges, s, t):
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    for _ in range(n):
        updated = False
        for u, v, w in edges:
            if dist[u] < inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    return -1 if dist[t] == inf else int(dist[t])
