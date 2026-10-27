def solve(n, edges, s, t):
    adj = [[None] * n for _ in range(n)]
    for u, v, w in edges:
        if u != v and (adj[u][v] is None or w < adj[u][v]):
            adj[u][v] = w
    INF = float("inf")
    dist = [INF] * n
    done = [False] * n
    dist[s] = 0
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not done[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        done[u] = True
        if u == t:
            return dist[t]
        for v in range(n):
            if adj[u][v] is not None and not done[v]:
                nd = best + adj[u][v]
                if nd < dist[v]:
                    dist[v] = nd
    return dist[t] if dist[t] != INF else -1
