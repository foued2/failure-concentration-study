def solve(n, edges, s, t):
    from collections import deque

    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    queue = deque([s])
    in_queue = [False] * n
    in_queue[s] = True

    while queue:
        u = queue.popleft()
        in_queue[u] = False
        du = dist[u]
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    in_queue[v] = True
                    queue.append(v)

    return dist[t] if dist[t] != inf else -1
