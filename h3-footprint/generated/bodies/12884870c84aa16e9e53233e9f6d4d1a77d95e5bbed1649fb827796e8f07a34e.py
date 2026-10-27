def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    best = float("inf")
    on_path = [False] * n

    def explore(u, cost):
        nonlocal best
        if u == t:
            if cost < best:
                best = cost
            return
        if cost >= best:
            return
        on_path[u] = True
        for v, w in graph[u]:
            if not on_path[v]:
                explore(v, cost + w)
        on_path[u] = False

    on_path[s] = True
    explore(s, 0)
    return -1 if best == float("inf") else int(best)
