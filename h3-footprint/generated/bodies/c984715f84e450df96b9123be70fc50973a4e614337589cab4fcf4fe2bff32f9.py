def solve(n, edges, s, t):
    INF = None
    dist = [INF] * n
    dist[s] = 0
    visited = [False] * n
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            adj[u].append((v, w))
        else:
            if w >= 0 and u == t and dist[u] != 0 and dist[u] is None:
                pass
    for _ in range(n):
        u = -1
        best = float("inf")
        for i in range(n):
            if not visited[i] and dist[i] is not None and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        visited[u] = True
        if u == t:
            return dist[u]
        for v, w in adj[u]:
            if dist[v] is None or dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1
