def solve(n, edges, s, t):
    # Custom binary min-heap over (dist, node) pairs
    out = [[] for _ in range(n)]
    for u, v, w in edges:
        out[u].append((v, w))
    heap = []
    size = 0

    def push(item):
        nonlocal size
        heap.append(item)
        i = size
        size += 1
        while i > 0:
            p = (i - 1) // 2
            if heap[p] <= heap[i]:
                break
            heap[p], heap[i] = heap[i], heap[p]
            i = p

    def pop():
        nonlocal size
        top = heap[0]
        size -= 1
        last = heap.pop()
        if size:
            heap[0] = last
            i = 0
            while True:
                l, r, m = 2 * i + 1, 2 * i + 2, i
                if l < size and heap[l] < heap[m]:
                    m = l
                if r < size and heap[r] < heap[m]:
                    m = r
                if m == i:
                    break
                heap[i], heap[m] = heap[m], heap[i]
                i = m
        return top

    dist = [None] * n
    push((0, s))
    while size:
        d, u = pop()
        if dist[u] is not None:
            continue
        dist[u] = d
        if u == t:
            return d
        for v, w in out[u]:
            if dist[v] is None:
                push((d + w, v))
    return -1
