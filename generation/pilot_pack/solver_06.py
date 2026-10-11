"""Directive: brute-force path enumeration."""


def solve(n, edges, s, t):
    best = [float("inf")]

    def dfs(u, cost, visited, used):
        if u == t:
            if cost < best[0]:
                best[0] = cost
            return
        for i, (a, b, w) in enumerate(edges):
            if i in used or a != u or b in visited:
                continue
            dfs(b, cost + w, visited | {b}, used | {i})

    dfs(s, 0, {s}, set())
    return -1 if best[0] == float("inf") else best[0]
