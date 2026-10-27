def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = [-1] * n
    def dfs(u, acc, visited):
        if u == t:
            return acc
        visited.add(u)
        result = None
        for v, w in adj[u]:
            nd = acc + w
            if v not in visited and (best[v] == -1 or nd < best[v]):
                sub = dfs(v, nd, visited)
                best[v] = sub
                if sub is not None and (result is None or sub < result):
                    result = sub
        visited.discard(u)
        return result
    res = dfs(s, 0, set())
    return res if res is not None else -1
