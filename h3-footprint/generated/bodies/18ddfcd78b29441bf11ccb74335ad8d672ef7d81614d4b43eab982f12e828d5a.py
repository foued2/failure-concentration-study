def solve(n, edges, s, t):
    if s == t:
        return 0

    inf = float("inf")
    matrix = [[inf] * n for _ in range(n)]
    for u, v, w in edges:
        if w < matrix[u][v]:
            matrix[u][v] = w

    dist = [inf] * n
    used = [False] * n
    dist[s] = 0

    for _ in range(n):
        node = -1
        smallest = inf
        for i in range(n):
            if not used[i] and dist[i] < smallest:
                smallest = dist[i]
                node = i

        if node == -1:
            break
        if node == t:
            return int(smallest)

        used[node] = True
        for nxt in range(n):
            weight = matrix[node][nxt]
            if not used[nxt] and weight != inf:
                candidate = smallest + weight
                if candidate < dist[nxt]:
                    dist[nxt] = candidate

    return -1
