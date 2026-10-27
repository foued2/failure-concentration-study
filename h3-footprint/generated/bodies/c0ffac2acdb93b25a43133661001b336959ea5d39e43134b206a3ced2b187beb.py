def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    done = bytearray(n)
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
            return best
        done[u] = 1
        for v, w in adj[u]:
            if not done[v] and best + w < dist[v]:
                dist[v] = best + w
    return -1 if dist[t] == INF else dist[t]
