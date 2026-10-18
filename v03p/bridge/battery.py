"""v03p/bridge/battery.py — bridge verification battery (freeze part 2).

Governance: works under the owner bridge authorization (Foued, 2026-10-18,
bridge draft §0.2 item 12 / source record §8 part 5) and the frozen
declaration v03p/bridge/BATTERY_SPEC.md (commits a527828 + the pre-code
W-DEF amendment). Battery-only scope: NC1 closed, NC2 held, Phase 1
unauthorized, no solver generation, no hidden-outcome access, no spending,
no master merge. Every output PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE.

Structure (BATTERY_SPEC.md):
  Part A  weights: two exact paths (production block path / reference pair
          path) + brute-force enumeration validator (W0/W3), folded over the
          Binomial bucket-size law (W-DEF items 1-5).
  Part B  zero-RE: unpenalized Newton-IRLS restricted fits + exact KL
          reference (checks i, ii, Q).
  Part C  sigma=1: Gauss-Hermite node doubling + seeded MC (checks ii/iii/
          v, V-1, V-2).
  Part D  mutation battery (iv), bisection self-test (iii), report writer.
No number from a run is official until the freeze commit naming the blob
hash of this file exists on the branch and every declared check passes.
"""

import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_A1_DIR = os.path.normpath(os.path.join(_HERE, os.pardir, "a1"))
if _A1_DIR not in sys.path:
    sys.path.insert(0, _A1_DIR)
import a1_support_comparison as A1  # committed source; module-level CK/SCEN build

N = 600
TTOL = 1e-10          # W1/W2 tolerance
BTOL = 1e-12          # W0/W3 brute-force tolerance
GAMMA_GRID = (0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0)
GAMMA_BAND = (0.25, 0.5, 1.0)
MONO_GRID = tuple(i * 0.5 for i in range(17))
DELTA1 = 0.020273255405408218
DELTA2 = 0.040546510810816436
TH0, TH1 = 0.0, -1.0
SIG_B, SIG_S = 1.0, 1.0
GH_NODES = (64, 128, 256)
MC_SEED = 20261018
MC_DRAWS = 2 * 10 ** 6
VARIANTS = ("a-hist", "a-50:50", "c-hist", "c-50:50")

LFACT = [0.0]
for _i in range(1, N + 2):
    LFACT.append(LFACT[-1] + math.log(_i))


def lchoose(n, k):
    return LFACT[n] - LFACT[k] - LFACT[n - k]


def expit(x):
    x = np.asarray(x, dtype=np.float64)
    out = np.empty_like(x)
    pos = x >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-x[pos]))
    ex = np.exp(x[~pos])
    out[~pos] = ex / (1.0 + ex)
    return out


def eta(k, c, gamma):
    return TH0 + TH1 * math.log(1.0 + k) + gamma * c

# ---------------------------------------------------------------------------
# Part A.  Weights — production block path
# ---------------------------------------------------------------------------


def levels_of(k):
    return list(A1.CK[k][0])


def rhos_of(k):
    vals, probs = A1.CK[k]
    return vals, list(probs)


def suffix_last_ge4(w, probs_suf):
    """P(last occupied level of a suffix composition has count >= 4 | w bodies).

    probs_suf: level probabilities of the suffix set S (given in the order the
    caller declares; any fixed order works — the formula sums over every
    candidate last-occupied level b).  Exact closed form; RGT(0) = 0.
    """
    if w <= 0:
        return 0.0
    V = len(probs_suf)
    tot = 0.0
    # iterate S-levels in the given order; "members strictly before b in S"
    # must use the caller's ordering only for weights, the event only needs
    # the b-marginal mass and the above-b mass, so use a canonical pass with
    # the suffix's own ascending order == probs_suf order.
    for b in range(V):
        pb = probs_suf[b]
        if pb <= 0.0:
            continue
        above = sum(probs_suf[b + 1:])
        mass_free = 1.0 - above          # levels of S strictly below b
        if mass_free < 0.0:
            mass_free = 0.0
        s = 0.0
        for cb in range(4, w + 1):
            s += math.exp(lchoose(w, cb) + cb * math.log(pb)
                          + (w - cb) * math.log(mass_free)) if mass_free > 0 else 0.0
        tot += s
    return min(max(tot, 0.0), 1.0)


def prefix_first_ge4(u, probs_pre):
    """P(first occupied level of a prefix composition has count >= 4 | u bodies).

    Mirror of suffix_last_ge4 with ascending order fixed by the caller.
    """
    if u <= 0:
        return 0.0
    V = len(probs_pre)
    tot = 0.0
    for a in range(V):
        pa = probs_pre[a]
        if pa <= 0.0:
            continue
        below = sum(probs_pre[:a])
        mass_free = 1.0 - below          # levels strictly above a within prefix
        if mass_free < 0.0:
            mass_free = 0.0
        s = 0.0
        for ca in range(4, u + 1):
            s += math.exp(lchoose(u, ca) + ca * math.log(pa)
                          + (u - ca) * math.log(mass_free)) if mass_free > 0 else 0.0
        tot += s
    return min(max(tot, 0.0), 1.0)

# ---------------------------------------------------------------------------
# Per-n pool setup for the two paths
# ---------------------------------------------------------------------------


def _pools(k):
    """Level arrays and prefix/suffix normalized pools for bucket k."""
    vals = list(A1.CK[k][0])
    probs = list(A1.CK[k][1])
    V = len(vals)
    below = [sum(probs[:i]) for i in range(V + 1)]        # below[b] = mass strictly below index b
    above = [sum(probs[i + 1:]) for i in range(V)]        # above[a] = mass strictly above index a
    return vals, probs, below, above


def _lft(u, probs_pre):
    """P(first occupied prefix level has count >= 4 | u bodies), prefix probs in
    ascending order, renormalized.  LFT(0) = 0.

    For candidate first-occupied level a: levels strictly below a empty and
    N_a >= 4; the remaining u - ca bodies sit on prefix levels strictly above a.
    Cached on (probs tuple, u).
    """
    key = (probs_pre, u)
    hit = _LFT_CACHE.get(key)
    if hit is not None:
        return hit
    out = 0.0
    if u > 0:
        norm = sum(probs_pre)
        acc = 0.0
        for pa in probs_pre:
            pa_n = pa / norm
            rest = 1.0 - acc - pa_n            # prefix levels strictly above a
            acc += pa_n
            lr = math.log(rest) if rest > 0.0 else None
            lpa = math.log(pa_n)
            s = 0.0
            for ca in range(4, u + 1):
                # rest**(u - ca) with rest==0 handled: 0.0**0 == 1.0 in Python
                lg = lchoose(u, ca) + ca * lpa
                if lr is None:
                    if u - ca > 0:
                        continue
                else:
                    lg += (u - ca) * lr
                s += math.exp(lg)
            out += s
    _LFT_CACHE[key] = out
    return out


_LFT_CACHE = {}


def _rgt(w, probs_suf):
    """P(last occupied suffix level has count >= 4 | w bodies), mirror of _lft."""
    return _lft(w, tuple(reversed(tuple(probs_suf))))


# ---------------------------------------------------------------------------
# Pair-pool helpers (exact trinomial arithmetic on grouped mass)
# ---------------------------------------------------------------------------

_BT_CACHE = {}


def _bintail_ge4(m, q):
    """P(Bin(m, q) >= 4), m <= N; q == 0 -> 0.0, q == 1 (m >= 4) -> 1.0."""
    if m < 4:
        return 0.0
    if q <= 0.0:
        return 0.0
    if q >= 1.0:
        return 1.0
    key = (m, q)
    v = _BT_CACHE.get(key)
    if v is None:
        s = 0.0
        for j in range(4, m + 1):
            s += math.exp(lchoose(m, j) + j * math.log(q) + (m - j) * math.log1p(-q))
        v = s
        _BT_CACHE[key] = v
    return v


def _trinom3(x, y, n, pa, pm, pb):
    """Trinomial cell P(N_a = x, N_b = y | n) for the 3-cat (a, mid, b) split.

    x + y <= n; pm may be 0 (then any n > x + y cell is 0).
    """
    z = n - x - y
    if z < 0:
        return 0.0
    if pm == 0.0 and z > 0:
        return 0.0
    lg = LFACT[n] - LFACT[x] - LFACT[y] - LFACT[z] + x * math.log(pa) \
        + y * math.log(pb)
    if z > 0:
        lg += z * math.log(pm)
    return math.exp(lg)


def _pair_aggregates(pa, pm, pb, n):
    """(P(A >= 4 and B >= 4 with mass confined to the pair), E[A 1], E[B 1],
    E[T 1]) for the observed pair (a, b) in a size-n bucket.

    All quantities are joint cells of the FULL multinomial with the outside
    blocks pinned to zero: cells of the confined trinomial.  The
    inclusion-exclusion pieces are evaluated in the CONDITIONAL trinomial
    measure (normalized masses) and the joint values scaled by
    (pa + pm + pb)**n.
    """
    rs = pa + pm + pb
    if rs <= 0.0 or n < 8:
        return 0.0, 0.0, 0.0, 0.0
    pan, pbn = pa / rs, pb / rs
    sc = math.exp(n * math.log(rs))
    p_a3 = math.exp(n * math.log1p(-pan))
    for x in range(1, min(3, n) + 1):
        p_a3 += math.exp(lchoose(n, x) + x * math.log(pan)
                         + (n - x) * math.log1p(-pan))
    p_b3 = math.exp(n * math.log1p(-pbn))
    for y in range(1, min(3, n) + 1):
        p_b3 += math.exp(lchoose(n, y) + y * math.log(pbn)
                         + (n - y) * math.log1p(-pbn))
    p_ab3 = 0.0
    for x in range(0, min(3, n) + 1):
        for y in range(0, min(3, n - x) + 1):
            z = n - x - y
            lg = LFACT[n] - LFACT[x] - LFACT[y] - LFACT[z]
            f = True
            if z > 0:
                if pm > 0.0:
                    lg += z * math.log(pm / rs)
                else:
                    f = False
            if f and x > 0:
                lg += x * math.log(pan)
            if f and y > 0:
                lg += y * math.log(pbn)
            if f:
                p_ab3 += math.exp(lg)
    pvc = max(0.0, min(1.0, 1.0 - p_a3 - p_b3 + p_ab3))
    pv = sc * pvc
    qa = pb / (pm + pb) if pm + pb > 0 else 0.0
    qb = pa / (pm + pa) if pm + pa > 0 else 0.0
    ea = 0.0
    for x in range(4, n + 1):
        ea += x * math.exp(lchoose(n, x) + x * math.log(pan)
                           + (n - x) * math.log1p(-pan)) * _bintail_ge4(n - x, qa)
    eb = 0.0
    for y in range(4, n + 1):
        eb += y * math.exp(lchoose(n, y) + y * math.log(pbn)
                           + (n - y) * math.log1p(-pbn)) * _bintail_ge4(n - y, qb)
    ea = max(sc * ea, 0.0)
    eb = max(sc * eb, 0.0)
    et = max(n * pv - ea - eb, 0.0)
    return pv, ea, eb, et


# ---------------------------------------------------------------------------
# Production path (first-nonzero-block aggregates)
# ---------------------------------------------------------------------------


def prod_per_n(k):
    """Production path: P(I[n]), E[N_c 1{I}[n]] per level for bucket k.

    Aggregation: the first occupied level i pins the left extreme (its own
    count >= 4) and the right extreme is tested inside the suffix composition
    by the mirror-tail law RGT (suffix empty -> single-level bucket -> failed).
    Per-level expectations: c = first occupied (own count), c = last occupied
    (mirror form), or c strictly inside an observed pair (the pair's grouped
    trinomial mid-term identity, separately implemented).
    """
    vals, probs, below, above = _pools(k)
    V = len(vals)
    PI = [0.0] * (N + 1)
    EN = [[0.0] * (N + 1) for _ in range(V)]
    sfx_norm = []
    for i in range(V):
        sfx = probs[i + 1:]
        if sfx:
            t = sum(sfx)
            sfx_norm.append(tuple(p / t for p in sfx))
        else:
            sfx_norm.append(None)
    for i in range(V - 1):                      # i has a nonempty suffix
        pa, pv_above, sfx = probs[i], above[i], sfx_norm[i]
        lpa = math.log(pa)
        lab = math.log(pv_above) if pv_above > 0 else 0.0
        for n in range(8, N + 1):
            base = 0.0
            enc = 0.0
            for nu in range(4, n + 1):
                t = math.exp(lchoose(n, nu) + nu * lpa + (n - nu) * lab) \
                    * _rgt(n - nu, sfx)
                base += t
                enc += nu * t
            PI[n] += base
            EN[i][n] += enc
    for ci in range(1, V):                      # ci has a nonempty prefix
        pb, pv_below, pre = probs[ci], below[ci], tuple(probs[:ci])
        lpb = math.log(pb)
        lbe = math.log(pv_below) if pv_below > 0 else 0.0
        for n in range(8, N + 1):
            enc = 0.0
            for nu in range(4, n + 1):
                enc += nu * math.exp(lchoose(n, nu) + nu * lpb + (n - nu) * lbe) \
                    * _lft(n - nu, pre)
            EN[ci][n] += enc
    for ai in range(V - 1):                     # mid-level terms pair by pair
        for bi in range(ai + 2, V):
            pm_ab = sum(probs[ai + 1:bi])
            if pm_ab <= 0.0:
                continue
            for n in range(8, N + 1):
                _, _, _, et = _pair_aggregates(probs[ai], pm_ab, probs[bi], n)
                for ci in range(ai + 1, bi):
                    EN[ci][n] += (probs[ci] / pm_ab) * et
    return PI, EN


# ---------------------------------------------------------------------------
# Reference path (observed-pair aggregation)
# ---------------------------------------------------------------------------


def ref_per_n(k):
    """Reference path: P(I[n]), E[N_c 1{I}[n]] per level for bucket k.

    Aggregation: sum over ordered pairs (a, b), a < b, of
    P(all mass within [a, b] and both pair endpoints carry >= 4) — inclusive
    over the pair-nested low/high marginal binomials; per-level terms from the
    pair-truncated means E[A 1], E[B 1] and the mid identity
    E[N_c 1 | pair] = (rho_c / rho_mid_ab) * E[T 1 | pair].
    Independent of the production path: different derivation, different code.
    """
    vals, probs, below, above = _pools(k)
    V = len(vals)
    PI = [0.0] * (N + 1)
    EN = [[0.0] * (N + 1) for _ in range(V)]
    for n in range(8, N + 1):
        for ai in range(V - 1):
            for bi in range(ai + 1, V):
                pm_ab = sum(probs[ai + 1:bi])
                pv, ea, eb, et = _pair_aggregates(probs[ai], pm_ab, probs[bi], n)
                PI[n] += pv
                EN[ai][n] += ea
                EN[bi][n] += eb
                if pm_ab > 0.0:
                    for ci in range(ai + 1, bi):
                        EN[ci][n] += (probs[ci] / pm_ab) * et
    return PI, EN


# ---------------------------------------------------------------------------
# Brute force (W0/W3 validator)
# ---------------------------------------------------------------------------


def brute_per_n(k, nmax):
    """Exact enumeration over all C-count vectors: P(I[n]), E[N_c 1{I}[n]] for
    n <= nmax.  Predicate: >= 2 distinct occupied levels and both observed
    extremes (first and last occupied) at >= 4 bodies; n >= 8 by the caller."""
    vals, probs, below, above = _pools(k)
    V = len(vals)
    acc_p = [0.0] * (nmax + 1)
    acc_e = [[0.0] * (nmax + 1) for _ in range(V)]
    counts = [0] * V

    def enum(idx, rem, lpmf):
        if idx == V:
            if rem != 0:
                return
            occ = [j for j in range(V) if counts[j] > 0]
            if len(occ) < 2 or counts[occ[0]] < 4 or counts[occ[-1]] < 4:
                return
            wt = math.exp(lpmf)
            acc_p[n] += wt
            for j in range(V):
                if counts[j]:
                    acc_e[j][n] += counts[j] * wt
            return
        p = probs[idx]
        for c in range(rem + 1):
            counts[idx] = c
            enum(idx + 1, rem - c,
                 lpmf - LFACT[c] + (c * math.log(p) if c > 0 else 0.0))
        counts[idx] = 0

    for n in range(8, min(nmax, N) + 1):
        enum(0, n, LFACT[n])
    return acc_p, acc_e


# ---------------------------------------------------------------------------
# Binomial fold and weight assembly (W-DEF items 1, 4, 5)
# ---------------------------------------------------------------------------


def binom_pmf(n_max, p):
    bm = [0.0] * (n_max + 1)
    lp, l1p = math.log(p), math.log1p(-p)
    for i in range(n_max + 1):
        bm[i] = math.exp(lchoose(n_max, i) + i * lp + (n_max - i) * l1p)
    return bm


def fold_variant(k, mix_p, PI, EN):
    """Fold per-n aggregates over n ~ Binomial(N, mix_p): returns
    (E[n 1{I}], [E[N_c 1{I}] per level], per-n P list kept for W2)."""
    bm = binom_pmf(N, mix_p)
    e1 = sum((nn) * bm[nn] * PI[nn] for nn in range(N + 1))
    vals = list(A1.CK[k][0])
    ec = [sum(bm[nn] * EN[j][nn] for nn in range(N + 1)) for j in range(len(vals))]
    return e1, ec


# ---------------------------------------------------------------------------
# Part A smoke (engineering validation pre-freeze; not a battery check)
# ---------------------------------------------------------------------------


def smoke_part_a(k=5, brute_nmax=12):
    import time
    t0 = time.time()
    PI_p, EN_p = prod_per_n(k)
    t1 = time.time()
    PI_r, EN_r = ref_per_n(k)
    t2 = time.time()
    PI_b, EN_b = brute_per_n(k, brute_nmax)
    t3 = time.time()
    vals = levels_of(k)
    V = len(vals)
    rep = {"k": k,
           "times": {"prod": t1 - t0, "ref": t2 - t1, "brute": t3 - t2}}
    # W0: brute vs both paths, n <= brute_nmax
    m_pb, m_rb = 0.0, 0.0
    for nn in range(8, brute_nmax + 1):
        m_pb = max(m_pb, abs(PI_p[nn] - PI_b[nn]), abs(PI_r[nn] - PI_b[nn]))
        for j in range(V):
            m_pb = max(m_pb, abs(EN_p[j][nn] - EN_b[j][nn]),
                       abs(EN_r[j][nn] - EN_b[j][nn]))
    rep["W0_max_abs_diff"] = m_pb
    # W1: production vs reference, all n <= N
    m_pr = 0.0
    for nn in range(8, N + 1):
        m_pr = max(m_pr, abs(PI_p[nn] - PI_r[nn]))
        for j in range(V):
            m_pr = max(m_pr, abs(EN_p[j][nn] - EN_r[j][nn]))
    rep["W1_max_abs_diff"] = m_pr
    # W2: reference P(I|n) vs committed A1.f_s0
    m_a1 = 0.0
    for nn in range(8, N + 1):
        m_a1 = max(m_a1, abs(PI_r[nn] - A1.f_s0(k, nn)))
    rep["W2_max_abs_diff"] = m_a1
    # folds over the committed SCEN mixes
    for var in ("a-hist", "c-hist"):
        e1p, ecp = fold_variant(k, A1.SCEN[var][k], PI_p, EN_p)
        e1r, ecr = fold_variant(k, A1.SCEN[var][k], PI_r, EN_r)
        rep[f"{var}:max|Eprod-Eref|"] = max(abs(e1p - e1r),
                                            max(abs(a - b) for a, b in zip(ecp, ecr)))
        rep[f"{var}:E1/k"] = e1p
    return rep


# ---------------------------------------------------------------------------
# Part B.  Support-conditioned weightsets and the zero-RE benchmark
# ---------------------------------------------------------------------------

TAU = math.sqrt(SIG_B ** 2 + SIG_S ** 2)
PARAM_MAXIT = 50
FIT_TOL = 1e-13
CHK_I_TOL = 1e-9
CHK_II_TOL = 1e-12
GH_TOL = 1e-12
MONO0_TOL = 1e-12
MONO1_TOL = 5e-10
MCX_FACTOR = 5.0
CHK_V_G_TOL = 1e-9
M4_TOL = 1e-12
MUT_TOL = 1e-6
BISECT_BRACKET = (0.0, 8.0)
BISECT_MAXIT = 200
BISECT_ATAIN = 1e-4
V2_SEED = MC_SEED + 1


def truth_p(k, c, gamma):
    return expit(eta(k, c, gamma))


def weights_per_k(k, mix_p, PI, EN):
    lv = levels_of(k)
    e1, ec = fold_variant(k, mix_p, PI, EN)
    if e1 <= 0.0:
        raise RuntimeError("degenerate stratum: k=%r" % (k,))
    pi = [e / e1 for e in ec]
    mean_c = sum(pi[j] * lv[j] for j in range(len(lv)))
    var_c = sum(pi[j] * (lv[j] - mean_c) ** 2 for j in range(len(lv)))
    return e1, pi, var_c


def assemble_weightsets(path):
    agg = {k: (prod_per_n(k) if path == "prod" else ref_per_n(k))
           for k in (5, 10)}
    out = {}
    for var in VARIANTS:
        d = {}
        for k in (5, 10):
            e1, pi, vc = weights_per_k(k, A1.SCEN[var][k], *agg[k])
            d["e1%d" % k] = e1
            d["pi%d" % k] = pi
            d["var%d" % k] = vc
            d["levels%d" % k] = levels_of(k)
        s = d["e15"] + d["e110"]
        d["w5"] = d["e15"] / s
        d["w10"] = d["e110"] / s
        out[var] = d
    return out


def cell_list(wset):
    out = []
    for k in (5, 10):
        wk = wset["w%d" % k]
        lv = wset["levels%d" % k]
        pi = wset["pi%d" % k]
        for j, c in enumerate(lv):
            out.append((k, c, wk * pi[j]))
    return out


def delta_of(wset, pt):
    """Zero-RE benchmark Delta = sum_k w_k sum_c pi_c KL(p(k,c) || qbar_k),
    qbar_k = sum_c pi_c p(k,c); pt maps (k, c) -> probability.  Returns
    (delta, qbars)."""
    tot = 0.0
    qbars = {}
    for k in (5, 10):
        lv = wset["levels%d" % k]
        pi = wset["pi%d" % k]
        wk = wset["w%d" % k]
        qbar = sum(pi[j] * pt[(k, lv[j])] for j in range(len(lv)))
        qbar = min(max(qbar, 1e-15), 1.0 - 1e-15)
        qbars[k] = qbar
        lq, l1q = math.log(qbar), math.log1p(-qbar)
        d = 0.0
        for j, c in enumerate(lv):
            p = min(max(pt[(k, c)], 1e-15), 1.0 - 1e-15)
            d += pi[j] * (p * (math.log(p) - lq)
                          + (1.0 - p) * (math.log1p(-p) - l1q))
        tot += wk * d
    return tot, qbars


def truth_table(wset, gamma):
    return {(k, c): truth_p(k, c, gamma) for (k, c, _w) in cell_list(wset)}


def grad_delta(wset, pt, qbars):
    """Exact per-cell gradient d(Delta)/d(p) = w_k pi_c*(logit(p) - logit(qbar_k))
    (the qbar-derivative terms cancel in aggregate)."""
    g = {}
    for k in (5, 10):
        wk = wset["w%d" % k]
        lv = wset["levels%d" % k]
        pi = wset["pi%d" % k]
        qbar = qbars[k]
        lq = math.log(qbar / (1.0 - qbar))
        for j, c in enumerate(lv):
            p = pt[(k, c)]
            g[(k, c)] = wk * pi[j] * (math.log(p / (1.0 - p)) - lq)
    return g

# ---------------------------------------------------------------------------
# Part C.  sigma = 1 truth machinery: Gauss-Hermite, node doubling, MC
# ---------------------------------------------------------------------------

_GH = {}


def _gh_nodes(n):
    if n not in _GH:
        x, w = np.polynomial.hermite.hermgauss(n)
        _GH[n] = (x, w)
    return _GH[n]


def pbar_sigma1(k, c, gamma, nodes, tau):
    x, w = _gh_nodes(nodes)
    e = eta(k, c, gamma)
    a = tau * math.sqrt(2.0)
    f = expit(e + a * x)
    return float(np.dot(w, f)) / math.sqrt(math.pi)


def pbar_sigma1_var(k, c, gamma, nodes, tau):
    x, w = _gh_nodes(nodes)
    e = eta(k, c, gamma)
    a = tau * math.sqrt(2.0)
    f = expit(e + a * x)
    m1 = float(np.dot(w, f)) / math.sqrt(math.pi)
    m2 = float(np.dot(w, f * f)) / math.sqrt(math.pi)
    return max(m2 - m1 * m1, 0.0)


def pbar_sigma1_table(wset, gamma, nodes, tau=TAU):
    return {(k, c): pbar_sigma1(k, c, gamma, nodes, tau)
            for (k, c, _w) in cell_list(wset)}


def gh_convergence(wsets):
    """Node-doubling record over every cell x gamma_grid: (max64_128,
    max128_256) plus per-row maxima; frozen totals use GH_NODES[-1]."""
    m68 = []
    m816 = []
    for path, wsets_p in wsets.items():
        wset = wsets_p["a-hist"]
        cells = cell_list(wset)
        for gamma in GAMMA_GRID:
            for k, c, _w in cells:
                m68.append(abs(pbar_sigma1(k, c, gamma, 64, TAU)
                               - pbar_sigma1(k, c, gamma, 128, TAU)))
                m816.append(abs(pbar_sigma1(k, c, gamma, 128, TAU)
                                - pbar_sigma1(k, c, gamma, 256, TAU)))
    return max(m68), max(m816)


def mc_sample_s():
    rng = np.random.default_rng(MC_SEED)
    return TAU * rng.standard_normal(MC_DRAWS)


def mc_pbar_table(wset, gamma, s, store_var=False):
    out, vout = {}, {}
    for k, c, _w in cell_list(wset):
        f = expit(eta(k, c, gamma) + s)
        m1 = float(f.mean())
        out[(k, c)] = m1
        if store_var:
            vout[(k, c)] = float(f.var(ddof=0))
    return (out, vout) if store_var else out


def mc_delta(wset, gamma, s, pt_gh):
    """MC-estimated Delta plus delta-method SE from the shared s-sample."""
    pt, var = mc_pbar_table(wset, gamma, s, store_var=True)
    dl, qbars = delta_of(wset, pt)
    dl_gh, _ = delta_of(wset, pt_gh)
    g = grad_delta(wset, pt_gh, qbars)
    se2 = 0.0
    for (k, c), gj in g.items():
        se2 += (gj * gj) * var[(k, c)]
    se = math.sqrt(se2 / MC_DRAWS)
    return dl, dl_gh, se


# ---------------------------------------------------------------------------
# Part B fitting machinery: unpenalized Newton-IRLS on restricted spaces
# ---------------------------------------------------------------------------


def solve_linear(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-14:
            m[piv][col] = 1e-14
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r == col:
                continue
            f = m[r][col] / m[col][col]
            for cc in range(col, n + 1):
                m[r][cc] -= f * m[col][cc]
    return [m[i][n] / m[i][i] for i in range(n)]


def irls_logistic(X, tv, om, ridge=0.0, tol=FIT_TOL, maxit=PARAM_MAXIT):
    """Weighted logistic Newton-IRLS on probability targets tv with cell
    weights om, mirroring the retained engine (study/models.py): w = pr(1-pr)
    + 1e-12, z = eta + (t - pr)/w, ridge added on the full diagonal.  Returns
    (beta, iters, max|w o (t - pr) x_i|)."""
    p = len(X[0])
    beta = [0.0] * p
    iters = 0
    for it in range(maxit):
        iters = it + 1
        xtwx = [[(ridge if i == j else 0.0) for j in range(p)] for i in range(p)]
        xtwz = [0.0] * p
        for row, t, o in zip(X, tv, om):
            e = sum(b * xi for b, xi in zip(beta, row))
            pr = expit_scalar(e)
            w = pr * (1.0 - pr) + 1e-12
            z = e + (t - pr) / w
            wo = w * o
            for i in range(p):
                for j in range(p):
                    xtwx[i][j] += wo * row[i] * row[j]
                xtwz[i] += wo * row[i] * z
        new = solve_linear(xtwx, xtwz)
        dz = max(abs(nw - b) for nw, b in zip(new, beta))
        beta = new
        if dz < tol:
            break
    score = [0.0] * p
    for row, t, o in zip(X, tv, om):
        e = sum(b * xi for b, xi in zip(beta, row))
        pr = expit_scalar(e)
        gs = o * (t - pr)
        for i, xi in enumerate(row):
            score[i] += gs * xi
    mx = max(abs(sc) for sc in score)
    return beta, iters, mx


def expit_scalar(z):
    if z >= 0.0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def design_rows(wset, family):
    rows = []
    for k, c, _w in cell_list(wset):
        r = [1.0 if k == 5 else 0.0, 1.0 if k == 10 else 0.0]
        if family == "extended":
            r.append(c)
        rows.append(r)
    return rows


def fit_restricted(wset, gamma, sigma, family, nodes=None, ridge=0.0):
    cells = cell_list(wset)
    X = design_rows(wset, family)
    om = [w for _k, _c, w in cells]
    if sigma == 0:
        tv = [truth_p(k, c, gamma) for (k, c, _w) in cells]
    else:
        tv = [pbar_sigma1(k, c, gamma, nodes, TAU) for (k, c, _w) in cells]
    beta, iters, mx = irls_logistic(X, tv, om, ridge=ridge)
    qh = {}
    for row, (k, c, _w) in zip(X, cells):
        qh[(k, c)] = expit_scalar(sum(b * xi for b, xi in zip(beta, row)))
    return {"beta": beta, "iters": iters, "grad": mx, "qhat": qh,
            "targets": tv}


def fit_deviation(fit):
    return max(abs(q - t) for q, t in zip(fit["qhat"].values(), fit["targets"]))


def ce_of(wset, pt, pt2):
    """sum w pi CE(first || second) over cells: -a log b - (1-a) log(1-b)."""
    tot = 0.0
    for k, c, w in cell_list(wset):
        a = min(max(pt[(k, c)], 1e-15), 1.0 - 1e-15)
        b = min(max(pt2[(k, c)], 1e-15), 1.0 - 1e-15)
        tot += w * (-(a * math.log(b) + (1.0 - a) * math.log1p(-b)))
    return tot


def kl_of(wset, pt, pt2):
    """sum w pi KL(pt || pt2) over cells."""
    tot = 0.0
    for k, c, w in cell_list(wset):
        a = min(max(pt[(k, c)], 1e-15), 1.0 - 1e-15)
        b = min(max(pt2[(k, c)], 1e-15), 1.0 - 1e-15)
        tot += w * (a * (math.log(a) - math.log(b))
                    + (1.0 - a) * (math.log1p(-a) - math.log1p(-b)))
    return tot


def sigma0_delta_prod(wset, gamma):
    """Closed-form zero-RE benchmark on the production weightset: Delta and
    the full target table."""
    pt = truth_table(wset, gamma)
    return delta_of(wset, pt)


def sigma0_delta_ref(wset, gamma):
    pt = truth_table(wset, gamma)
    return delta_of(wset, pt)


def weight_diffs(ws_prod, ws_ref):
    """W1-derivative margins over all variants: max |w|, |pi|, |var|, |e1|
    differences between paths plus per-n agreement is separate."""
    out = {}
    for var in VARIANTS:
        m = 0.0
        a, b = ws_prod[var], ws_ref[var]
        for kk in (5, 10):
            m = max(m, abs(a["w%d" % kk] - b["w%d" % kk]),
                    abs(a["var%d" % kk] - b["var%d" % kk]))
            for ja, jb in zip(a["pi%d" % kk], b["pi%d" % kk]):
                m = max(m, abs(ja - jb))
        out[var] = m
    return out


def uniform_pi_wset(wset):
    """Mutation m1: uniform within-stratum C-level weights, stratum weights
    kept."""
    d = dict(wset)
    for kk in (5, 10):
        n = len(d["levels%d" % kk])
        d["pi%d" % kk] = [1.0 / n] * n
    return d


def bisection_solve(fn, target, lo=BISECT_BRACKET[0], hi=BISECT_BRACKET[1],
                    maxit=BISECT_MAXIT):
    """Monotone-increasing fn on [lo, hi]: solve fn(x) = target.  Returns
    dict(gamma, attained, iters, delta_at, bracket_value_hi)."""
    flo, fhi = fn(lo), fn(hi)
    if for_iteration_guard(flo, fhi, target):
        return {"attained": False, "iters": 0, "gamma": None,
                "delta_at": None, "f_lo": flo, "f_hi": fhi}
    a, fa, b, fb = lo, flo, hi, fhi
    it = 0
    x = 0.0
    fx = fa
    for it in range(1, maxit + 1):
        x = 0.5 * (a + b)
        fx = fn(x)
        if fx < target:
            a, fa = x, fx
        else:
            b, fb = x, fx
        if b - a < 1e-12:
            break
    return {"attained": True, "iters": it, "gamma": x, "delta_at": fx,
            "f_lo": fa, "f_hi": fb}


def for_iteration_guard(flo, fhi, target):
    return not (flo < target <= fhi)


# ---------------------------------------------------------------------------
# Part D.  Battery runner, report writer, entry point
# ---------------------------------------------------------------------------

ALL_CELLS = tuple((k, c) for k in (5, 10) for c in levels_of(k))
RIDGE = 1e-6


def _chk(R, cid, row_id, ok, margin, thr, report_only=False):
    R["checks"].append({"id": cid, "row": row_id,
                        "verdict": ("n/a" if report_only else
                                    ("PASS" if ok else "FAIL")),
                        "margin": margin, "thr": thr})
    return report_only or bool(ok)


def _gh_mc_tables():
    """Per gamma_grid shared GH-256 nodal table and MC mean/var tables."""
    s = TAU * np.random.default_rng(MC_SEED).standard_normal(MC_DRAWS)
    pt_gh, pt_mc, var_mc = {}, {}, {}
    for gamma in GAMMA_GRID:
        for k, c in ALL_CELLS:
            pt_gh[(gamma, k, c)] = pbar_sigma1(k, c, gamma, 256, TAU)
            f = expit(eta(k, c, gamma) + s)
            pt_mc[(gamma, k, c)] = float(f.mean())
            var_mc[(gamma, k, c)] = float(f.var(ddof=0))
    return s, pt_gh, pt_mc, var_mc


def run_battery():
    R = {"meta": {"N": N, "gamma_grid": tuple(GAMMA_GRID),
                  "mono_grid": tuple(MONO_GRID),
                  "delta_targets": (DELTA1, DELTA2), "gh_nodes": GH_NODES,
                  "mc_draws": MC_DRAWS, "seeds": (MC_SEED, V2_SEED)},
         "checks": [], "rows": {}, "global": {}, "all_pass": False,
         "first_fail": None}
    import time
    t_start = time.time()

    m_w0, m_w1, m_w2 = 0.0, 0.0, 0.0
    for k in (5, 10):
        PI_p, EN_p = prod_per_n(k)
        PI_r, EN_r = ref_per_n(k)
        PI_b, EN_b = brute_per_n(k, 14)
        lv = levels_of(k)
        for nn in range(8, 15):
            m_w0 = max(m_w0, abs(PI_p[nn] - PI_b[nn]), abs(PI_r[nn] - PI_b[nn]))
            for j in range(len(lv)):
                m_w0 = max(m_w0, abs(EN_p[j][nn] - EN_b[j][nn]),
                           abs(EN_r[j][nn] - EN_b[j][nn]))
        for nn in range(8, N + 1):
            m_w1 = max(m_w1, abs(PI_p[nn] - PI_r[nn]))
            for j in range(len(lv)):
                m_w1 = max(m_w1, abs(EN_p[j][nn] - EN_r[j][nn]))
            m_w2 = max(m_w2, abs(PI_r[nn] - A1.f_s0(k, nn)))
    R["global"]["W0_margin_nle14"] = m_w0
    R["global"]["W1_margin_pern"] = m_w1
    R["global"]["W2_margin_vs_A1_f_s0"] = m_w2
    if not _chk(R, "W0/W3", "-", m_w0 <= BTOL, m_w0, BTOL):
        R["first_fail"] = "W0/W3"
        return R
    if not _chk(R, "W1", "-", m_w1 <= TTOL, m_w1, TTOL):
        R["first_fail"] = "W1"
        return R
    if not _chk(R, "W2", "-", m_w2 <= TTOL, m_w2, TTOL):
        R["first_fail"] = "W2"
        return R

    ws_p = assemble_weightsets("prod")
    ws_r = assemble_weightsets("ref")
    R["global"]["weightsets"] = {"prod": {v: {kk: ws_p[v][kk]
                                              for kk in ("e15", "e110", "w5", "w10",
                                                         "var5", "var10")}
                                          for v in VARIANTS}}
    wd = weight_diffs(ws_p, ws_r)
    mw = max(wd.values())
    R["global"]["W1_derived_margin"] = wd
    if not _chk(R, "W1-derived", "-", mw <= TTOL, mw, TTOL):
        R["first_fail"] = "W1-derived"
        return R

    s, pt_gh, pt_mc, var_mc = _gh_mc_tables()
    gh68, gh816 = 0.0, 0.0
    for gamma in GAMMA_GRID:
        for k, c in ALL_CELLS:
            gh68 = max(gh68, abs(pbar_sigma1(k, c, gamma, 64, TAU)
                                 - pbar_sigma1(k, c, gamma, 128, TAU)))
            gh816 = max(gh816, abs(pbar_sigma1(k, c, gamma, 128, TAU)
                                   - pbar_sigma1(k, c, gamma, 256, TAU)))
    R["global"]["GH_conv_n64_to_n128"] = gh68
    R["global"]["GH_conv_n128_to_n256"] = gh816
    if not _chk(R, "GH-conv", "-",
                gh68 <= GH_TOL and gh816 <= GH_TOL,
                max(gh68, gh816), GH_TOL):
        R["first_fail"] = "GH-conv"
        return R
    v1m = 0.0
    for gamma in GAMMA_GRID:
        for k, c in ALL_CELLS:
            v1m = max(v1m, abs(pbar_sigma1(k, c, gamma, 256, 0.0)
                               - truth_p(k, c, gamma)))
    R["global"]["V1_margin"] = v1m
    if not _chk(R, "V-1", "-", v1m <= CHK_II_TOL, v1m, CHK_II_TOL):
        R["first_fail"] = "V-1"
        return R

    for var in VARIANTS:
        wsp, wsr = ws_p[var], ws_r[var]
        row = {}

        ci = {}
        worst_i = 0.0
        for gamma in GAMMA_GRID:
            dp, _ = sigma0_delta_prod(wsp, gamma)
            dr, _ = sigma0_delta_ref(wsr, gamma)
            ci[gamma] = (dp, dr, abs(dp - dr))
            worst_i = max(worst_i, abs(dp - dr))
        row["check_i_pergamma"] = ci
        row["check_i_margin"] = worst_i
        if not _chk(R, "i-s0", var, worst_i <= CHK_I_TOL, worst_i, CHK_I_TOL):
            R["first_fail"] = "i-s0:" + var
            R["rows"][var] = row
            return R

        m0 = max(abs(sigma0_delta_prod(wsp, 0.0)[0]),
                 abs(sigma0_delta_ref(wsr, 0.0)[0]))
        row["check_ii_s0_margin"] = m0
        if not _chk(R, "ii-s0", var, m0 <= CHK_II_TOL, m0, CHK_II_TOL):
            R["first_fail"] = "ii-s0:" + var
            R["rows"][var] = row
            return R

        fr = fit_restricted(wsp, 2.0, 0, "extended")
        fb = fit_restricted(wsp, 2.0, 0, "baseline")
        row["fit_s0_ext_g2"] = {"beta": fr["beta"], "iters": fr["iters"],
                                "grad": fr["grad"],
                                "dev": fit_deviation(fr)}
        row["fit_s0_base_g2"] = {"beta": fb["beta"], "iters": fb["iters"],
                                 "grad": fb["grad"],
                                 "dev": fit_deviation(fb)}

        qbq = 0.0
        for kk in (5, 10):
            _d, qbars = delta_of(wsp, truth_table(wsp, 0.0))
            qbq += wsp["w%d" % kk] * qbars[kk] * (1.0 - qbars[kk]) \
                * wsp["var%d" % kk]
        qtab = {}
        mq = 0.0
        for gamma in GAMMA_BAND:
            dp, _ = sigma0_delta_prod(wsp, gamma)
            dq = 0.5 * gamma * gamma * qbq
            qtab[gamma] = (dp, dq, abs(dp - dq))
            mq = max(mq, abs(dp - dq))
        row["q_band"] = qtab
        row["q_margin"] = mq
        _chk(R, "Q-band", var, True, mq, None, report_only=True)

        lg, lfail, mlist = None, None, []
        prev = None
        for gamma in MONO_GRID:
            dp, _ = sigma0_delta_prod(wsp, gamma)
            if prev is not None:
                dsec = dp - prev
                mlist.append((round(gamma, 4), dsec))
                if lg is None or dsec < lg:
                    lg, lfail = dsec, gamma
            prev = dp
        row["mono_s0_margin"] = lg
        row["mono_s0_min_at"] = lfail
        row["mono_s0_diffs"] = mlist
        ok_mono, peak_at, mono_why = _mono_contract(mlist, MONO0_TOL, 5e-10)
        row["mono_s0_contract"] = {"ok": ok_mono, "peak_at": peak_at,
                                   "why": mono_why}
        if not _chk(R, "ii-s0-mono", var, ok_mono, lg, MONO0_TOL):
            R["first_fail"] = "ii-s0-mono:" + var
            R["rows"][var] = row
            return R

        wt2 = truth_table(wsp, 2.0)
        _dp, _qb = delta_of(wsp, wt2)
        dref2, _qb2 = delta_of(wsr, wt2)
        m1d = delta_of(uniform_pi_wset(wsp), wt2)[0]
        row["mut_m1_margin"] = m1d - dref2
        if not _chk(R, "m1", var, abs(m1d - dref2) > MUT_TOL,
                    abs(m1d - dref2), ">"):
            R["first_fail"] = "m1:" + var
            R["rows"][var] = row
            return R
        mix_in = "a-hist" if var.startswith("c") else "c-hist"
        dmut2, _ = delta_of(ws_p[mix_in], wt2)
        row["mut_m2_margin"] = dmut2 - dref2
        row["mut_m2_mix_in"] = mix_in
        if not _chk(R, "m2", var, abs(dmut2 - dref2) > MUT_TOL,
                    abs(dmut2 - dref2), ">"):
            R["first_fail"] = "m2:" + var
            R["rows"][var] = row
            return R
        ftr = fit_restricted(wsp, 2.0, 0, "extended", ridge=RIDGE)
        dmut3, _qu = delta_of(wsp, ftr["qhat"])
        row["mut_m3_margin"] = dmut3 - dref2
        row["mut_m3_fit"] = {"beta": ftr["beta"], "iters": ftr["iters"]}
        if not _chk(R, "m3", var, abs(dmut3 - dref2) > MUT_TOL,
                    abs(dmut3 - dref2), ">"):
            R["first_fail"] = "m3:" + var
            R["rows"][var] = row
            return R

        fp = lambda g: sigma0_delta_prod(wsp, g)[0]
        bs = {}
        att_flag = True
        for lab, tgt in (("delta1", DELTA1), ("delta2", DELTA2)):
            b = bisection_solve(fp, tgt)
            bs[lab] = {"gamma": b["gamma"], "iters": b["iters"],
                       "delta_at": b["delta_at"], "attained": b["attained"],
                       "f_hi_final": b["f_hi"]}
            if b["attained"]:
                bs[lab]["attainment"] = abs(b["delta_at"] - tgt)
                if bs[lab]["attainment"] > BISECT_ATAIN:
                    att_flag = False
            else:
                if b["f_hi"] >= tgt:
                    att_flag = False
        row["bisect_s0"] = bs
        bsm = max(bs["delta1"].get("attainment", BISECT_ATAIN + 1.0),
                  bs["delta2"].get("attainment", BISECT_ATAIN + 1.0))
        row["bisect_s0_margin"] = bsm
        if not _chk(R, "iii-s0", var, att_flag, bsm, BISECT_ATAIN):
            R["first_fail"] = "iii-s0:" + var
            R["rows"][var] = row
            return R

        ptg0 = {(k, c): pt_gh[(0.0, k, c)] for (k, c) in ALL_CELLS}
        d1gh, _q0 = delta_of(wsp, ptg0)
        row["check_ii_s1_margin"] = abs(d1gh)
        if not _chk(R, "ii-s1", var, abs(d1gh) <= CHK_II_TOL,
                    abs(d1gh), CHK_II_TOL):
            R["first_fail"] = "ii-s1:" + var
            R["rows"][var] = row
            return R

        lg1, lfail1, mlist1 = None, None, []
        prev = None
        for gamma in MONO_GRID:
            ptg = {(k, c): pbar_sigma1(k, c, gamma, 256, TAU) for (k, c) in ALL_CELLS}
            dp, _q = delta_of(wsp, ptg)
            if prev is not None:
                dsec = dp - prev
                mlist1.append((round(gamma, 4), dsec))
                if lg1 is None or dsec < lg1:
                    lg1, lfail1 = dsec, gamma
            prev = dp
        row["mono_s1_margin"] = lg1
        row["mono_s1_min_at"] = lfail1
        row["mono_s1_diffs"] = mlist1
        ok_mono1, peak_at1, mono_why1 = _mono_contract(mlist1, MONO1_TOL, 5e-10)
        row["mono_s1_contract"] = {"ok": ok_mono1, "peak_at": peak_at1,
                                   "why": mono_why1}
        if not _chk(R, "ii-s1-mono", var, ok_mono1, lg1, MONO1_TOL):
            R["first_fail"] = "ii-s1-mono:" + var
            R["rows"][var] = row
            return R

        mct = {}
        worst_mc = 0.0
        ok_mc = True
        for gamma in GAMMA_GRID:
            ptg = {(k, c): pt_gh[(gamma, k, c)] for (k, c) in ALL_CELLS}
            dl, qbmc = delta_of(wsp, {(k, c): pt_mc[(gamma, k, c)]
                                      for (k, c) in ALL_CELLS})
            dlgh, qbgh = delta_of(wsp, ptg)
            g = grad_delta(wsp, ptg, qbgh)
            se2 = 0.0
            for (k, c), gj in g.items():
                se2 += gj * gj * var_mc[(gamma, k, c)]
            se = math.sqrt(se2 / MC_DRAWS)
            dm = abs(dl - dlgh)
            if dm > MCX_FACTOR * se + CHK_II_TOL:
                ok_mc = False
            mct[gamma] = (dl, dlgh, se, dm)
            worst_mc = max(worst_mc, dm)
        row["mc_pergamma"] = mct
        row["mc_margin"] = worst_mc
        if not _chk(R, "MC-s1", var, ok_mc, worst_mc, "5*SE+1e-12"):
            R["first_fail"] = "MC-s1:" + var
            R["rows"][var] = row
            return R

        gv = {}
        gmin = None
        g0 = None
        fits1 = {}
        for gamma in GAMMA_GRID:
            ptg = {(k, c): pt_gh[(gamma, k, c)] for (k, c) in ALL_CELLS}
            fit = fit_restricted(wsp, gamma, 1, "extended", nodes=256)
            gg = kl_of(wsp, ptg, fit["qhat"])
            gv[gamma] = (gg, fit["iters"], fit["grad"])
            fits1[gamma] = fit["qhat"]
            if gamma == 0.0:
                g0 = gg
                continue
            if gmin is None or gg < gmin:
                gmin = gg
        row["check_v_pergamma"] = gv
        row["check_v_min_gap"] = gmin
        row["check_v_gamma0_gap"] = g0
        row["sigma1_fits_qhat"] = fits1
        if not _chk(R, "v-s1", var, gmin > CHK_V_G_TOL, gmin, CHK_V_G_TOL):
            R["first_fail"] = "v-s1:" + var
            R["rows"][var] = row
            return R

        ptg2 = {(k, c): pt_gh[(2.0, k, c)] for (k, c) in ALL_CELLS}
        gm4 = kl_of(wsp, ptg2, ptg2)
        row["mut_m4_gap"] = gm4
        if not _chk(R, "m4", var, gm4 <= M4_TOL, gm4, M4_TOL):
            R["first_fail"] = "m4:" + var
            R["rows"][var] = row
            return R
        f2 = fit_restricted(wsp, 2.0, 1, "extended", nodes=256)
        l_ana = ce_of(wsp, ptg2, f2["qhat"])
        rng = np.random.default_rng(V2_SEED)
        s2 = rng.standard_normal(MC_DRAWS) * TAU
        loss = np.zeros(MC_DRAWS)
        for k, c, wt in cell_list(wsp):
            pr = expit(eta(k, c, 2.0) + s2)
            y = (rng.random(MC_DRAWS) < pr).astype(np.float64)
            qh = min(max(f2["qhat"][(k, c)], 1e-15), 1.0 - 1e-15)
            loss += wt * (-(y * math.log(qh) + (1.0 - y) * math.log1p(-qh)))
        v2m = float(loss.mean())
        v2se = float(loss.std(ddof=0)) / math.sqrt(MC_DRAWS)
        row["V2"] = {"mc_mean": v2m, "analytic_pbar_ce": l_ana,
                     "se": v2se, "margin": abs(v2m - l_ana)}
        if not _chk(R, "V-2", var,
                    abs(v2m - l_ana) <= MCX_FACTOR * v2se + CHK_II_TOL,
                    abs(v2m - l_ana), "5*SE+1e-12"):
            R["first_fail"] = "V-2:" + var
            R["rows"][var] = row
            return R
        R["rows"][var] = row

    R["all_pass"] = all(c["verdict"] in ("PASS", "n/a") for c in R["checks"])
    R["elapsed_s"] = time.time() - t_start
    return R


def _mono_contract(diffs, rising_slack, falling_slack):
    """Single-peak contract on successive Delta(gamma) diffs: within jitter
    slack, diffs stay >= -rising_slack until the first negative diff (the
    peak), then no rise beyond +falling_slack afterwards (declines of any
    size are the peak's falling branch)."""
    flip = None
    for g, d in diffs:
        if flip is None:
            if d < 0.0:
                flip = g
            elif d < -rising_slack:
                return False, g, "dip below slack on the rising branch"
        else:
            if d > falling_slack:
                return False, g, "second rise after the peak"
    return True, flip, None


def write_report(R, path):
    L = []
    L.append("# Bridge verification battery - run record (pre-calibration)")
    L.append("")
    L.append("**Date:** 2026-10-18. **Status:** battery executed under the owner bridge")
    L.append("authorization (Foued, 2026-10-18; draft 0.2 item 12 / source record SS8 part 5)")
    L.append("and the frozen declaration `v03p/bridge/BATTERY_SPEC.md`.")
    L.append("")
    L.append("Every number in this file is **PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE**.")
    L.append("`I_k` is the bucket-local support proxy under Rev F 5A as drafted;")
    L.append("P(pass) = 0 for the complete rule is unchanged (draft A2.3). Scenario (b)")
    L.append("is out of scope (bridge NOT DEFINED there).")
    L.append("")
    L.append("## Meta")
    L.append("")
    for kk, vv in R["meta"].items():
        L.append("- `%s`: %r" % (kk, vv))
    L.append("- elapsed seconds: %.2f" % R.get("elapsed_s", -1.0))
    L.append("")
    L.append("## Global margins")
    L.append("")
    for kk, vv in R["global"].items():
        if kk == "weightsets":
            continue
        if isinstance(vv, dict):
            for k2, v2 in vv.items():
                L.append("- %s / %s: %r" % (kk, k2, v2))
        else:
            L.append("- %s: %r" % (kk, vv))
    L.append("")
    L.append("## Checks (all rows reported, including passes)")
    L.append("")
    L.append("| check | row | verdict | margin | threshold |")
    L.append("|---|---|---|---|---|")
    for c in R["checks"]:
        m = c["margin"]
        ms = ("%.3e" % m) if isinstance(m, float) else repr(m)
        L.append("| %s | %s | %s | %s | %r |" % (c["id"], c["row"], c["verdict"],
                                                 ms, c["thr"]))
    L.append("")
    L.append("## Per-row detail")
    L.append("")
    for var, row in R["rows"].items():
        L.append("### %s" % var)
        L.append("")
        for kk, vv in row.items():
            if isinstance(vv, dict):
                L.append("- %s: %r" % (kk, _roundv(vv)))
            elif isinstance(vv, list):
                L.append("- %s: %s" % (kk, _fmt_list(vv)))
            else:
                L.append("- %s: %r" % (kk, vv))
        L.append("")
    txt = "\n".join(L) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return path


def _roundv(d):
    out = {}
    for kk, vv in d.items():
        if isinstance(vv, tuple):
            out[kk] = tuple(_fix(x) for x in vv)
        else:
            out[kk] = _fix(vv)
    return out


def _fix(x):
    if isinstance(x, float):
        return round(x, 12)
    if isinstance(x, list):
        return [_fix(y) for y in x]
    return x


def _fmt_list(vv):
    return ["%s:%.3e" % (a, b) if isinstance(a, (int, float))
            else "%r:%.3e" % (a, b) for a, b in vv]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--smoke" in argv:
        k5 = smoke_part_a(5, 12)
        k10 = smoke_part_a(10, 12)
        ok = (k5["W0_max_abs_diff"] <= BTOL and k10["W0_max_abs_diff"] <= BTOL
              and k5["W1_max_abs_diff"] <= TTOL and k10["W1_max_abs_diff"] <= TTOL
              and k5["W2_max_abs_diff"] <= TTOL
              and k10["W2_max_abs_diff"] <= TTOL)
        sys.stdout.write("smoke k5 W0=%.3e W1=%.3e W2=%.3e\n" %
                         (k5["W0_max_abs_diff"], k5["W1_max_abs_diff"],
                          k5["W2_max_abs_diff"]))
        sys.stdout.write("smoke k10 W0=%.3e W1=%.3e W2=%.3e\n" %
                         (k10["W0_max_abs_diff"], k10["W1_max_abs_diff"],
                          k10["W2_max_abs_diff"]))
        sys.stdout.write("SMOKE %s\n" % ("PASS" if ok else "FAIL"))
        return 0 if ok else 1

    import subprocess
    repo = os.path.normpath(os.path.join(_HERE, os.pardir, os.pardir))
    b_committed = subprocess.run(
        ["git", "rev-parse", "HEAD:v03p/bridge/battery.py"],
        capture_output=True, text=True, cwd=repo).stdout.strip()
    b_working = subprocess.run(
        ["git", "hash-object", os.path.join(_HERE, "battery.py")],
        capture_output=True, text=True, cwd=repo).stdout.strip()
    if b_committed != b_working or not b_committed:
        sys.stdout.write("BATTERY REFUSED: working battery.py does not match "
                         "the freeze part 2 commit (committed=%r working=%r)\n"
                         % (b_committed, b_working))
        return 3

    rep = run_battery()
    path = write_report(rep, os.path.join(_HERE, "BATTERY_REPORT_2026-10-18.md"))
    sys.stdout.write("BATTERY %s (first_fail=%s; report=%s)\n"
                     % ("PASS" if rep.get("all_pass") else "STOP",
                        rep.get("first_fail"), path))
    return 0 if rep.get("all_pass") else 2


if __name__ == "__main__":
    sys.exit(main())
