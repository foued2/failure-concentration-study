def solve(n, edges, s, t):
    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    heap = [(0, s)]

    def push(item):
        heap.append(item)
        i = len(heap) - 1
        while i > 0:
            p = (i - 1) // 2
            if heap[p][0] <= heap[i][0]:
                break
            heap[p], heap[i] = heap[i], heap[p]
            i = p

    def pop():
        top = heap[0]
        last = heap.pop()
        if heap:
            heap[0] = last
            i = 0
            while True:
                left = 2 * i + 1
                right = left + 1
                smallest = i
                if left < len(heap) and heap[left][0] < heap[smallest][0]:
                    smallest = left
                if right < len(heap) and heap[right][0] < heap[smallest][0]:
                    smallest = right
                if smallest == i:
                    break
                heap[i], heap[smallest] = heap[smallest], heap[i]
                i = smallest
        return top

    while heap:
        d, u = pop()
        if d != dist[u]:
            continue
        if u == t:
            return d

        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                push((nd, v))

    return -1
