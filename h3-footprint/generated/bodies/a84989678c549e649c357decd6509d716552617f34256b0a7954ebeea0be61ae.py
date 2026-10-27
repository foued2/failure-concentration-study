def solve(n, edges, s, t):
    maxw = max((w for _, _, w in edges), default=0)
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    buckets = [deque() for _ in range(maxw + 1)]
    buckets[0].append(s)
    processed = 0
    maxdist = n * maxw + 1
    b = 0
    while processed < n and b <= maxdist:
        while buckets[b % (maxw + 1)]:
            u = buckets[b % (maxw + 1)].popleft()
            if dist[u] != b:
                continue
            processed += 1
            for v, w in adj[u]:
                nd = b + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets[nd % (maxw + 1)].append(v)
        b += 1
    return dist[t] if dist[t] != INF else -1
