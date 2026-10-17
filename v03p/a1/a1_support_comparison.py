"""A1 support-rule comparison — deterministic, stdlib only.

Work order: GPT scientific work order A1 (support-rule comparison).
Policy: deterministic non-sampling calculation only. No `random`, no Monte
Carlo, no bootstrap, no generation, no hidden-outcome access. All
probabilities are exact finite enumerations (multinomial / hypergeometric in
log space via precomputed log-factorials) with documented truncation bounds
where an exhaustive sum is infeasible.

Rules (B_min = 8 and 2 <= k <= 24 preserved throughout):
  S0: n >= 8, >= 2 distinct C values, >= 4 bodies at each OBSERVED C extreme.
  S1(m): n >= 8 and n - max_c n_c >= m  ( >= m bodies outside the modal value).
  S2(m): n >= 8 and >= m bodies in each prespecified disjoint C stratum.
    Strata are defined from the instrument's mathematically attainable C values
    per k (candidate operationalization, NOT an owner decision):
      z_k(C) = (C - Cmin(k)) / (Cmax(k) - Cmin(k));
      low  = {z <= 1/3}, high = {z >= 2/3}.

Population sizes N_b are fixed numbers of unique valid bodies (NOT exact
attempt-axis probabilities). 113/450 are plug-in proxies for expected unique
counts under rho=0.25 at 150/600 attempts. Validity losses unmodeled.

Split: 25% body holdout, fixed size T = round-half-up(0.25*N) = (N+2)//4,
hence T = 28/38/113/150 for N = 113/150/450/600. Exact hypergeometric
allocation logic; marginal probabilities are never multiplied.
"""

import math
import json

# --------------------------------------------------------------------------
# 0. Exact C|k distributions (uniform over feasible family-count vectors).
# --------------------------------------------------------------------------

def enumerate_ck(k):
    """Return (Z, {C value: vector count}) for given k.

    Feasible vectors: 6 families, each 0..5, summing to k.
    """
    counts = {}
    z = 0

    def rec(i, rem, cur):
        nonlocal z
        if i == 5:
            if 0 <= rem <= 5:
                f = tuple(cur + [rem])
                z += 1
                c = (max(f) / k) if k else 0.0
                counts[c] = counts.get(c, 0) + 1
            return
        for v in range(0, min(5, rem) + 1):
            rec(i + 1, rem - v, cur + [v])

    rec(0, k, [])
    return z, counts


CK = {}          # k -> (sorted values list, probs list)
CK_Z = {}        # k -> Z
for _k in (5, 10, 20, 24):
    _z, _c = enumerate_ck(_k)
    _vals = sorted(_c)
    _tot = float(_z)
    CK[_k] = (_vals, [_c[v] / _tot for v in _vals])
    CK_Z[_k] = _z

# S2 strata from attainable values (candidate operationalization).
S2_STRATA = {}   # k -> dict(low_idx, high_idx, p_low, p_mid, p_high)
for _k, (_vals, _probs) in CK.items():
    if _k not in (5, 10, 20):
        continue
    cmin, cmax = _vals[0], _vals[-1]
    rng = cmax - cmin
    low_idx = [i for i, v in enumerate(_vals) if (v - cmin) / rng <= 1.0 / 3.0 + 1e-12]
    high_idx = [i for i, v in enumerate(_vals) if (v - cmin) / rng >= 2.0 / 3.0 - 1e-12]
    assert low_idx and high_idx, _k
    assert not set(low_idx) & set(high_idx), _k
    p_low = sum(_probs[i] for i in low_idx)
    p_high = sum(_probs[i] for i in high_idx)
    S2_STRATA[_k] = {
        "vals": _vals, "probs": _probs,
        "low_vals": [_vals[i] for i in low_idx],
        "high_vals": [_vals[i] for i in high_idx],
        "cmin": cmin, "cmax": cmax,
        "p_low": p_low, "p_mid": 1.0 - p_low - p_high, "p_high": p_high,
    }

# --------------------------------------------------------------------------
# 1. Log-factorial table + pmf helpers (all exact finite sums).
# --------------------------------------------------------------------------

NMAX = 600
LFACT = [0.0] * (NMAX + 1)
for _n in range(1, NMAX + 1):
    LFACT[_n] = LFACT[_n - 1] + math.log(_n)


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


def binom_lower(n, m, p):
    """P(Bin(n,p) <= m)."""
    if m < 0:
        return 0.0
    if m >= n:
        return 1.0
    return sum(binom_pmf(n, i, p) for i in range(0, m + 1))


def binom_upper(n, thresh, p):
    """P(Bin(n,p) >= thresh)."""
    if thresh <= 0:
        return 1.0
    if thresh > n:
        return 0.0
    return sum(binom_pmf(n, i, p) for i in range(thresh, n + 1))


def mpmf2(n, i, j, p1, p2, p3):
    """Multinomial(n; i, j, n-i-j) with probs (p1, p2, p3). 0^0 -> 1."""
    k = n - i - j
    if k < 0:
        return 0.0
    if (p1 <= 0.0 and i > 0) or (p2 <= 0.0 and j > 0) or (p3 <= 0.0 and k > 0):
        return 0.0
    t = LFACT[n] - LFACT[i] - LFACT[j] - LFACT[k]
    if i:
        t += i * math.log(p1)
    if j:
        t += j * math.log(p2)
    if k:
        t += k * math.log(p3)
    return math.exp(t) if t > -745.0 else 0.0


def hg_pmf(N, K, n, k):
    """Hypergeometric: P(draw k of K-type in n draws from N with K specials)."""
    if k < 0 or k > K or (n - k) < 0 or (n - k) > (N - K):
        return 0.0
    t = log_comb(K, k) + log_comb(N - K, n - k) - log_comb(N, n)
    return math.exp(t) if t > -745.0 else 0.0


def hg2_pmf(a, b, o, NTR, ta, tb):
    """P(training (ta,tb) | global (a,b,o), training size NTR)."""
    to = NTR - ta - tb
    oo = o
    if ta < 0 or ta > a or tb < 0 or tb > b or to < 0 or to > oo:
        return 0.0
    t = (log_comb(a, ta) + log_comb(b, tb) + log_comb(oo, to)
         - log_comb(a + b + oo, NTR))
    return math.exp(t) if t > -745.0 else 0.0


# --------------------------------------------------------------------------
# 2. Per-bucket pass probabilities f_k(n) for S0 / S1(m) / S2(m).
# --------------------------------------------------------------------------

def f_s2(k, n, m):
    """S2(m): n>=8 and >=m in each prespecified stratum."""
    if n < 8:
        return 0.0
    s = S2_STRATA[k]
    pL, pM, pH = s["p_low"], s["p_mid"], s["p_high"]
    # P(L>=m and H>=m) = 1 - P(L<m) - P(H<m) + P(both<m)
    p_l = sum(binom_pmf(n, i, pL) for i in range(0, min(m - 1, n) + 1))
    p_h = sum(binom_pmf(n, j, pH) for j in range(0, min(m - 1, n) + 1))
    both = 0.0
    for i in range(0, min(m - 1, n) + 1):
        for j in range(0, min(m - 1, n - i) + 1):
            both += mpmf2(n, i, j, pL, pH, pM)
    return max(0.0, min(1.0, 1.0 - p_l - p_h + both))


def f_s1(k, n, m):
    """S1(m): n>=8 and n - max_c >= m (all C counts <= n-m)."""
    if n < 8:
        return 0.0
    cap = n - m
    if cap < 0:
        return 0.0
    vals, probs = CK[k]
    V = len(vals)
    if n > 2 * m:
        # Exceedance events {count_v >= cap+1} are pairwise disjoint.
        tot = 0.0
        for pv in probs:
            tot += binom_upper(n, cap + 1, pv)
        return max(0.0, min(1.0, 1.0 - tot))
    # Small n (n <= 2m <= 12): brute-force enumeration over count vectors.
    return _brute_allbounded(k, n, cap)


def _brute_allbounded(k, n, cap):
    vals, probs = CK[k]
    V = len(vals)
    acc = [0.0]

    def rec(i, rem, denom_log, lp_acc):
        if i == V - 1:
            if rem <= cap:
                t = LFACT[n] - denom_log - LFACT[rem] + lp_acc
                if rem and probs[i] > 0:
                    t += rem * math.log(probs[i])
                elif rem and probs[i] <= 0:
                    return
                acc[0] += math.exp(t) if t > -745.0 else 0.0
            return
        for c in range(0, rem + 1):
            if c > cap:
                continue
            t_d = denom_log + LFACT[c]
            t_l = lp_acc
            if c:
                if probs[i] <= 0:
                    continue
                t_l += c * math.log(probs[i])
            rec(i + 1, rem - c, t_d, t_l)

    rec(0, n, 0.0, 0.0)
    return max(0.0, min(1.0, acc[0]))


def f_s0(k, n):
    """S0: n>=8, >=2 distinct C, >=4 at each OBSERVED extreme.

    Sum over ordered pairs (a,b), a<b, of P(no draws outside [a,b],
    count_a>=4, count_b>=4). Pair events are disjoint.
    """
    if n < 8:
        return 0.0
    vals, probs = CK[k]
    V = len(vals)
    total = 0.0
    for ai in range(V):
        for bi in range(ai + 1, V):
            pa, pb = probs[ai], probs[bi]
            p_mid = sum(probs[ai + 1:bi])
            p_out = 1.0 - pa - pb - p_mid
            p_in = 1.0 - p_out
            if p_in <= 0.0:
                continue
            log_pin = math.log(p_in)
            if n * log_pin <= -745.0:
                continue  # 0-dagger: log-space underflow, abs err < 5e-324
            qa, qb = pa / p_in, pb / p_in
            qm = p_mid / p_in
            pa_lt = sum(binom_pmf(n, i, qa) for i in range(0, 4))
            pb_lt = sum(binom_pmf(n, j, qb) for j in range(0, 4))
            both_lt = 0.0
            for i in range(0, 4):
                for j in range(0, 4):
                    if i + j <= n:
                        both_lt += mpmf2(n, i, j, qa, qb, qm)
            cond = 1.0 - pa_lt - pb_lt + both_lt
            if cond <= 0.0:
                continue
            total += math.exp(n * log_pin) * cond
    return max(0.0, min(1.0, total))


def f_s0_nomin(k, n):
    """S0 conditions 3-4 WITHOUT the B_min>=8 conjunct (redundancy check)."""
    if n < 2:
        return 0.0
    # Same pair sum, but the n>=8 gate is lifted. For n < 8 the
    # >=4-per-extreme condition already forces n>=8 whenever >=2 distinct
    # values are present, so this equals f_s0 for all n; computed directly.
    vals, probs = CK[k]
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
            qa, qb = pa / p_in, pb / p_in
            qm = p_mid / p_in
            pa_lt = sum(binom_pmf(n, i, qa) for i in range(0, min(4, n + 1)))
            pb_lt = sum(binom_pmf(n, j, qb) for j in range(0, min(4, n + 1)))
            both_lt = 0.0
            for i in range(0, min(4, n + 1)):
                for j in range(0, min(4, n - i + 1)):
                    both_lt += mpmf2(n, i, j, qa, qb, qm)
            cond = 1.0 - pa_lt - pb_lt + both_lt
            if cond <= 0.0:
                continue
            total += math.exp(n * log_pin) * cond
    return max(0.0, min(1.0, total))


def f_s2_nomin(k, n, m):
    """S2(m) stratum part WITHOUT the B_min>=8 conjunct."""
    s = S2_STRATA[k]
    pL, pM, pH = s["p_low"], s["p_mid"], s["p_high"]
    p_l = sum(binom_pmf(n, i, pL) for i in range(0, min(m - 1, n) + 1))
    p_h = sum(binom_pmf(n, j, pH) for j in range(0, min(m - 1, n) + 1))
    both = 0.0
    for i in range(0, min(m - 1, n) + 1):
        for j in range(0, min(m - 1, n - i) + 1):
            both += mpmf2(n, i, j, pL, pH, pM)
    return max(0.0, min(1.0, 1.0 - p_l - p_h + both))


# --------------------------------------------------------------------------
# 3. Brute-force validators (small n, explicit count-vector enumeration).
# --------------------------------------------------------------------------

def brute_probs(k, n):
    """Exact pass probs by enumerating all C-count vectors.

    Returns dict with s0, s1_{m}, s2_{m} for m in (2,4,6).
    """
    vals, probs = CK[k]
    V = len(vals)
    s = S2_STRATA[k]
    # map value index -> stratum (0=low,1=mid,2=high)
    zmap = []
    for v in vals:
        z = (v - s["cmin"]) / (s["cmax"] - s["cmin"])
        zmap.append(0 if z <= 1.0 / 3.0 + 1e-12 else (2 if z >= 2.0 / 3.0 - 1e-12 else 1))
    out = {"s0": 0.0, "s1": {2: 0.0, 4: 0.0, 6: 0.0}, "s2": {2: 0.0, 4: 0.0, 6: 0.0}}

    def emit(counts, pmf):
        # S0
        if n >= 8:
            obs = [i for i, c in enumerate(counts) if c > 0]
            if len(obs) >= 2 and counts[obs[0]] >= 4 and counts[obs[-1]] >= 4:
                out["s0"] += pmf
        # S1 / S2
        for m in (2, 4, 6):
            if n >= 8 and n - max(counts) >= m:
                out["s1"][m] += pmf
            if n >= 8:
                lo = sum(c for c, z in zip(counts, zmap) if z == 0)
                hi = sum(c for c, z in zip(counts, zmap) if z == 2)
                if lo >= m and hi >= m:
                    out["s2"][m] += pmf

    def rec(i, rem, denom_log, lp_acc):
        if i == V - 1:
            t = LFACT[n] - denom_log - LFACT[rem] + lp_acc
            if rem:
                if probs[i] <= 0:
                    return
                t += rem * math.log(probs[i])
            pmf = math.exp(t) if t > -745.0 else 0.0
            # reconstruct counts
            counts_holder.append(rem)
            emit(list(counts_holder), pmf)
            counts_holder.pop()
            return
        for c in range(0, rem + 1):
            if probs[i] <= 0 and c > 0:
                continue
            counts_holder.append(c)
            t_d = denom_log + LFACT[c]
            t_l = lp_acc + (c * math.log(probs[i]) if c else 0.0)
            rec(i + 1, rem - c, t_d, t_l)
            counts_holder.pop()

    counts_holder = []
    rec(0, n, 0.0, 0.0)
    return out


# --------------------------------------------------------------------------
# 4. Scenarios (body-level k categorical; C|k as above).
# --------------------------------------------------------------------------

SCEN = {
    "a-hist": {0: 0.80, 5: 0.10, 10: 0.05, 25: 0.05},
    "a-50:50": {0: 0.80, 5: 0.075, 10: 0.075, 25: 0.05},
    "b-hist": {0: 0.75, 5: 0.075, 10: 0.025, 20: 0.025, 25: 0.125},
    "b-thirds": {0: 0.75, 5: 0.125 / 3, 10: 0.125 / 3, 20: 0.125 / 3, 25: 0.125},
    "c-hist": {0: 0.94, 5: 0.03, 10: 0.02, 25: 0.01},
    "c-50:50": {0: 0.94, 5: 0.025, 10: 0.025, 25: 0.01},
    "d": {0: 0.90, 25: 0.10},
}
INRANGE = {"a-hist": (5, 10), "a-50:50": (5, 10), "b-hist": (5, 10, 20),
           "b-thirds": (5, 10, 20), "c-hist": (5, 10), "c-50:50": (5, 10),
           "d": ()}

RULES = ["S0", "S1-m2", "S1-m4", "S1-m6", "S2-m2", "S2-m4", "S2-m6"]

FTABLE = {}  # (rule, k) -> list length NMAX+1


def build_ftables():
    for k in (5, 10, 20):
        FTABLE[("S0", k)] = [f_s0(k, n) for n in range(NMAX + 1)]
        for m in (2, 4, 6):
            FTABLE[(f"S1-m{m}", k)] = [f_s1(k, n, m) for n in range(NMAX + 1)]
            FTABLE[(f"S2-m{m}", k)] = [f_s2(k, n, m) for n in range(NMAX + 1)]


def global2(N, p5, p10, f5, f10, n_lo=8):
    """P(both buckets pass) for 2-bucket scenarios. Exact double sum.

    n_lo is the per-bucket count floor baked into the summation range;
    it MUST match the B_min conjunct inside f5/f10 (default 8). Pass
    n_lo=0 when comparing against B_min-free per-bucket functions.
    """
    if p5 <= 0 or p10 <= 0:
        return 0.0
    pO = 1.0 - p5 - p10
    if pO < 0:
        return 0.0
    lp5, lp10 = math.log(p5), math.log(p10)
    lpO = math.log(pO) if pO > 0 else 0.0
    tot = 0.0
    for n5 in range(n_lo, N + 1):
        a5 = f5[n5]
        if a5 <= 0.0:
            continue
        base5 = LFACT[N] - LFACT[n5] + n5 * lp5
        for n10 in range(n_lo, N - n5 + 1):
            a10 = f10[n10]
            if a10 <= 0.0:
                continue
            nO = N - n5 - n10
            if pO <= 0.0 and nO > 0:
                continue
            t = base5 - LFACT[n10] - LFACT[nO] + n10 * lp10
            if nO and pO > 0:
                t += nO * lpO
            if t <= -745.0:
                continue
            tot += math.exp(t) * a5 * a10
    return tot


def global3_full(N, probs, ftabs):
    """P(>=2 of 3 buckets pass). Exact triple sum (N <= ~200)."""
    (p5, p10, p20) = probs
    (f5, f10, f20) = ftabs
    pO = 1.0 - p5 - p10 - p20
    lp5, lp10, lp20 = math.log(p5), math.log(p10), math.log(p20)
    lpO = math.log(pO) if pO > 0 else 0.0
    tot = 0.0
    for n5 in range(0, N + 1):
        a5 = f5[n5]
        for n10 in range(0, N - n5 + 1):
            a10 = f10[n10]
            rem = N - n5 - n10
            base = (LFACT[N] - LFACT[n5] - LFACT[n10]
                    + n5 * lp5 + n10 * lp10)
            for n20 in range(0, rem + 1):
                a20 = f20[n20]
                # P(>=2 pass | counts) via conditional independence
                q5, q10, q20 = a5, a10, a20
                pat = (q5 * q10 * (1 - q20) + q5 * (1 - q10) * q20
                       + (1 - q5) * q10 * q20 + q5 * q10 * q20)
                if pat <= 0.0:
                    continue
                nO = rem - n20
                if pO <= 0.0 and nO > 0:
                    continue
                t = base - LFACT[n20] - LFACT[nO] + n20 * lp20
                if nO and pO > 0:
                    t += nO * lpO
                if t <= -745.0:
                    continue
                tot += math.exp(t) * pat
    return tot


def global3_box(N, probs, ftabs, tail=1e-15):
    """P(>=2 of 3 pass) over a truncated box with union-bound omission.

    Returns (prob, omitted_bound). Box per bucket: smallest interval with
    marginal Binomial(N,p) outside-mass <= tail.
    """
    (p5, p10, p20) = probs
    (f5, f10, f20) = ftabs
    pO = 1.0 - p5 - p10 - p20
    lp5, lp10, lp20 = math.log(p5), math.log(p10), math.log(p20)
    lpO = math.log(pO) if pO > 0 else 0.0

    def bounds(p):
        # increasing lo until left tail <= tail; decreasing hi likewise
        lo, hi = 0, N
        s = 0.0
        for i in range(0, N + 1):
            s += binom_pmf(N, i, p)
            if s > tail:
                lo = i
                break
        s = 0.0
        for i in range(N, -1, -1):
            s += binom_pmf(N, i, p)
            if s > tail:
                hi = i
                break
        return lo, hi

    lo5, hi5 = bounds(p5)
    lo10, hi10 = bounds(p10)
    lo20, hi20 = bounds(p20)
    tot = 0.0
    for n5 in range(lo5, hi5 + 1):
        a5 = f5[n5]
        for n10 in range(lo10, hi10 + 1):
            if n5 + n10 > N:
                continue
            a10 = f10[n10]
            base = (LFACT[N] - LFACT[n5] - LFACT[n10]
                    + n5 * lp5 + n10 * lp10)
            for n20 in range(lo20, hi20 + 1):
                if n5 + n10 + n20 > N:
                    continue
                a20 = f20[n20]
                q5, q10, q20 = a5, a10, a20
                pat = (q5 * q10 * (1 - q20) + q5 * (1 - q10) * q20
                       + (1 - q5) * q10 * q20 + q5 * q10 * q20)
                if pat <= 0.0:
                    continue
                nO = N - n5 - n10 - n20
                t = base - LFACT[n20] - LFACT[nO] + n20 * lp20
                if nO and pO > 0:
                    t += nO * lpO
                if t <= -745.0:
                    continue
                tot += math.exp(t) * pat
    return tot, 3.0 * tail


def bucket_marginals(N, p, f):
    """P(bucket passes) and E[n*I] (bucket-marginal, no G conjunct)."""
    if p <= 0:
        return 0.0, 0.0
    lp = math.log(p)
    lq = math.log1p(-p)
    P, E = 0.0, 0.0
    for n in range(0, N + 1):
        a = f[n]
        if a <= 0.0:
            continue
        pmf = math.exp(log_comb(N, n) + n * lp + (N - n) * lq)
        P += pmf * a
        E += pmf * a * n
    return P, E


# --------------------------------------------------------------------------
# 5. Fixed-size split: marginals are fresh-sample globals; joint uses the
#    exact hypergeometric subset logic (R-a global-membership, count-based
#    train/test criteria). h-tables are scenario- and rule-independent.
# --------------------------------------------------------------------------

def split_sizes(N):
    T = (N + 2) // 4  # round-half-up(0.25*N)
    return N - T, T


def _hg_ratio(a, b, o, NTR, ta, tb):
    N = a + b + o
    to = NTR - ta - tb
    if ta < 0 or ta > a or tb < 0 or tb > b or to < 0 or to > o:
        return 0.0
    t = (log_comb(a, ta) + log_comb(b, tb) + log_comb(o, to)
         - log_comb(N, NTR))
    return math.exp(t) if t > -745.0 else 0.0


def h_joint_lib(a, b, o, NTR):
    """P(TrainRa and TestLib1 | global counts (a,b,o)).

    TrainRa: tra>=1, trb>=1, tra+trb>=8.
    TestLib1: tea>=1, teb>=1  (tea = a-tra).
    Exact inclusion-exclusion over the 5 failure atoms.
    Requires a,b >= 8 in every contributing call (guaranteed: f=0 else).
    """
    N = a + b + o
    if a < 8 or b < 8:
        return 0.0
    # single-state helper
    single = lambda ta, tb: _hg_ratio(a, b, o, NTR, ta, tb)

    def margA0():  # P(tra=0)
        t = log_comb(N - a, NTR) - log_comb(N, NTR)
        return math.exp(t) if t > -745.0 else 0.0

    def margB0():
        t = log_comb(N - b, NTR) - log_comb(N, NTR)
        return math.exp(t) if t > -745.0 else 0.0

    def margAfull():  # P(tra=a)
        if NTR < a:
            return 0.0
        t = log_comb(N - a, NTR - a) - log_comb(N, NTR)
        return math.exp(t) if t > -745.0 else 0.0

    def margBfull():
        if NTR < b:
            return 0.0
        t = log_comb(N - b, NTR - b) - log_comb(N, NTR)
        return math.exp(t) if t > -745.0 else 0.0

    def sum_le7():  # P(tra+trb<=7)
        s = 0.0
        for ta in range(0, min(7, a, NTR) + 1):
            for tb in range(0, min(7 - ta, b, NTR - ta) + 1):
                s += single(ta, tb)
        return s

    def sum_A0_le7():  # P(tra=0, trb<=7)
        s = 0.0
        for tb in range(0, min(7, b, NTR) + 1):
            s += single(0, tb)
        return s

    def sum_B0_le7():  # P(trb=0, tra<=7)
        s = 0.0
        for ta in range(0, min(7, a, NTR) + 1):
            s += single(ta, 0)
        return s

    # Atoms: F1={tra=0}, F2={trb=0}, F3={sum<=7}, G1={tra=a}, G2={trb=b}.
    # Union via inclusion-exclusion; empty intersections skipped
    # (F1&G1, F2&G2, F3&G1, F3&G2 and supersets are empty since a,b>=8).
    p1, p2, p3 = margA0(), margB0(), sum_le7()
    g1, g2 = margAfull(), margBfull()
    # pairs
    p12 = single(0, 0)
    p1g2 = single(0, b)
    p2g1 = single(a, 0)
    g12 = single(a, b) if NTR >= a + b else 0.0
    p13 = sum_A0_le7()
    p23 = sum_B0_le7()
    # F3 with G1/G2: empty. F1&G1, F2&G2: empty.
    # triples among {F1,F2,G1,G2} (no F3): every one contains an opposed
    # pair (F1&G1 or F2&G2), hence all are structural zeros.
    # Triples with F3: only F1&F2&F3 = {(0,0)} is non-empty (t123 below);
    # F1&F3&G2 needs trb=b>=8 with sum<=7 (empty), and symmetrically the
    # rest are empty. All quadruples/quintuples are empty for the same reason.
    t123 = single(0, 0)           # F1&F2&F3 = {(0,0)} (in F3)
    # F1&F3&G2 = {tra=0,trb=b,sum<=7} -> b>=8 -> empty. Similarly others empty.
    # quadruples: all contain an opposed pair or F3&G -> empty, except none.
    union = (p1 + p2 + p3 + g1 + g2
             - p12 - p1g2 - p2g1 - g12 - p13 - p23
             + t123)
    # NOTE: pairs F1&G1, F2&G2, F3&G1, F3&G2 and triples/quadruples
    # containing them are structural zeros (a,b>=8) and contribute 0.
    return max(0.0, min(1.0, 1.0 - union))


def h_joint_cons(a, b, o, NTR):
    """P(TrainRa and TestCons8 | global counts).

    TrainRa as above; TestCons8: tea>=8, teb>=8 (test re-applies count rule).
    Structural support (UNION=0.0 returned EXACTLY outside it): the success
    event is {1<=tra<=a-8, 1<=trb<=b-8, tra+trb>=8} in training plus
    {tea>=8, teb>=8} in testing (T = N-NTR), which is non-empty iff
      a>=9, b>=9, a+b>=24, NTR>=8, T>=16.
    Outside it every draw lies in a failure atom, so the union is exactly 1
    and h is exactly 0 (do not rely on the IE union evaluating to 1 only up
    to round-off: an earlier revision left spurious positive residues of
    order 1e-12 on impossible states).

    Failure atoms: F1={tra=0}, F2={trb=0}, F3={tra+trb<=7},
    Q1={tea<=7}={tra>=a-7}, Q2={teb<=7}={trb>=b-7}. Exact inclusion-exclusion
    over the 5 atoms; empty intersections are skipped, with the exact
    emptiness conditions (a,b>=8 throughout):
      F1&Q1, F2&Q2: empty (opposed constraints).
      F3&Q1: empty iff a>=15 (needs tra in [a-7, 7]); F3&Q2 iff b>=15.
      F1&F3&Q2: empty iff b>=15; F2&F3&Q1: empty iff a>=15.
      F3&Q1&Q2: empty iff a+b>=22.
      Every quadruple/quintuple contains F1&Q1 or F2&Q2: empty.
    Requires a,b >= 8 in every contributing call (guaranteed: f=0 else).
    """
    N = a + b + o
    if a < 9 or b < 9 or a + b < 24 or NTR < 8 or (N - NTR) < 16:
        return 0.0
    single = lambda ta, tb: _hg_ratio(a, b, o, NTR, ta, tb)

    def margA0():
        t = log_comb(N - a, NTR) - log_comb(N, NTR)
        return math.exp(t) if t > -745.0 else 0.0

    def margB0():
        t = log_comb(N - b, NTR) - log_comb(N, NTR)
        return math.exp(t) if t > -745.0 else 0.0

    def sum_le7():
        s = 0.0
        for ta in range(0, min(7, a, NTR) + 1):
            for tb in range(0, min(7 - ta, b, NTR - ta) + 1):
                s += single(ta, tb)
        return s

    def sum_A0_le7():
        return sum(single(0, tb) for tb in range(0, min(7, b, NTR) + 1))

    def sum_B0_le7():
        return sum(single(ta, 0) for ta in range(0, min(7, a, NTR) + 1))

    def tailA():  # P(tea<=7) = P(tra>=a-7)
        s = 0.0
        for ta in range(max(0, a - 7), min(a, NTR) + 1):
            # trb free -> marginal over trb: sum_{tb} HG = C(a,ta)C(N-a,NTR-ta)/C(N,NTR)
            t = log_comb(a, ta) + log_comb(N - a, NTR - ta) - log_comb(N, NTR)
            if t > -745.0:
                s += math.exp(t)
        return s

    def tailB():
        s = 0.0
        for tb in range(max(0, b - 7), min(b, NTR) + 1):
            t = log_comb(b, tb) + log_comb(N - b, NTR - tb) - log_comb(N, NTR)
            if t > -745.0:
                s += math.exp(t)
        return s

    def pair_A0_tailB():  # {tra=0} & {teb<=7} = {tra=0, trb>=b-7}
        s = 0.0
        for tb in range(max(0, b - 7), min(b, NTR) + 1):
            s += single(0, tb)
        return s

    def pair_B0_tailA():
        s = 0.0
        for ta in range(max(0, a - 7), min(a, NTR) + 1):
            s += single(ta, 0)
        return s

    def pair_tailA_tailB():  # {tra>=a-7} & {trb>=b-7}
        s = 0.0
        for ta in range(max(0, a - 7), min(a, NTR) + 1):
            for tb in range(max(0, b - 7), min(b, NTR - ta) + 1):
                s += single(ta, tb)
        return s

    def pair_A0_B0():
        return single(0, 0)

    p1, p2, p3 = margA0(), margB0(), sum_le7()
    q1, q2 = tailA(), tailB()
    # pairs (non-empty only)
    s12 = pair_A0_B0()
    s1q2 = pair_A0_tailB()
    s2q1 = pair_B0_tailA()
    sqq = pair_tailA_tailB()
    s13 = sum_A0_le7()
    s23 = sum_B0_le7()
    # F1&tailA = {tra=0, tra>=a-7} -> empty (a>=8). F2&tailB empty.
    # F3&tailA: {sum<=7, tra>=a-7} -> empty iff a>=15 (needs tra in
    # [a-7, 7]); non-empty for 8 <= a <= 14. Symmetrically F3&tailB.
    # (An earlier version treated both as always empty, which overstated
    # the union and clamped small h to 0; caught by the exact-enumeration
    # regression in run_a1.py section 5b, counterexample a=9, b=15,
    # o=126, NTR=112.)
    s3q1 = 0.0
    if a <= 14:
        for ta in range(max(0, a - 7), min(7, a, NTR) + 1):
            for tb in range(0, min(7 - ta, b, NTR - ta) + 1):
                s3q1 += single(ta, tb)
    s3q2 = 0.0
    if b <= 14:
        for tb in range(max(0, b - 7), min(7, b, NTR) + 1):
            for ta in range(0, min(7 - tb, a, NTR - tb) + 1):
                s3q2 += single(ta, tb)
    # triples: F1&F2&F3={(0,0)}; F1&F2&tailA, F1&F2&tailB, F1&tailA&tailB,
    # F2&tailA&tailB empty (a,b>=8). Conditional triples:
    # F1&F3&tailB = {tra=0, sum<=7, trb>=b-7} -> empty iff b>=15;
    # F2&F3&tailA = {trb=0, sum<=7, tra>=a-7} -> empty iff a>=15;
    # F3&tailA&tailB = {sum<=7, tra>=a-7, trb>=b-7} -> empty iff a+b>=22.
    t123 = single(0, 0)
    t13q2 = 0.0
    if b <= 14:
        for tb in range(max(0, b - 7), min(7, b, NTR) + 1):
            t13q2 += single(0, tb)
    t23q1 = 0.0
    if a <= 14:
        for ta in range(max(0, a - 7), min(7, a, NTR) + 1):
            t23q1 += single(ta, 0)
    t3q1q2 = 0.0
    if a + b <= 21:
        for ta in range(max(0, a - 7), min(7, a, NTR) + 1):
            for tb in range(max(0, b - 7), min(7 - ta, b, NTR - ta) + 1):
                t3q1q2 += single(ta, tb)
    # every quadruple/quintuple intersects F1&tailA or F2&tailB inside:
    # opposed constraints, structural zeros (a,b>=8).
    union = (p1 + p2 + p3 + q1 + q2
             - s12 - s1q2 - s2q1 - sqq - s13 - s23 - s3q1 - s3q2
             + t123 + t13q2 + t23q1 + t3q1q2)
    return max(0.0, min(1.0, 1.0 - union))


def joint2(N, p5, p10, f5, f10, htable):
    """P(Global and TrainRa and TestX) for 2-bucket scenarios.

    htable[(a,b)] precomputed by h_joint_*. Exact: sum over global counts
    of Mult * f5*f10 * h(a,b). h is rule- and scenario-independent.
    """
    if p5 <= 0 or p10 <= 0:
        return 0.0
    pO = 1.0 - p5 - p10
    lp5, lp10 = math.log(p5), math.log(p10)
    lpO = math.log(pO) if pO > 0 else 0.0
    tot = 0.0
    for n5 in range(8, N + 1):
        a5 = f5[n5]
        if a5 <= 0.0:
            continue
        base5 = LFACT[N] - LFACT[n5] + n5 * lp5
        for n10 in range(8, N - n5 + 1):
            a10 = f10[n10]
            if a10 <= 0.0:
                continue
            h = htable.get((n5, n10))
            if h is None or h <= 0.0:
                continue
            nO = N - n5 - n10
            if pO <= 0.0 and nO > 0:
                continue
            t = base5 - LFACT[n10] - LFACT[nO] + n10 * lp10
            if nO and pO > 0:
                t += nO * lpO
            if t <= -745.0:
                continue
            tot += math.exp(t) * a5 * a10 * h
    return tot
