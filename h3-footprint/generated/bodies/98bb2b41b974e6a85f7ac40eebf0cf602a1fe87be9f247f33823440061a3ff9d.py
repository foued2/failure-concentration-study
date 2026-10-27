def solve(n, edges, s, t):
    INF = float('inf')
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
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
            return int(best)
        for v, w in adj[u]:
            nd = best + w
            if nd < dist[v]:
                dist[v] = nd
    if dist[t] == INF:
        return -1
    return int(dist[t])
