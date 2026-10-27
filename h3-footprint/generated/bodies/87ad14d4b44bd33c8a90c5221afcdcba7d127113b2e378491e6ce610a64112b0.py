def solve(n, edges, s, t):
    inf = float("inf")
    distance = [inf] * n
    distance[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if distance[u] != inf and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                changed = True
        if not changed:
            break
    return -1 if distance[t] == inf else int(distance[t])
