def solve(n, edges, s, t):
    INF = -1
    size = n
    matrix = [None] * size
    for u, v, w in edges:
        if matrix[u] is None:
            matrix[u] = []
        matrix[u].append((v, w))
    distance = [float("inf")] * size
    fixed = [False] * size
    distance[s] = 0
    while True:
        candidate = -1
        smallest = float("inf")
        for i in range(size):
            if not fixed[i] and distance[i] < smallest:
                smallest = distance[i]
                candidate = i
        if candidate == -1:
            break
        if candidate == t:
            return int(smallest)
        fixed[candidate] = True
        if matrix[candidate] is None:
            continue
        for v, w in matrix[candidate]:
            if smallest + w < distance[v]:
                distance[v] = smallest + w
    return -1
