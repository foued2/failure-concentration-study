def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    order = list(range(n))
    in_queue = [False] * n
    in_queue[s] = True
    queue = [s]
    head = 0
    counts = [0] * n
    counts[s] = 1
    while head < len(queue):
        u = queue[head]
        head += 1
        in_queue[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    in_queue[v] = True
                    queue.append(v)
                    counts[v] += 1
                    if counts[v] > n:
                        return -1
    return -1 if dist[t] == INF else dist[t]
