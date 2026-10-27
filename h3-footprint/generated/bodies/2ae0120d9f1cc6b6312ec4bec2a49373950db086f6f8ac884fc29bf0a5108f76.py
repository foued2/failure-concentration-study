def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = {}
    stack = [(0, s)]
    best[s] = 0
    while stack:
        d, u = heapq.heappop(stack)
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if v not in best or nd < best[v]:
                best[v] = nd
                heapq.heappush(stack, (nd, v))
    return -1
