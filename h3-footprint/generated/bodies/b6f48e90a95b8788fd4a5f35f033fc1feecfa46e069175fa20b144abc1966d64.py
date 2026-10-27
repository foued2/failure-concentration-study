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
        du = INF
        for i in range(n):
            if not done[i] and dist[i] < du:
                du = dist[i]
                u = i
        if u == -1:
            break
        done[u] = True
        if u == t:
            break
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist[t] if dist[t] != INF else -1
