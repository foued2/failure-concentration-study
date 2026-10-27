def solve(n, edges, s, t):
    neighbours = [dict() for _ in range(n)]
    for a, b, c in edges:
        if b not in neighbours[a] or c < neighbours[a][b]:
            neighbours[a][b] = c
    INF = float("inf")
    dist = [INF] * n
    settled = [False] * n
    dist[s] = 0
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not settled[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        if u == t:
            return best
        settled[u] = True
        for v, w in neighbours[u].items():
            if best + w < dist[v]:
                dist[v] = best + w
    return -1 if dist[t] == INF else dist[t]
