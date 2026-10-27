def solve(n, edges, s, t):
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    done = [False] * n
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not done[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        if u == t:
            return dist[t]
        done[u] = True
        for a, b, w in edges:
            if a == u and dist[u] + w < dist[b]:
                dist[b] = dist[u] + w
    return -1 if dist[t] == INF else dist[t]
