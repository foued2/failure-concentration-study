def solve(n, edges, s, t):
    from collections import deque
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    buckets = [deque([s])]
    cur = 0
    while cur < len(buckets):
        bucket = buckets[cur]
        while bucket:
            u = bucket.popleft()
            if dist[u] != cur:
                continue
            for v, w in graph[u]:
                nd = cur + w
                if nd < dist[v]:
                    dist[v] = nd
                    while len(buckets) <= nd:
                        buckets.append(deque())
                    buckets[nd].append(v)
        cur += 1
    return -1 if dist[t] == INF else dist[t]
