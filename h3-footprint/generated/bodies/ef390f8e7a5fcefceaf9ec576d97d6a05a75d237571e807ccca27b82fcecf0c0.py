def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    settled = set()
    pending = {0: [s]}
    while pending:
        d = min(pending)
        layer = pending.pop(d)
        nxt = []
        for u in layer:
            if u in settled:
                continue
            settled.add(u)
            if u == t:
                return d
            for v, w in adj[u]:
                if v not in settled:
                    pending.setdefault(d + w, []).append(v)
    return -1
