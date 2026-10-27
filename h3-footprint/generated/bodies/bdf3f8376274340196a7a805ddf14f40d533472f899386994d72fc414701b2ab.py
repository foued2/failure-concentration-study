def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    best = inf
    seen = [False] * n

    def explore(u, cost):
        nonlocal best
        if cost >= best:
            return
        if u == t:
            best = cost
            return
        seen[u] = True
        for v, w in graph[u]:
            if not seen[v]:
                explore(v, cost + w)
        seen[u] = False

    explore(s, 0)
    return -1 if best == inf else best
