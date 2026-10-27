def solve(n, edges, s, t):
    best = [None] * n
    best[s] = 0
    for u, v, w in edges:
        if best[u] is not None:
            cand = best[u] + w
            if best[v] is None or cand < best[v]:
                best[v] = cand
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if best[u] is not None:
                cand = best[u] + w
                if best[v] is None or cand < best[v]:
                    best[v] = cand
                    changed = True
        if not changed:
            break
    return -1 if best[t] is None else best[t]
