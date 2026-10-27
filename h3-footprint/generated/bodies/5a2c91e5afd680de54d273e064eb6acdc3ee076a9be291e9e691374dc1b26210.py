def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    heap = []

    def push(item):
        heap.append(item)
        i = len(heap) - 1
        while i > 0:
            parent = (i - 1) // 2
            if heap[parent][0] <= heap[i][0]:
                break
            heap[parent], heap[i] = heap[i], heap[parent]
            i = parent

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

    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    push((0, s))
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
