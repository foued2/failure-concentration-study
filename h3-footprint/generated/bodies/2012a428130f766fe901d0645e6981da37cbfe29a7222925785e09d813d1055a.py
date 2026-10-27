def solve(n, edges, s, t):
    import sys

    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    best = inf
    visited = [False] * n
    visited[s] = True

    sys.setrecursionlimit(max(sys.getrecursionlimit(), n + 10))

    def search(u, total):
        nonlocal best

        if total >= best:
            return
        if u == t:
            best = total
            return

        for v, w in graph[u]:
            if not visited[v]:
                visited[v] = True
                search(v, total + w)
                visited[v] = False

    search(s, 0)
    return -1 if best == inf else int(best)
