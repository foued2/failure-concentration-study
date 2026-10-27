def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    for neighbors in adj:
        neighbors.sort(key=lambda item: item[1])
    inf = float("inf")
    best = inf
    stack = [(s, 0, {s})]
    while stack:
        u, cost, seen = stack.pop()
        if cost >= best:
            continue
        for v, w in adj[u]:
            new_cost = cost + w
            if new_cost >= best:
                continue
            if v == t:
                if new_cost < best:
                    best = new_cost
            elif v not in seen:
                stack.append((v, new_cost, seen | {v}))
    return best if best != inf else -1
