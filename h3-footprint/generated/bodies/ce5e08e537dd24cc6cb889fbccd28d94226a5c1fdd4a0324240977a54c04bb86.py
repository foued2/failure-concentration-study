def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
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
        done[u] = True
        if u == t:
            break
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
    return -1 if dist[t] == INF else int(dist[t])
