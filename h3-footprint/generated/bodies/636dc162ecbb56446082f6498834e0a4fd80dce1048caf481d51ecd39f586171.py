def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = 10**30
    dist = [INF] * n
    dist[s] = 0
    REMOVED = object()
    entry_finder = {}
    counter = count()
    heap = []

    def add_task(node, priority):
        if node in entry_finder:
            entry_finder[node][-1] = REMOVED
        entry = [priority, next(counter), node]
        entry_finder[node] = entry
        heapq.heappush(heap, entry)

    def pop_task():
        while heap:
            priority, _, task = heapq.heappop(heap)
            if task is not REMOVED:
                del entry_finder[task]
                return priority, task
        return None

    add_task(s, 0)
    while True:
        item = pop_task()
        if item is None:
            break
        d, u = item
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                add_task(v, nd)
    return -1
