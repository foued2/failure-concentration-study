def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    settled = [False] * n
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not settled[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1 or dist[u] == INF:
            break
        settled[u] = True
        if u == t:
            return dist[u]
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1
