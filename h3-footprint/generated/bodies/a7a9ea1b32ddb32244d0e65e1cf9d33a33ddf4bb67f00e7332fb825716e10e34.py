def solve(n, edges, s, t):
    dist = [10**18] * n
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return dist[t] if dist[t] < 10**18 else -1
