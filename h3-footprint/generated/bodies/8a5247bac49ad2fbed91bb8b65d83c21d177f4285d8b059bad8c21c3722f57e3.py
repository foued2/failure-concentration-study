def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    frontier = [(s, 0)]
    done = [False] * n

    while frontier:
        idx = 0
        for i in range(1, len(frontier)):
            if frontier[i][1] < frontier[idx][1]:
                idx = i
        u, d = frontier.pop(idx)
        if done[u]:
            continue
        done[u] = True
        if u == t:
            break
        for v, w in graph[u]:
            nd = d + w
            if not done[v] and nd < dist[v]:
                dist[v] = nd
                frontier.append((v, nd))

    return -1 if dist[t] == inf else dist[t]
