def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    INF = float("inf")
    best = INF
    on_path = [False] * n

    sys.setrecursionlimit(max(sys.getrecursionlimit(), n + 100))

    def walk(u, cost):
        nonlocal best
        if cost >= best:
            return
        if u == t:
            best = cost
            return
        on_path[u] = True
        for v, w in graph[u]:
            if not on_path[v]:
                walk(v, cost + w)
        on_path[u] = False

    walk(s, 0)
    return best if best != INF else -1
