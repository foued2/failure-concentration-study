def solve(n, edges, s, t):
    import heapq
    graph = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        if 0 <= u < n and 0 <= v < n:
            graph[u].append((v, w))
    done = set()
    reach = {s: 0}
    stackheap = [(0, s)]
    while stackheap:
        d, node = heapq.heappop(stackheap)
        if node in done:
            continue
        done.add(node)
        if node == t:
            return d
        for nxt, wt in graph[node]:
            if nxt not in done:
                ndist = d + wt
                if nxt not in reach or ndist < reach[nxt]:
                    reach[nxt] = ndist
                    heapq.heappush(stackheap, (ndist, nxt))
    return -1
