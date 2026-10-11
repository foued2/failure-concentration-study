"""Instance and hidden-suite generators. Hidden suite uses an independent code path."""
from __future__ import annotations

import random

from .probes import stable_seed


def make_instance(seed: int) -> dict:
    rng = random.Random(stable_seed(seed, "anchor"))
    n = rng.randint(8, 13)
    m = int(2.2 * n)
    edges = []
    for _ in range(m):
        u = rng.randrange(n)
        v = rng.randrange(n)
        while v == u:
            v = rng.randrange(n)
        edges.append((u, v, rng.randint(1, 9)))
    return {"seed": seed, "n": n, "edges": edges, "s": 0, "t": n - 1}


def make_hidden_suite(seed: int, m_count: int = 20) -> list[dict]:
    """Independent construction: random graphs (n 5..8, w 0..9) + fixed edge-case templates."""
    rng = random.Random(stable_seed(seed, "hidden"))
    suite: list[dict] = []
    for i in range(15):
        n = rng.randint(5, 8)
        m = max(n - 1, int(1.8 * n))
        edges = []
        for _ in range(m):
            u = rng.randrange(n)
            v = rng.randrange(n)
            while v == u:
                v = rng.randrange(n)
            edges.append((u, v, rng.randint(0, 9)))
        suite.append({"hid": f"r{i}", "n": n, "edges": edges, "s": 0, "t": n - 1})
    templates = [
        {"hid": "e0", "n": 2, "edges": [(0, 1, 1 + seed % 7)], "s": 0, "t": 1},
        {"hid": "e1", "n": 3, "edges": [(0, 1, 1)], "s": 0, "t": 2},
        {"hid": "e2", "n": 4, "edges": [(0, 1, 0), (1, 2, 1), (2, 3, 1)], "s": 0, "t": 3},
        {"hid": "e3", "n": 3, "edges": [(0, 1, 2), (0, 1, 5), (1, 2, 1)], "s": 0, "t": 2},
        {"hid": "e4", "n": 20, "edges": [(i, i + 1, 1 + (i + seed) % 4) for i in range(19)], "s": 0, "t": 19},
    ]
    suite.extend(templates[: m_count - 15])
    return suite
