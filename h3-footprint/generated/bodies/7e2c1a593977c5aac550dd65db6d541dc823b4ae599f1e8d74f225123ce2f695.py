def solve(n, edges, s, t):
    import heapq

    if n <= 0 or s < 0 or t < 0 or s >= n or t >= n:
        return -1
    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    reverse = [[] for _ in range(n)]
    for u, v, w in edges:
        if 0 <= u < n and 0 <= v < n:
            graph[u].append((v, w))
            reverse[v].append((u, w))

    infinity = float("inf")
    forward_dist = [infinity] * n
    backward_dist = [infinity] * n
    forward_dist[s] = 0
    backward_dist[t] = 0
    forward_queue = [(0, s)]
    backward_queue = [(0, t)]
    forward_done = [False] * n
    backward_done = [False] * n
    best = infinity

    def clean(queue, dist, done):
        while queue:
            d, u = queue[0]
            if done[u] or d != dist[u]:
                heapq.heappop(queue)
            else:
                return d
        return infinity

    while forward_queue and backward_queue:
        forward_min = clean(forward_queue, forward_dist, forward_done)
        backward_min = clean(backward_queue, backward_dist, backward_done)
        if forward_min == infinity or backward_min == infinity:
            break
        if forward_min + backward_min >= best:
            break

        if forward_min <= backward_min:
            d, u = heapq.heappop(forward_queue)
            if forward_done[u] or d != forward_dist[u]:
                continue
            forward_done[u] = True
            if backward_dist[u] != infinity:
                candidate = d + backward_dist[u]
                if candidate < best:
                    best = candidate
            for v, w in graph[u]:
                candidate = d + w
                if not forward_done[v] and candidate < forward_dist[v]:
                    forward_dist[v] = candidate
                    heapq.heappush(forward_queue, (candidate, v))
        else:
            d, u = heapq.heappop(backward_queue)
            if backward_done[u] or d != backward_dist[u]:
                continue
            backward_done[u] = True
            if forward_dist[u] != infinity:
                candidate = d + forward_dist[u]
                if candidate < best:
                    best = candidate
            for v, w in reverse[u]:
                candidate = d + w
                if not backward_done[v] and candidate < backward_dist[v]:
                    backward_dist[v] = candidate
                    heapq.heappush(backward_queue, (candidate, v))

    return best if best != infinity else -1
