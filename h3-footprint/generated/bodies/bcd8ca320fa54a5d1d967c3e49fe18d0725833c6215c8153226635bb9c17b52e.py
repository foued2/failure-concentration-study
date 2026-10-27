def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    settled = [False] * n
    dist = [float('inf')] * n
    dist[s] = 0
    for _ in range(n):
        u = -1
        best = float('inf')
        for i in range(n):
            if not settled[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1 or u == t:
            break
        settled[u] = True
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return int(dist[t]) if dist[t] != float('inf') else -1
