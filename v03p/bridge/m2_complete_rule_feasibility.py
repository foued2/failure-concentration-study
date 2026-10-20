"""Bounded M2 complete-rule feasibility under the declared support model.

Work order: "CORRECT M2 FEASIBILITY BOUNDS AND DUPLICATE-RATE SCOPE"
(2026-10-20, Foued via GPT/ and Claude/). Deterministic, bounded calculation
only: no sampling, no generation, no hidden outcomes, no Phase 1 execution.

Declared support model (Rev F section 9.1; same marginals as the committed
`v03p/a1/a1_support_comparison.py`):
  * each simulated body independently draws k from the scenario categorical
    mix SCEN (in-range k in {5, 10, 20}; k = 0/25 are outside the support);
  * conditional on k, C is uniform over the feasible 6-family count vectors
    (each family count 0..5, counts summing to k).

Support rule (Rev F conditions 1-4): per in-range bucket n >= 8, at least two
distinct C values, and at least four bodies at each observed extreme; at least
two in-range buckets must pass.

Bounding statement (corrected):
  * The support probability is computed over a bounded multinomial count box.
    The omitted mass T is recorded; the true support probability is bounded by
    p_box <= p_support <= p_box + T. Intervals are propagated monotonically to
    E[N_eligible] and P(N_eligible >= 39).
  * The complete rule adds kappa_eff <= 30. The cell table does NOT compute a
    cell-wide complete-rule lower bound. Its upper bound is the support upper
    bound (the gate can only reject); its lower bound is 0. Cells are labelled
    NOT CERTIFIED unless a negative bound rules a candidate rule out. Exact
    gate-violation enumeration is reported separately for the small supports
    where it is feasible and is not a cell-wide certificate.
  * The conditional uniform-CK model is an engineered support model, not the
    natural-solver population.

Duplicate semantics:
  * Rev F section 9.3 says the Phase 1 simulation's N_b is simulated valid
    unique bodies by construction, and duplicate-rate modelling at the
    attempt axis is O1. That is the fixed-unique-body (rho=0) arm.
  * Rev F section 9.1 also declares an attempt/slot copy mechanism: each slot
    after the first copies an earlier slot with probability rho. If N_b denotes
    generated slots and support counts unique canonical bodies, then
    M = 1 + Binomial(N_b - 1, 1 - rho) and the rho=0.25 support probability is
    E_M[p_support(M)]. Both readings are computed and separately labelled;
    the document records the unresolved semantics rather than choosing one.
  * Neither arm changes the estimand or authorizes Phase 1.

Outputs: printed summary plus `m2_complete_rule_feasibility_2026-10-20.json`.
"""

import json
import math
import sys

import numpy as np

R_REPS = 2000
TAU_RANK = 1e-9
KAPPA_MAX = 30.0
GAP = {5: 0.2, 10: 0.1, 20: 0.05}
INRANGE = {5, 10, 20}
SIZES = [60, 113, 120, 150, 240, 300, 400, 450, 600]
CANDIDATE_SIZES = {60, 120}
DUPLICATE_RATES = (0.0, 0.25)
O3_FLOOR = 39
O3_PROB_TARGET = 0.95
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
LFACT_NP = np.asarray(LFACT, dtype=np.float64)
FTAB_NP = {k: np.asarray(FTAB[k], dtype=np.float64) for k in INRANGE}


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


_SUPPORT_CACHE = {}


def _box_ranges(nb, means, sds):
    out = []
    for mean, sd in zip(means, sds):
        out.append((max(0, int(math.floor(mean - 8.0 * sd))),
                    min(nb, int(math.ceil(mean + 8.0 * sd)))))
    return out


def support_cell(scenario, nb):
    """Bounded count-box support calculation for exactly nb unique bodies.

    Returns p_box and tail such that p_box <= P(conditions 1-4) <= p_box + tail.
    The count box covers +/- 8 marginal SDs for every in-range bucket; all
    configurations outside it are charged to the tail, whether or not they
    would pass.
    """
    key = (scenario, int(nb))
    cached = _SUPPORT_CACHE.get(key)
    if cached is not None:
        return cached

    scen = SCENARIOS[scenario]
    ks = [k for k in sorted(scen) if k in INRANGE]
    if len(ks) < 2:
        out = {
            "scenario": scenario,
            "N_b": int(nb),
            "in_range_buckets": ks,
            "p_box": 0.0,
            "tail": 1.0,
            "box_mass": 0.0,
            "box_count": 0,
            "structural": ("no in-range buckets" if not ks
                           else "fewer than two in-range buckets"),
        }
        _SUPPORT_CACHE[key] = out
        return out

    probs = [scen[k] for k in ks]
    p_other = 1.0 - sum(probs)
    means = [nb * p for p in probs]
    sds = [math.sqrt(nb * p * (1.0 - p)) for p in probs]
    boxes = _box_ranges(nb, means, sds)
    ranges = [np.arange(lo, hi + 1, dtype=np.int64) for lo, hi in boxes]
    log_probs = [math.log(p) for p in probs]
    log_other = math.log(p_other) if p_other > 0.0 else None

    if len(ks) == 2:
        A, B = np.meshgrid(ranges[0], ranges[1], indexing="ij")
        A = A.ravel()
        B = B.ravel()
        O = nb - A - B
        mask = O >= 0
        if log_other is None:
            mask &= (O == 0)
        A, B, O = A[mask], B[mask], O[mask]
        if A.size == 0:
            logp = np.empty(0)
        else:
            logp = (LFACT_NP[nb] - LFACT_NP[A] - LFACT_NP[B] - LFACT_NP[O]
                    + A * log_probs[0] + B * log_probs[1])
            if log_other is not None:
                logp = logp + O * log_other
        f0 = FTAB_NP[ks[0]][A]
        f1 = FTAB_NP[ks[1]][B]
        q = f0 * f1
    else:
        A, B, C = np.meshgrid(ranges[0], ranges[1], ranges[2], indexing="ij")
        A = A.ravel()
        B = B.ravel()
        C = C.ravel()
        O = nb - A - B - C
        mask = O >= 0
        if log_other is None:
            mask &= (O == 0)
        A, B, C, O = A[mask], B[mask], C[mask], O[mask]
        if A.size == 0:
            logp = np.empty(0)
        else:
            logp = (LFACT_NP[nb] - LFACT_NP[A] - LFACT_NP[B] - LFACT_NP[C]
                    - LFACT_NP[O] + A * log_probs[0] + B * log_probs[1]
                    + C * log_probs[2])
            if log_other is not None:
                logp = logp + O * log_other
        f0 = FTAB_NP[ks[0]][A]
        f1 = FTAB_NP[ks[1]][B]
        f2 = FTAB_NP[ks[2]][C]
        q = f0 * f1 + f0 * f2 + f1 * f2 - 2.0 * f0 * f1 * f2

    w = np.zeros_like(logp)
    valid = logp > -745.0
    w[valid] = np.exp(logp[valid])
    p_box = float(np.sum(w * q)) if w.size else 0.0
    box_mass = float(np.sum(w)) if w.size else 0.0
    p_box = max(0.0, min(1.0, p_box))
    tail = max(0.0, min(1.0, 1.0 - box_mass))
    out = {
        "scenario": scenario,
        "N_b": int(nb),
        "in_range_buckets": ks,
        "p_box": p_box,
        "tail": tail,
        "box_mass": box_mass,
        "box_count": int(w.size),
        "box_ranges": {str(k): [int(lo), int(hi)]
                       for k, (lo, hi) in zip(ks, boxes)},
    }
    _SUPPORT_CACHE[key] = out
    return out


def _arm_record(p_lower, p_upper):
    p_lower = max(0.0, min(1.0, p_lower))
    p_upper = max(p_lower, min(1.0, p_upper))
    e_lower = R_REPS * p_lower
    e_upper = R_REPS * p_upper
    pn_lower = binom_sf(O3_FLOOR - 1, R_REPS, p_lower)
    pn_upper = binom_sf(O3_FLOOR - 1, R_REPS, p_upper)
    complete_e_upper = R_REPS * p_upper
    complete_pn_upper = binom_sf(O3_FLOOR - 1, R_REPS, p_upper)
    expected_status = ("ruled_out" if complete_e_upper < O3_FLOOR
                       else "not_certified")
    probability_status = ("ruled_out" if complete_pn_upper < O3_PROB_TARGET
                          else "not_certified")
    if expected_status == "ruled_out" and probability_status == "ruled_out":
        overall = "both_candidate_rules_ruled_out"
    elif expected_status == "ruled_out":
        overall = "expected_count_rule_ruled_out"
    elif probability_status == "ruled_out":
        overall = "probability_rule_ruled_out"
    else:
        overall = "not_certified_no_complete_rule_lower_bound"
    return {
        "P_support_lower": p_lower,
        "P_support_upper": p_upper,
        "E_support_lower": e_lower,
        "E_support_upper": e_upper,
        "P_N_ge_39_support_lower": pn_lower,
        "P_N_ge_39_support_upper": pn_upper,
        "P_complete_lower": 0.0,
        "P_complete_upper": p_upper,
        "E_complete_lower": 0.0,
        "E_complete_upper": complete_e_upper,
        "P_N_ge_39_complete_lower": 0.0,
        "P_N_ge_39_complete_upper": complete_pn_upper,
        "o3_expected_count_status": expected_status,
        "o3_probability_status": probability_status,
        "o3_label": overall,
    }


def _duplicate_support(scenario, nb, rho):
    p_lower = 0.0
    tail_mix = 0.0
    mass = 0.0
    new_prob = 1.0 - rho
    for m in range(1, nb + 1):
        pmf = binom_pmf(nb - 1, m - 1, new_prob)
        if pmf == 0.0:
            continue
        base = support_cell(scenario, m)
        if base.get("structural"):
            return {
                "rho": rho,
                "N_b_semantics": "attempt_slots",
                "structural": base["structural"],
            }
        p_lower += pmf * base["p_box"]
        tail_mix += pmf * base["tail"]
        mass += pmf
    mass = min(1.0, mass)
    omitted = max(0.0, 1.0 - mass)
    p_upper = min(1.0, p_lower + tail_mix + omitted)
    return {
        "rho": rho,
        "N_b_semantics": "attempt_slots",
        "M_formula": "M = 1 + Binomial(N_b - 1, 1 - rho)",
        "M_mean": 1.0 + (nb - 1) * new_prob,
        "M_sd": math.sqrt((nb - 1) * rho * new_prob),
        "mixture_mass_covered": mass,
        "mixture_omitted_mass": omitted,
        "p_lower": p_lower,
        "p_upper": p_upper,
        "tail_mixture": tail_mix,
    }


def cell(scenario, nb):
    base = support_cell(scenario, nb)
    size_class = "candidate" if nb in CANDIDATE_SIZES else "planning_sensitivity"
    note = None
    if nb == 113:
        note = "approximately E[M] for 150 slots at rho=0.25 (112.75)"
    elif nb == 450:
        note = "approximately E[M] for 600 slots at rho=0.25 (450.25)"
    if base.get("structural"):
        return {
            "scenario": scenario,
            "N_b": int(nb),
            "size_class": size_class,
            "size_note": note,
            "in_range_buckets": base["in_range_buckets"],
            "structural": base["structural"],
            "arms": {
                "fixed_unique_rho_0": {"rho": 0.0,
                                       "N_b_semantics": "unique_bodies",
                                       "status": "structural_zero"},
                "attempt_copy_rho_0_25": {"rho": 0.25,
                                          "N_b_semantics": "attempt_slots",
                                          "status": "structural_zero"},
            },
        }

    fixed = _arm_record(base["p_box"], base["p_box"] + base["tail"])
    fixed.update({"rho": 0.0, "N_b_semantics": "unique_bodies"})
    duplicate = _duplicate_support(scenario, nb, 0.25)
    if "structural" in duplicate:
        duplicate["status"] = "structural_zero"
    else:
        duplicate.update(_arm_record(duplicate["p_lower"], duplicate["p_upper"]))
    return {
        "scenario": scenario,
        "N_b": int(nb),
        "size_class": size_class,
        "size_note": note,
        "in_range_buckets": base["in_range_buckets"],
        "box_count": base["box_count"],
        "box_mass": base["box_mass"],
        "box_tail_bound": base["tail"],
        "arms": {
            "fixed_unique_rho_0": fixed,
            "attempt_copy_rho_0_25": duplicate,
        },
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
            "calculation_version": "2026-10-20-correction-1",
            "model": "Rev F 9.1 declared support: k ~ SCEN, C|k uniform over feasible 6-family vectors; bodies iid per replication; R=2000 independent replications",
            "support_rule": "Rev F conditions 1-4 (S0) per in-range bucket; >=2 buckets pass",
            "support_interval": "p_box <= P(conditions 1-4) <= p_box + (1 - box_mass); propagated monotonically to E and P(N_ge_39)",
            "complete_rule_interval": "0 <= P(conditions 1-4 AND kappa_eff <= 30) <= P(conditions 1-4 upper); no cell-wide lower bound is computed",
            "m2_gate": "kappa_eff <= 30 on column-standardized extended matrix; rank tol 1e-9; body rows",
            "tau_rank": TAU_RANK,
            "kappa_max": KAPPA_MAX,
            "ck_z": CK_Z,
            "ck_probs": {str(k): list(zip(CK[k][0], CK[k][1])) for k in CK},
            "reps": R_REPS,
            "size_classes": {
                "candidate": [60, 120],
                "planning_sensitivity": [113, 150, 240, 300, 400, 450, 600],
                "note": "113 and 450 are near E[M] for 150 and 600 slots at rho=0.25; none of the planning sizes is an adopted Rev F grid value",
            },
            "duplicate_scope": {
                "conflict": "Rev F 9.2 lists duplicate rate as a grid factor; Rev F 9.3 says Phase 1 N_b is simulated valid unique bodies and duplicate-rate modelling at the attempt axis is O1",
                "arms": [
                    {"rho": 0.0, "N_b_semantics": "unique_bodies",
                     "source": "Rev F 9.3 fixed-unique-body reading"},
                    {"rho": 0.25, "N_b_semantics": "attempt_slots",
                     "source": "Rev F 9.1 slot-copy mechanism; M = 1 + Binomial(N_b - 1, 1 - rho)"},
                ],
                "resolution": "unresolved; both arms reported, no design adopted",
            },
            "o3_rules": {
                "floor_realized_count": O3_FLOOR,
                "expected_count_threshold": O3_FLOOR,
                "expected_count_p_threshold": O3_FLOOR / float(R_REPS),
                "probability_target": O3_PROB_TARGET,
                "probability_p_threshold": required_p_for_prob(
                    O3_FLOOR, O3_PROB_TARGET, R_REPS),
            },
        },
        "o3_floor": floor_summary(),
        "required_p_95": required_p_for_prob(O3_FLOOR, O3_PROB_TARGET, R_REPS),
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
            rec = cell(scenario, nb)
            out["cells"].append(rec)
            if "arms" in rec and "fixed_unique_rho_0" in rec["arms"]:
                f = rec["arms"]["fixed_unique_rho_0"]
                d = rec["arms"]["attempt_copy_rho_0_25"]
                print(scenario, nb,
                      "rho0", f.get("P_support_lower"), f.get("P_support_upper"),
                      "rho.25", d.get("P_support_lower"), d.get("P_support_upper"),
                      "labels", f.get("o3_label"), d.get("o3_label"), flush=True)
            else:
                print(scenario, nb, rec.get("structural"), flush=True)
    with open("v03p/bridge/m2_complete_rule_feasibility_2026-10-20.json", "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("written")


if __name__ == "__main__":
    main()
