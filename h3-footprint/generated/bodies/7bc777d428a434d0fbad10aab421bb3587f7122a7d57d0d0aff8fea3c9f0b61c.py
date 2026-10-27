def solve(n, edges, s, t):
    if n <= 0 or s < 0 or t < 0 or s >= n or t >= n:
        return -1
    if s == t:
        return 0

    infinity = float("inf")
    distance = [infinity] * n
    distance[s] = 0

    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if 0 <= u < n and 0 <= v < n and distance[u] != infinity:
                candidate = distance[u] + w
                if candidate < distance[v]:
                    distance[v] = candidate
                    changed = True
        if not changed:
            break

    return distance[t] if distance[t] != infinity else -1
