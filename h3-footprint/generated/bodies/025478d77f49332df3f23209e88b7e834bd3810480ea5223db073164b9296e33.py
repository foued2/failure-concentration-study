def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    limit = 0
    while True:
        next_limit = INF
        on_path = {s}
        stack = [(s, 0, iter(adj[s]))]
        hit = -1
        while stack:
            node, walked, outs = stack[-1]
            if node == t:
                hit = walked
                break
            advanced = False
            for nxt, w in outs:
                total = walked + w
                if total > limit:
                    if total < next_limit:
                        next_limit = total
                    continue
                if nxt in on_path:
                    continue
                on_path.add(nxt)
                stack.append((nxt, total, iter(adj[nxt])))
                advanced = True
                break
            if not advanced:
                stack.pop()
                on_path.discard(node)
        if hit >= 0:
            return hit
        if next_limit == INF:
            return -1
        limit = next_limit
