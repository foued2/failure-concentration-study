def solve(n, edges, s, t):
    if s == t:
        return 0

    import heapq

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    settled = [False] * n
    buckets = {0: [s]}
    pending = [0]

    while pending:
        d = heapq.heappop(pending)
        if d not in buckets:
            continue

        bucket = buckets.pop(d)
        i = 0

        while i < len(bucket):
            u = bucket[i]
            i += 1

            if settled[u] or dist[u] != d:
                continue

            settled[u] = True
            if u == t:
                return d

            for v, w in graph[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    if nd == d:
                        bucket.append(v)
                    else:
                        if nd not in buckets:
                            buckets[nd] = []
                            heapq.heappush(pending, nd)
                        buckets[nd].append(v)

    return -1
