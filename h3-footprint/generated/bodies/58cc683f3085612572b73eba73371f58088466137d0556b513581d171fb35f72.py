def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = 10**30
    dist = [INF] * n
    dist[s] = 0
    done = [False] * n
    frontier = [(0, s)]
    idx = 0
    while idx < len(frontier):
        d, u = frontier[idx]
        idx += 1
        if done[u]:
            continue
        done[u] = True
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                insort(frontier, (nd, v))
    return -1
