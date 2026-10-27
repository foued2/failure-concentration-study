def solve(n, edges, s, t):
    if s == t:
        return 0
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    best = float("inf")
    on_path = set()

    def visit(u, cost):
        nonlocal best
        if cost >= best:
            return
        if u == t:
            best = cost
            return
        on_path.add(u)
        for v, w in graph[u]:
            if v not in on_path:
                visit(v, cost + w)
        on_path.remove(u)

    visit(s, 0)
    return -1 if best == float("inf") else int(best)
