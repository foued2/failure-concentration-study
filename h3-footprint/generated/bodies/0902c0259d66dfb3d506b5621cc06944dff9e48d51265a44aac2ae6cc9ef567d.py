def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    used = [False] * n
    dist[s] = 0

    for _ in range(n):
        u = -1
        best = inf
        for i in range(n):
            if not used[i] and dist[i] < best:
                best = dist[i]
                u = i

        if u == -1:
            break
        if u == t:
            return best

        used[u] = True
        for v, w in adj[u]:
            nd = best + w
            if nd < dist[v]:
                dist[v] = nd

    return -1
