def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
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
        if u == t:
            return int(dist[u])
        done[u] = True
        for v, w in graph[u]:
            if not done[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == INF else int(dist[t])
