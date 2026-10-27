def solve(n, edges, s, t):
    from collections import deque
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [None] * n
    dist[s] = 0
    in_queue = [False] * n
    queue = deque([s])
    in_queue[s] = True
    while queue:
        u = queue.popleft()
        in_queue[u] = False
        du = dist[u]
        if du is None:
            continue
        for v, w in graph[u]:
            nd = du + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    in_queue[v] = True
                    queue.append(v)
    return -1 if dist[t] is None else dist[t]
