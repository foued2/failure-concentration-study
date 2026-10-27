def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    inf = float("inf")
    dist = [inf] * n
    settled = [False] * n
    dist[s] = 0
    for _ in range(n):
        node = -1
        current = inf
        for i in range(n):
            if not settled[i] and dist[i] < current:
                current = dist[i]
                node = i
        if node == -1:
            break
        if node == t:
            return int(current)
        settled[node] = True
        for nxt, cost in adj[node]:
            if not settled[nxt] and current + cost < dist[nxt]:
                dist[nxt] = current + cost
    return -1
