def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    class MinHeap:
        def __init__(self):
            self.a = []

        def push(self, key, val):
            a = self.a
            a.append((key, val))
            i = len(a) - 1
            while i > 0:
                p = (i - 1) // 2
                if a[p][0] <= a[i][0]:
                    break
                a[p], a[i] = a[i], a[p]
                i = p

        def pop(self):
            a = self.a
            top = a[0]
            last = a.pop()
            if a:
                a[0] = last
                i = 0
                m = len(a)
                while True:
                    l = 2 * i + 1
                    r = 2 * i + 2
                    smallest = i
                    if l < m and a[l][0] < a[smallest][0]:
                        smallest = l
                    if r < m and a[r][0] < a[smallest][0]:
                        smallest = r
                    if smallest == i:
                        break
                    a[i], a[smallest] = a[smallest], a[i]
                    i = smallest
            return top

        def __bool__(self):
            return bool(self.a)

    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    heap = MinHeap()
    heap.push(0, s)
    while heap:
        d, u = heap.pop()
        if d > dist[u]:
            continue
        if u == t:
            return d
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heap.push(nd, v)
    return -1 if dist[t] == INF else int(dist[t])
