def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    best_found = INF
    reached = {s: 0}
    trail = {s}
    stack = [(s, 0, iter(adj[s]))]
    while stack:
        node, walked, outs = stack[-1]
        advanced = False
        for nxt, w in outs:
            total = walked + w
            if total >= best_found:
                continue
            if nxt == t:
                best_found = total
                continue
            if nxt in trail or reached.get(nxt, total) < total:
                continue
            reached[nxt] = total
            trail.add(nxt)
            stack.append((nxt, total, iter(adj[nxt])))
            advanced = True
            break
        if not advanced:
            stack.pop()
            trail.discard(node)
    return best_found if best_found != INF else -1
