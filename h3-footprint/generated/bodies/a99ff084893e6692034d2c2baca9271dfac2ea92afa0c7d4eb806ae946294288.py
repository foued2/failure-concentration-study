def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = None
    visited = [False] * n
    visited[s] = True
    stack = [(s, 0, 0)]
    while stack:
        u, cost, idx = stack[-1]
        if u == t:
            if best is None or cost < best:
                best = cost
            stack.pop()
            visited[u] = False
            continue
        if idx >= len(adj[u]):
            stack.pop()
            visited[u] = False
            continue
        stack[-1] = (u, cost, idx + 1)
        v, w = adj[u][idx]
        if not visited[v] and (best is None or cost + w < best):
            visited[v] = True
            stack.append((v, cost + w, 0))
    return -1 if best is None else best
