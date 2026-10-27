def solve(n, edges, s, t):
    if s == t:
        return 0
    INF = float("inf")
    distance = [INF] * n
    distance[s] = 0
    rounds = n - 1
    while rounds > 0:
        changed = False
        for u, v, w in edges:
            if distance[u] != INF and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                changed = True
        if not changed:
            break
        rounds -= 1
    return distance[t] if distance[t] != INF else -1
