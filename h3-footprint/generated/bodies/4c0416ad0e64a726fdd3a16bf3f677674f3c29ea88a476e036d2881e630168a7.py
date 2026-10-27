def solve(n, edges, s, t):
    dist = [1 << 60] * n
    dist[s] = 0
    for _ in range(n):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    if dist[t] >= 1 << 60:
        return -1
    return dist[t]
