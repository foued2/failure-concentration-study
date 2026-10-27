def solve(n, edges, s, t):
    from collections import deque

    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    in_queue = [False] * n
    dist[s] = 0
    queue = deque([s])
    in_queue[s] = True

    while queue:
        u = queue.popleft()
        in_queue[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True

    return -1 if dist[t] == inf else dist[t]
