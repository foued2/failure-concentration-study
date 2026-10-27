def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    best = [None] * n
    best[s] = 0
    frontier = [(0, s)]

    while frontier:
        frontier.sort(reverse=True)
        cost, u = frontier.pop()

        if best[u] != cost:
            continue

        if u == t:
            return cost

        for v, w in adj[u]:
            new_cost = cost + w
            if best[v] is None or new_cost < best[v]:
                best[v] = new_cost
                frontier.append((new_cost, v))

    return -1
