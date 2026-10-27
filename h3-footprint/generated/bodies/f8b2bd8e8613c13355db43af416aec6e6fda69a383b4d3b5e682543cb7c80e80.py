def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if w >= 0:
            adj[u].append((v, w))
    best = [None] * n
    best[s] = 0
    found = []

    def dfs(u, acc, seen):
        if u == t:
            found.append(acc)
            return
        for v, w in adj[u]:
            if v in seen:
                continue
            nb = best[v]
            if nb is not None and acc + w >= nb:
                continue
            best[v] = acc + w
            seen.add(v)
            dfs(v, acc + w, seen)
            seen.remove(v)

    dfs(s, 0, {s})
    return min(found) if found else -1
