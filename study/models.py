"""Models A/B, relabel control, LOIO grouped CV, bootstrap. Pure stdlib."""
from __future__ import annotations

import math

from .features import balanced_groups, relabelled_concentration

KNOTS = [1.0986122886681098, 1.6094379124341003, 2.302585092994046, 2.995732273553991, 3.4339872044851463]
RIDGE = 1e-6
MAX_ITER = 50


def _pos(x: float) -> float:
    return x if x > 0 else 0.0


def rcs_basis(x: float, knots: list[float] = KNOTS) -> list[float]:
    t1, tk = knots[0], knots[-1]
    cols = [x]
    for j in range(1, len(knots) - 1):
        tj = knots[j]
        d = (_pos(x - tj) ** 3 - _pos(x - tk) ** 3) - ((tk - tj) / (tk - t1)) * (
            _pos(x - t1) ** 3 - _pos(x - tk) ** 3
        )
        cols.append(d / (tk - t1) ** 2)
    return cols


def design_row(k: int, c: float | None) -> list[float]:
    x = math.log(1 + k)
    row = [1.0] + rcs_basis(x)
    if c is not None:
        row.append(c)
    return row


def _expit(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def _solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            m[piv][col] = 1e-12
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r == col:
                continue
            f = m[r][col] / m[col][col]
            for cc in range(col, n + 1):
                m[r][cc] -= f * m[col][cc]
    return [m[i][n] / m[i][i] for i in range(n)]


def logistic_fit(x_rows: list[list[float]], y: list[int]) -> list[float]:
    p = len(x_rows[0])
    beta = [0.0] * p
    for _ in range(MAX_ITER):
        xtwx = [[RIDGE if i == j else 0.0 for j in range(p)] for i in range(p)]
        xtwz = [0.0] * p
        for row, yi in zip(x_rows, y):
            eta = sum(b * xi for b, xi in zip(beta, row))
            pr = min(max(_expit(eta), 1e-12), 1 - 1e-12)
            w = pr * (1 - pr) + 1e-12
            z = eta + (yi - pr) / w
            for i in range(p):
                for j in range(p):
                    xtwx[i][j] += w * row[i] * row[j]
                xtwz[i] += w * row[i] * z
        new = _solve_linear(xtwx, xtwz)
        if max(abs(a - b) for a, b in zip(new, beta)) < 1e-10:
            return new
        beta = new
    return beta


def _predict(beta: list[float], row: list[float]) -> float:
    return min(max(_expit(sum(b * xi for b, xi in zip(beta, row))), 1e-12), 1 - 1e-12)


def log_loss(y: int, p: float) -> float:
    return -(y * math.log(p) + (1 - y) * math.log(1 - p))


def loo_delta(obs: list[dict]) -> tuple[list[float], float]:
    """obs: [{'instance': idx, 'k': int, 'C': float, 'Y': int}]. Returns (delta_i per instance, mean)."""
    instances = sorted({o["instance"] for o in obs})
    deltas: list[float] = []
    for i in instances:
        train = [o for o in obs if o["instance"] != i]
        test = [o for o in obs if o["instance"] == i]
        if not test or not train:
            deltas.append(float("nan"))
            continue
        xa_tr = [design_row(o["k"], None) for o in train]
        xb_tr = [design_row(o["k"], o["C"]) for o in train]
        ya = [o["Y"] for o in train]
        ba = logistic_fit(xa_tr, ya)
        bb = logistic_fit(xb_tr, ya)
        la = sum(log_loss(o["Y"], _predict(ba, design_row(o["k"], None))) for o in test) / len(test)
        lb = sum(log_loss(o["Y"], _predict(bb, design_row(o["k"], o["C"]))) for o in test) / len(test)
        deltas.append(la - lb)
    finite = [d for d in deltas if not math.isnan(d)]
    return deltas, (sum(finite) / len(finite) if finite else float("nan"))


def bootstrap_ci(delta_i: list[float], n_boot: int = 10000, seed: int = 99) -> tuple[float, float]:
    import random

    vals = [d for d in delta_i if not math.isnan(d)]
    n = len(vals)
    if n == 0:
        return (float("nan"), float("nan"))
    rng = random.Random(seed)
    means = sorted(sum(rng.choice(vals) for _ in range(n)) / n for _ in range(n_boot))
    lo = means[int(0.025 * n_boot)]
    hi = means[min(int(0.975 * n_boot), n_boot - 1)]
    return lo, hi


def relabel_control_deltas(pairs: list[dict], instance_seeds: dict[int, int], r_max: int = 100) -> list[float]:
    """pairs: [{'instance', 'fails', 'Y'}]. Returns list of Δ_real-sized means under relabeling."""
    results: list[float] = []
    for r in range(1, r_max + 1):
        obs = []
        for pr in pairs:
            groups = balanced_groups(instance_seeds[pr["instance"]], r)
            c = relabelled_concentration(pr["fails"], groups)
            obs.append({"instance": pr["instance"], "k": pr["k"], "C": c, "Y": pr["Y"]})
        _, delta = loo_delta(obs)
        results.append(delta)
    return results
