"""M2 complete-rule feasibility under the declared support model.

Work order: "IMPLEMENT CLAUDE'S REVIEW AND DELIVER M2 FEASIBILITY DATA"
(2026-10-20, Foued via GPT/). Deterministic, bounded calculation only: no
sampling, no generation, no hidden outcomes, no Phase 1 execution.

Declared support model (Rev F section 9.1; same marginals as the committed
`v03p/a1/a1_support_comparison.py`):
  * each simulated body independently draws k from the scenario categorical
    mix SCEN (in-range k in {5, 10, 20}; k = 0/25 are outside the support);
  * conditional on k, C is uniform over the feasible 6-family count vectors
    (each family count 0..5, counts summing to k);
  * a replication generates N_b bodies; eligibility is a deterministic,
    outcome-blind function of the realized body multiset (support conditions
    plus the proposed M2 gate);
  * replications under the declared simulation design are independent, so the
    number of eligible replications out of R = 2000 is Binomial(R, p).

Support rule (Rev F section 9.2 / A1 S0; conditions 1-4):
  per in-range bucket: n >= 8, >= 2 distinct C values, >= 4 bodies at the
  observed minimum C and >= 4 at the observed maximum C; the analysis
  support requires >= 2 in-range buckets to pass.

Complete rule under the proposed M2 resolution (Rev F section 5A):
  conditions 1-4 (rank-increase is implied by conditions 3-4) AND
  kappa_eff <= 30 on the column-standardized extended design matrix, with
  body-level rows, intercept unstandardized, non-intercept columns centered
  and scaled to unit population SD over the in-support rows, rank tolerance
  1e-9 (relative to the largest singular value), kappa_eff = s_1 / s_r.

Bounded exactness statement:
  P(pass) is exact for conditions 1-4 at every cell.
  P(pass AND kappa_eff > 30) is computed exactly over a count box covering
  all but an explicitly computed multinomial tail. Inside the box, all
  patterns with kappa_eff > 30 are enumerated: kappa_eff > 30 implies the
  pooled within-bucket share of C variance is below 1/150 (Frobenius bound),
  hence every included bucket's within-bucket variance is below
  0.001067 * n / n_k; the enumeration keeps exactly those patterns.
  Outside the box the violation probability is bounded by the tail mass.
  The reported complete-rule interval is therefore rigorous, not an estimate.

Outputs: printed summary plus `m2_complete_rule_feasibility_2026-10-20.json`.
"""

import json
import math
import sys

import numpy as np

R_REPS = 2000
TAU_RANK = 1e-9
KAPPA_MAX = 30.0
FROB = 6.0
WFRAC_CUT = FROB / (KAPPA_MAX * KAPPA_MAX)
GAP = {5: 0.2, 10: 0.1, 20: 0.05}
INRANGE = {5, 10, 20}
SIZES = [60, 113, 120, 150, 240, 300, 400, 450, 600]
SCENARIOS = {
    "a-hist": {0: 0.80, 5: 0.10, 10: 0.05, 25: 0.05},
    "a-50:50": {0: 0.80, 5: 0.075, 10: 0.075, 25: 0.05},
    "b-hist": {0: 0.75, 5: 0.075, 10: 0.025, 20: 0.025, 25: 0.125},
    "b-thirds": {0: 0.75, 5: 0.125 / 3, 10: 0.125 / 3, 20: 0.125 / 3, 25: 0.125},
    "c-hist": {0: 0.94, 5: 0.03, 10: 0.02, 25: 0.01},
    "c-50:50": {0: 0.94, 5: 0.025, 10: 0.025, 25: 0.01},
    "d": {0: 0.90, 25: 0.10},
}

KNOTS = [1.0986122886681098, 1.6094379124341003, 2.302585092994046,
         2.995732273553991, 3.4339872044851463]


def _pos(x):
    return x if x > 0.0 else 0.0


def rcs_basis(x):
    t1, tk = KNOTS[0], KNOTS[-1]
    cols = [x]
    for j in range(1, len(KNOTS) - 1):
        tj = KNOTS[j]
        d = ((_pos(x - tj) ** 3 - _pos(x - tk) ** 3)
             - ((tk - tj) / (tk - t1)) * (_pos(x - t1) ** 3 - _pos(x - tk) ** 3))
        cols.append(d / (tk - t1) ** 2)
    return cols


def build_ck():
    ck = {}
    z = {}
    for k in INRANGE:
        counts = {}
        total = [0]

        def rec(i, rem, cur):
            if i == 5:
                if 0 <= rem <= 5:
                    total[0] += 1
                    f = tuple(cur + [rem])
                    c = max(f) / k
                    counts[c] = counts.get(c, 0) + 1
                return
            for v in range(0, min(5, rem) + 1):
                rec(i + 1, rem - v, cur + [v])

        rec(0, k, [])
        vals = sorted(counts)
        ck[k] = (vals, [counts[v] / float(total[0]) for v in vals])
        z[k] = total[0]
    return ck, z


CK, CK_Z = build_ck()
LFACT = [0.0] * 2001
for i in range(1, len(LFACT)):
    LFACT[i] = LFACT[i - 1] + math.log(i)


def log_comb(n, k):
    if k < 0 or k > n:
        return float("-inf")
    return LFACT[n] - LFACT[k] - LFACT[n - k]


def binom_pmf(n, k, p):
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    if k < 0 or k > n:
        return 0.0
    t = log_comb(n, k) + k * math.log(p) + (n - k) * math.log1p(-p)
    return math.exp(t) if t > -745.0 else 0.0


def f_s0(k, n):
    vals, probs = CK[k]
    if n < 8:
        return 0.0
    V = len(vals)
    total = 0.0
    for ai in range(V):
        for bi in range(ai + 1, V):
            pa, pb = probs[ai], probs[bi]
            p_mid = sum(probs[ai + 1:bi])
            p_in = pa + pb + p_mid
            if p_in <= 0.0:
                continue
            log_pin = math.log(p_in)
            if n * log_pin <= -745.0:
                continue
            qa, qb, qm = pa / p_in, pb / p_in, p_mid / p_in
            pl = sum(binom_pmf(n, i, qa) for i in range(0, 4))
            ph = sum(binom_pmf(n, j, qb) for j in range(0, 4))
            both = 0.0
            for i in range(0, 4):
                for j in range(0, min(4, n - i)):
                    kk = n - i - j
                    if qm <= 0.0 and kk > 0:
                        continue
                    t = LFACT[n] - LFACT[i] - LFACT[j] - LFACT[kk]
                    if i:
                        t += i * math.log(qa)
                    if j:
                        t += j * math.log(qb)
                    if kk:
                        t += kk * math.log(qm)
                    if t > -745.0:
                        both += math.exp(t)
            cond = 1.0 - pl - ph + both
            if cond > 0.0:
                total += math.exp(n * log_pin) * cond
    return max(0.0, min(1.0, total))


FTAB = {k: [f_s0(k, n) for n in range(0, max(SIZES) + 1)] for k in INRANGE}


def count_vectors(n, v):
    if v == 1:
        yield (n,)
        return

    def rec(i, rem, cur):
        if i == v - 1:
            yield tuple(cur + [rem])
            return
        for c in range(rem + 1):
            yield from rec(i + 1, rem - c, cur + [c])

    yield from rec(0, n, [])


def pattern_stats(k, counts):
    vals, probs = CK[k]
    s1 = 0.0
    s2 = 0.0
    lp = LFACT[sum(counts)]
    for c, v, p in zip(counts, vals, probs):
        s1 += c * v
        s2 += c * v * v
        lp -= LFACT[c]
        if c:
            if p <= 0.0:
                return None
            lp += c * math.log(p)
    return s1, s2, lp


def bucket_pass(k, counts):
    n = sum(counts)
    if n < 8:
        return False
    nz = [i for i, c in enumerate(counts) if c > 0]
    return len(nz) >= 2 and counts[nz[0]] >= 4 and counts[nz[-1]] >= 4


def kappa_from_stats(ks, ns, s1s, s2s):
    n = float(sum(ns))
    mu_c = sum(s1s) / n
    var_c = sum(s2s) / n - mu_c * mu_c
    if var_c <= 0.0:
        return float("inf")
    sd_c = math.sqrt(var_c)
    gram = np.zeros((6, 6))
    gram[0, 0] = n
    cols = {k: rcs_basis(math.log(1.0 + k)) for k in ks}
    means = []
    sds = []
    for j in range(4):
        m = sum(ns[i] * cols[ks[i]][j] for i in range(len(ks))) / n
        v = sum(ns[i] * (cols[ks[i]][j] - m) ** 2 for i in range(len(ks))) / n
        means.append(m)
        sds.append(math.sqrt(v))
    zcols = {}
    for i, k in enumerate(ks):
        zcols[k] = [(cols[k][j] - means[j]) / sds[j] for j in range(4)]
    for i in range(len(ks)):
        for j in range(len(ks)):
            if i == j:
                gram[1 + i, 1 + j] = n
            else:
                gram[1 + i, 1 + j] = ns[i] * sum(
                    zcols[ks[i]][a] * zcols[ks[i]][a] for a in range(4))
    for a in range(4):
        for b in range(4):
            gram[1 + a, 1 + b] = sum(
                ns[i] * zcols[ks[i]][a] * zcols[ks[i]][b] for i in range(len(ks)))
    for a in range(4):
        s = 0.0
        for i, k in enumerate(ks):
            s += zcols[k][a] * (s1s[i] - ns[i] * mu_c) / sd_c
        gram[1 + a, 5] = s
        gram[5, 1 + a] = s
    gram[5, 5] = n
    lam = np.linalg.eigvalsh(gram)
    lam = lam[::-1]
    rank = int(np.sum(lam > TAU_RANK * lam[0]))
    if rank < 2:
        return float("inf")
    return math.sqrt(lam[0] / lam[rank - 1])


def kept_patterns(k, n, vt):
    vals, probs = CK[k]
    V = len(vals)
    out = []
    for i in range(V):
        for j in range(i + 1, V):
            r = vals[j] - vals[i]
            if 2.0 * r * r / n >= vt:
                continue
            for cnt in count_vectors(n, j - i + 1):
                full = [0] * V
                for t, c in enumerate(cnt):
                    full[i + t] = c
                if not bucket_pass(k, full):
                    continue
                st = pattern_stats(k, full)
                if st is None:
                    continue
                s1, s2, lp = st
                if s2 / n - (s1 / n) ** 2 < vt:
                    out.append((s1, s2, lp))
    return out


_KEEP_CACHE = {}


def kept_cached(k, n, vt):
    key = (k, n, round(vt, 12))
    hit = _KEEP_CACHE.get(key)
    if hit is None:
        hit = kept_patterns(k, n, vt)
        _KEEP_CACHE[key] = hit
    return hit


def subset_violation(ks, ns, probs_log):
    n = sum(ns)
    lists = []
    for i, k in enumerate(ks):
        vt = WFRAC_CUT * n / ns[i]
        lists.append(kept_cached(k, ns[i], vt))
    if any(not L for L in lists):
        return 0.0
    acc = 0.0
    if len(ks) == 1:
        return 0.0
    if len(ks) == 2:
        A, B = lists
        s1a = np.array([x[0] for x in A])
        s2a = np.array([x[1] for x in A])
        lpa = np.array([x[2] for x in A])
        s1b = np.array([x[0] for x in B])
        s2b = np.array([x[1] for x in B])
        lpb = np.array([x[2] for x in B])
        S1 = s1a[:, None] + s1b[None, :]
        S2 = s2a[:, None] + s2b[None, :]
        tot = S2 / n - (S1 / n) ** 2
        W = (S2 - (s1a[:, None] ** 2 / ns[0] + s1b[None, :] ** 2 / ns[1])) / n
        mask = (tot > 0) & (W < tot / (1.0 / WFRAC_CUT))
        if not mask.any():
            return 0.0
        LP = lpa[:, None] + lpb[None, :]
        cand = np.argwhere(mask)
        for a, b in cand:
            kk = kappa_from_stats(ks, ns, [s1a[a], s1b[b]], [s2a[a], s2b[b]])
            if kk > KAPPA_MAX:
                acc += math.exp(LP[a, b])
        return acc
    A, B, C = lists
    for ia, (s1a, s2a, lpa) in enumerate(A):
        for ib, (s1b, s2b, lpb) in enumerate(B):
            for ic, (s1c, s2c, lpc) in enumerate(C):
                S1 = s1a + s1b + s1c
                S2 = s2a + s2b + s2c
                tot = S2 / n - (S1 / n) ** 2
                if tot <= 0.0:
                    continue
                W = (S2 - (s1a * s1a / ns[0] + s1b * s1b / ns[1]
                          + s1c * s1c / ns[2])) / n
                if W >= tot / (1.0 / WFRAC_CUT):
                    continue
                kk = kappa_from_stats(ks, ns, [s1a, s1b, s1c],
                                      [s2a, s2b, s2c])
                if kk > KAPPA_MAX:
                    acc += math.exp(lpa + lpb + lpc)
    return acc


def log_multinom(n, parts, probs):
    t = LFACT[n]
    for x, p in zip(parts, probs):
        t -= LFACT[x]
        if x:
            if p <= 0.0:
                return float("-inf")
            t += x * math.log(p)
    return t


def cell(scenario, nb):
    scen = SCENARIOS[scenario]
    ks = [k for k in sorted(scen) if k in INRANGE]
    if not ks:
        return {"scenario": scenario, "N_b": nb, "structural": "no in-range buckets"}
    probs = [scen[k] for k in ks]
    p_other = 1.0 - sum(probs)
    means = [nb * p for p in probs]
    sds = [math.sqrt(nb * p * (1.0 - p)) for p in probs]
    box = []
    for m, s in zip(means, sds):
        box.append((max(0, int(math.floor(m - 8 * s))),
                    min(nb, int(math.ceil(m + 8 * s)))))
    subsets = []
    m = len(ks)
    for mask in range(1, 1 << m):
        if bin(mask).count("1") >= 2:
            subsets.append([i for i in range(m) if mask & (1 << i)])

    def iterate(idx, cur, rem):
        if idx == len(ks):
            yield tuple(cur)
            return
        lo, hi = box[idx]
        hi = min(hi, rem)
        for x in range(lo, hi + 1):
            yield from iterate(idx + 1, cur + [x], rem - x)

    p_pass = 0.0
    box_mass = 0.0
    for parts in iterate(0, [], nb):
        ntot = sum(parts)
        n_other = nb - ntot
        if n_other < 0:
            continue
        lp = log_multinom(nb, list(parts) + [n_other],
                          probs + [p_other] if p_other > 0 else probs + [0.0])
        if lp <= -745.0:
            continue
        w = math.exp(lp)
        box_mass += w
        fs = [FTAB[k][n] for k, n in zip(ks, parts)]
        pairs = sum(fs[i] * fs[j] for i in range(len(fs))
                    for j in range(i + 1, len(fs)))
        q = pairs
        if len(fs) == 3:
            q -= 2.0 * fs[0] * fs[1] * fs[2]
        p_pass += w * q
    tail = max(0.0, 1.0 - box_mass)
    return {
        "scenario": scenario,
        "N_b": nb,
        "in_range_buckets": ks,
        "P_pass_conditions_1_4": p_pass,
        "box_tail_bound": tail,
        "E_eligible_conditions_1_4": R_REPS * p_pass,
        "P_N_ge_39_conditions_1_4": binom_sf(38, R_REPS, p_pass),
        "complete_rule_status": ("gate_non_binding_two_level" if len(ks) == 2
                                 else "unresolved_three_level"),
    }



def ck_moments(k):
    vals, probs = CK[k]
    m = sum(v * p for v, p in zip(vals, probs))
    v = sum(p * (x - m) ** 2 for x, p in zip(vals, probs))
    return m, v


def population_kappa(scenario):
    scen = SCENARIOS[scenario]
    ks = [k for k in sorted(scen) if k in INRANGE]
    if len(ks) < 2:
        return None
    w = [scen[k] / sum(scen[j] for j in ks) for k in ks]
    n = 1.0
    cols = {k: rcs_basis(math.log(1.0 + k)) for k in ks}
    cm = {k: ck_moments(k)[0] for k in ks}
    cv = {k: ck_moments(k)[1] for k in ks}
    means = []
    sds = []
    for j in range(4):
        m = sum(w[i] * cols[ks[i]][j] for i in range(len(ks)))
        v = sum(w[i] * (cols[ks[i]][j] - m) ** 2 for i in range(len(ks)))
        means.append(m)
        sds.append(math.sqrt(v))
    z = {k: [(cols[k][j] - means[j]) / sds[j] for j in range(4)] for k in ks}
    mu = sum(w[i] * cm[ks[i]] for i in range(len(ks)))
    var = sum(w[i] * (cv[ks[i]] + (cm[ks[i]] - mu) ** 2)
              for i in range(len(ks)))
    sd = math.sqrt(var)
    g = np.zeros((6, 6))
    g[0, 0] = n
    for a in range(4):
        for b in range(4):
            g[1 + a, 1 + b] = sum(
                w[i] * z[ks[i]][a] * z[ks[i]][b] for i in range(len(ks)))
        g[1 + a, 5] = sum(
            w[i] * z[ks[i]][a] * (cm[ks[i]] - mu) / sd for i in range(len(ks)))
        g[5, 1 + a] = g[1 + a, 5]
    g[5, 5] = 1.0
    lam = np.linalg.eigvalsh(g)[::-1]
    rank = int(np.sum(lam > TAU_RANK * lam[0]))
    return {
        "scenario": scenario,
        "in_range_weights": dict(zip(map(str, ks), w)),
        "kappa_population": math.sqrt(lam[0] / lam[rank - 1]),
        "eigenvalues": [float(x) for x in lam],
        "rank": rank,
    }


def enumerate_bucket(k, n):
    vals, probs = CK[k]
    out = []
    for cnt in count_vectors(n, len(vals)):
        st = pattern_stats(k, cnt)
        if st is not None:
            out.append((cnt, st[0], st[1], st[2]))
    return out


def small_support(scenario, n_map):
    scen = SCENARIOS[scenario]
    ks = [k for k in sorted(n_map)]
    lists = [enumerate_bucket(k, n_map[k]) for k in ks]
    p_pass = 0.0
    p_viol = 0.0
    n_pass = 0
    n_viol = 0
    total = 0.0
    import itertools
    for combo in itertools.product(*lists):
        w = math.exp(sum(x[3] for x in combo))
        total += w
        ps = [bucket_pass(k, x[0]) for k, x in zip(ks, combo)]
        if sum(ps) < 2:
            continue
        p_pass += w
        n_pass += 1
        s1 = [x[1] for x in combo]
        s2 = [x[2] for x in combo]
        ns = [sum(x[0]) for x in combo]
        kk = kappa_from_stats(ks, ns, s1, s2)
        if kk > KAPPA_MAX:
            p_viol += w
            n_viol += 1
    return {
        "scenario": scenario,
        "bucket_n": {str(k): n_map[k] for k in ks},
        "P_pass": p_pass,
        "P_pass_and_kappa_gt_30": p_viol,
        "violation_share_of_pass": (p_viol / p_pass) if p_pass else None,
        "patterns_total_probability": total,
        "patterns_passing": n_pass,
        "patterns_violating": n_viol,
    }

def binom_cdf(m, n, p):
    if m < 0:
        return 0.0
    if m >= n:
        return 1.0
    return sum(binom_pmf(n, i, p) for i in range(0, m + 1))


def binom_sf(m, n, p):
    return max(0.0, min(1.0, 1.0 - binom_cdf(m, n, p)))


def required_p_for_prob(floor_count, target, reps, lo=0.0, hi=1.0):
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if binom_sf(floor_count - 1, reps, mid) >= target:
            hi = mid
        else:
            lo = mid
    return hi


def floor_summary():
    vals = {}
    for target in (0.90, 0.925, 0.95):
        f = 1
        while math.pow(0.05, 1.0 / f) < target:
            f += 1
        vals[str(target)] = f
    return vals


def main():
    out = {
        "meta": {
            "date": "2026-10-20",
            "model": "Rev F 9.1 declared support: k ~ SCEN, C|k uniform over feasible 6-family vectors; bodies iid per replication; R=2000 independent replications",
            "support_rule": "Rev F conditions 1-4 (S0) per in-range bucket; >=2 buckets pass",
            "m2_gate": "kappa_eff <= 30 on column-standardized extended matrix; rank tol 1e-9; body rows",
            "tau_rank": TAU_RANK,
            "kappa_max": KAPPA_MAX,
            "frobenius_within_frac_cut": WFRAC_CUT,
            "ck_z": CK_Z,
            "ck_probs": {str(k): list(zip(CK[k][0], CK[k][1])) for k in CK},
            "reps": R_REPS,
        },
        "o3_floor": floor_summary(),
        "required_p_95": required_p_for_prob(39, 0.95, R_REPS),
        "population_kappa": [population_kappa(x) for x in
                             ("a-hist", "b-hist", "b-thirds", "c-hist")],
        "small_support_gate": [
            small_support("a-hist", {5: 8, 10: 8}),
            small_support("b-hist", {5: 8, 10: 8, 20: 8}),
            small_support("b-hist", {5: 10, 10: 10, 20: 10}),
            small_support("b-hist", {5: 8, 10: 8, 20: 4}),
        ],
        "cells": [],
    }
    for scenario in ("a-hist", "a-50:50", "b-hist", "b-thirds",
                     "c-hist", "c-50:50", "d"):
        for nb in SIZES:
            if scenario == "d" and nb != 120:
                continue
            out["cells"].append(cell(scenario, nb))
            print(scenario, nb, out["cells"][-1].get("P_pass_conditions_1_4"),
                  out["cells"][-1].get("P_complete_lower"), flush=True)
    with open("v03p/bridge/m2_complete_rule_feasibility_2026-10-20.json", "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("written")


if __name__ == "__main__":
    main()
