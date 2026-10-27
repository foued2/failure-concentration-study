def solve(n, edges, s, t):
    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    best = inf
    stack = [(s, 0, 1 << s)]

    while stack:
        u, d, seen = stack.pop()
        if d >= best:
            continue
        for v, w in graph[u]:
            if seen & (1 << v):
                continue
            nd = d + w
            if v == t:
                if nd < best:
                    best = nd
            elif nd < best:
                stack.append((v, nd, seen | (1 << v)))

    return best if best != inf else -1
