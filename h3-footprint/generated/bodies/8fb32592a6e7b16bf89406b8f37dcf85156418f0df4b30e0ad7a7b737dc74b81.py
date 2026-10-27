def solve(n, edges, s, t):
    INF = float("inf")
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = [INF] * n
    dist[s] = 0

    keys = []
    nodes = []
    place = [-1] * n

    def swap(i, j):
        keys[i], keys[j] = keys[j], keys[i]
        nodes[i], nodes[j] = nodes[j], nodes[i]
        place[nodes[i]] = i
        place[nodes[j]] = j

    def sift_up(i):
        while i > 0:
            p = (i - 1) // 2
            if keys[p] <= keys[i]:
                break
            swap(i, p)
            i = p

    def sift_down(i):
        size = len(keys)
        while True:
            left = 2 * i + 1
            right = left + 1
            smallest = i
            if left < size and keys[left] < keys[smallest]:
                smallest = left
            if right < size and keys[right] < keys[smallest]:
                smallest = right
            if smallest == i:
                break
            swap(i, smallest)
            i = smallest

    def push(node, key):
        place[node] = len(keys)
        keys.append(key)
        nodes.append(node)
        sift_up(len(keys) - 1)

    def pop_min():
        swap(0, len(keys) - 1)
        node = nodes.pop()
        key = keys.pop()
        place[node] = -1
        if keys:
            sift_down(0)
        return key, node

    def decrease(node, key):
        i = place[node]
        keys[i] = key
        sift_up(i)

    push(s, 0)
    while keys:
        d, u = pop_min()
        if u == t:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                if place[v] >= 0:
                    decrease(v, nd)
                else:
                    push(v, nd)
    return -1 if dist[t] == INF else int(dist[t])
