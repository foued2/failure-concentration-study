def solve(n, edges, s, t):
    best = {}
    for u, v, w in edges:
        if u not in best:
            best[u] = {}
        if v not in best[u] or w < best[u][v]:
            best[u][v] = w
    dist = [float('inf')] * n
    dist[s] = 0
    visited = [False] * n
    for _ in range(n):
        u = -1
        md = float('inf')
        for i in range(n):
            if not visited[i] and dist[i] < md:
                md = dist[i]
                u = i
        if u == -1:
            break
        if u == t:
            break
        visited[u] = True
        for v, w in best.get(u, {}).items():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == float('inf') else dist[t]
