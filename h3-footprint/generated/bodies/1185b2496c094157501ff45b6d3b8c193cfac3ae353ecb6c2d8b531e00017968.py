def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    done = [False] * n
    dist[s] = 0
    for _ in range(n):
        u = -1
        for i in range(n):
            if not done[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        if u == -1 or dist[u] == INF:
            break
        if u == t:
            return int(dist[u])
        done[u] = True
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
    return -1 if dist[t] == INF else int(dist[t])
