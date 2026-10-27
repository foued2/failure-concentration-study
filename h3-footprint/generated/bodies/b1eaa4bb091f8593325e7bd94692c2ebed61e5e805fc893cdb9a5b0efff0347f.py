def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    frontier = [s]

    for _ in range(n - 1):
        if not frontier:
            break
        snapshot = dist[:]
        updated = {}
        for u in frontier:
            du = snapshot[u]
            for v, w in adj[u]:
                nd = du + w
                if nd < dist[v]:
                    dist[v] = nd
                    updated[v] = True
        if not updated:
            break
        frontier = list(updated.keys())

    return -1 if dist[t] == INF else dist[t]
