def solve(n, edges, s, t):
    if n <= 0 or s < 0 or t < 0 or s >= n or t >= n:
        return -1
    if s == t:
        return 0

    matrix = [[None] * n for _ in range(n)]
    for u, v, w in edges:
        if 0 <= u < n and 0 <= v < n:
            if matrix[u][v] is None or w < matrix[u][v]:
                matrix[u][v] = w

    distance = [None] * n
    distance[s] = 0
    visited = [False] * n

    for _ in range(n):
        node = -1
        best = None
        for candidate in range(n):
            if not visited[candidate] and distance[candidate] is not None:
                if best is None or distance[candidate] < best:
                    best = distance[candidate]
                    node = candidate
        if node == -1:
            break
        if node == t:
            return best
        visited[node] = True
        row = matrix[node]
        for neighbor in range(n):
            weight = row[neighbor]
            if weight is not None and not visited[neighbor]:
                candidate = best + weight
                if distance[neighbor] is None or candidate < distance[neighbor]:
                    distance[neighbor] = candidate

    return -1
