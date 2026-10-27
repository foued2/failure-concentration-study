def solve(n, edges, s, t):
    import heapq
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        rev[v].append((u, w))
    f = [None] * n
    b = [None] * n
    f[s] = 0
    b[t] = 0
    hf = [(0, s)]
    hb = [(0, t)]
    mu = None
    forward = True
    while hf and hb:
        if forward:
            d = None
            while hf:
                cand, u = heapq.heappop(hf)
                if cand == f[u]:
                    d = cand
                    break
            if d is None:
                break
            if b[u] is not None:
                c = d + b[u]
                if mu is None or c < mu:
                    mu = c
            if u == t:
                return d
            if mu is not None and d >= mu:
                return mu
            for v, w in adj[u]:
                nd = d + w
                if f[v] is None or nd < f[v]:
                    f[v] = nd
                    heapq.heappush(hf, (nd, v))
        else:
            d = None
            while hb:
                cand, u = heapq.heappop(hb)
                if cand == b[u]:
                    d = cand
                    break
            if d is None:
                break
            if f[u] is not None:
                c = f[u] + d
                if mu is None or c < mu:
                    mu = c
            if u == s:
                return d
            if mu is not None and d >= mu:
                return mu
            for v, w in rev[u]:
                nd = d + w
                if b[v] is None or nd < b[v]:
                    b[v] = nd
                    heapq.heappush(hb, (nd, v))
        forward = not forward
    return -1
