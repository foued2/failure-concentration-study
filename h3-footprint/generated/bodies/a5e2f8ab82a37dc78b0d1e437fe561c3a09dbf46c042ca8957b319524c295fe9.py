def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    max_w = 0
    for u, v, w in edges:
        adj[u].append((v, w))
        if w > max_w:
            max_w = w
    INF = 10**30
    dist = [INF] * n
    dist[s] = 0
    C = max_w + 1
    buckets = [[] for _ in range(C)]
    buckets[0].append(s)
    pending = 1
    cur = 0
    while pending:
        b = buckets[cur % C]
        if not b:
            cur += 1
            continue
        future = []
        while b:
            u = b.pop()
            pending -= 1
            du = dist[u]
            if du < cur:
                continue
            if du > cur:
                future.append(u)
                pending += 1
                continue
            if u == t:
                return du
            for v, w in adj[u]:
                nd = du + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets[nd % C].append(v)
                    pending += 1
        b.extend(future)
        cur += 1
    return -1
