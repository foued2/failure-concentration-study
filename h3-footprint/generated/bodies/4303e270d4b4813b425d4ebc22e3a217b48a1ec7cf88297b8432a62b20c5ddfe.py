def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0

    for _ in range(n):
        updated = False
        for u in range(n):
            if dist[u] == INF:
                continue
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
        if not updated:
            break

    return -1 if dist[t] == INF else dist[t]
