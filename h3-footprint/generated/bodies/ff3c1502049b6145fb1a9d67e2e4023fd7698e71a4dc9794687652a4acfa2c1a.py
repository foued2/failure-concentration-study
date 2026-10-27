def solve(n, edges, s, t):
    best = [None] * n
    best[s] = 0
    stack = [s]
    while stack:
        u = stack.pop()
        du = best[u]
        for e_u, v, w in edges:
            if e_u != u:
                continue
            nd = du + w
            if best[v] is None or nd < best[v]:
                best[v] = nd
                stack.append(v)
    return -1 if best[t] is None else best[t]
