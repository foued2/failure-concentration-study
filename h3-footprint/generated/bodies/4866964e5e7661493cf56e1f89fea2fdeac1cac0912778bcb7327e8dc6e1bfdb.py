def solve(n, edges, s, t):
    if n <= 0 or s < 0 or t < 0 or s >= n or t >= n:
        return -1
    if s == t:
        return 0

    infinity = float("inf")
    distance = [[infinity] * n for _ in range(n)]
    for i in range(n):
        distance[i][i] = 0
    for u, v, w in edges:
        if 0 <= u < n and 0 <= v < n and w < distance[u][v]:
            distance[u][v] = w

    for k in range(n):
        row_k = distance[k]
        for i in range(n):
            through_k = distance[i][k]
            if through_k == infinity:
                continue
            row_i = distance[i]
            for j in range(n):
                candidate = through_k + row_k[j]
                if candidate < row_i[j]:
                    row_i[j] = candidate

    return distance[s][t] if distance[s][t] != infinity else -1
