"""Deterministic probe construction: 5 probes per family, exact-one predicate satisfaction."""
from __future__ import annotations

import hashlib


def stable_seed(*parts: object) -> int:
    key = ":".join(str(p) for p in parts).encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:4], "big")


def _build_f1(v: int) -> tuple[int, list[tuple[int, int, int]], int, int]:
    n = 4 + v
    edges = [(i, i + 1, 10 + i + v) for i in range(n - 1)]  # unique weights, t isolated as target
    # t = n-1 has no INCOMING edges; chain covers 0..n-2 but last chain edge must not reach t
    edges = [(i, i + 1, 10 + i + v) for i in range(n - 2)]
    return n, edges, 0, n - 1


def _build_f2(v: int) -> tuple[int, list[tuple[int, int, int]], int, int]:
    n = 4 + v
    # unique path 0 -> 1 -> ... -> n-1; first edge weight 0; all other weights distinct >= 1
    edges = [(i, i + 1, 1 if i > 0 else 0) for i in range(n - 1)]
    # weights: 0, then 1,1,1... -> plateau! fix: distinct positives
    edges = [(i, i + 1, 0 if i == 0 else 2 + i + v) for i in range(n - 1)]
    return n, edges, 0, n - 1


def _build_f3(v: int) -> tuple[int, list[tuple[int, int, int]], int, int]:
    n = 4 + v
    a, b = 2 + v, 10 + v  # parallel s->t weights, different, both >= 1
    edges = [(0, n - 1, a), (0, n - 1, b)]
    # filler unique-path branch with fresh distinct weights, avoiding plateau and zero
    for i in range(n - 2):
        edges.append((i, i + 1, 20 + v + i))
    return n, edges, 0, n - 1


def _build_f4(v: int) -> tuple[int, list[tuple[int, int, int]], int, int]:
    n = 4 + v
    edges = [(i, i + 1, 2 + v + i) for i in range(n - 1)]  # unique path, distinct weights
    edges.append((1, 1, 50 + v))  # self-loop, fresh weight
    return n, edges, 0, n - 1


def _build_f5(v: int) -> tuple[int, list[tuple[int, int, int]], int, int]:
    # two internally disjoint paths s->a->t and s->b->t with equal total weight, 4 distinct weights
    base = 1 + v
    w1, w2 = base, base + 3
    w3, w4 = base + 1, base + 2  # w1+w2 == w3+w4, all four distinct
    n = 4
    edges = [(0, 1, w1), (1, 3, w2), (0, 2, w3), (2, 3, w4)]
    return n, edges, 0, 3


def _build_f6(v: int) -> tuple[int, list[tuple[int, int, int]], int, int]:
    n = 4
    p = 3 + v  # plateau value, >= 3
    edges = [(0, 1, p), (1, 2, p), (2, 3, p)]  # exactly 3 edges share weight p; unique path
    return n, edges, 0, 3


BUILDERS = {
    "F1": _build_f1,
    "F2": _build_f2,
    "F3": _build_f3,
    "F4": _build_f4,
    "F5": _build_f5,
    "F6": _build_f6,
}


def make_probe_suite(instance_seed: int) -> list[dict]:
    """30 probes, family-major: F1 variants 0-4, then F2, ... F6."""
    from .families import FAMILY_ORDER, PREDICATES

    probes: list[dict] = []
    for fam in FAMILY_ORDER:
        for v in range(5):
            n, edges, s, t = BUILDERS[fam](v)
            pred = PREDICATES[fam](n, edges, s, t)
            sat = [PREDICATES[f](n, edges, s, t) for f in FAMILY_ORDER]
            probes.append(
                {
                    "probe_id": f"{fam}_{v}",
                    "family": fam,
                    "variant": v,
                    "n": n,
                    "edges": edges,
                    "s": s,
                    "t": t,
                    "assigned_predicate": pred,
                    "sat_vector": sat,
                    "seed": stable_seed(instance_seed, "probe", fam, v),
                }
            )
    return probes
