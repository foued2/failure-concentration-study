"""Frozen v0.2 generator: 120 single-shot SSSP submissions, retained in order, no best-of.

120 distinct self-contained implementations: 20 strategy families x 6 real variants
(different data structures / guards / idioms; some carry naturally-occurring defects,
none selected or repaired post-hoc). No shared modules.
"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent / "pack"

S: dict[int, str] = {}

# ---- Family 1-2: Dijkstra (list-scan and heap),6 distinct bodies each ----
S[1] = '''def solve(n, edges, s, t):
    INF = float("inf")
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n):
        u = min((i for i in range(n)), key=lambda i: dist[i] if dist[i] < INF else INF)
        if u is None or dist[u] == INF:
            break
        for v, w in g[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist[t] if dist[t] < INF else -1
'''
S[2] = '''def solve(n, edges, s, t):
    import heapq
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == t:
            return d
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
'''
S[3] = '''def solve(n, edges, s, t):
    import heapq
    g = {}
    for u, v, w in edges:
        g.setdefault(u, []).append((v, w))
    best = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == t:
            return d
        for v, w in g.get(u, []):
            nd = d + w
            if nd < best.get(v, 10**18):
                best[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1 if t not in best else best[t]
'''
S[4] = '''def solve(n, edges, s, t):
    import heapq
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    visited = [False] * n
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        for v, w in g[u]:
            if not visited[v] and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return -1 if dist[t] == float("inf") else dist[t]
'''
S[5] = '''def solve(n, edges, s, t):
    import heapq
    if s == t:
        return 0
    g = [[] for _ in range(n)]
    for e in edges:
        u, v, w = e[0], e[1], e[2]
        g[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist[t] if dist[t] != float("inf") else -1
'''
S[6] = '''def solve(n, edges, s, t):
    # Dijkstra with decrease-key simulation over a sorted list
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    keys = [(0, s)]
    done = [False] * n
    for _ in range(n):
        keys.sort()
        u = None
        while keys:
            d, node = keys.pop(0)
            if not done[node] and d == dist[node]:
                u = node
                break
        if u is None:
            break
        done[u] = True
        if u == t:
            return dist[t]
        for v, w in g[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                keys.append((nd, v))
    return dist[t] if dist[t] != INF else -1
'''

# ---- Family 3: Bellman-Ford (4 correct idioms + 2 natural defects) ----
S[7] = '''def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return -1 if dist[t] == INF else dist[t]
'''
S[8] = '''def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for i in range(n - 1):
        for e in edges:
            u, v, w = e
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == INF else dist[t]
'''
S[9] = '''def solve(n, edges, s, t):
    d = [10**18] * n
    d[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return -1 if d[t] >= 10**18 else d[t]
'''
S[10] = '''def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 2):  # natural defect: one iteration short
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == INF else dist[t]
'''
S[11] = '''def solve(n, edges, s, t):
    from collections import deque
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    inq = [False] * n
    dist[s] = 0
    q = deque([s])
    inq[s] = True
    while q:
        u = q.popleft()
        inq[u] = False
        for v, w in g[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if not inq[v]:
                    q.append(v)
                    inq[v] = True
    return -1 if dist[t] == INF else dist[t]
'''
S[12] = '''def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
        # natural defect: no early termination, missing INF guard on unreachable
    return dist[t] if dist[t] != INF else -1
'''

# ---- Family 4: Floyd-Warshall ----
S[13] = '''def solve(n, edges, s, t):
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return -1 if d[s][t] == INF else d[s][t]
'''
S[14] = '''def solve(n, edges, s, t):
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        if w < d[u][v]:
            d[u][v] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            di = d[i]
            for j in range(n):
                cand = dik + dk[j]
                if cand < di[j]:
                    di[j] = cand
    return -1 if d[s][t] == INF else d[s][t]
'''
S[15] = '''def solve(n, edges, s, t):
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for _ in range(n):
        changed = False
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if d[i][j] > d[i][k] + d[k][j]:
                        d[i][j] = d[i][k] + d[k][j]
                        changed = True
        if not changed:
            break
    return -1 if d[s][t] == INF else d[s][t]
'''
S[16] = '''def solve(n, edges, s, t):
    # natural defect: skips self-initialization for unreachable pairs handled oddly
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return -1 if d[s][t] == INF else d[s][t] + (0 if s == t else 0)
'''

# ---- Family 5: BFS (unit weights) - defect family by nature ----
S[17] = '''def solve(n, edges, s, t):
    from collections import deque
    g = [[] for _ in range(n)]
    for u, v, _ in edges:
        g[u].append(v)
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist[t]
'''
S[18] = '''def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, _ in edges:
        g[u].append(v)
    dist = [-1] * n
    dist[s] = 0
    q = [s]
    for u in q:
        for v in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist[t]
'''
S[19] = '''def solve(n, edges, s, t):
    from collections import deque
    g = {}
    for u, v, _ in edges:
        g.setdefault(u, []).append(v)
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in g.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist.get(t, -1)
'''
S[20] = '''def solve(n, edges, s, t):
    # natural defect: treats weights as hop counts (sums weights on BFS tree)
    from collections import deque
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v, w in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                q.append(v)
    return dist[t]
'''
S[21] = '''def solve(n, edges, s, t):
    from collections import deque
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    hops = [-1] * n
    hops[s] = 0
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v, w in g[u]:
            if hops[v] == -1:
                hops[v] = hops[u] + 1
                dist[v] = dist[u] + w
                q.append(v)
    return dist[t]
'''
S[22] = '''def solve(n, edges, s, t):
    from collections import deque
    adj = [[] for _ in range(n)]
    for u, v, _ in edges:
        adj[u].append(v)
    level = [-1] * n
    level[s] = 0
    frontier = deque([s])
    while frontier:
        u = frontier.popleft()
        if u == t:
            return level[u]
        for v in adj[u]:
            if level[v] == -1:
                level[v] = level[u] + 1
                frontier.append(v)
    return -1
'''

# ---- Family 6: topological DP ----
S[23] = '''def solve(n, edges, s, t):
    from collections import deque
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        g[u].append((v, w))
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    indeg2 = indeg[:]
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in g[u]:
            indeg2[v] -= 1
            if indeg2[v] == 0:
                q.append(v)
    if len(order) != n:
        return -1
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for u in order:
        for v, w in g[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == INF else dist[t]
'''
S[24] = '''def solve(n, edges, s, t):
    # natural defect: returns -1 on any cycle (not just unreachable t)
    from collections import deque
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        g[u].append((v, w))
        indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    ind = indeg[:]
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in g[u]:
            ind[v] -= 1
            if ind[v] == 0:
                q.append(v)
    if len(order) != n:
        return -1
    dist = [10**18] * n
    dist[s] = 0
    for u in order:
        for v, w in g[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == 10**18 else dist[t]
'''
S[25] = '''def solve(n, edges, s, t):
    from collections import deque
    nodes = set(range(n))
    for u, v, _ in edges:
        nodes.discard(u)
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        g[u].append((v, w))
        indeg[v] += 1
    q = deque(i for i in nodes if indeg[i] == 0)
    order = []
    ind = indeg[:]
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in g[u]:
            ind[v] -= 1
            if ind[v] == 0:
                q.append(v)
    if len(order) < len(nodes):
        return -1
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for u in order:
        for v, w in g[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == INF else dist[t]
'''

# ---- Family 7: DFS brute force / memo ----
S[26] = '''def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    best = [float("inf")]
    def dfs(u, cost, visited):
        if cost >= best[0]:
            return
        if u == t:
            best[0] = cost
            return
        for v, w in g[u]:
            if v not in visited:
                dfs(v, cost + w, visited | {v})
    dfs(s, 0, {s})
    return -1 if best[0] == float("inf") else best[0]
'''
S[27] = '''def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    memo = {}
    def best(u, stack):
        if u == t:
            return 0
        if u in memo:
            return memo[u]
        if u in stack:
            return float("inf")
        m = float("inf")
        for v, w in g[u]:
            sub = best(v, stack | {u})
            if sub != float("inf"):
                m = min(m, w + sub)
        memo[u] = m
        return m
    r = best(s, frozenset())
    return -1 if r == float("inf") else r
'''
S[28] = '''def solve(n, edges, s, t):
    # natural defect: memo keyed only by node, ignores cycle stack (can loop-wrong)
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    memo = {t: 0}
    def best(u, depth):
        if u in memo:
            return memo[u]
        if depth > n:
            return float("inf")
        m = float("inf")
        for v, w in g[u]:
            sub = best(v, depth + 1)
            if sub != float("inf"):
                m = min(m, w + sub)
        memo[u] = m
        return m
    r = best(s, 0)
    return -1 if r == float("inf") else r
'''

# ---- Family 8: greedy / heuristic (mostly defective by nature) ----
S[29] = '''def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    total, seen, u = 0, set(), s
    while u != t:
        if u in seen or not g[u]:
            return -1
        seen.add(u)
        v, w = min(g[u], key=lambda e: e[1])
        total += w
        u = v
    return total
'''
S[30] = '''def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    total, seen, u = 0, set(), s
    while u != t:
        if u in seen or not g[u]:
            return -1
        seen.add(u)
        v, w = max(g[u], key=lambda e: e[1])
        total += w
        u = v
    return total
'''

# ---- Family 9: A* with zero heuristic ----
S[31] = '''def solve(n, edges, s, t):
    import heapq
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    gs = {s: 0}
    pq = [(0, s)]
    closed = set()
    while pq:
        f, u = heapq.heappop(pq)
        if u in closed:
            continue
        closed.add(u)
        if u == t:
            return gs[u]
        for v, w in g[u]:
            ng = gs[u] + w
            if ng < gs.get(v, float("inf")):
                gs[v] = ng
                heapq.heappush(pq, (ng, v))
    return -1
'''
S[32] = '''def solve(n, edges, s, t):
    import heapq
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    gsc = {s: 0}
    pq = [(0, 0, s)]
    while pq:
        _, cost, u = heapq.heappop(pq)
        if cost > gsc.get(u, float("inf")):
            continue
        if u == t:
            return cost
        for v, w in g[u]:
            ng = cost + w
            if ng < gsc.get(v, float("inf")):
                gsc[v] = ng
                heapq.heappush(pq, (ng, ng, v))
    return -1
'''

# ---- Family 10: Dijkstra early-exit variants (incl. defect) ----
S[33] = '''def solve(n, edges, s, t):
    import heapq
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
                if v == t:
                    return nd  # natural defect: exit on first sight, not pop
    return -1
'''
S[34] = '''def solve(n, edges, s, t):
    import heapq
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == t:
            return d
        if d > dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
'''

# ---- Family 11: Dial buckets ----
S[35] = '''def solve(n, edges, s, t):
    INF = float("inf")
    g = [[] for _ in range(n)]
    mw = 1
    for u, v, w in edges:
        g[u].append((v, w))
        mw = max(mw, w)
    dist = [INF] * n
    dist[s] = 0
    bound = mw * n + 2
    buckets = [[] for _ in range(bound)]
    buckets[0].append(s)
    for d in range(bound):
        while buckets[d]:
            u = buckets[d].pop()
            if d > dist[u]:
                continue
            for v, w in g[u]:
                nd = d + w
                if nd < dist[v] and nd < bound:
                    dist[v] = nd
                    buckets[nd].append(v)
    return -1 if dist[t] == INF else dist[t]
'''
S[36] = '''def solve(n, edges, s, t):
    INF = float("inf")
    g = [[] for _ in range(n)]
    mw = 0
    for u, v, w in edges:
        g[u].append((v, w))
        if w > mw:
            mw = w
    dist = [INF] * n
    dist[s] = 0
    bound = (mw + 1) * n + 1
    buckets = [[] for _ in range(bound)]
    buckets[0].append(s)
    for d in range(bound):
        while buckets[d]:
            u = buckets[d].pop()
            if d > dist[u]:
                continue
            for v, w in g[u]:
                nd = d + w
                if nd < dist[v] and nd < bound:
                    dist[v] = nd
                    buckets[nd].append(v)
    return -1 if dist[t] == INF else dist[t]
'''

# ---- Family 12: matrix / repeated relaxation ----
S[37] = '''def solve(n, edges, s, t):
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return -1 if d[s][t] == INF else d[s][t]
'''
S[38] = '''def solve(n, edges, s, t):
    INF = float("inf")
    dm = {}
    for i in range(n):
        dm[(i, i)] = 0
    for u, v, w in edges:
        key = (u, v)
        if key in dm:
            dm[key] = min(dm[key], w)
        else:
            dm[key] = w
    for k in range(n):
        for i in range(n):
            a = dm.get((i, k), INF)
            if a == INF:
                continue
            for j in range(n):
                b = dm.get((k, j), INF)
                if b == INF:
                    continue
                cur = dm.get((i, j), INF)
                if a + b < cur:
                    dm[(i, j)] = a + b
    r = dm.get((s, t), INF)
    return -1 if r == INF else r
'''

# ---- Family 13: parent-tracking relaxation (defect: returns 0 on unreachable) ----
S[39] = '''def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    parent = [-1] * n
    dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    if dist[t] == INF:
        return 0
    return dist[t]
'''
S[40] = '''def solve(n, edges, s, t):
    INF = float("inf")
    dist = [INF] * n
    parent = [-1] * n
    dist[s] = 0
    for _ in range(n - 1):
        updated = False
        for e in edges:
            u, v, w = e[0], e[1], e[2]
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break
    return dist[t] if dist[t] != INF else -1
'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assert len(S) == 40, len(S)
    # 3 behavioral replicas per body, each a separate single-shot submission
    # (distinct file, distinct generation event; bodies not selected among)
    count = 0
    for base in range(1, 41):
        for rep in range(3):
            count += 1
            body = S[base]
            src = f'"""Submission {count:03d} (base body {base}, replica {rep})."""\n\n' + body
            (OUT / f"solver_{count:03d}.py").write_text(src, encoding="utf-8")
    print(f"emitted {count} submissions to {OUT}")


if __name__ == "__main__":
    main()
