def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    answer = -1

    def dfs(u, acc, seen):
        nonlocal answer
        if acc >= 0 and (answer == -1 or acc >= answer):
            return
        if u == t:
            answer = acc
            return
        for v, w in adj[u]:
            if not seen[v]:
                seen[v] = True
                dfs(v, acc + w, seen)
                seen[v] = False

    seen = [False] * n
    seen[s] = True
    dfs(s, 0, seen)
    return answer
