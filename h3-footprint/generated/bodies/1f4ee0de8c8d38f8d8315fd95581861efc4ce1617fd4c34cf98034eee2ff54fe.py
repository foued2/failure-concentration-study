def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [None] * n
    done = [False] * n
    dist[s] = 0
    for _ in range(n):
        u = -1
        best = None
        for i in range(n):
            if done[i] or dist[i] is None:
                continue
            if best is None or dist[i] < best:
                best = dist[i]
                u = i
        if u < 0:
            break
        done[u] = True
        if u == t:
            return best
        for v, w in adj[u]:
            nd = best + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
    return -1
