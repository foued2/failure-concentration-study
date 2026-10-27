def solve(n, edges, s, t):
    nbr = [[] for _ in range(n)]
    maxw = 0
    for u, v, w in edges:
        nbr[u].append((v, w))
        if w > maxw:
            maxw = w
    span = maxw + 1
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    cells = {0: [s]}
    alive = 1
    d = 0
    while alive:
        cell = cells.get(d % span)
        if not cell:
            d += 1
            continue
        while cell:
            u = cell.pop()
            alive -= 1
            if dist[u] != d:
                continue
            if u == t:
                return d
            for v, w in nbr[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    key = nd % span
                    if key in cells:
                        cells[key].append(v)
                    else:
                        cells[key] = [v]
                    alive += 1
        d += 1
    return -1
