def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    used = [False] * n
    for _ in range(n):
        u = -1
        current = INF
        for i in range(n):
            if not used[i] and dist[i] < current:
                current = dist[i]
                u = i
        if u == -1:
            break
        used[u] = True
        for a, b, w in edges:
            if a == u and not used[b] and dist[u] + w < dist[b]:
                dist[b] = dist[u] + w
    return -1 if dist[t] == INF else int(dist[t])
