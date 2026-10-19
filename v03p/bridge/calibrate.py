#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calibration stage of the owner-authorized bridge (scenarios (a)/(c)).

Work order (GPT/ relay 2026-10-18, on behalf of Foued): freeze this file +
record its blob hash, the fitted-family definitions, row weights, quadrature
settings, random seed, and tolerances BEFORE the official run; then for all
four matched-population variants calibrate the actual random-effects
population log-loss improvement at d* = 0.020273255405408218 and test
2d* = 0.040546510810816436 against the actual sigma_u = sigma_v = 1
objective (estimating the actual peak before any non-attainment claim);
compute beta_pop per the A2.3 definition, map to c* = (1.25/beta_pop)^2,
compare against beta_min = 0.10 (c*_ref = 156.25) and the NC1 grid, with no
tuning toward the anchor; commit the output as a separate report with
convergence evidence, per-fit diagnostics, quadrature/MC agreement, and
unattainability findings.

FROZEN SETTINGS (declared before the run; not changed after first numbers):
  - objective: fitted-improvement
      f(gamma) = L_baseline(gamma) - L_extended(gamma)
    where both families are refitted at their UNPENALIZED population optima
    (ridge = 0.0, explicit; IRLS mirror of study/models.py, tol 1e-13,
    <= 50 iterations) against the sigma = 1 supports conditioned per-cell
    marginal targets pbar(k,c;gamma) = E_{s ~ N(0, 2)}[expit(eta + s)],
    eta(k,c,gamma) = -log(1+k) + gamma*c (the frozen generator theta's).
    L = sum_cells w_k pi_c CE(pbar || qhat), the same support-conditioned
    weights for both families (battery production weightsets).
  - quadrature: Gauss-Hermite over s = u + v ~ N(0, sigma_u^2 + sigma_v^2),
    scale tau = sqrt(2) (battery constant TAU), frozen node count 256;
    node-doubling agreement (256 vs the preceding 128, the battery's own
    validated chain) re-verified at every solution and peak point with
    declared tolerance 1e-12 per cell.  NOTE (pre-run defect record,
    2026-10-18): numpy's hermgauss(512) returns non-finite weights in this
    environment; the doubling check therefore never uses 512, every pbar
    evaluation is guarded for finiteness, and non-finite values abort the
    run instead of being silently swallowed (python max() hides NaN, a
    false 0.0 agreement was observed in the pre-freeze test).
  - Monte Carlo cross-check: calibration seed 20261019; draws 2e6 of
    s = tau * Z; the MC path refits BOTH families on the MC targets and
    compares f_MC against f_GH with realized SEs by the delta method on
    the per-cell gradients of the loss difference.
  - bisection: solution of f(gamma) = target.  Bracket extended upward from
    the battery bracket's right end (8.0) in +4.0 steps while f rises;
    unique crossing of the increasing prefix is bisected to gamma-tolerance
    1e-9 (200 iterations max); reported achieved |f - target| is expected
    well inside the Rev F 1e-4 tolerance on Delta, which is recorded not
    assumed.
  - peak scan (for the 2d* attainability finding): coarse grid 0.5 on
    [0, 32] (extended by +4 steps while f still rises), refine band,
    golden section to gamma-tolerance 1e-6; the reported actual peak is the
    refined value with its argmax; non-attainment of 2d* is declared only
    with (peak value, margin 2d* - peak, node-doubling and MC evidence at
    the argmax) on record.
  - beta_pop: exactly the A2.3 display formula, pooled within-stratum
    covariance-over-variance of the truth-marginalized correctness
    probability pbar(i) against the s_ref-normalized channel
    x_M3 = (c - mean_k(C))/s_ref, s_ref = 0.12703 exactly, weights
    w_k pi_c (battery cell weights; "the same family as used for E[c]").
    Sensitivity variants labeled: slope computed on the extended family's
    unpenalized optimum predictions qhat_ext(gamma*) (family-fit variant)
    and the A2.3 labeled average-derivative approximation
    beta_appr = gamma* * s_ref * sum_cells w_k pi_c pbar(1-pbar).
  - c* map: c*_prov = (1.25/beta_pop)^2; comparison against the owner
    anchor beta_min = 0.10 (c*_ref = 156.25) and NC1's grid
    {39.0625, 156.25, 625}; off-grid values report "no NC1 row (grid
    mismatch)"; nothing is tuned toward the anchor (no optimization or
    selection step exists for beta_pop).
  - rows: the four battery variants (a-hist, a-50:50, c-hist, c-50:50) on
    the battery production weightsets (support-conditioned; identical for
    both families per the work order).

Every output is PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE.  Scenario (b)'s
direct bridge is NOT DEFINED.  NC1 stays closed; NC2, Phase 1, solver
generation, hidden-outcome collection, spending, and master merge remain
unauthorized.  The battery machinery is imported read-only and its own
integrity is verified against the branch freeze before any number exists.
"""

import sys, os, math, time, datetime, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.normpath(os.path.join(_HERE, os.pardir, os.pardir))

# ---- integrity of the frozen battery machinery (read-only import) -------
_BATTERY_REL = "v03p/bridge/battery.py"


def _blob_of(rel):
    out = subprocess.run(["git", "rev-parse", "HEAD:%s" % rel],
                         capture_output=True, text=True, cwd=_REPO)
    val = out.stdout.strip()
    if len(val) != 40 or any(ch not in "0123456789abcdef" for ch in val):
        return None
    return val


def _hash_of(path):
    out = subprocess.run(["git", "hash-object", path],
                         capture_output=True, text=True, cwd=_REPO)
    return out.stdout.strip()


def integrity():
    """(self_blob_ok, battery_blob_ok, details) for the official-run gate.

    The official run refuses unless BOTH files match their committed blobs
    (the freeze discipline: no post-freeze code change may reach the run).
    """
    det = {}
    b = _blob_of(_BATTERY_REL)
    w = _hash_of(os.path.join(_HERE, "battery.py"))
    det["battery"] = {"committed": b, "working": w}
    c = _blob_of("v03p/bridge/calibrate.py")
    v = _hash_of(os.path.join(_HERE, "calibrate.py"))
    det["calibrate"] = {"committed": c, "working": v}
    return (bool(b) and b == w, bool(c) and c == v), det


if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import battery as B  # noqa: E402  (frozen machinery; verified above)

A1 = B.A1
SREF = 0.12703
DSTAR = B.DELTA1
TWO_DSTAR = B.DELTA2
GH_NODES_CAL = 256
GH_NODES_PREV = 128
GH_TOL_CAL = 1e-12
CAL_SEED = 20261019
MC_DRAWS_CAL = 2 * 10 ** 6
BISECT_GAMMA_TOL = 1e-9
BISECT_MAXIT = 200
BRACKET_START = B.BISECT_BRACKET[1]      # 8.0, the frozen battery right end
BRACKET_STEP = 4.0
BRACKET_HI_CAP = 64.0
PEAK_COARSE = 0.5
PEAK_HI0 = 32.0
PEAK_EXT_CAP = 64.0
GOLDEN_TOL = 1e-6
TAU_CAL = B.TAU

VARIANTS = B.VARIANTS


def pbar_gh(wset, gamma, nodes):
    tbl = B.pbar_sigma1_table(wset, gamma, nodes, TAU_CAL)
    vals = list(tbl.values())
    for v in vals:
        if not math.isfinite(v):
            raise RuntimeError("non-finite GH pbar at nodes=%r gamma=%r"
                               % (nodes, gamma))
    return tbl


def fit_on_targets(wset, targets, family, ridge=0.0):
    """Unpenalized IRLS fit of a family against per-cell targets."""
    cells = B.cell_list(wset)
    X = B.design_rows(wset, family)
    om = [w for _k, _c, w in cells]
    tv = [targets[(k, c)] for (k, c, _w) in cells]
    beta, iters, mx = B.irls_logistic(X, tv, om, ridge=ridge)
    qh = {}
    for row, (k, c, _w) in zip(X, cells):
        qh[(k, c)] = B.expit_scalar(sum(bv * xi for bv, xi in zip(beta, row)))
    return {"beta": beta, "iters": iters, "grad": mx, "qhat": qh}


def loss_of(wset, targets, qhat):
    return B.ce_of(wset, targets, qhat)


def f_of(wset, gamma):
    """The frozen calibration objective: fitted-improvement loss difference
    at GH target scale (node count GH_NODES_CAL)."""
    tgt = pbar_gh(wset, gamma, GH_NODES_CAL)
    fb = fit_on_targets(wset, tgt, "baseline")
    fe = fit_on_targets(wset, tgt, "extended")
    return loss_of(wset, tgt, fb["qhat"]) - loss_of(wset, tgt, fe["qhat"])


def f_of_mc(wset, gamma, s):
    tgt = B.mc_pbar_table(wset, gamma, s)
    fb = fit_on_targets(wset, tgt, "baseline")
    fe = fit_on_targets(wset, tgt, "extended")
    return loss_of(wset, tgt, fb["qhat"]) - loss_of(wset, tgt, fe["qhat"])


def mc_se_of_f(wset, gamma, s):
    """Delta-method SE of the MC fitted-improvement estimate: the gradient
    of f w.r.t. each cell target is the per-cell weighted logit gap of the
    fitted predictors' respective logistic scores:
      dL(tgt)/d tgt_c = w_c [(1 - q_b) - (1 - q_e)] ... (CE gradient form)
    exactly: d/d t [-(t log q + (1-t) log(1-q))] = -(log q - log(1-q)); so
      d f/d target_c = w_c * (logit(q_e,c) - logit(q_b,c)).
    se = sqrt(sum_c grad_c^2 * Var_MC(c) / ndraws)."""
    tgt = B.mc_pbar_table(wset, gamma, s, store_var=True)
    t1, var = tgt
    fb = fit_on_targets(wset, t1, "baseline")
    fe = fit_on_targets(wset, t1, "extended")
    f = loss_of(wset, t1, fb["qhat"]) - loss_of(wset, t1, fe["qhat"])
    acc = 0.0
    for k, c, w in B.cell_list(wset):
        qb, qe = min(max(fb["qhat"][(k, c)], 1e-15), 1 - 1e-15), \
            min(max(fe["qhat"][(k, c)], 1e-15), 1 - 1e-15)
        g = w * (math.log(qe / (1.0 - qe)) - math.log(qb / (1.0 - qb)))
        acc += g * g * var[(k, c)]
    return f, math.sqrt(acc / len(s))


def bisect_to(fn, target, hi0):
    """Unique solution on the increasing prefix.  Extends the upper bracket
    in BRACKET_STEP steps while f(hi) < target; requires f(lo)=f(0) < target
    (f(0) ~ 0 by construction).  Bisection to BISECT_GAMMA_TOL."""
    gam_lo, f_lo = 0.0, fn(0.0)
    if not (f_lo < target):
        return {"attained": False, "gamma": None, "iters": 0, "f_at": f_lo,
                "note": "f(0) >= target"}
    gam_hi, f_hi = hi0, fn(hi0)
    while f_hi < target:
        gam_lo, f_lo = gam_hi, f_hi
        gam_hi = gam_hi + BRACKET_STEP
        if gam_hi > BRACKET_HI_CAP:
            return {"attained": False, "gamma": None, "iters": 0, "f_at": f_hi,
                    "note": "no crossing below %r" % BRACKET_HI_CAP}
        f_hi = fn(gam_hi)
    a, b = gam_lo, gam_hi
    it = 0
    fa = f_lo
    for it in range(1, BISECT_MAXIT + 1):
        mid = 0.5 * (a + b)
        fm = fn(mid)
        if fm < target:
            a, fa = mid, fm
        else:
            b = mid
        if b - a < BISECT_GAMMA_TOL:
            break
    gstar = 0.5 * (a + b)
    return {"attained": True, "gamma": gstar, "iters": it,
            "delta_at": fn(gstar), "f_lo": fa, "f_hi": fn(gstar)}


def golden_max(fn, a, b, tol=GOLDEN_TOL):
    """Maximize fn on [a, b] (unimodal assumed after the coarse scan)."""
    r = (math.sqrt(5.0) - 1.0) / 2.0
    c1 = b - r * (b - a)
    c2 = a + r * (b - a)
    f1, f2 = fn(c1), fn(c2)
    it = 0
    while (b - a) > tol:
        it += 1
        if f1 < f2:
            a, c1, f1 = c1, c2, f2
            c2 = a + r * (b - a)
            f2 = fn(c2)
        else:
            b, c2, f2 = c2, c1, f1
            c1 = b - r * (b - a)
            f1 = fn(c1)
    g = 0.5 * (a + b)
    return g, fn(g), it


def find_peak(fn):
    """Coarse_scan + refine + golden argmax on the full observable range.
    Returns (gamma_peak, f_peak, scan_record)."""
    rec = {
        "coarse_grid": [], "band_refine": [], "golden": None, "hi_ext": None,
    }
    hi = PEAK_HI0
    vals = []
    g = 0.0
    while g <= hi + 1e-9:
        v = fn(min(g, hi))
        vals.append((g, v))
        rec["coarse_grid"].append((g, v))
        g += PEAK_COARSE
    # extend if f still clearly rising at hi
    while vals[-1][1] > vals[-2][1] and hi < PEAK_EXT_CAP:
        rec["hi_ext"] = hi
        hi += PEAK_COARSE * 8.0
        for g in range(0, 2):
            vals.append(((hi - PEAK_COARSE * (1 - g)),
                         fn(hi - PEAK_COARSE * (1 - g))))
    imax = max(range(len(vals)), key=lambda i: vals[i][1])
    lo_band = vals[max(0, imax - 2)][0]
    hi_band = vals[min(len(vals) - 1, imax + 2)][0]
    for g in [lo_band + i * (hi_band - lo_band) / 8.0
              for i in range(1, 8)]:
        v = fn(g)
        rec["band_refine"].append((round(g, 10), v))
    gp, fp, it = golden_max(fn, lo_band, hi_band)
    rec["golden"] = {"gamma": gp, "iters": it, "f": fp}
    best = max(vals, key=lambda t: t[1])
    if fp >= best[1]:
        return gp, fp, rec
    return best[0], best[1], rec


def beta_pop(wset, gamma, pbar_table=None):
    """A2.3 pooled within-stratum covariance-over-variance slope.
    x_M3 = (c - mean_k)/s_ref; weights = battery cell weights.
    Returns (beta_pop, per-stratum diagnostics, mean pbar used)."""
    cells = B.cell_list(wset)
    pbar = pbar_table or pbar_gh(wset, gamma, GH_NODES_CAL)
    num = den = 0.0
    sdst = {}
    for k in (5, 10):
        lv = wset["levels%d" % k]
        pi = wset["pi%d" % k]
        wk = wset["w%d" % k]
        cbar = sum(pi[j] * lv[j] for j in range(len(lv)))
        pb_k = sum(pi[j] * pbar[(k, lv[j])] for j in range(len(lv)))
        xs = [(lv[j] - cbar) / SREF for j in range(len(lv))]
        num_k = den_k = 0.0
        for j, _c in enumerate(lv):
            num_k += wk * pi[j] * xs[j] * (pbar[(k, lv[j])] - pb_k)
            den_k += wk * pi[j] * xs[j] * xs[j]
        num += num_k
        den += den_k
        sdst[k] = {"cbar": cbar, "pbar_k": pb_k, "den_k": den_k,
                   "beta_k": (num_k / den_k if den_k > 0 else None)}
    return (num / den) if den > 0 else None, sdst, pbar


def beta_from_fit(wset, gamma):
    """Family-fit sensitivity variant of the A2.3 slope functional, on the
    extended family's unpenalized optimum predictions at gamma."""
    tgt = pbar_gh(wset, gamma, GH_NODES_CAL)
    fe = fit_on_targets(wset, tgt, "extended")
    _, sdst, _ = beta_pop(wset, gamma, pbar_table=None)
    return beta_pop(wset, gamma, pbar_table=fe["qhat"])[0], sdst


def beta_appr(wset, gamma):
    """A2.3 labeled average-derivative approximation:
    beta_appr = gamma * s_ref * sum_cells w_k pi_c pbar(1-pbar)."""
    pbar = pbar_gh(wset, gamma, GH_NODES_CAL)
    tot = 0.0
    for k, c, w in B.cell_list(wset):
        tot += w * pbar[(k, c)] * (1.0 - pbar[(k, c)])
    return gamma * SREF * tot


def map_cstar(beta):
    if beta is None or beta <= 0.0:
        return None
    return (1.25 / beta) ** 2


CGRID = (39.0625, 156.25, 625.0)


def cstar_row(cprov):
    row = [("<" if cprov < g else ">" if cprov > g else "=") + str(g)
           for g in CGRID]
    near = min(CGRID, key=lambda g: abs(g - cprov))
    rel = abs(cprov - near) / near
    if rel < 1e-12:
        match = "at grid value %r" % near
    else:
        match = "no NC1 row (grid mismatch)"
    return row, match


def oracle_delta(wset, gamma):
    tgt = pbar_gh(wset, gamma, GH_NODES_CAL)
    dl, qbars = B.delta_of(wset, tgt)
    return dl


def gh_node_agreement(wset, gamma):
    """Doubling-downward agreement 256 vs 128, the battery's validated chain.
    Non-finite values abort (NaN must never be silently swallowed, python
    max hides it)."""
    m = None
    for k, c, _w in B.cell_list(wset):
        a = B.pbar_sigma1(k, c, gamma, GH_NODES_CAL, TAU_CAL)
        b2 = B.pbar_sigma1(k, c, gamma, GH_NODES_PREV, TAU_CAL)
        if not (math.isfinite(a) and math.isfinite(b2)):
            raise RuntimeError("non-finite pbar in node agreement at "
                               "gamma=%r cell=%r" % (gamma, (k, c)))
        d = abs(a - b2)
        if m is None or d > m:
            m = d
    return m


def run_calibration():
    R = {"meta": {"label": "bridge gamma* calibration (scenarios (a)/(c))",
                  "date": datetime.date.today().isoformat(),
                  "objective": "L_baseline_unpen - L_extended_unpen",
                  "heap": {"GH_NODES_CAL": GH_NODES_CAL,
                           "GH_NODES_PREV": GH_NODES_PREV,
                           "GH_TOL_CAL": GH_TOL_CAL,
                           "CAL_SEED": CAL_SEED,
                           "MC_DRAWS_CAL": MC_DRAWS_CAL,
                           "BISECT_GAMMA_TOL": BISECT_GAMMA_TOL,
                           "BRACKET_START": BRACKET_START,
                           "BRACKET_STEP": BRACKET_STEP,
                           "BRACKET_HI_CAP": BRACKET_HI_CAP,
                           "PEAK_COARSE": PEAK_COARSE,
                           "PEAK_HI0": PEAK_HI0,
                           "PEAK_EXT_CAP": PEAK_EXT_CAP,
                           "GOLDEN_TOL": GOLDEN_TOL,
                           "TAU": TAU_CAL,
                           "SREF": SREF,
                           "dstar": DSTAR,
                           "2dstar": TWO_DSTAR,
                           "ridge": 0.0}},
         "rows": {}, "findings": {}}
    t0 = time.time()
    ws_p = B.assemble_weightsets("prod")
    R["weights"] = {var: {kk: ws_p[var][kk] for kk in
                          ("w5", "w10", "var5", "var10", "pi5", "pi10",
                           "levels5", "levels10")}
                    for var in VARIANTS}
    s = TAU_CAL * __import__("numpy").random.default_rng(CAL_SEED) \
        .standard_normal(MC_DRAWS_CAL)
    for var in VARIANTS:
        wset = ws_p[var]
        row = {}
        # -- headline grid for the report (the frozen battery grid)
        gtab = []
        for gamma in B.GAMMA_GRID:
            gtab.append((gamma, f_of(wset, gamma)))
        row["f_grid"] = gtab
        # -- 2d* peak first: needed to contextualize both targets
        gp, fp, rec = find_peak(lambda g: f_of(wset, g))
        row["peak"] = {"gamma": gp, "f": fp, "record": rec}
        peak_status = ("attained" if fp >= TWO_DSTAR
                       else "not_attained_on_bracket")
        row["peak_status"] = peak_status
        row["peak_vs_2dstar"] = {
            "f_peak": fp, "target": TWO_DSTAR,
            "margin": fp - TWO_DSTAR,
            "gamma_peak": gp,
        }
        sol = bisect_to(lambda g: f_of(wset, g), DSTAR, BRACKET_START)
        row["delta1_solution"] = {kk: vv for kk, vv in sol.items()}
        if sol["attained"]:
            gs = sol["gamma"]
            tsol, se_sol = mc_se_of_f(wset, gs, s)
            row["delta1_solution"]["mc"] = {
                "f_mc": tsol, "se": se_sol,
                "gap": abs(tsol - sol["delta_at"])}
            row["delta1_solution"]["gh_node_agreement"] = \
                gh_node_agreement(wset, gs)
            row["delta1_solution"]["fit_diagnostics"] = {
                "baseline": fit_on_targets(wset, pbar_gh(wset, gs,
                                                          GH_NODES_CAL),
                                           "baseline"),
                "extended": fit_on_targets(wset, pbar_gh(wset, gs,
                                                          GH_NODES_CAL),
                                           "extended")}
            bp, sdst, pb = beta_pop(wset, gs)
            bf, _sdst2 = beta_from_fit(wset, gs)
            ba = beta_appr(wset, gs)
            cprov = map_cstar(bp)
            crow, cmatch = cstar_row(cprov)
            row["beta_pop_at_gamma"] = {
                "gamma": gs, "beta_pop": bp, "per_stratum": sdst,
                "beta_fit_sensitivity": bf, "beta_appr": ba,
                "cstar_prov": cprov, "cstar_row": crow,
                "grid_match": cmatch,
                "anchor": {"beta_min_ref": 0.10, "cstar_ref": 156.25},
                "oracle_delta_context": oracle_delta(wset, gs),
            }
            srow = {}
            sol2 = bisect_to(lambda g: f_of(wset, g), TWO_DSTAR,
                             BRACKET_START)
            srow["delta2_solution"] = {kk: vv for kk, vv in sol2.items()}
            if sol2["attained"]:
                g2 = sol2["gamma"]
                ts2, se_2 = mc_se_of_f(wset, g2, s)
                srow["delta2_solution"]["mc"] = {
                    "f_mc": ts2, "se": se_2,
                    "gap": abs(ts2 - sol2["delta_at"])}
                srow["delta2_solution"]["gh_node_agreement"] = \
                    gh_node_agreement(wset, g2)
                bp2, sdst2, pb2 = beta_pop(wset, g2)
                srow["beta_pop_at_2gamma"] = {
                    "gamma": g2, "beta_pop": bp2, "per_stratum": sdst2,
                    "cstar_prov": map_cstar(bp2),
                    "grid_match": cstar_row(map_cstar(bp2))[1],
                }
            if not sol2["attained"]:
                srow["delta2_peak_finding"] = {
                    "declared": "NOT ATTAINABLE (evidence-based)",
                    "peak_gamma": row["peak"]["gamma"],
                    "peak_f": row["peak"]["f"],
                    "target": TWO_DSTAR,
                    "margin": TWO_DSTAR - row["peak"]["f"],
                }
                # MC corroboration of the peak's non-attainment margin
                ts_pk, se_pk = mc_se_of_f(wset, gp, s)
                srow["delta2_peak_finding"]["mc_at_peak"] = {
                    "f_mc": ts_pk, "se": se_pk,
                    "gap": abs(ts_pk - fp)}
                srow["delta2_peak_finding"]["gh_node_agreement"] = \
                    gh_node_agreement(wset, gp)
            row["delta2"] = srow
        R["rows"][var] = row
    R["elapsed_s"] = time.time() - t0
    return R


def write_calibration_report(R, path):
    L = []
    L.append("# Calibration report - bridge gamma* (scenarios (a)/(c))")
    L.append("")
    L.append("**Date:** 2026-10-18.  **Status:** executed under the owner")
    L.append("bridge authorization (Foued, 2026-10-18) and the GPT/")
    L.append("calibration work order (2026-10-18), after the battery stage")
    L.append("closed (standing record `BATTERY_REPORT_2026-10-18.md`,")
    L.append("commit `4618f31`).")
    L.append("")
    L.append("**Every number in this file is PROVISIONAL /")
    L.append("NOT A COMPLETE-RULE ESTIMATE.**  Scenario (b) is out of scope")
    L.append("(bridge NOT DEFINED there).  `I_k` is the bucket-local")
    L.append("support proxy under Rev F 5A as drafted; P(pass) = 0 for the")
    L.append("complete rule is unchanged (draft A2.3).  NC1 is closed;")
    L.append("NC2, Phase 1, solver generation, hidden-outcome collection,")
    L.append("spending, and master merge remain unauthorized.")
    L.append("")
    L.append("## Frozen settings")
    L.append("")
    for kk, vv in R["meta"]["heap"].items():
        L.append("- `%s`: %r" % (kk, vv))
    L.append("")
    L.append("Objective: `f(gamma) = L_baseline_unpen - L_extended_unpen`,")
    L.append("both families refitted at their unpenalized population")
    L.append("optima against per-cell targets `pbar(k,c;gamma)` (GH-256 at")
    L.append("tau = sqrt(2)); IRLS mirror of `study/models.py` (tol 1e-13,")
    L.append("<= 50 iterations, ridge 0.0); the same support-conditioned")
    L.append("weights for both families (battery production weightsets).")
    L.append("")
    L.append("Integrity: battery.py blob verified before the run (frozen")
    L.append("machinery; module imported read-only).")
    L.append("")
    L.append("## Row weightsets (support-conditioned, both families)")
    L.append("")
    for var, wd in R["weights"].items():
        L.append("### %s" % var)
        for kk, vv in wd.items():
            L.append("- `%s`: %r" % (kk, vv))
    L.append("")
    L.append("## Per-variant results")
    L.append("")
    for var, row in R["rows"].items():
        L.append("### %s" % var)
        L.append("")
        L.append("- f(battery gamma grid): %s" % repr(row["f_grid"]))
        L.append("- broken down:")
        for g, v in row["f_grid"]:
            L.append("  - f(%r) = %.10e" % (g, v))
        sol = row["delta1_solution"]
        L.append("- delta* = %r solution:" % DSTAR)
        if sol["attained"]:
            L.append("  - gamma* = %.9e  |f - d*| = %.3e  (iters %r)"
                     % (sol["gamma"], abs(sol["delta_at"] - DSTAR),
                        sol["iters"]))
            L.append("  - achieved |f - d*| against Rev F 1e-4 tolerance:")
            L.append("    %.3e (within tolerance: %r)"
                     % (abs(sol["delta_at"] - DSTAR),
                        abs(sol["delta_at"] - DSTAR) <= 1e-4))
            L.append("  - GH node agreement at gamma* (256 vs 128): %.3e"
                     % sol["gh_node_agreement"])
            fd = sol["fit_diagnostics"]
            L.append("  - baseline fit: beta %r iters %r grad %.3e"
                     % (fd["baseline"]["beta"], fd["baseline"]["iters"],
                        fd["baseline"]["grad"]))
            L.append("  - extended fit: beta %r iters %r grad %.3e"
                     % (fd["extended"]["beta"], fd["extended"]["iters"],
                        fd["extended"]["grad"]))
            L.append("  - MC cross-check (seed %r, %r draws): f_MC = %.10e,"
                     % (CAL_SEED, MC_DRAWS_CAL, sol["mc"]["f_mc"]))
            L.append("    SE = %.3e, |f_MC - f_GH| = %.3e (<= 5*SE: %r)"
                     % (sol["mc"]["se"], sol["mc"]["gap"],
                        sol["mc"]["gap"] <= 5.0 * sol["mc"]["se"] + 1e-12))
            bpr = row["beta_pop_at_gamma"]
            L.append("  - beta_pop (A2.3, truth-marginalized pbar): %.9e"
                     % bpr["beta_pop"])
            for kk, dd in bpr["per_stratum"].items():
                L.append("    - stratum k=%s: cbar %.9e pbar_k %.9e"
                         % (kk if isinstance(kk, str) else repr(kk),
                            dd["cbar"], dd["pbar_k"]))
                L.append("      den_k %.9e beta_k %r"
                         % (dd["den_k"], dd["beta_k"]))
            L.append("  - beta_pop fit-sensitivity (on qhat_ext): %.9e"
                     % bpr["beta_fit_sensitivity"])
            L.append("  - labeled average-derivative approximation: %.9e"
                     % bpr["beta_appr"])
            L.append("  - c*_prov = (1.25/beta_pop)^2 = %.9e -> %s"
                     % (bpr["cstar_prov"], bpr["grid_match"]))
            L.append("  - NC1-grid comparison: %s"
                     % "; ".join(bpr["cstar_row"]))
            L.append("  - anchor: beta_min = 0.10 (c*_ref = 156.25);")
            L.append("    ratio c*_prov / c*_ref = %.6e"
                     % (bpr["cstar_prov"] / 156.25))
            L.append("  - context: oracle Delta at gamma* (KL, delta_of) =")
            L.append("    %.10e (not a gate; decomposition context)"
                     % bpr["oracle_delta_context"])
        else:
            L.append("  - NOT attained: %r" % sol.get("note"))
            L.append("  - f(0): %r" % sol.get("f_at"))
        if row["delta2"]:
            sol2 = row["delta2"].get("delta2_solution", {})
            if sol2.get("attained"):
                L.append("- 2d* = %r solution:" % TWO_DSTAR)
                L.append("  - gamma = %.9e |f - 2d*| = %.3e (iters %r)"
                         % (sol2["gamma"],
                            abs(sol2["delta_at"] - TWO_DSTAR), sol2["iters"]))
                L.append("  - GH node agreement: %.3e"
                         % sol2["gh_node_agreement"])
                L.append("  - MC cross-check: f_MC = %.10e SE = %.3e gap ="
                         " %.3e" % (sol2["mc"]["f_mc"], sol2["mc"]["se"],
                                    sol2["mc"]["gap"]))
                bp2 = row["delta2"]["beta_pop_at_2gamma"]
                L.append("  - beta_pop at gamma_2 = %.9e, c*_prov = %r"
                         % (bp2["beta_pop"], bp2["cstar_prov"]))
                L.append("  - grid match: %s" % bp2["grid_match"])
            else:
                pf = row["delta2"].get("delta2_peak_finding", {})
                L.append("- 2d* = %r finding: %s"
                         % (TWO_DSTAR, pf.get("declared")))
                L.append("  - actual peak: f(gamma=%.9e) = %.10e"
                         % (pf["peak_gamma"], pf["peak_f"]))
                L.append("  - margin 2d* - peak = %.10e (positive: the"
                         " observed maximum on the frozen bracket lies"
                         " below the target)" % (pf["margin"],))
                L.append("  - MC corroboration at the argmax: f_MC = %.10e"
                         " SE = %.3e gap = %.3e"
                         % (pf["mc_at_peak"]["f_mc"],
                            pf["mc_at_peak"]["se"],
                            pf["mc_at_peak"]["gap"]))
                L.append("  - GH node agreement at the argmax: %.3e"
                         % pf["gh_node_agreement"])
        pk = row["peak"]
        L.append("- actual peak of the sigma=1 objective on the scan:")
        L.append("  gamma_peak = %.9e, f_peak = %.10e (golden iters %r)"
                 % (pk["gamma"], pk["f"], pk["record"]["golden"]["iters"]))
        L.append("")
    L.append("## Findings (PROVISIONAL, NOT A COMPLETE-RULE ESTIMATE)")
    L.append("")
    for var, row in R["rows"].items():
        fnd = []
        sol = row["delta1_solution"]
        if sol["attained"]:
            bpr = row["beta_pop_at_gamma"]
            fnd.append("gamma*(d*) = %.4f; beta_pop = %.4f per s_ref unit"
                       "-> c*_prov = %s (%s)"
                       % (sol["gamma"], bpr["beta_pop"],
                          "%g" % bpr["cstar_prov"], bpr["grid_match"]))
        else:
            fnd.append("delta* NOT attained (%r)" % sol.get("note"))
        if row.get("peak_status") == "not_attained_on_bracket":
            pf = row["delta2"].get("delta2_peak_finding", {})
            fnd.append("2d* not attainable: actual peak %.6e at gamma-peak"
                       " %.4f, margin %.3e" %
                       (pf["peak_f"], pf["peak_gamma"], pf["margin"]))
        else:
            sol2 = row["delta2"].get("delta2_solution", {})
            if sol2.get("attained"):
                fnd.append("2d* attained at gamma = %.4f" % sol2["gamma"])
        L.append("- %s: %s" % (var, "; ".join(fnd)))
    L.append("")
    L.append("Elapsed seconds: %.2f" % R.get("elapsed_s", -1.0))
    txt = "\n".join(L) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return path


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--check" in argv:
        _ok, det = integrity()
        sys.stdout.write("integrity self_and_battery=%r detail=%r\n" % (_ok, det))
        return 0 if _ok else 1
    _ok, det = integrity()
    if not _ok:
        sys.stdout.write("CALIBRATION REFUSED: working files do not match "
                         "their committed blobs (%r)\n" % (det,))
        return 3
    R = run_calibration()
    path = write_calibration_report(
        R, os.path.join(_HERE, "CALIBRATION_REPORT_2026-10-18.md"))
    sys.stdout.write("CALIBRATION DONE report=%s elapsed=%.1fs\n"
                     % (path, R.get("elapsed_s", -1.0)))
    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
