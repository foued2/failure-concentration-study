def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    cost = [INF] * n
    cost[s] = 0
    used = [False] * n
    for _ in range(n):
        pick = -1
        best = INF
        for i in range(n):
            if not used[i] and cost[i] < best:
                best = cost[i]
                pick = i
        if pick == -1:
            break
        if pick == t:
            return best
        used[pick] = True
        for v, w in adj[pick]:
            if best + w < cost[v]:
                cost[v] = best + w
    return -1
