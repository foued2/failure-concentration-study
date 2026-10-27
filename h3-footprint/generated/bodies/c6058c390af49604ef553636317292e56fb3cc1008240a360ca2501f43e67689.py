def solve(n, edges, s, t):
    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    layers = {0: [s]}
    finished = [False] * n

    while layers:
        current = min(layers)
        nodes = layers.pop(current)

        for u in nodes:
            if finished[u] or dist[u] != current:
                continue
            finished[u] = True

            if u == t:
                return current

            for v, w in graph[u]:
                candidate = current + w
                if candidate < dist[v]:
                    dist[v] = candidate
                    if candidate not in layers:
                        layers[candidate] = []
                    layers[candidate].append(v)

    return -1
