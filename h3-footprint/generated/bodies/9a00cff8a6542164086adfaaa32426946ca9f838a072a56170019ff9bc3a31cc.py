def solve(n, edges, s, t):
    import heapq

    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    settled = [False] * n
    buckets = {0: [s]}
    keys = [0]
    while keys:
        k = keys[0]
        bucket = buckets.get(k)
        if not bucket:
            heapq.heappop(keys)
            continue
        del buckets[k]
        for u in bucket:
            if settled[u]:
                continue
            settled[u] = True
            du = dist[u]
            if u == t:
                return int(du)
            for v, w in adj[u]:
                nd = du + w
                if nd < dist[v]:
                    dist[v] = nd
                    if nd in buckets:
                        buckets[nd].append(v)
                    else:
                        buckets[nd] = [v]
                        heapq.heappush(keys, nd)
    return -1 if dist[t] == INF else int(dist[t])
