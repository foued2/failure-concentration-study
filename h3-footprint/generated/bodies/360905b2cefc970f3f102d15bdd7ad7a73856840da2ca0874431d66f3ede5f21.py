def solve(n, edges, s, t):
    out = [[] for _ in range(n)]
    for u, v, w in edges:
        out[u].append((v, w))
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    done = [False] * n
    buckets = {0: [s]}
    while buckets:
        level = min(buckets)
        layer = buckets.pop(level)
        for u in layer:
            if done[u] or dist[u] != level:
                continue
            done[u] = True
            if u == t:
                return int(level)
            for v, w in out[u]:
                nd = level + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets.setdefault(nd, []).append(v)
    return -1
