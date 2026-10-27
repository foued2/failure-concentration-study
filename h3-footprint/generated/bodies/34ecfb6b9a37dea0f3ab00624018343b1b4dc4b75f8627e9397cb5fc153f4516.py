def solve(n, edges, s, t):
    if n <= 0 or s < 0 or t < 0 or s >= n or t >= n:
        return -1
    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        if 0 <= u < n and 0 <= v < n:
            graph[u].append((v, w))

    infinity = float("inf")
    best = infinity
    visited = [False] * n
    visited[s] = True
    stack = [(s, 0, 0)]

    while stack:
        node, cost, index = stack[-1]
        if node == t:
            if cost < best:
                best = cost
            visited[node] = False
            stack.pop()
            continue
        if index >= len(graph[node]):
            visited[node] = False
            stack.pop()
            continue

        neighbor, weight = graph[node][index]
        stack[-1] = (node, cost, index + 1)
        next_cost = cost + weight
        if next_cost >= best or visited[neighbor]:
            continue
        visited[neighbor] = True
        stack.append((neighbor, next_cost, 0))

    return best if best != infinity else -1
