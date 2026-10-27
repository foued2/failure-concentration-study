def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    max_w = 0
    for u, v, w in edges:
        adj[u].append((v, w))
        if w > max_w:
            max_w = w
    width = max_w if max_w > 0 else 1
    dist = [None] * n
    done = [False] * n
    dist[s] = 0
    buckets = [[(0, s)]]
    idx = 0
    while idx < len(buckets):
        bucket = buckets[idx]
        while bucket:
            pick = 0
            for i in range(1, len(bucket)):
                if bucket[i][0] < bucket[pick][0]:
                    pick = i
            d, u = bucket.pop(pick)
            if done[u] or d > dist[u]:
                continue
            done[u] = True
            if u == t:
                return d
            for v, w in adj[u]:
                nd = d + w
                if dist[v] is None or nd < dist[v]:
                    dist[v] = nd
                    b = nd // width
                    while len(buckets) <= b:
                        buckets.append([])
                    buckets[b].append((nd, v))
        idx += 1
    return -1
