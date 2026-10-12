"""Submission 103 (base body 35, replica 0)."""

def solve(n, edges, s, t):
    INF = float("inf")
    g = [[] for _ in range(n)]
    mw = 1
    for u, v, w in edges:
        g[u].append((v, w))
        mw = max(mw, w)
    dist = [INF] * n
    dist[s] = 0
    bound = mw * n + 2
    buckets = [[] for _ in range(bound)]
    buckets[0].append(s)
    for d in range(bound):
        while buckets[d]:
            u = buckets[d].pop()
            if d > dist[u]:
                continue
            for v, w in g[u]:
                nd = d + w
                if nd < dist[v] and nd < bound:
                    dist[v] = nd
                    buckets[nd].append(v)
    return -1 if dist[t] == INF else dist[t]
