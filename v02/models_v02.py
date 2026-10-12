"""v0.2 analysis: pair-level soft-label logistic with instance-equal weights,
LOIO scoring aggregated pair -> instance, shared-partition relabel control."""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from study.models import KNOTS, RIDGE, design_row, log_loss, rcs_basis  # v0.1-frozen basis

MAX_ITER = 50
R_RELABEL = 200


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


def logistic_fit_weighted(x_rows: list[list[float]], y: list[float], w: list[float]) -> list[float]:
    """Weighted logistic MLE; y may be fractional (soft labels)."""
    p = len(x_rows[0])
    beta = [0.0] * p
    for _ in range(MAX_ITER):
        xtwx = [[RIDGE if i == j else 0.0 for j in range(p)] for i in range(p)]
        xtwz = [0.0] * p
        for row, yi, wi in zip(x_rows, y, w):
            eta = sum(b * xi for b, xi in zip(beta, row))
            pr = min(max(_expit(eta), 1e-12), 1 - 1e-12)
            wv = wi * pr * (1 - pr) + 1e-15
            z = eta + (yi - pr) / (pr * (1 - pr) + 1e-15)
            for i in range(p):
                for j in range(p):
                    xtwx[i][j] += wv * row[i] * row[j]
                xtwz[i] += wv * row[i] * z
        new = _solve_linear(xtwx, xtwz)
        if max(abs(a - b) for a, b in zip(new, beta)) < 1e-10:
            return new
        beta = new
    return beta


def _predict(beta: list[float], row: list[float]) -> float:
    return min(max(_expit(sum(b * xi for b, xi in zip(beta, row))), 1e-12), 1 - 1e-12)


def build_pairs(obs: list[dict]) -> list[dict]:
    """obs: eligible pairs {'instance','k','C','fails','successes'} -> pair rows with soft label/weight."""
    by_inst: dict[int, list[dict]] = {}
    for o in obs:
        by_inst.setdefault(o["instance"], []).append(o)
    pairs = []
    for inst, rows in by_inst.items():
        n = len(rows)
        for o in rows:
            pairs.append(
                {
                    "instance": inst,
                    "k": o["k"],
                    "C": o["C"],
                    "y": o["successes"] / 20.0,
                    "w": 1.0 / n,
                }
            )
    return pairs


def loo_delta_pairs(pairs: list[dict]) -> tuple[list[float], float]:
    """LOIO: fit on other instances (weighted soft-label), score held-out instance
    via pair mean log-loss with soft label, then equal instance weights."""
    instances = sorted({p["instance"] for p in pairs})
    deltas: list[float] = []
    for i in instances:
        train = [p for p in pairs if p["instance"] != i]
        test = [p for p in pairs if p["instance"] == i]
        if not test or not train:
            deltas.append(float("nan"))
            continue
        xa = [design_row(p["k"], None) for p in train]
        xb = [design_row(p["k"], p["C"]) for p in train]
        y = [p["y"] for p in train]
        w = [p["w"] for p in train]
        ba = logistic_fit_weighted(xa, y, w)
        bb = logistic_fit_weighted(xb, y, w)
        la = sum(log_loss(p["y"], _predict(ba, design_row(p["k"], None))) for p in test) / len(test)
        lb = sum(log_loss(p["y"], _predict(bb, design_row(p["k"], p["C"]))) for p in test) / len(test)
        deltas.append(la - lb)
    finite = [d for d in deltas if not math.isnan(d)]
    return deltas, (sum(finite) / len(finite) if finite else float("nan"))


def bootstrap_ci(delta_i: list[float], n_boot: int = 10000, seed: int = 99) -> tuple[float, float]:
    vals = [d for d in delta_i if not math.isnan(d)]
    n = len(vals)
    if n == 0:
        return (float("nan"), float("nan"))
    rng = random.Random(seed)
    means = sorted(sum(rng.choice(vals) for _ in range(n)) / n for _ in range(n_boot))
    return means[int(0.025 * n_boot)], means[min(int(0.975 * n_boot), n_boot - 1)]


def shared_relabel_groups(r: int) -> list[list[int]]:
    """One balanced partition of 30 probe slots, applied consistently across instances."""
    seed = int.from_bytes(__import__("hashlib").sha256(f"v02:relabel:{r}".encode()).digest()[:4], "big")
    rng = random.Random(seed)
    idx = list(range(30))
    rng.shuffle(idx)
    return [idx[i * 5 : (i + 1) * 5] for i in range(6)]


def relabel_pairs(obs: list[dict], groups: list[list[int]]) -> list[dict]:
    """Recompute C under relabelled groups; keep k, successes, weights."""
    out = []
    for o in obs:
        k = o["k"]
        c = max(sum(o["fails"][slot] for slot in g) for g in groups) / k if k else 0.0
        out.append({"instance": o["instance"], "k": k, "C": c, "successes": o["successes"], "fails": o["fails"]})
    return out


def relabel_control(obs: list[dict], r_max: int = R_RELABEL) -> list[float]:
    results = []
    for r in range(1, r_max + 1):
        groups = shared_relabel_groups(r)
        pairs = build_pairs(relabel_pairs(obs, groups))
        _, delta = loo_delta_pairs(pairs)
        results.append(delta)
    return results


def classify(delta: float, ci_lo: float, ci_hi: float, relabel_p95: float, delta_threshold: float = 0.01) -> str:
    if ci_lo > delta_threshold and delta > relabel_p95:
        return "POSITIVE"
    if ci_hi < delta_threshold:
        return "NEGATIVE"
    if delta >= delta_threshold and delta <= relabel_p95:
        return "AMBIGUOUS"
    if ci_hi >= delta_threshold and ci_lo <= delta_threshold:
        return "INCONCLUSIVE (CI straddles threshold)"
    return "INCONCLUSIVE"
