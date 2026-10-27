def solve(n, edges, s, t):
    adj = [None] * n
    for u, v, w in edges:
        if adj[u] is None:
            adj[u] = [(v, w)]
        else:
            adj[u].append((v, w))
    dist_map = {}
    dist_map[s] = 0
    queue = [(0, s)]
    while queue:
        d, cur = heapq.heappop(queue)
        stale = dist_map.get(cur, -1) != d
        if stale:
            continue
        if cur == t:
            return d
        nxt = adj[cur]
        if nxt:
            for v, w in nxt:
                nd = d + w
                old = dist_map.get(v)
                if old is None or nd < old:
                    dist_map[v] = nd
                    heapq.heappush(queue, (nd, v))
    return dist_map.get(t, -1)
