def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    frontier = {s}
    for _ in range(n):
        if not frontier:
            break
        new_frontier = set()
        for u in frontier:
            for v, w in adj[u]:
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd
                    new_frontier.add(v)
        frontier = new_frontier
        if dist[t] != INF and t not in frontier:
            break
    return -1 if dist[t] == INF else dist[t]
