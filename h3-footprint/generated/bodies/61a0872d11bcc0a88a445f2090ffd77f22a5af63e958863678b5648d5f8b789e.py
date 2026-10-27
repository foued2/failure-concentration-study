def solve(n, edges, s, t):
    distances = {s: 0}

    for _ in range(n):
        updated = False
        for u, v, w in edges:
            if u in distances:
                candidate = distances[u] + w
                if v not in distances or candidate < distances[v]:
                    distances[v] = candidate
                    updated = True
        if not updated:
            break

    return distances.get(t, -1)
