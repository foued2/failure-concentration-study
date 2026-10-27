def solve(n, edges, s, t):
    from collections import deque
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    inf = float("inf")
    dist = [inf] * n
    in_queue = [False] * n
    dist[s] = 0
    in_queue[s] = True
    queue = deque([s])
    while queue:
        u = queue.popleft()
        in_queue[u] = False
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    in_queue[v] = True
                    queue.append(v)
    return dist[t] if dist[t] != inf else -1
