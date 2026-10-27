def solve(n, edges, s, t):
    import sys

    if s == t:
        return 0

    sys.setrecursionlimit(max(sys.getrecursionlimit(), n + 10))

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    best = [float("inf")]
    visited = [False] * n
    visited[s] = True

    def dfs(u, cost):
        if cost >= best[0]:
            return

        if u == t:
            best[0] = cost
            return

        for v, w in graph[u]:
            if not visited[v]:
                visited[v] = True
                dfs(v, cost + w)
                visited[v] = False

    dfs(s, 0)

    return best[0] if best[0] != float("inf") else -1
