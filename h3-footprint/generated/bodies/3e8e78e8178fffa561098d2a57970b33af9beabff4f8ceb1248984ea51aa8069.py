def solve(n, edges, s, t):
    if n <= 0:
        return -1
    if s == t:
        return 0
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        relaxed = False
        for a, b, weight in edges:
            if dist[a] != INF:
                through = dist[a] + weight
                if through < dist[b]:
                    dist[b] = through
                    relaxed = True
        if not relaxed:
            break
    return dist[t] if dist[t] != INF else -1
