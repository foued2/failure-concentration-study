#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NC1 gate-conditioned c-distribution -- TEMPORARY pre-freeze computation.

Authorization (owner, 2026-10-18): NC1 only.  Exact deterministic computation
in stdlib Python; no sampling; no repository changes; A1 imported read-only
via the pinned absolute path (same convention as the O2 temp stage).  Temp
artifacts only, referenced to the frozen packages.

Outputs (this folder):
  nc1_results.json   machine-readable stage tables + all checks
  nc1_report.md      human-readable tables, findings, R1 status

Definitions (engine spec v1 section 2, M3 addendum Rev d, A1 rev 3):
  C levels: k=5 -> {0.2,0.4,0.6,0.8,1.0}; k=10 -> {0.2,0.3,0.4,0.5}
  integer labels g = C/delta_k: k=5 g in 1..5; k=10 g in 2..5
  X_k = t_k * sum_i n_i g_i^2 - (sum_i n_i g_i)^2 = sum_{i<j} (g_i-g_j)^2
  c = (delta_5^2 * X5/t5 + delta_10^2 * X10/t10) / s_ref^2,
      delta_5^2 = 0.04, delta_10^2 = 0.01, s_ref = 0.12703 exactly
      => s_ref^2 = 161366209/1e10 ; every c>=tau comparison is done in
      exact integer arithmetic (see pooled_R0 / ssfloor_x).
  Engine-spec anchors reproduced as checks:
      c_floor(t) = delta^2 (t-1)/t / s_ref^2   (min nonzero c at size t)
      c_ceil(t)  = R_k^2 floor(t^2/4)/t / s_ref^2
  c* exact values (M3 addendum): c* = (1.25/beta)^2, sigma_max*z_req = 1.25:
      beta .20 -> 625/16 = 39.0625; .10 -> 156.25; .05 -> 625.00
  Split: (NTR, NTE) = A.split_sizes(N); NTR = N - (N+2)//4, NTE = (N+2)//4.
  Train positions (t5,t10) ~ Mult(NTR; p5,p10,pO); test positions
  (te5,te10) ~ Mult(NTE; p5,p10,pO), independent; bucket train comps
  ~ Mult(t_k, pi_k) and test comps ~ Mult(te_k, pi_k), all independent
  given sizes (exact A1 identity, as used in O2).

Chain stages (cumulative gates; every stage reported, both CVD readings,
each with and without the test gate TN = [te5>=1][te10>=1][te5+te10>=8]):
  base, +support (s5 & s10), +TrainRa (t5>=1,t10>=1,t5+t10>=8),
  +CVD(one) == +M3 rank (c>0 identity), +CVD(each),
  +c>=c* per variant: (v1=one reading) P(sup&TR&c>=c*),
      (v2=each reading) P(sup&TR&each&c>=c*), c* in {625/16,156.25,625}.

Key identities used (each verified numerically in this run):
  c > 0  <=>  NOT(bucket5 train-constant AND bucket10 train-constant)
          <=>  CVD literal reading  <=>  M3 rank-full.
  Pure-train threshold events are independent of the test block:
      P(TR & TN & c>=tau) = P(TR & c>=tau) * P(TN).
  P(sup & TR & c>=tau) = P(TR & c>=tau) - C_not5 - C_not10 + C_notnot,
      C_notk = P(not s_k & TR & c>=tau), C_notnot = both buckets failing.
  not s_k  <=>  {n_k >= 8 and some class j with <= 3 combined outsiders}
            U   {n_k <= 7 and support fails (always)}   (disjoint).
  The first branch is enumerated by violation configuration (class j,
  a<=3 train outsiders with labels, test side massed by b<=3-a outsiders
  at the same class j); the second branch is certain at n<=7.
  Aggregation: per train size x the violating configurations are folded
  into a weighted X_k table w[x]; C_notk/one-restricted and C_notnot/
  both-restricted thresholds are evaluated by an O(nA+nB) two-pointer.
  C_notnot is NOT zero at tau = 39.0625: e.g. 3 train outsiders 4 label
  steps away from the dominant class give asymptotic c5 -> 119.
  P(each & c>=tau) = P(c>=tau) - P(same5 & c>=tau) - P(same10 & c>=tau)
      (+ P(same5&same10&c>=tau) = 0 for tau > 0).

R1 risk handling (blowup; probe2/probe3/probe4 measurements):
  - N = 113, 150: exact full range (DP unpruned; (x,y) truncation 1e-30).
  - N = 450, 600: DP states with p < 1e-14 dropped for t > 112 (dropped
    mass accumulated exactly; certified bound ~1e-9), and (x,y) pairs
    with R[x][y] < 1e-18 dropped (bound ~1.4e-16).  These threshold-stage
    values are flagged PROVISIONAL pending owner acceptance of the R1
    amendment; every other stage is exact at all N.
"""

import sys, os, math, json, time, datetime
from bisect import bisect_left
from array import array

sys.dont_write_bytecode = True

A1DIR = r"C:\Users\pakla\PycharmProjects\failure-concentration-study\v03p\a1"
sys.path.insert(0, A1DIR)
import a1_support_comparison as A  # noqa: E402

OUTDIR = os.path.dirname(os.path.abspath(__file__))
NB = (113, 150, 450, 600)
SCENS = ("a-hist", "a-50:50", "c-hist", "c-50:50")
NMAX = 600
NTRMAX = 450                  # max train size (N=600 -> NTR=450)
T_EXACT = 112                 # DP exact up to this t (covers NTR(150)=112)
EPS_DP = 1e-14                # DP state prune threshold for t > T_EXACT
R_CUT_SMALL = 1e-30           # (x,y) pair truncation, N <= 150
R_CUT_BIG = 1e-18             # (x,y) pair truncation, N >= 450
SREF2_NUM = 161366209         # s_ref^2 = SREF2_NUM / 1e10  (0.12703^2, exact)
UINTC = 10 ** 10
SREF2 = SREF2_NUM / UINTC
DELTA2 = {5: 0.04, 10: 0.01}
INV_D2 = {5: 25.0, 10: 100.0}
TAUS = (10.0, 20.0, 39.0625, 60.0, 100.0, 156.25, 250.0, 400.0, 625.0,
        1000.0, 1600.0, 2500.0)
CSTAR = (39.0625, 156.25, 625.0)
GVALS = {5: (1, 2, 3, 4, 5), 10: (2, 3, 4, 5)}
KT_SUM = 120                  # per-(k,t) summary stats up to this t
KT_DIST = 40                  # full per-(k,t) X distributions up to this t

CHECKS = []


def check(name, ok, detail="", vac=False):
    st = "VACUOUS" if vac else ("PASS" if ok else "FAIL")
    CHECKS.append({"name": name, "ok": bool(ok), "vacuous": bool(vac),
                   "status": st, "detail": str(detail)})
    print(st + " " + name + ((" | " + detail) if detail else ""))
    return bool(ok)


def fmt(x):
    return f"{x:.1f}s"


# ==========================================================================
# Part 0: exact tau arithmetic
# ==========================================================================

def tau_frac(tau):
    """exact (num, den) for a terminating decimal tau."""
    s = repr(float(tau))
    if "e" in s or "E" in s:
        raise ValueError(tau)
    if "." not in s:
        return int(tau), 1
    dn = len(s.split(".")[1])
    return int(round(tau * 10 ** dn)), 10 ** dn


def pooled_R0(x, y, num, den):
    """c >= tau (tau = num/den) <=> 4*X5*y + X10*x >= R0, where
    R0 = ceil(100 * tau * s_ref^2 * x * y)."""
    nume = num * SREF2_NUM * 100 * x * y
    deno = den * UINTC
    return (nume + deno - 1) // deno


def ssfloor_x(k, t, num, den):
    """1D: c_k >= tau <=> X_k >= ssfloor.  c_k = delta^2 X/(t s^2) >= tau
    <=> X >= tau * s^2 * t / delta^2."""
    m = 25 if k == 5 else 100
    nume = num * SREF2_NUM * m * t
    deno = den * UINTC
    return (nume + deno - 1) // deno


# ==========================================================================
# Part 1: bucket DP over (A,B) = (sum g, sum g^2); per-t X = t*B - A^2
# ==========================================================================

class DPTab(object):
    __slots__ = ("xs", "ps", "cum", "bce", "drop")

    def __init__(self, xs, ps, cum, bce, drop):
        self.xs = xs
        self.ps = ps
        self.cum = cum
        self.bce = bce   # backward cumulative: bce[i] = P(X >= xs[i])
        self.drop = drop


DP = {}        # k -> list of DPTab indexed by t = 0..NTRMAX
DP_DROP = {}   # k -> total dropped mass (certified bias bound)


def bucket_dp(k, tmax, t_exact, eps):
    """Streaming DP over integer-label multinomials.

    At each t the (A,B) states are updated; for t > t_exact states with
    p < eps are dropped (their mass is removed from the chain forever and
    accumulated), then the X-marginal of the survivors is stored."""
    gv = GVALS[k]
    pi = list(A.CK[k][1])
    cur = {(0, 0): 1.0}
    tabs = [None] * (tmax + 1)
    dropped_total = 0.0
    for t in range(tmax + 1):
        if t:
            nxt = {}
            get = nxt.get
            for (a, b), p in cur.items():
                for g, pp in zip(gv, pi):
                    k2 = (a + g, b + g * g)
                    nxt[k2] = get(k2, 0.0) + p * pp
            cur = nxt
        if t > t_exact and eps > 0.0:
            surv = {}
            drop = 0.0
            for kk, p in cur.items():
                if p < eps:
                    drop += p
                else:
                    surv[kk] = p
            cur = surv
        else:
            drop = 0.0
        dropped_total += drop
        Xd = {}
        dget = Xd.get
        for (a, b), p in cur.items():
            X = t * b - a * a
            Xd[X] = dget(X, 0.0) + p
        xs = sorted(Xd)
        n = len(xs)
        ps = array("d", [0.0] * n)
        cum = array("d", [0.0] * n)
        bce = array("d", [0.0] * n)
        s = 0.0
        for i, xx in enumerate(xs):
            p = Xd[xx]
            ps[i] = p
            s += p
            cum[i] = s
        bt = 0.0
        for i in range(n - 1, -1, -1):
            # backward accumulation: tiny far-tail values are summed first,
            # keeping tiny tails cancellation-free
            bt += ps[i]
            bce[i] = bt
        bce[0] = s   # anchor the full tail to the forward-order total
        tabs[t] = DPTab(array("q", xs), ps, cum, bce, drop)
    return tabs, dropped_total


def tailx(k, t, xmin):
    """P(X >= xmin | bucket k, train size t).
    Uses the backward-cumulative array: forward-cum complements lose
    tiny tails to accumulated float error (cum noise ~1e-16 >> tail)."""
    tab = DP[k][t]
    xs, bce = tab.xs, tab.bce
    if len(xs) == 0:
        return 0.0 if xmin > 0 else 1.0
    if xmin <= xs[0]:
        return 1.0
    if xmin > xs[-1]:
        return 0.0
    return bce[bisect_left(xs, xmin)]


def gen_tail(Axs, Aw, Bxs, Bce, coefA, coefB, r0):
    """P(coefA*A + coefB*B >= r0), A/B sorted weighted tables.
    A side (values Axs asc, weights Aw); B side (values Bxs asc, backward
    cumulative weights Bce with Bce[j] = P(B >= Bxs[j])).
    Only the active region of A (where the largest B can still reach r0)
    is walked: for i before it the tail probability is exactly 0."""
    if not Axs or not Bxs:
        return 0.0
    bmax = Bxs[-1]
    lim = (r0 - coefB * bmax + coefA - 1) // coefA if r0 > coefB * bmax \
        else Axs[0] - 1
    i0 = bisect_left(Axs, lim) if lim > Axs[0] else 0
    j0 = len(Bxs)
    tot = 0.0
    for i in range(i0, len(Axs)):
        num = r0 - coefA * Axs[i]
        thr = 0 if num <= 0 else (num + coefB - 1) // coefB
        while j0 > 0 and Bxs[j0 - 1] >= thr:
            j0 -= 1
        if j0 == 0:
            tot += sum(Aw[i:]) * Bce[0]
            break
        w = Aw[i]
        if w != 0.0:
            t = Bce[j0]
            if t != 0.0:
                tot += w * t
    return tot


def dp_side(k, t):
    """(xs, ps, bce, total) view of DP[k][t] for gen_tail.
    bce[i] = P(X >= xs[i]); total = bce[0] = full support mass."""
    tab = DP[k][t]
    return tab.xs, tab.ps, tab.bce, tab.bce[0]


def pair_dp_dp(x, y, r0):
    """P(4*X5*y + X10*x >= r0), X5 ~ DP5[x], X10 ~ DP10[y]."""
    a = dp_side(5, x)
    b = dp_side(10, y)
    return gen_tail(a[0], a[1], b[0], b[2], 4 * y, x, r0)


_CCOMP = {}   # (k, n) -> list of (X, prob) for small train comps


def ccomp(k, n):
    """(X, prob) table for a small bucket-k train comp of n bodies."""
    key = (k, n)
    lst = _CCOMP.get(key)
    if lst is None:
        acc = {}
        for ct in comps(k, n):
            lg = comp_logp(k, ct)
            if lg is None or lg < -745.0:
                continue
            X = comp_X(k, ct)
            acc[X] = acc.get(X, 0.0) + math.exp(lg)
        lst = sorted(acc.items())
        _CCOMP[key] = lst
    return lst


def brute_pair(x, y, r0):
    """Exact O(n*m) reference for pair_dp_dp (direct comp enumeration)."""
    tot = 0.0
    for X5, p5 in ccomp(5, x):
        rem = r0 - 4 * X5 * y
        if rem <= 0:
            tot += p5
            continue
        need = (rem + x - 1) // x
        for X10, p10 in ccomp(10, y):
            if X10 >= need:
                tot += p5 * p10
    return tot

# ==========================================================================
# Part 2: closed-form moments of X (independent of the DP)
# ==========================================================================

MOM = {}


def pi_moments(k):
    gv = GVALS[k]
    pi = list(A.CK[k][1])
    m1 = sum(p * g for g, p in zip(gv, pi))
    m2 = sum(p * g * g for g, p in zip(gv, pi))
    var = m2 - m1 * m1
    ed2 = 0.0       # E[(g1-g2)^4]
    edsh = 0.0      # E[(g1-g2)^2 (g1-g3)^2]
    for i, pa in enumerate(pi):
        ga = gv[i]
        for j, pb in enumerate(pi):
            gb = gv[j]
            d1 = ga - gb
            ed2 += pa * pb * d1 ** 4
            for l, pc in enumerate(pi):
                gc = gv[l]
                d2 = ga - gc
                edsh += pa * pb * pc * d1 * d1 * d2 * d2
    MOM[k] = (m1, m2, var, ed2, edsh)


def ex(k, x):
    """E[X | train size x] = x(x-1) Var_g  (X = sum_{i<j}(g_i-g_j)^2)."""
    return x * (x - 1) * MOM[k][2]


def ex2(k, x):
    """E[X^2 | train size x] via the pairwise decomposition; exact."""
    if x < 2:
        return 0.0
    _, _, var, ed2, edsh = MOM[k]
    ed1 = 2.0 * var
    c2 = x * (x - 1) // 2
    c3 = x * (x - 1) * (x - 2) // 6
    c4 = x * (x - 1) * (x - 2) * (x - 3) // 24
    return c2 * ed2 + 2.0 * (3 * c3 * edsh + 3 * c4 * ed1 * ed1)


def c_mean5(x):
    return (DELTA2[5] * ex(5, x) / x) / SREF2 if x >= 1 else 0.0


def c_mean10(y):
    return (DELTA2[10] * ex(10, y) / y) / SREF2 if y >= 1 else 0.0


def c_msq5(x):
    return ((DELTA2[5] ** 2) * ex2(5, x) / (x * x)) / (SREF2 * SREF2) if x >= 1 else 0.0


def c_msq10(y):
    return ((DELTA2[10] ** 2) * ex2(10, y) / (y * y)) / (SREF2 * SREF2) if y >= 1 else 0.0


# ==========================================================================
# Part 3: O2-mirror support machinery (Q / H tables / F tables)
# ==========================================================================

def _Q_small(pi, u, t, c):
    v = len(pi)
    tot = [0.0]
    counts = [0] * v

    def emit():
        if counts[c] > u - 4:
            return
        for i in range(v):
            if i != c and counts[i] > t + u - 4:
                return
        lg = A.LFACT[u]
        for x, p in zip(counts, pi):
            lg -= A.LFACT[x]
            if x:
                if p <= 0.0:
                    return
                lg += x * math.log(p)
        if lg > -745.0:
            tot[0] += math.exp(lg)

    def rec(i, rem):
        if i == v - 1:
            counts[i] = rem
            emit()
            return
        for x in range(rem + 1):
            counts[i] = x
            rec(i + 1, rem - x)

    rec(0, u)
    return tot[0]


def Q(pi, u, t, c):
    """P(test multinomial size u satisfies t_c <= u-4, t_i <= t+u-4, i!=c).
    Verbatim semantics from O2."""
    if u < 4:
        return 0.0
    big = A.binom_upper(u, u - 3, pi[c])
    if t >= 4:
        return max(0.0, min(1.0, 1.0 - big))
    if u <= 5:
        return max(0.0, min(1.0, _Q_small(pi, u, t, c)))
    res = 1.0 - big
    thr = u + t - 3
    for i in range(len(pi)):
        if i != c:
            res -= A.binom_upper(u, thr, pi[i])
    return max(0.0, min(1.0, res))


def build_H(pi, ntrmax=NTRMAX):
    """H[(n,t)] = P(S1-m4 support AND all t train bodies share one C value).
    Verbatim methodology from O2 (o2_calc.py)."""
    v = len(pi)
    logs = [math.log(p) if p > 0.0 else None for p in pi]
    H = {}
    for n in range(8, NMAX + 1):
        for t in range(1, min(n, ntrmax) + 1):
            u = n - t
            s = 0.0
            for c in range(v):
                lg = t * logs[c]
                if lg < -745.0:
                    continue
                q = Q(pi, u, t, c)
                if q > 0.0:
                    s += math.exp(lg) * q
            if s > 0.0:
                H[(n, t)] = s
    return H


F5 = None
F10 = None
H5 = None
H10 = None
POW5 = None   # P(train comp of t bodies all one C value): sum_j pi_j^t
POW10 = None  # POW[k][0] = 1.0 (empty bucket is vacuously constant)


def hval(H, F, n, t):
    """P(support & train-constant | bucket size n, train t); t=0 vacuous."""
    if t <= 0:
        return F[n]
    return H.get((n, t), 0.0)


def prep_tables():
    global F5, F10, H5, H10, POW5, POW10
    F5 = [A.f_s1(5, n, 4) for n in range(NMAX + 1)]
    F10 = [A.f_s1(10, n, 4) for n in range(NMAX + 1)]
    t0 = time.time()
    H5 = build_H(list(A.CK[5][1]))
    print(f"H5 built: {len(H5)} entries ({fmt(time.time()-t0)})")
    t0 = time.time()
    H10 = build_H(list(A.CK[10][1]))
    print(f"H10 built: {len(H10)} entries ({fmt(time.time()-t0)})")
    pow5 = [1.0] + [sum(p ** t for p in A.CK[5][1]) for t in range(1, NTRMAX + 1)]
    pow10 = [1.0] + [sum(p ** t for p in A.CK[10][1]) for t in range(1, NTRMAX + 1)]
    POW5 = pow5
    POW10 = pow10


# ==========================================================================
# Part 4: generalized R/S gate passes (T0/T_HF/T_FH/T_HH + moments)
# ==========================================================================

def build_RS(N, p5, p10, rmask, smask):
    """R[x][y] and S[u][v] multinomial rows.
    rmask 'tr' keeps x>=1, y>=1, x+y>=8; smask 'tn' keeps u>=1, v>=1,
    u+v>=8; False keeps everything.  Returns (R, S, NTR, NTE)."""
    NTR, NTE = A.split_sizes(N)
    pO = 1.0 - p5 - p10
    R = [dict() for _ in range(NTR + 1)]
    for x in range(0, NTR + 1):
        if rmask and x < 1:
            continue
        ylo = 1 if rmask else 0
        row = R[x]
        for y in range(ylo, NTR - x + 1):
            if rmask and x + y < 8:
                continue
            p = A.mpmf2(NTR, x, y, p5, p10, pO)
            if p > 0.0:
                row[y] = p
    S = [dict() for _ in range(NTE + 1)]
    for u in range(0, NTE + 1):
        if smask and u < 1:
            continue
        vlo = 1 if smask else 0
        row = S[u]
        for v in range(vlo, NTE - u + 1):
            if smask and u + v < 8:
                continue
            p = A.mpmf2(NTE, u, v, p5, p10, pO)
            if p > 0.0:
                row[v] = p
    return R, S, NTR, NTE


WCE = {5: {}, 10: {}}   # k -> {N: (E1, E2)} per-(train,out) not-support c-moments


def wc_tables(k, N):
    d = WCE[k].get(N)
    if d is None:
        d = build_wc(k, N)
        WCE[k][N] = d
    return d


def rs_terms(N, p5, p10, rmask, smask, with_moments=True):
    """Gate passes.  Returns (T, M, NTR, NTE):
      T0   = P(prefix & s5 & s10)
      T_HF = P(prefix & s5 & same5 & s10)     (same-k = train-constant)
      T_FH = P(prefix & s5 & s10 & same10)
      T_HH = P(prefix & s5 & same5 & s10 & same10)
      P_atleastone = T0 - T_HH ; P_each = T0 - T_HF - T_FH + T_HH
    and (optionally, with_moments=True) EXACT conditional moment sums
      M1sup/M2sup = E[c * 1{.}], E[c^2 * 1{.}] over prefix & s5 & s10
      M1hf/M2hf over prefix & s5 & same5 & s10 (c = c10 there)
      M1fh/M2fh over prefix & s5 & s10 & same10 (c = c5 there)
    The same5/same10 blocks make c5/c10 vanish, and the c10/c5 parts are
    conditioned on the support events through the exact not-support
    moment tables (build_wc), so no independence shortcut is taken."""
    R, S, NTR, NTE = build_RS(N, p5, p10, rmask, smask)
    if with_moments:
        E1g5, E2g5 = wc_tables(5, N)
        E1g10, E2g10 = wc_tables(10, N)
        Sf = [[0.0] * (NTE + 1) for _ in range(NTR + 1)]
        Xi = [[0.0] * (NTE + 1) for _ in range(NTR + 1)]
        SW1 = [[0.0] * (NTE + 1) for _ in range(NTR + 1)]
        SW2 = [[0.0] * (NTE + 1) for _ in range(NTR + 1)]
        S5m = [0.0] * (NTE + 1)
    else:
        E1g5 = E2g5 = E1g10 = E2g10 = None
        Sf = [[0.0] * (NTE + 1) for _ in range(NTR + 1)]
        Xi = [[0.0] * (NTE + 1) for _ in range(NTR + 1)]
        SW1 = SW2 = S5m = None
    h10get = H10.get
    w10a = E1g10.get if with_moments else None
    w10b = E2g10.get if with_moments else None
    for u in range(0, NTE + 1):
        Su = S[u]
        if not Su:
            continue
        for v, s in Su.items():
            if s <= 0.0:
                continue
            if with_moments:
                S5m[u] += s
            for y in range(0, NTR + 1):
                s2 = y + v
                fv = F10[s2]
                if fv > 0.0:
                    Sf[y][u] += s * fv
                if y >= 1:
                    hv = h10get((s2, y), 0.0)
                    if hv > 0.0:
                        Xi[y][u] += s * hv
                    if with_moments:
                        e1 = w10a((y, v), 0.0)
                        if e1 > 0.0:
                            SW1[y][u] += s * e1
                        e2 = w10b((y, v), 0.0)
                        if e2 > 0.0:
                            SW2[y][u] += s * e2
    T = {"T0": 0.0, "T_HF": 0.0, "T_FH": 0.0, "T_HH": 0.0}
    M = {"M1sup": 0.0, "M2sup": 0.0, "M1hf": 0.0, "M2hf": 0.0,
         "M1fh": 0.0, "M2fh": 0.0}
    h5get = H5.get
    w5a = E1g5.get if with_moments else None
    w5b = E2g5.get if with_moments else None
    for x in range(0, NTR + 1):
        Rx = R[x]
        if not Rx:
            continue
        cm5 = c_mean5(x) if x >= 1 else 0.0
        cms5 = c_msq5(x) if x >= 1 else 0.0
        for y, r in Rx.items():
            sfy = Sf[y]
            xiy = Xi[y]
            cm10 = c_mean10(y)
            cms10 = c_msq10(y)
            l0 = l1 = l2 = l3 = 0.0
            m1 = m2 = mh1 = mh2 = mf1 = mf2 = 0.0
            for u in range(0, NTE + 1):
                sf = sfy[u]
                xi = xiy[u]
                if sf <= 0.0 and xi <= 0.0:
                    continue
                n = x + u
                f5v = F5[n]
                h5v = h5get((n, x), 0.0) if x >= 1 else f5v
                if sf > 0.0:
                    if f5v > 0.0:
                        l0 += sf * f5v
                    if h5v > 0.0:
                        l1 += sf * h5v
                if xi > 0.0:
                    if f5v > 0.0:
                        l2 += xi * f5v
                    if h5v > 0.0:
                        l3 += xi * h5v
                if with_moments:
                    e1u = w5a((x, u), 0.0)
                    e2u = w5b((x, u), 0.0)
                    sw1 = SW1[y][u]
                    sw2 = SW2[y][u]
                    s5m = S5m[u]
                    c5e = cm5 - e1u          # E[c5 * 1{s5} | x, u]
                    d10 = cm10 * s5m - sw1   # sum_v S[u][v] * E[c10*1{s10}|y,v]
                    D10 = cms10 * s5m - sw2
                    m1 += sf * c5e + f5v * d10
                    m2 += sf * (cms5 - e2u) + f5v * D10 + 2.0 * c5e * d10
                    if h5v > 0.0:
                        mh1 += h5v * d10
                        mh2 += h5v * D10
                    if xi > 0.0:
                        mf1 += xi * c5e
                        mf2 += xi * (cms5 - e2u)
            T["T0"] += r * l0
            T["T_HF"] += r * l1
            T["T_FH"] += r * l2
            T["T_HH"] += r * l3
            if with_moments and r > 0.0:
                M["M1sup"] += r * m1
                M["M2sup"] += r * m2
                M["M1hf"] += r * mh1
                M["M2hf"] += r * mh2
                M["M1fh"] += r * mf1
                M["M2fh"] += r * mf2
    T["P_atleastone"] = T["T0"] - T["T_HH"]
    T["P_each"] = T["T0"] - T["T_HF"] - T["T_FH"] + T["T_HH"]
    return T, M, NTR, NTE

# ==========================================================================
# Part 5: not-s_k machinery
#   nu enumeration (class j, a <= 3 train outsiders with labels),
#   test-side B factors, direct branch (n <= 7), folded weighted X tables
# ==========================================================================

def multisets(size, labels):
    """all multisets of given size over labels (tuples, nondecreasing)."""
    if size == 0:
        return [()]
    out = []

    def rec(start, rem, cur):
        if rem == 0:
            out.append(tuple(cur))
            return
        for g in labels:
            if g < start:
                continue
            cur.append(g)
            rec(g, rem - 1, cur)
            cur.pop()

    rec(min(labels), size, [])
    return out


NU = {}      # k -> list of (j_index, jg, a, multiset)


def prep_nu():
    for k in (5, 10):
        gv = GVALS[k]
        nus = []
        for j in range(len(gv)):
            jg = gv[j]
            others = tuple(g for g in gv if g != jg)
            for a in range(0, 4):
                for ms in multisets(a, others):
                    nus.append((j, jg, a, ms))
        NU[k] = nus


def x_of(k, x, jg, ms):
    """X value of the train comp (x - a bodies at label jg) + outsiders ms."""
    a = len(ms)
    s2 = 0
    s1 = 0
    for g in ms:
        s2 += g * g
        s1 += g
    return x * ((x - a) * jg * jg + s2) - ((x - a) * jg + s1) ** 2


def conf_logp(k, x, jg, ms):
    """log multinomial prob of (x-a) at label jg plus outsider multiset ms."""
    a = len(ms)
    if x - a < 0:
        return None
    gv = GVALS[k]
    pi = list(A.CK[k][1])
    counts = [0] * len(gv)
    counts[gv.index(jg)] += x - a
    for g in ms:
        counts[gv.index(g)] += 1
    lg = A.LFACT[x]
    for cnt, p in zip(counts, pi):
        if cnt:
            if p <= 0.0:
                return None
            lg -= A.LFACT[cnt]
            lg += cnt * math.log(p)
    return lg


def comps(k, n):
    """all compositions of n bodies over bucket-k labels (count tuples)."""
    gv = GVALS[k]
    v = len(gv)
    out = []
    cur = [0] * v

    def rec(i, rem):
        if i == v - 1:
            cur[i] = rem
            out.append(tuple(cur))
            return
        for x in range(rem + 1):
            cur[i] = x
            rec(i + 1, rem - x)

    rec(0, n)
    return out


def comp_X(k, counts):
    gv = GVALS[k]
    s1 = 0
    s2 = 0
    n = 0
    for c, g in zip(counts, gv):
        s1 += c * g
        s2 += c * g * g
        n += c
    return n * s2 - s1 * s1


def comp_logp(k, counts):
    gv = GVALS[k]
    pi = list(A.CK[k][1])
    n = sum(counts)
    lg = A.LFACT[n] if n else 0.0
    for cnt, p in zip(counts, pi):
        if cnt:
            if p <= 0.0:
                return None
            lg -= A.LFACT[cnt]
            lg += cnt * math.log(p)
    return lg


def Gk(k, u, jg, b):
    """P(test comp of size u: (u-b) bodies at label jg + b outsiders),
    summed over outsider multisets (labels != jg)."""
    if b > u:
        return 0.0
    gv = GVALS[k]
    pi = list(A.CK[k][1])
    jidx = gv.index(jg)
    others = tuple(g for g in gv if g != jg)
    tot = 0.0
    for ms in multisets(b, others):
        counts = [0] * len(gv)
        counts[jidx] = u - b
        for g in ms:
            counts[gv.index(g)] += 1
        lg = A.LFACT[u] if u else 0.0
        ok = True
        for cnt, p in zip(counts, pi):
            if cnt:
                if p <= 0.0:
                    ok = False
                    break
                lg -= A.LFACT[cnt]
                lg += cnt * math.log(p)
        if ok and lg > -745.0:
            tot += math.exp(lg)
    return max(0.0, min(1.0, tot))


def build_Bsum(k, umax):
    """Bsum[(u, j, a)] = sum_{b <= 3-a} Gk(k, u, gv[j], b): probability that
    the test comp has at most (3-a) bodies outside class j."""
    gv = GVALS[k]
    tb = {}
    for u in range(0, umax + 1):
        for j in range(len(gv)):
            jg = gv[j]
            gcache = [Gk(k, u, jg, b) for b in range(0, 4)]
            for a in range(0, 4):
                s = 0.0
                for b in range(0, 4 - a):
                    s += gcache[b]
                tb[(u, j, a)] = s
        # multisets are cached via recursion overhead; acceptable
    return tb


def bucket_marginals(N, p5, p10, smask):
    """test-block marginal of bucket-k test size, k=5 and k=10."""
    _, S, NTR, NTE = build_RS(N, p5, p10, False, smask)
    S5m = [0.0] * (NTE + 1)
    S10m = [0.0] * (NTE + 1)
    for u in range(0, NTE + 1):
        for v, p in S[u].items():
            if p <= 0.0:
                continue
            S5m[u] += p
            S10m[v] += p
    return S5m, S10m, NTR, NTE


def w_pure(k, x, u, Bsum):
    """Per-(x,u) aggregated not-s_k measure by X value:
      concentrated branch (n = x+u >= 8): sum over nu of P(train cfg) *
        Bsum[(u, j, a)]  (test side concentrates on the same class j);
      direct branch (n <= 7): support fails for every comp, so the
        measure is P(train comp) itself (test side sums out).
    Returns dict X -> weight."""
    acc = {}
    n = x + u
    if n >= 8:
        for (j, jg, a, ms) in NU[k]:
            if a > x:
                continue
            lg = conf_logp(k, x, jg, ms)
            if lg is None or lg < -745.0:
                continue
            w = math.exp(lg) * Bsum[(u, j, a)]
            if w > 0.0:
                X = x_of(k, x, jg, ms)
                acc[X] = acc.get(X, 0.0) + w
    else:
        for ct in comps(k, x):
            lg = comp_logp(k, ct)
            if lg is None or lg < -745.0:
                continue
            X = comp_X(k, ct)
            acc[X] = acc.get(X, 0.0) + math.exp(lg)
    return acc


def brute_w(k, x, u):
    """Brute-force reference for w_pure: enumerate train and test comps,
    apply the exact support predicate."""
    acc = {}
    n = x + u
    for ct in comps(k, x):
        lg = comp_logp(k, ct)
        if lg is None or lg < -745.0:
            continue
        p = math.exp(lg)
        X = comp_X(k, ct)
        if n < 8:
            acc[X] = acc.get(X, 0.0) + p
        else:
            tot_ct = sum(cc * gg for cc, gg in zip(ct, GVALS[k]))
            for cs in comps(k, u):
                tot_cs = sum(cc * gg for cc, gg in zip(cs, GVALS[k]))
                lg2 = comp_logp(k, cs)
                if lg2 is None or lg2 < -745.0:
                    continue
                # n - max_c n_c : counts of the joint comp
                joint = tuple(a + b for a, b in zip(ct, cs))
                mx = max(joint)
                if n - mx <= 3:
                    acc[X] = acc.get(X, 0.0) + p * math.exp(lg2)
    return acc


def build_w(k, N, p5, p10, smask):
    """Folded not-s_k weighted X tables over train size x:
      W[x] = (xs, ws, cumw, tot) with
        w[x][X] = sum_u Smarg[u] * w_pure(k, x, u)[X].
    Also returns S marginals for identity checks."""
    gv = GVALS[k]
    S5m, S10m, NTR, NTE = bucket_marginals(N, p5, p10, smask)
    Smarg = S5m if k == 5 else S10m
    Bsum = build_Bsum(k, NTE)
    gv = GVALS[k]
    W = [None] * (NTR + 1)
    maxu_needed = min(NTE, 7)   # direct branch u range
    for x in range(1, NTR + 1):
        acc = {}
        umin = max(0, 8 - x)
        wtest = None
        if umin <= NTE:
            # P(E_j | config class j with a train outsiders), folded over u
            wtest = {}
            for j in range(len(gv)):
                for a in range(0, 4):
                    s = 0.0
                    for u in range(umin, NTE + 1):
                        p = Smarg[u]
                        if p > 0.0:
                            s += p * Bsum[(u, j, a)]
                    wtest[(j, a)] = s
            for (j, jg, a, ms) in NU[k]:
                if a > x:
                    continue
                lg = conf_logp(k, x, jg, ms)
                if lg is None or lg < -745.0:
                    continue
                w = math.exp(lg) * wtest[(j, a)]
                if w > 0.0:
                    X = x_of(k, x, jg, ms)
                    acc[X] = acc.get(X, 0.0) + w
        for u in range(0, maxu_needed + 1):
            if x + u > 7:
                break
            sm = Smarg[u]
            if sm <= 0.0:
                continue
            for ct in comps(k, x):
                lg = comp_logp(k, ct)
                if lg is None or lg < -745.0:
                    continue
                X = comp_X(k, ct)
                acc[X] = acc.get(X, 0.0) + math.exp(lg) * sm
        if acc:
            xs = sorted(acc)
            ws = [acc[v] for v in xs]
            cumw = []
            s = 0.0
            for w in ws:
                s += w
                cumw.append(s)
            bws = [0.0] * len(ws)
            bt = 0.0
            for i in range(len(ws) - 1, -1, -1):
                bt += ws[i]
                bws[i] = bt
            bws[0] = s
            W[x] = (xs, ws, cumw, bws, s)
    return W, Smarg


def build_wc(k, N):
    """Exact per-(train,out) conditional not-support moment tables (c units):
      e1[k][(x,u)] = E[c_k * 1{not s_k} | x train, u test]
      e2[k][(x,u)] = E[c_k^2 * 1{not s_k} | x train, u test]
    c_k = delta_k^2 * X / (x * s_ref^2) with X the train-block SS."""
    NTR, NTE = A.split_sizes(N)
    del2 = DELTA2[k]
    scale = del2 / SREF2
    Bsum = build_Bsum(k, NTE)
    gv = GVALS[k]
    E1 = {}
    E2 = {}
    for x in range(1, NTR + 1):
        umin = max(0, 8 - x)
        acc1 = {}
        acc2 = {}
        if umin <= NTE:
            for (j, jg, a, ms) in NU[k]:
                if a > x:
                    continue
                lg = conf_logp(k, x, jg, ms)
                if lg is None or lg < -745.0:
                    continue
                P = math.exp(lg)
                X0 = x_of(k, x, jg, ms)
                for u in range(umin, NTE + 1):
                    bf = Bsum[(u, j, a)]
                    if bf <= 0.0:
                        continue
                    w1 = P * X0 * bf
                    w2 = P * X0 * X0 * bf
                    acc1[u] = acc1.get(u, 0.0) + w1
                    acc2[u] = acc2.get(u, 0.0) + w2
        for u in range(0, min(NTE, 7 - x) + 1):
            for X0, P in ccomp(k, x):
                acc1[u] = acc1.get(u, 0.0) + P * X0
                acc2[u] = acc2.get(u, 0.0) + P * X0 * X0
        for u, w1 in acc1.items():
            E1[(x, u)] = w1 * scale / x
            E2[(x, u)] = acc2[u] * (scale / x) ** 2
    return E1, E2


def Smarg_weight(Smarg, Bsum, NTE, umin, j, a):
    """sum_{u >= umin} Smarg[u] * Bsum[(u, j, a)]."""
    s = 0.0
    for u in range(umin, NTE + 1):
        p = Smarg[u]
        if p > 0.0:
            s += p * Bsum[(u, j, a)]
    return s

# ==========================================================================
# Part 6: threshold stage computation
# ==========================================================================

def w0_of(Wx):
    """weight at X = 0 (the train-constant slice) of a folded w table."""
    if Wx is None:
        return 0.0
    xs, ws = Wx[0], Wx[1]
    if xs and xs[0] == 0:
        return ws[0]
    return 0.0


_PURE = {}   # (k, x, u) -> (xs list, backward-cum left tail list) not-s_k table
_BSUM = {}   # k -> Bsum dict (test-side not-support complements), u up to 200


def _bsum(k):
    b = _BSUM.get(k)
    if b is None:
        b = build_Bsum(k, 200)
        _BSUM[k] = b
    return b


def purtail(k, x, u, thr):
    """P(X >= thr AND not-s_k | bucket k with x train, u test bodies).

    Exact complement side for the s_k & X-tail joints:
      P(X >= thr & s_k) = tailx(k, x, thr) - purtail(k, x, u, thr).
    Backed by w_pure's exact enumeration (concentrated configuration branch
    for n = x+u >= 8, exhaustive train comps for n <= 7); cached per (k,x,u)."""
    key = (k, x, u)
    arr = _PURE.get(key)
    if arr is None:
        d = w_pure(k, x, u, _bsum(k))
        xs = sorted(d)
        ws = [d[v] for v in xs]
        bce = [0.0] * len(ws)
        bt = 0.0
        for i in range(len(ws) - 1, -1, -1):
            bt += ws[i]
            bce[i] = bt
        arr = (xs, bce, bt)
        _PURE[key] = arr
    xs, bce, tot = arr
    if not xs or thr <= xs[0]:
        return tot
    i = bisect_left(xs, thr)
    if i >= len(xs):
        return 0.0
    return bce[i]


def build_rows(N, p5, p10, rmask, cut):
    """R rows truncated at cut: per x the kept (y, r) pairs (ys, rs arrays)
    and the exact dropped mass; also the total kept for P(TR) style sums."""
    NTR, NTE = A.split_sizes(N)
    pO = 1.0 - p5 - p10
    rows = [None] * (NTR + 1)
    dropped = 0.0
    total = 0.0
    for x in range(0, NTR + 1):
        if rmask and x < 1:
            continue
        ylo = 1 if rmask else 0
        ys = []
        rs = []
        rowdrop = 0.0
        for y in range(ylo, NTR - x + 1):
            if rmask and x + y < 8:
                continue
            p = A.mpmf2(NTR, x, y, p5, p10, pO)
            total += p
            if p >= cut:
                ys.append(y)
                rs.append(p)
            else:
                rowdrop += p
        dropped += rowdrop
        if ys:
            rows[x] = (array("q", ys), array("d", rs))
    return rows, dropped, total, NTR, NTE


def p_gate_tn(N, p5, p10):
    """P(TN) = P(te5>=1, te10>=1, te5+te10>=8); exact sum."""
    NTR, NTE = A.split_sizes(N)
    pO = 1.0 - p5 - p10
    s = 0.0
    for u in range(1, NTE + 1):
        for v in range(1, NTE - u + 1):
            if u + v >= 8:
                s += A.mpmf2(NTE, u, v, p5, p10, pO)
    return s


def scen_thresholds(scen, N, taus, verbose=True):
    """All threshold-stage quantities for one (scen, N).

    Returns a dict with per tau:
      P_c_ge_tau_tr    P(TR & c>=tau)                    (pure train)
      P_c_ge_tau       P(c>=tau) unconditioned           (N <= 150 only)
      C_not5/C_not10/C_notnot, D5/D10, C5_same/C10_same
      v2_one / v2_each stage values and their TN variants
      bound_abs        certified absolute error bound
    Supported by the folded w tables for both S masks."""
    p5 = A.SCEN[scen][5]
    p10 = A.SCEN[scen][10]
    NTR, NTE = A.split_sizes(N)
    cut = R_CUT_BIG if N >= 450 else R_CUT_SMALL
    rows_tr, drop_tr, P_TR, _, _ = build_rows(N, p5, p10, True, cut)
    P_TN = p_gate_tn(N, p5, p10)
    if N <= 150:
        rows_fu, drop_fu, _, _, _ = build_rows(N, p5, p10, False, cut)
    else:
        rows_fu, drop_fu = None, 0.0
    W5F, S5mF = build_w(5, N, p5, p10, False)
    W5T, _ = build_w(5, N, p5, p10, True)
    W10F, S10mF = build_w(10, N, p5, p10, False)
    W10T, _ = build_w(10, N, p5, p10, True)
    # exact same-bucket decomposition slices (CVD-each reading):
    #   E55(tau):   {c >= tau} & X5 = 0 (same5)   -> requires X10 >= fl10(y)
    #   E1010(tau): {c >= tau} & X10 = 0 (same10) -> requires X5 >= fl5(x)
    # Given (x,y) and the (u,v) test-split law S (3-way multinomial over
    # u / v / unobserved; pairs satisfy u + v <= NTE) the two buckets' bodies
    # are disjoint draws, so each slice factorizes over buckets and is
    # double-folded over u, v exactly:
    #   E1010(x,y) = sum_{u+v<=NTE} S(u,v) a5t(x,u,fl5) H10(y+v,y)
    #   E55(x,y)   = sum_{u+v<=NTE} S(u,v) H5(x+u,x) a10t(y,v,fl10)
    #   a5t(x,u,thr)  = P(X5 >= thr & s5 | 5-bucket)
    #                 = tailx(5,x,thr) - purtail(5,x,u,thr)
    #   a10t(y,v,thr) = P(X10 >= thr & s10 | 10-bucket)
    #                 = tailx(10,y,thr) - purtail(10,y,v,thr)
    # H5/H10 are the exact P(s_k & train-constant) measures.  No independence
    # shortcut inside a bucket: the (X_k & not-s_k) joints come from purtail's
    # exact per-(x,u) configuration enumeration.  T-chain variants fold the
    # TN-masked split law S^T over the same per-bucket factors.
    S_F = build_RS(N, p5, p10, False, False)[1]
    S_T = build_RS(N, p5, p10, False, True)[1]
    w0_5F = [w0_of(W5F[x]) for x in range(NTR + 1)]
    w0_5T = [w0_of(W5T[x]) for x in range(NTR + 1)]
    w0_10F = [w0_of(W10F[y]) for y in range(NTR + 1)]
    w0_10T = [w0_of(W10T[y]) for y in range(NTR + 1)]
    bnd_dp = DP_DROP[5] + DP_DROP[10]
    out = {"P_TR": P_TR, "P_TN": P_TN, "R_drop_tr": drop_tr,
           "R_drop_full": drop_fu, "dp_drop": bnd_dp, "taus": {}}
    for tau in taus:
        num, den = tau_frac(tau)
        ptr = cn5 = cn10 = cnn = 0.0
        cn5t = cn10t = cnnt = 0.0
        d5 = d10 = c5s = c10s = 0.0
        c5st = c10st = 0.0
        e55 = e1010 = e55t = e1010t = 0.0
        h5get = H5.get
        h10get = H10.get
        # Per-y folded other-bucket factors over the 3-way test-split law
        #   GG55[y][u]  = sum_v<=NTE-u S(u,v)   a10t(y,v,fl10)
        #   GG10[y][u]  = sum_v<=NTE-u S(u,v)   H10(y+v,y)
        # (t-variants use S^T); built once per tau and reused over all x.
        GG55 = [None] * (NTR + 1)
        GG55t = [None] * (NTR + 1)
        GG10 = [None] * (NTR + 1)
        GG10t = [None] * (NTR + 1)
        y_a10 = [None] * (NTR + 1)
        for y in range(1, NTR + 1):
            fl10y = ssfloor_x(10, y, num, den)
            tx10y = tailx(10, y, fl10y)
            a10v = [0.0] * (NTE + 1)
            any10 = False
            for vv in range(NTE + 1):
                av = tx10y - purtail(10, y, vv, fl10y)
                if av > 0.0:
                    a10v[vv] = av
                    any10 = True
            y_a10[y] = (tx10y, a10v)
            g5 = [0.0] * (NTE + 1)
            g5t = [0.0] * (NTE + 1)
            g1 = [0.0] * (NTE + 1)
            g1t = [0.0] * (NTE + 1)
            h10v = [h10get((y + vv, y), 0.0) for vv in range(NTE + 1)]
            for uu in range(NTE + 1):
                sFu = S_F[uu]
                for vv, s in sFu.items():
                    if s > 0.0:
                        if any10 and a10v[vv] > 0.0:
                            g5[uu] += s * a10v[vv]
                        hv = h10v[vv]
                        if hv > 0.0:
                            g1[uu] += s * hv
                sTu = S_T[uu]
                for vv, s in sTu.items():
                    if s > 0.0:
                        if any10 and a10v[vv] > 0.0:
                            g5t[uu] += s * a10v[vv]
                        hv = h10v[vv]
                        if hv > 0.0:
                            g1t[uu] += s * hv
            GG55[y] = g5
            GG55t[y] = g5t
            GG10[y] = g1
            GG10t[y] = g1t
        # per-bucket-5 floor at X5 = 0 (same5) and X10 = 0 (same10):
        #   X10 >= ceil(r0/x) (= ssfloor_x(10,y));  X5 >= ceil(r0/(4y)).
        for x in range(1, NTR + 1):
            rowt = rows_tr[x]
            if rowt is None:
                continue
            ys, rs = rowt
            w5f = W5F[x]
            w5t = W5T[x]
            p5w = POW5[x]
            w05f = w0_5F[x]
            w05t = w0_5T[x]
            ds5 = dp_side(5, x)
            fl5 = ssfloor_x(5, x, num, den)
            tx5 = tailx(5, x, fl5)
            # bucket-5 factors of the E1010 slice and the E55 s5-side,
            # per test side u
            a5 = [0.0] * (NTE + 1)
            h5u = [0.0] * (NTE + 1)
            for uu in range(NTE + 1):
                av = tx5 - purtail(5, x, uu, fl5)
                if av > 0.0:
                    a5[uu] = av
                h5u[uu] = h5get((x + uu, x), 0.0)
            for i, y in enumerate(ys):
                r = rs[i]
                if r <= 0.0:
                    continue
                r0 = pooled_R0(x, y, num, den)
                cy = 4 * y
                fl10 = ssfloor_x(10, y, num, den)
                ds10 = dp_side(10, y)
                tx10 = tailx(10, y, fl10)
                # exact same-bucket slices via the per-y GG folds
                g5 = GG55[y]
                g5t = GG55t[y]
                g1 = GG10[y]
                g1t = GG10t[y]
                se55 = se55t = se1010 = se1010t = 0.0
                for uu in range(NTE + 1):
                    h5v = h5u[uu]
                    if h5v > 0.0:
                        w10v = g5[uu]
                        if w10v > 0.0:
                            se55 += h5v * w10v
                        w10v = g5t[uu]
                        if w10v > 0.0:
                            se55t += h5v * w10v
                    a5v = a5[uu]
                    if a5v > 0.0:
                        w5v = g1[uu]
                        if w5v > 0.0:
                            se1010 += a5v * w5v
                        w5v = g1t[uu]
                        if w5v > 0.0:
                            se1010t += a5v * w5v
                # pure-train pair tail, diagnostics
                ptr += r * gen_tail(ds5[0], ds5[1], ds10[0], ds10[2],
                                    cy, x, r0)
                d5 += r * p5w * tx10
                d10 += r * POW10[y] * tx5
                # one-side corrections (unmasked S)
                cn5 += r * gen_tail(w5f[0], w5f[1], ds10[0], ds10[2],
                                    cy, x, r0)
                cn10 += r * gen_tail(ds5[0], ds5[1],
                                     W10F[y][0], W10F[y][3],
                                     cy, x, r0)
                cnn += r * gen_tail(w5f[0], w5f[1],
                                    W10F[y][0], W10F[y][3],
                                    cy, x, r0)
                c5s += r * w05f * tx10
                c10s += r * w0_10F[y] * tx5
                e55 += r * se55
                e1010 += r * se1010
                # TN-masked corrections
                cn5t += r * gen_tail(w5t[0], w5t[1], ds10[0], ds10[2],
                                     cy, x, r0)
                cn10t += r * gen_tail(ds5[0], ds5[1],
                                      W10T[y][0], W10T[y][3],
                                      cy, x, r0)
                cnnt += r * gen_tail(w5t[0], w5t[1],
                                     W10T[y][0], W10T[y][3],
                                     cy, x, r0)
                c5st += r * w05t * tx10
                c10st += r * w0_10T[y] * tx5
                e55t += r * se55t
                e1010t += r * se1010t
        pfull = 0.0
        if rows_fu is not None:
            rowf = rows_fu[0]
            if rowf is not None:
                ysf, rsf = rowf
                for i, y in enumerate(ysf):
                    rf = rsf[i]
                    if rf <= 0.0:
                        continue
                    # x = 0: c >= tau  <=>  X10 >= ssfloor_x(10, y)
                    pfull += rf * tailx(10, y,
                                        ssfloor_x(10, y, num, den))
            for x in range(1, NTR + 1):
                rowf = rows_fu[x]
                if rowf is None:
                    continue
                ds5 = dp_side(5, x)
                ysf, rsf = rowf
                for i, y in enumerate(ysf):
                    rf = rsf[i]
                    if rf <= 0.0:
                        continue
                    r0 = pooled_R0(x, y, num, den)
                    ds10 = dp_side(10, y)
                    pfull += rf * gen_tail(ds5[0], ds5[1], ds10[0], ds10[2],
                                           4 * y, x, r0)
        sup_tr_c = ptr - cn5 - cn10 + cnn
        v2_one = sup_tr_c
        v2_each = sup_tr_c - e55 - e1010
        sup_tr_tn_c = ptr * P_TN - cn5t - cn10t + cnnt
        v2_one_tn = sup_tr_tn_c
        v2_each_tn = sup_tr_tn_c - e55t - e1010t
        bnd = drop_tr + bnd_dp
        out["taus"][repr(tau)] = {
            "tau": tau,
            "P_c_ge_tau_tr": ptr, "P_c_ge_tau": pfull,
            "C_not5": cn5, "C_not10": cn10, "C_notnot": cnn,
            "E55": e55, "E1010": e1010,
            "same5_c_ge_tau": d5, "same10_c_ge_tau": d10,
            "not5_same5": c5s, "not10_same10": c10s,
            "v2_one": v2_one, "v2_each": v2_each,
            "sup_tr_c_ge_tau": sup_tr_c,
            "E55_tn": e55t, "E1010_tn": e1010t,
            "v2_one_tn": v2_one_tn, "v2_each_tn": v2_each_tn,
            "sup_tr_tn_c_ge_tau": sup_tr_tn_c,
            "bound_abs": bnd,
        }
        if verbose:
            print(f"  tau={tau:g}: ptr={ptr:.6e} v2_one={v2_one:.6e} "
                  f"v2_each={v2_each:.6e} (bound {bnd:.2e})")
    return out

# ==========================================================================
# Part 9: verification battery
# ==========================================================================

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O2JSON = os.path.join(_ROOT, "o2_calc", "o2_results.json")


def v01():
    r33 = pooled_R0(3, 3, 390625, 10000)
    r1010 = pooled_R0(10, 10, 15625, 100)
    ok = (tau_frac(39.0625) == (390625, 10000)
          and tau_frac(156.25) == (15625, 100)
          and tau_frac(625.0) == (6250, 10)
          and r33 == (390625 * SREF2_NUM * 100 * 9 + 10000 * UINTC - 1)
          // (10000 * UINTC)
          and r1010 == (15625 * SREF2_NUM * 100 * 100 + 100 * UINTC - 1)
          // (100 * UINTC)
          and r33 == 568)
    check("V01 exact tau arithmetic", ok,
          detail=f"39.0625->{tau_frac(39.0625)} R0(3,3)={r33} "
                 f"R0(10,10;156.25)={r1010}")


def v02():
    for k in (5, 10):
        ok = True
        det = ""
        for t in range(0, 9):
            tab = DP[k][t]
            xd = {}
            for ct in comps(k, t):
                lg = comp_logp(k, ct)
                if lg is None or lg < -745.0:
                    continue
                X = comp_X(k, ct)
                xd[X] = xd.get(X, 0.0) + math.exp(lg)
            if sorted(xd) != list(tab.xs):
                ok = False
                det = f"k{k} t{t} support set differs"
                break
            worst = max((abs(xd[X] - tab.ps[i])
                         for i, X in enumerate(tab.xs)), default=0.0)
            if worst > 1e-13:
                ok = False
                det = f"k{k} t{t} worst abs {worst:.3e}"
                break
        check(f"V02 dp vs comps k={k}", ok, det)


def _extreme_prob(k, t, xtarget):
    s = 0.0
    for ct in comps(k, t):
        if comp_X(k, ct) == xtarget:
            lg = comp_logp(k, ct)
            if lg is not None and lg > -745.0:
                s += math.exp(lg)
    return s


def v03():
    for k in (5, 10):
        gv = GVALS[k]
        Rg = gv[-1] - gv[0]
        bad_min = bad_max = bad_att = 0
        vac = False
        det = []
        for t in range(2, KT_SUM + 1):
            tab = DP[k][t]
            xs = tab.xs
            if not xs:
                continue
            bound = (t * t // 4) * Rg * Rg
            if xs[-1] > bound:
                bad_max += 1
                det.append(f"k{k} t{t} maxX={xs[-1]}>{bound}")
            if t <= 20 and xs[0] == 0 and len(xs) > 1 and xs[1] != t - 1:
                bad_min += 1
                det.append(f"k{k} t{t} minNZ={xs[1]}!={t-1}")
            if t <= 8 and xs[-1] != bound:
                if _extreme_prob(k, t, bound) < 1e-13:
                    vac = True
                else:
                    bad_att += 1
                    det.append(f"k{k} t{t} maxX={xs[-1]}!={bound}")
        check(f"V03 X-range invariants k={k}",
              bad_min == 0 and bad_max == 0 and bad_att == 0,
              "; ".join(det[:4]) if det else
              f"minNZ=t-1 (t<=20), max<=floor(t^2/4)R^2 (all t), "
              f"attained (t<=8) OK", vac=vac)


def v04():
    pairs = [(2, 2), (3, 3), (4, 5), (5, 3), (6, 4), (7, 7), (8, 6),
             (1, 9), (9, 1), (0, 9)]
    ok = True
    det = ""
    worst = 0.0
    for (x, y) in pairs:
        for tau in (10.0, 39.0625, 156.25, 625.0):
            num, den = tau_frac(tau)
            r0 = pooled_R0(x, y, num, den)
            a = pair_dp_dp(x, y, r0)
            b = brute_pair(x, y, r0)
            d = abs(a - b) / max(a, b, 1e-300) if max(a, b) > 0 else 0.0
            worst = max(worst, d)
            if d > 1e-12:
                ok = False
                det = f"({x},{y}) tau={tau} dp={a:.3e} brute={b:.3e}"
                break
        if not ok:
            break
    check("V04 pair dp vs brute enums", ok, det or f"worst rel {worst:.3e}")


def v05():
    for name, Hh, Fn in (("H5", H5, F5), ("H10", H10, F10)):
        worst = 0.0
        for n in range(0, NMAX + 1):
            if Fn[n] > 0.0:
                d = abs(Hh.get((n, 1), 0.0) - Fn[n]) / Fn[n]
                worst = max(worst, d)
        check(f"V05 {name}(n,1)==F(n) all n (rel)", worst <= 1e-12,
              f"worst rel {worst:.3e}")
        viol = sum(1 for (n, t), h in Hh.items() if h > Fn[n] + 1e-15)
        check(f"V05 {name}<=F pointwise", viol == 0, f"{viol} violations")

def v06():
    with open(O2JSON, "r") as fh:
        o2 = json.load(fh)
    res = o2["results"]
    ok = True
    worst = {}
    y_scaled = {}
    for key in sorted(res):
        row = res[key]
        scen, ns = key.split("|")
        N = int(ns)
        p5 = A.SCEN[scen][5]
        p10 = A.SCEN[scen][10]
        T, _M, _ntr, _nte = rs_terms(N, p5, p10, "tr", "tn",
                                    with_moments=False)
        for nm in ("T0", "P_atleastone", "P_each"):
            ref = row[nm]
            got = T[nm]
            d = abs(got - ref) / max(abs(ref), 1e-300) if ref else abs(got)
            worst[nm] = max(worst.get(nm, 0.0), d)
            if d > 1e-11:
                ok = False
                y_scaled.setdefault(nm, []).append(
                    f"{key} ref={ref:.12g} got={got:.12g}")
    det = " ".join(f"{k}:{v:.3e}" for k, v in sorted(worst.items()))
    if not ok:
        det += " | misses: " + "; ".join(
            x for vs in y_scaled.values() for x in vs[:2])
    check("V06 O2 cross-check (16 scen,N, rel)", ok, det)


def v07():
    # w_pure vs brute_w; x<=3 with u>=8-x exercises the a=x (test-only
    # dominant violating class) configs of the joint S1 rule.
    for k in (5, 10):
        cases = sorted(set((x, u) for x in range(1, 9) for u in range(0, 9)
                           if x + u <= 10))
        ok = True
        det = ""
        worst = 0.0
        for (x, u) in cases:
            wp = w_pure(k, x, u, build_Bsum(k, u))
            bw = brute_w(k, x, u)
            if sorted(wp) != sorted(bw):
                ok = False
                det = f"k{k} ({x},{u}) support keys differ"
                break
            wk = max((abs(wp[X] - bw[X]) / max(wp[X], bw[X], 1e-300)
                      for X in wp if wp[X] or bw[X]), default=0.0)
            worst = max(worst, wk)
            if worst > 1e-13:
                ok = False
                det = f"k{k} ({x},{u}) worst rel {wk:.3e}"
                break
        check(f"V07 w_pure vs brute_w k={k}", ok,
              det or f"worst rel {worst:.3e} over {len(cases)} cases")


def v08():
    # fold identity: W[x] total = sum_u Smarg[u] * P(not s_k | x, u)
    # complement identity: sum_u Smarg[u]*F(x+u) + W[x] total = 1
    N = 113
    scen = "a-hist"
    NTR_v, nte_V = A.split_sizes(N)
    p5 = A.SCEN[scen][5]
    p10 = A.SCEN[scen][10]
    worst = {}
    for k in (5, 10):
        Fn = F5 if k == 5 else F10
        W, Smarg = build_w(k, N, p5, p10, False)
        wc = 0.0
        wf = 0.0
        for x in range(1, NTR_v + 1):
            row = W[x]
            if row is None:
                continue
            xs_v, ws_v, _fwd, _bwd, tot = row
            if abs(tot - sum(ws_v)) > wf:
                wf = abs(tot - sum(ws_v))
            lhs = tot + sum(Smarg[u] * Fn[x + u]
                            for u in range(0, nte_V + 1))
            if abs(lhs - 1.0) > wc:
                wc = abs(lhs - 1.0)
        worst[k] = max(wc, wf)
    ok = worst[5] <= 1e-11 and worst[10] <= 1e-11
    check(f"V08 W-fold complement identity (a-hist {N})", ok,
          f"k5 dev {worst[5]:.3e} k10 dev {worst[10]:.3e}")


def _cond_tail_value(x, u, y, r0):
    """P(not s5 AND 4y*X5 + x*X10 >= r0 | x train, u test, y train-10),
    via the w_pure X table and the DP10 slide."""
    aw = w_pure(5, x, u, build_Bsum(5, u))
    bt = dp_side(10, y)
    btot = bt[3]
    acc = 0.0
    for Xa, wa in aw.items():
        s = r0 - 4 * y * Xa
        xb = (s + x - 1) // x if s > 0 else 0
        if xb <= 0:
            acc += wa * btot
            continue
        ci = bisect_left(bt[0], xb)
        if ci >= len(bt[0]):
            continue
        acc += wa * bt[2][ci]
    return acc


def _cond_tail_brute(x, u, y, r0):
    """Direct enumeration of the same conditional event."""
    acc = 0.0
    ct5 = comps(5, x)
    cs5 = comps(5, u)
    ct10 = [(comp_X(10, ct), comp_logp(10, ct)) for ct in comps(10, y)]
    for ct in ct5:
        lga = comp_logp(5, ct)
        wa = math.exp(lga) if lga > -745.0 else 0.0
        if wa <= 0.0:
            continue
        for cs in cs5:
            lgb = comp_logp(5, cs)
            wb = math.exp(lgb) if lgb > -745.0 else 0.0
            if wb <= 0.0:
                continue
            lab = tuple(a + b for a, b in zip(ct, cs))
            n = x + u
            nj = max(lab)
            if n >= 8 and n - nj > 3:
                continue
            X5 = comp_X(5, ct)
            for X10, lg10 in ct10:
                if 4 * y * X5 + x * X10 < r0:
                    continue
                w10 = math.exp(lg10) if lg10 > -745.0 else 0.0
                acc += wa * wb * w10
    return acc


def v09():
    cases = [(3, 3), (6, 3), (8, 3), (8, 1), (1, 7), (2, 6), (3, 8)]
    ok = True
    det = ""
    worst = 0.0
    for (x, u) in cases:
        for y in (3, 5):
            for tau in (10.0, 39.0625, 625.0):
                num, den = tau_frac(tau)
                r0 = pooled_R0(x, y, num, den)
                a = _cond_tail_value(x, u, y, r0)
                b = _cond_tail_brute(x, u, y, r0)
                d = abs(a - b) / max(a, b, 1e-300) if max(a, b) > 0 else 0.0
                worst = max(worst, d)
                if d > 1e-11:
                    ok = False
                    det = f"({x},{u};{y}) tau={tau} mach={a:.6e} " \
                          f"brute={b:.6e}"
    check("V09 conditional not-s+threshold machinery vs brute", ok,
          det or f"worst rel {worst:.3e} over {3*2*len(cases)} cases")

def v10():
    # monotonicity of the T0/P_atleastone/P_each stage across mask combos
    Ns = (113, 150)
    scen = "a-hist"
    p5 = A.SCEN[scen][5]
    p10 = A.SCEN[scen][10]
    ok = True
    det = ""
    for N in Ns:
        vals = {}
        for m1 in (False, "tr"):
            for m2 in (False, "tn"):
                T, _M, _ntr, _nte = rs_terms(N, p5, p10, m1, m2,
                                             with_moments=False)
                vals[(m1, m2)] = T
        for nm in ("T0", "P_atleastone", "P_each"):
            ff = vals[(False, False)][nm]
            tf = vals[("tr", False)][nm]
            ft = vals[(False, "tn")][nm]
            tt = vals[("tr", "tn")][nm]
            if not (tt <= max(ft, tf) + 1e-15 and min(ft, tf) <= ff + 1e-15
                    and tt <= ff + 1e-15):
                ok = False
                det += f" N{N} {nm}: {tt:.6e} {tf:.6e} {ft:.6e} {ff:.6e};"
            if vals[(False, False)]["P_each"] > ff + 1e-15:
                ok = False
                det += f" N{N} each>T0;"
    check("V10 stage monotonicity across masks (a-hist)", ok, det or
          "T0('tr','tn') <= singles <= T0(False,False), each <= P_al1")


def v13():
    # ceil(pooled_R0/x) = ssfloor_x(10,y); ceil(pooled_R0/(4y)) = ssfloor_x(5,x)
    pairs = [(2, 3), (3, 3), (4, 5), (5, 5), (6, 8), (8, 8), (11, 13),
             (13, 21), (21, 34), (34, 55), (1, 10), (10, 1)]
    ok = True
    det = ""
    for (x, y) in pairs:
        for tau in TAUS:
            num, den = tau_frac(tau)
            r0 = pooled_R0(x, y, num, den)
            a = (r0 + x - 1) // x
            b = (r0 + 4 * y - 1) // (4 * y)
            if a != ssfloor_x(10, y, num, den) or b != ssfloor_x(5, x, num, den):
                ok = False
                det = f"({x},{y}) tau={tau}"
    check("V13 per-bucket ceil identities (12 pairs x 12 taus)", ok, det)


def v14():
    """V14: brute-check the per-bucket (X >= thr & s) / (X >= thr & not-s)
    joints that feed the E-slice folds:
      tx   = P(X >= thr)            vs  tailx(k, x, thr)
      pur  = P(X >= thr & not-s_k)  vs  purtail(k, x, u, thr)
      a    = tx - pur = P(X & s_k)  vs  tx - purtail
    Enumeration: train comps and test comps independently over the GVALS
    labels with the CK probabilities; the frozen S1-m4 rule on the JOINT
    counts (n >= 8 and max_c <= n-4; s fails for n < 8)."""
    worst = {"tx": 0.0, "pur": 0.0, "a": 0.0}
    ncase = 0
    taus14 = (10.0, 39.0625, 156.25)
    for k in (5, 10):
        for x in (1, 4, 6, 8):
            tcs = comps(k, x)
            for u in (0, 1, 2, 3, 4, 6, 8, 10, 12):
                if x + u > 20:
                    continue
                n = x + u
                ucs = comps(k, u)
                pu = []
                for cU in ucs:
                    lg = comp_logp(k, cU)
                    pu.append(0.0 if (lg is None or lg < -745.0)
                              else math.exp(lg))
                thrs = {0, 1, 4, 16, 64, 256, 1024, 4096, 8192}
                for t14 in taus14:
                    tnum, tden = tau_frac(t14)
                    thrs.add(ssfloor_x(k, x, tnum, tden))
                tabS = {}
                tabN = {}
                for cT in tcs:
                    lgt = comp_logp(k, cT)
                    if lgt is None or lgt < -745.0:
                        continue
                    pT = math.exp(lgt)
                    Xv = comp_X(k, cT)
                    for j, cU in enumerate(ucs):
                        w = pT * pu[j]
                        if w <= 0.0:
                            continue
                        cJ = tuple(a + b for a, b in zip(cT, cU))
                        if n >= 8 and max(cJ) <= n - 4:
                            tabS[Xv] = tabS.get(Xv, 0.0) + w
                        else:
                            tabN[Xv] = tabN.get(Xv, 0.0) + w
                totS = sum(tabS.values())
                totN = sum(tabN.values())
                alltab = dict(tabS)
                for Xv, mval in tabN.items():
                    alltab[Xv] = alltab.get(Xv, 0.0) + mval
                for thr in thrs:
                    ncase += 1
                    if thr <= 0:
                        txbr = totS + totN
                        purbr = totN
                        abr = totS
                    else:
                        txbr = sum(m for Xv, m in alltab.items() if Xv >= thr)
                        purbr = sum(m for Xv, m in tabN.items() if Xv >= thr)
                        abr = txbr - purbr
                    tx = tailx(k, x, thr)
                    pur = purtail(k, x, u, thr)
                    amach = tx - pur
                    ascale = max(txbr, purbr, 1e-300)
                    worst["tx"] = max(worst["tx"],
                                      abs(tx - txbr) / max(txbr, 1e-300))
                    worst["pur"] = max(worst["pur"],
                                       abs(pur - purbr) / max(purbr, 1e-300))
                    worst["a"] = max(worst["a"],
                                     abs(amach - abr) / ascale)
    ok = worst["tx"] <= 1e-11 and worst["pur"] <= 1e-11 \
        and worst["a"] <= 1e-11
    check("V14 per-bucket (X,tail x s/not-s) joints vs brute", ok,
          detail=f"over {ncase} cases tx={worst['tx']:.3e} "
                 f"pur={worst['pur']:.3e} a={worst['a']:.3e}")


# ==========================================================================
# Part 10: per-(k,t) tables, scenario collection, outputs, run control
# ==========================================================================

def per_kt_tables():
    out = {"k5": {}, "k10": {}}
    worst = {"unpruned_E1": 0.0, "unpruned_E2": 0.0,
             "pruned_E1": 0.0, "pruned_E2": 0.0}
    for k in (5, 10):
        Fn = F5 if k == 5 else F10
        summ = {}
        dist = {}
        for t in range(0, KT_SUM + 1):
            tab = DP[k][t]
            tot = tab.cum[-1]
            e1 = e2 = pzero = 0.0
            for i, xx in enumerate(tab.xs):
                w = tab.ps[i]
                e1 += w * xx
                e2 += w * xx * xx
                if xx == 0:
                    pzero += w
            row = {"F": Fn[t], "dp_tot": tot, "dp_drop": tab.drop,
                   "E1_dp": e1, "E2_dp": e2, "P_X0_dp": pzero}
            if t >= 1:
                row["E1_closed"] = ex(k, t)
                row["E2_closed"] = ex2(k, t)
                row["P_X0_closed"] = sum(p ** t for p in A.CK[k][1])
                if tot > 1e-250:
                    d1 = abs(e1 - row["E1_closed"]) / max(row["E1_closed"],
                                                         1e-12)
                    d2 = abs(e2 - row["E2_closed"]) / max(row["E2_closed"],
                                                          1e-12)
                    if t <= T_EXACT:
                        worst["unpruned_E1"] = max(worst["unpruned_E1"], d1)
                        worst["unpruned_E2"] = max(worst["unpruned_E2"], d2)
                    else:
                        worst["pruned_E1"] = max(worst["pruned_E1"], d1)
                        worst["pruned_E2"] = max(worst["pruned_E2"], d2)
            summ[t] = row
            if t <= KT_DIST:
                xs = tab.xs
                dd = {str(int(xx)): float(tab.ps[i])
                      for i, xx in enumerate(xs)}
                dist[t] = {"xs_p": dd, "tot": tot}
        out[f"k{k}" if False else ("k5" if k == 5 else "k10")] = {
            "summary": summ, "dist": dist}
    check("V12 closed vs DP empirical moments, t<=112 (rel)",
          worst["unpruned_E1"] <= 1e-9 and worst["unpruned_E2"] <= 1e-9,
          f"E1 {worst['unpruned_E1']:.3e} E2 {worst['unpruned_E2']:.3e}")
    check("V12 pruned band t in 113..120 (rel, <=1e-6)",
          worst["pruned_E1"] <= 1e-6 and worst["pruned_E2"] <= 1e-6,
          f"E1 {worst['pruned_E1']:.3e} E2 {worst['pruned_E2']:.3e}")
    return out


MASK_KEYS = {(False, False): "none", ("tr", False): "tr",
             (False, "tn"): "tn", ("tr", "tn"): "tr_tn"}


def scen_stage_terms(N, p5, p10):
    """rs_terms over all four mask combos, with exact c-moments."""
    st = {}
    for m1 in (False, "tr"):
        for m2 in (False, "tn"):
            T, M, ntr, nte = rs_terms(N, p5, p10, m1, m2, with_moments=True)
            key = MASK_KEYS[(m1, m2)]
            entry = dict(T)
            entry.update(M)
            entry["N"] = N
            entry["NTR"] = ntr
            entry["NTE"] = nte
            st[key] = entry
    return st


def scen_validate(tag, tout):
    """Internal consistency of the threshold-stage pieces per tau."""
    worst_res = 0.0
    worst_neg = 0.0
    worst_ord = 0.0
    for tk in tout["taus"]:
        r = tout["taus"][tk]
        res55 = r["E55"] + r["not5_same5"] - r["same5_c_ge_tau"]
        res1010 = r["E1010"] + r["not10_same10"] - r["same10_c_ge_tau"]
        worst_res = max(worst_res, res55, res1010)
        worst_neg = max(worst_neg, -r["v2_each"], -r["v2_each_tn"],
                        r["E55"] - r["sup_tr_c_ge_tau"],
                        r["E1010"] - r["sup_tr_c_ge_tau"],
                        r["E55_tn"] - r["sup_tr_tn_c_ge_tau"],
                        r["E1010_tn"] - r["sup_tr_tn_c_ge_tau"])
        ordv = max(r["v2_each"] - r["v2_one"],
                   r["v2_each_tn"] - r["v2_one_tn"],
                   r["sup_tr_tn_c_ge_tau"] - r["sup_tr_c_ge_tau"])
        worst_ord = max(worst_ord, ordv)
    tol = 1e-12
    ok = (worst_res <= tol and worst_neg <= tol and worst_ord <= tol)
    check(f"V11 {tag} same-partition/monotone invariants", ok,
          f"resid(<=1e-12) {worst_res:.3e} neg {worst_neg:.3e} "
          f"order {worst_ord:.3e}")


def _hash_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_outputs(per_kt, scen_res, timing):
    meta = {
        "run_date": datetime.datetime.now().isoformat(),
        "python": sys.version.split()[0],
        "module_hash_sha256": _hash_file(os.path.abspath(__file__)),
        "a1_hash_sha256": _hash_file(os.path.join(A1DIR,
                                                  "a1_support_comparison.py")),
        "N_B": list(NB),
        "scen": list(SCENS),
        "taus": list(TAUS),
        "cstar": list(CSTAR),
        "T_EXACT": T_EXACT,
        "EPS_DP": EPS_DP,
        "R_CUT_SMALL": R_CUT_SMALL,
        "R_CUT_BIG": R_CUT_BIG,
        "timing_s": timing,
    }
    doc = {"meta": meta, "checks": CHECKS, "per_kt": per_kt,
           "scen": scen_res}
    pth = os.path.join(OUTDIR, "nc1_results.json")
    with open(pth, "w") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")
    print(f"wrote {pth}")
    return pth


def fmt_cell(v):
    if v is None:
        return ""
    if v == 0.0:
        return "0"
    if abs(v) >= 1e-4:
        return f"{v:.9g}"
    return f"{v:.4e}"


def write_report(per_kt, scen_res, timing):
    L = []
    L.append("# NC1 report: gate-conditioned c-distribution\n")
    L.append("Pre-freeze temporary computation (owner-authorized NC1, "
             "no repo changes). A1 read-only import; same conventions as "
             "O2 temp stage. Support rule S1-m4 on the joint bucket "
             "(train+test bodies); CVD readings on the training block; "
             "TrainRa and Test-gate (TN) position masks as in O2.\n")
    L.append("## Findings summary")
    L.append("")
    fails = [c for c in CHECKS if c["status"] == "FAIL"]
    vac = [c for c in CHECKS if c["status"] == "VACUOUS"]
    L.append(f"Checks: {len(CHECKS)} run, {len(fails)} FAIL, "
             f"{len(vac)} VACUOUS.")
    for c in CHECKS:
        L.append(f"- {c['status']}: {c['name']} | {c['detail']}")
    L.append("")
    L.append("## Per-(k,t) summary (t <= 120)")
    L.append("")
    for kk in ("k5", "k10"):
        k = 5 if kk == "k5" else 10
        L.append(f"### bucket k={k}")
        L.append("")
        L.append("| t | F(t) | dp sum | dropped | minNZ-X | max-X | EX dp | "
                 "EX closed | rel dev |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        summ = per_kt[kk]["summary"]
        for t in range(0, KT_SUM + 1):
            r = summ[t]
            tab = DP[k][t]
            minnz = tab.xs[1] if (len(tab.xs) > 1 and tab.xs[0] == 0) else \
                (tab.xs[0] if tab.xs else "-")
            dev = ""
            if "E1_closed" in r:
                dev = f"{abs(r['E1_dp'] - r['E1_closed']) / max(r['E1_closed'], 1e-12):.1e}"
            L.append(f"| {t} | {fmt_cell(r['F'])} | {fmt_cell(r['dp_tot'])} |"
                     f" {fmt_cell(r['dp_drop'])} | {minnz} |"
                     f" {tab.xs[-1] if tab.xs else '-'} |"
                     f" {fmt_cell(r['E1_dp'])} |"
                     f" {fmt_cell(r.get('E1_closed'))} | {dev} |")
        L.append("")
        L.append(f"Full X distributions for t <= {KT_DIST} are in "
                 "nc1_results.json (per_kt.<k>.dist).")
        L.append("")
    L.append("## Scenario stage tables (N and scenario grid;")
    L.append("mask combos: none, tr=TrainRa, tn=test-gate, tr_tn)")
    L.append("")
    for key in sorted(scen_res):
        r = scen_res[key]
        L.append(f"### {key}  (NTR={r['NTR']}, NTE={r['NTE']})")
        L.append("")
        L.append("Stage probabilities (with exact c-moments):")
        L.append("")
        L.append("| stage | T0 | P_atleastone | P_each |")
        L.append("|---|---|---|---|")
        for mk in ("none", "tr", "tn", "tr_tn"):
            s = r["stages"][mk]
            L.append(f"| {mk} | {fmt_cell(s['T0'])} |"
                     f" {fmt_cell(s['P_atleastone'])} |"
                     f" {fmt_cell(s['P_each'])} |")
        L.append("")
        L.append(f"P_TR = {fmt_cell(r['P_TR'])}, "
                 f"P_TN = {fmt_cell(r['P_TN'])}, "
                 f"R_drop_tr = {fmt_cell(r['R_drop_tr'])}, "
                 f"R_drop_full = {fmt_cell(r['R_drop_full'])}, "
                 f"dp_drop = {fmt_cell(r['dp_drop'])}")
        L.append("")
        L.append("Threshold stages (c >= tau):")
        L.append("")
        L.append("| tau | P(c>=tau) unmasked | P(TR & c>=tau) |"
                 " v2_one (sup) | v2_each (sup) | v2_one TN |"
                 " v2_each TN | C_not5 | C_not10 | C_notnot |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        prov = "PROVISIONAL" if int(key.split("|")[1]) >= 450 else "exact"
        for tk in sorted(r["taus"], key=lambda x: float(x)):
            rr = r["taus"][tk]
            L.append(
                f"| {tk} | {fmt_cell(rr['P_c_ge_tau'])} |"
                f" {fmt_cell(rr['P_c_ge_tau_tr'])} |"
                f" {fmt_cell(rr['v2_one'])} | {fmt_cell(rr['v2_each'])} |"
                f" {fmt_cell(rr['v2_one_tn'])} | {fmt_cell(rr['v2_each_tn'])} |"
                f" {fmt_cell(rr['C_not5'])} | {fmt_cell(rr['C_not10'])} |"
                f" {fmt_cell(rr['C_notnot'])} |")
        if int(key.split("|")[1]) < 150:
            L.append("")
            L.append("P_c_ge_tau unmasked is exact for N <= 150; "
                     "the 450/600 unmasked values are not computed "
                     "(R-table size) and remain empty.")
        L.append("")
        L.append(f"R1 status for this block: {prov} "
                 f"(bound_abs = {fmt_cell(r['taus'][sorted(r['taus'], key=lambda x: float(x))[0]]['bound_abs'])})"
                 if prov == "PROVISIONAL" else
                 "R1 status for this block: exact.")
        L.append("")
    L.append("## R1 protocol notes")
    L.append("")
    L.append("- DP streaming: EPS_DP = 1e-14 for t > 112; dropped mass "
             "accumulated exactly; certified bias bound ~1e-9 on "
             "threshold-stage CDFs at N = 450, 600 (PROVISIONAL).")
    L.append("- R-table pair truncation: 1e-30 (N <= 150), 1e-18 "
             "(N >= 450); contribution bound ~1.4e-16.")
    L.append("- All other stages (support gates, CVD readings, moments) "
             "exact at every N; cross-checked against O2 (V06).")
    L.append(f"- Runtime: {timing}")
    pth = os.path.join(OUTDIR, "nc1_report.md")
    with open(pth, "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"wrote {pth}")
    return pth


def run(quick=False):
    t_all = time.time()
    tag = "QUICK" if quick else "FULL"
    print(f"NC1 {tag} run start "
          f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    timing = {}
    t0 = time.time()
    pi_moments(5)
    pi_moments(10)
    prep_nu()
    timing["prep"] = time.time() - t0
    print(f"moment/nu prep: {fmt(timing['prep'])}")
    t0 = time.time()
    for k in (5, 10):
        DP[k], DP_DROP[k] = bucket_dp(k, NTRMAX, T_EXACT, EPS_DP)
        print(f"DP[{k}] built: drop={DP_DROP[k]:.3e} "
              f"t={time.time() - t0:.1f}s")
    timing["dp"] = time.time() - t0
    t0 = time.time()
    prep_tables()
    timing["tables"] = time.time() - t0
    print(f"F/H/POW tables: {fmt(timing['tables'])}")
    t0 = time.time()
    v01()
    v02()
    v03()
    v04()
    v05()
    v06()
    v07()
    v08()
    v09()
    v10()
    v13()
    v14()
    timing["checks1"] = time.time() - t0
    print(f"battery V01-V10,V13: {fmt(timing['checks1'])}")
    per_kt = per_kt_tables()
    scen_res = {}
    ts = TAUS
    nlist = (113, 150) if quick else NB
    slist = ("a-hist", "c-50:50") if quick else SCENS
    for N in nlist:
        for scen in slist:
            t1 = time.time()
            st = scen_stage_terms(N, A.SCEN[scen][5], A.SCEN[scen][10])
            tout = scen_thresholds(scen, N, ts)
            scen_validate(f"{scen}|{N}", tout)
            scen_res[f"{scen}|{N}"] = {
                "N": N, "NTR": A.split_sizes(N)[0],
                "NTE": A.split_sizes(N)[1],
                "P_TR": tout["P_TR"], "P_TN": tout["P_TN"],
                "R_drop_tr": tout["R_drop_tr"],
                "R_drop_full": tout["R_drop_full"],
                "dp_drop": tout["dp_drop"],
                "stages": st, "taus": tout["taus"]}
            dt = time.time() - t1
            timing[f"scen_{scen}_{N}"] = dt
            print(f"{scen} N={N}: {fmt(dt)}")
    timing["total"] = time.time() - t_all
    tstr = f"total {timing['total']:.1f}s ({tag})"
    write_outputs(per_kt, scen_res, timing)
    write_report(per_kt, scen_res, tstr)
    nf = sum(1 for c in CHECKS if c["status"] == "FAIL")
    print(f"NC1 {tag} done: {len(CHECKS)} checks, {nf} FAIL, {tstr}")
    return 1 if nf else 0


def main():
    if "--quick" in sys.argv:
        sys.exit(run(quick=True))
    sys.exit(run(quick=False))


if __name__ == "__main__":
    main()
