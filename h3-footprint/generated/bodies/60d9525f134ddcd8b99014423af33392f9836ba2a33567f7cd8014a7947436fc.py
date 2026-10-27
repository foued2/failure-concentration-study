def solve(n, edges, s, t):
    dist = {s: 0}
    queue = [s]
    idx = 0
    while idx < len(queue):
        u = queue[idx]
        idx += 1
        for u0, v, w in edges:
            if u0 == u:
                nd = dist[u] + w
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    queue.append(v)
    return dist.get(t, -1)
