def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = [float('inf')]
    seen = [False] * n
    seen[s] = True

    def walk(u, acc):
        if u == t:
            if acc < best[0]:
                best[0] = acc
            return
        for v, w in adj[u]:
            if not seen[v]:
                seen[v] = True
                walk(v, acc + w)
                seen[v] = False

    walk(s, 0)
    return -1 if best[0] == float('inf') else best[0]
