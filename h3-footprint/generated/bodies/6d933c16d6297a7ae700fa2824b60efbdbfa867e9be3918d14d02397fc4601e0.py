def solve(n, edges, s, t):
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    visited = [False] * n
    while True:
        u = -1
        best = INF
        for i in range(n):
            if not visited[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            return -1
        if u == t:
            return dist[t]
        visited[u] = True
        for a, b, w in edges:
            if a == u and dist[u] + w < dist[b]:
                dist[b] = dist[u] + w
