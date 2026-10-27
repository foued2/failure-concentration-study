def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    buckets = [[s]]
    layer = 0
    while layer < len(buckets):
        cur = buckets[layer]
        while cur:
            u = cur.pop()
            if dist[u] != layer:
                continue
            for v, w in adj[u]:
                nd = layer + w
                if nd < dist[v]:
                    dist[v] = nd
                    while nd >= len(buckets):
                        buckets.append([])
                    buckets[nd].append(v)
        layer += 1
    return -1 if dist[t] == INF else int(dist[t])
