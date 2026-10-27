def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    class _PQ:
        __slots__ = ("key", "item", "idx")

        def __init__(self):
            self.key = []
            self.item = []
            self.idx = {}

        def _swap(self, i, j):
            self.key[i], self.key[j] = self.key[j], self.key[i]
            self.item[i], self.item[j] = self.item[j], self.item[i]
            self.idx[self.item[i]] = i
            self.idx[self.item[j]] = j

        def _up(self, i):
            while i > 0:
                p = (i - 1) // 2
                if self.key[p] <= self.key[i]:
                    break
                self._swap(i, p)
                i = p

        def _down(self, i):
            size = len(self.key)
            while True:
                l = 2 * i + 1
                r = l + 1
                m = i
                if l < size and self.key[l] < self.key[m]:
                    m = l
                if r < size and self.key[r] < self.key[m]:
                    m = r
                if m == i:
                    break
                self._swap(i, m)
                i = m

        def decrease(self, node, k):
            i = self.idx.get(node)
            if i is None:
                self.key.append(k)
                self.item.append(node)
                self.idx[node] = len(self.key) - 1
                self._up(len(self.key) - 1)
            elif k < self.key[i]:
                self.key[i] = k
                self._up(i)

        def pop(self):
            last = len(self.key) - 1
            self._swap(0, last)
            node = self.item.pop()
            k = self.key.pop()
            del self.idx[node]
            if self.key:
                self._down(0)
            return k, node

        def __bool__(self):
            return bool(self.key)

    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    pq = _PQ()
    pq.decrease(s, 0)
    while pq:
        d, u = pq.pop()
        if d > dist[u]:
            continue
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                pq.decrease(v, nd)
    return -1
