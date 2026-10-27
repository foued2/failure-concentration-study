def solve(n, edges, s, t):
    from collections import defaultdict, deque
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [-1] * n
    dist[s] = 0
    buckets = defaultdict(deque)
    buckets[0].append(s)
    cur = 0
    top = 0
    while cur <= top:
        b = buckets[cur]
        while b:
            u = b.popleft()
            if dist[u] != cur:
                continue
            for v, w in g[u]:
                nd = cur + w
                if dist[v] == -1 or nd < dist[v]:
                    dist[v] = nd
                    buckets[nd].append(v)
                    if nd > top:
                        top = nd
        cur += 1
    return dist[t]
