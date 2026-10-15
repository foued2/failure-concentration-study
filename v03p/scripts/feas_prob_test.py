"""feas_prob_test.py (Revision B, corrected) - exact fixed-size block readings.

Exact deterministic log-space computation (stdlib only; no sampling, no simulation).

Readings of the Section 7 test/training-block support rules:
  F     reference: full-population count rule (>=2 in-range buckets >= B_MIN bodies)
  FF    reference: full-population full Section 5 rule (cond 1-4, observed extremes)
  CONS  conservative: test block re-applies the Section 5 COUNT rule itself
        (>=2 in-range buckets with >= B_MIN=8 test bodies each). The conservative
        reading with conditions 3-4 re-applied at test level is statedly OMITTED
        (it requires the joint (k, C) split distribution).
  TONL  training-block alone: train block (>=2 in-range buckets >= 8 train bodies).
  LIB   liberal: full-population rule determines support; test block must hold
        >= B_MIN supported bodies across >= 2 supported buckets (>=1 test each).
  TRN   training+test (R9): LIB additionally requires the training block to hold
        >= B_MIN supported bodies across >= 2 supported buckets.
  NOSUP no-usable-support: P(test block holds zero supported bodies); reported
        jointly and conditional on full support existing.
Each of LIB/TRN/NOSUP is computed twice: "c" with support = count rule,
"f" with support = full Section 5 rule (random pass pattern via g_k).

Split (exact, fixed size): test = uniform random subset of T body identities,
T = floor(0.25*N + 0.5) (round-half-up convention, stated). Given full in-range
counts, test counts in supported buckets are multivariate hypergeometric
(test and train multinomials are exactly independent; no binomial thinning).
Train-block-alone readings use train ~ Mult(N-T, p) exactly.

Omissions (stated): conditions 3-4 not re-applied at block level (CONS fuller);
rho/validity not modeled; terms below CUT dropped (omitted mass < 1e-13);
structural zeros 0*; log-space underflow 0-dagger.
"""

import math
import sys

B_MIN = 8
CUT = -46.0
N_GRID = [60, 113, 120, 150, 240, 300, 400, 450, 600]

SCENARIOS = {
    "a": ({0: 0.80, 5: 0.10, 10: 0.05, 25: 0.05}, [5, 10]),
    "b": ({0: 0.75, 5: 0.075, 10: 0.025, 20: 0.025, 25: 0.125}, [5, 10, 20]),
    "c": ({0: 0.94, 5: 0.03, 10: 0.02, 25: 0.01}, [5, 10]),
    "d": ({0: 0.90, 25: 0.10}, []),
}
O4 = {
    "a50": ({0: 0.80, 5: 0.075, 10: 0.075, 25: 0.05}, [5, 10]),
    "b3": ({0: 0.75, 5: 0.125 / 3, 10: 0.125 / 3, 20: 0.125 / 3, 25: 0.125}, [5, 10, 20]),
    "c50": ({0: 0.94, 5: 0.025, 10: 0.025, 25: 0.01}, [5, 10]),
}

LC = []


def build_lc(nmax):
    global LC
    LC = [float("-inf")] * (nmax + 2)
    for i in range(1, nmax + 2):
        LC[i] = math.lgamma(i)


def logcomb(n, r):
    if r < 0 or r > n:
        return float("-inf")
    return LC[n + 1] - LC[r + 1] - LC[n - r + 1]


def exp_lse(logs):
    if not logs:
        return 0.0
    m = max(logs)
    if m <= -745.0:
        return 0.0
    tot = 0.0
    for v in logs:
        tot += math.exp(v - m)
    return math.exp(m) * tot


def p_at_least_two(gs):
    rest = [1.0 - g for g in gs]
    p0 = 1.0
    for x in rest:
        p0 *= x
    p1 = 0.0
    for j, g in enumerate(gs):
        if g == 0.0:
            continue
        t = g
        for i, x in enumerate(rest):
            if i != j:
                t *= x
        p1 += t
    return 1.0 - p0 - p1


def iter2(m):
    for t in range(m + 1):
        yield (t, m - t)


def iter3(m):
    for t in range(m + 1):
        r = m - t
        for u in range(r + 1):
            yield (t, u, r - u)


def c_dist(k):
    from collections import Counter
    counts = Counter()
    total = [0]

    def rec(idx, rem, mx):
        if idx == 6:
            if rem == 0:
                counts[mx] += 1
                total[0] += 1
            return
        hi = 5 if rem > 5 else rem
        for f in range(hi + 1):
            rec(idx + 1, rem - f, mx if mx > f else f)

    rec(0, k, 0)
    items = sorted(counts.items())
    return [(c, n / total[0]) for c, n in items], total[0]


def tail3(m, rho):
    if rho >= 1.0:
        return 1.0 if m <= 3 else 0.0
    if m < 0:
        return 1.0
    tot = 0.0
    om = 1.0 - rho
    for b in range(min(3, m) + 1):
        tot += math.comb(m, b) * (rho ** b) * (om ** (m - b))
    return tot


_GFULL = {}


def g_full(k, nmax):
    if k in _GFULL:
        return _GFULL[k]
    dist, _ = c_dist(k)
    probs = [p for _, p in dist]
    s = len(probs)
    g = [0.0] * (nmax + 1)
    if s >= 2:
        lp = [math.log(p) for p in probs]
        for i in range(s):
            pi = probs[i]
            for j in range(i + 1, s):
                pj = probs[j]
                between = 0.0
                for l in range(i + 1, j):
                    between += probs[l]
                denom = pj + between
                rho = pj / denom
                t3 = [tail3(mm, rho) for mm in range(nmax + 1)]
                lpi = lp[i]
                lden = math.log(denom)
                pid = pi / denom
                for n in range(B_MIN, nmax + 1):
                    lw = LC[n + 1] - LC[5] - LC[n - 3] + 4.0 * lpi + (n - 4) * lden
                    w = math.exp(lw) if lw > -745.0 else 0.0
                    acc = w * (1.0 - t3[n - 4])
                    a = 5
                    while a <= n:
                        w *= (n - a + 1) / a * pid
                        acc += w * (1.0 - t3[n - a])
                        a += 1
                    g[n] += acc
    _GFULL[k] = g
    return g


def pass_prob(n, masses, inrange, gfun):
    M = 0.0
    for k in inrange:
        M += masses[k]
    if M <= 0.0 or len(inrange) < 2:
        return 0.0
    lcond = {}
    for k in inrange:
        lcond[k] = math.log(masses[k] / M)
    logM = math.log(M)
    log1m = math.log1p(-M)
    use3 = len(inrange) == 3
    acc = []
    for m in range(n + 1):
        logpm = LC[n + 1] - LC[m + 1] - LC[n - m + 1] + m * logM + (n - m) * log1m
        if logpm < CUT:
            continue
        vecs = iter3(m) if use3 else iter2(m)
        for vec in vecs:
            ok = 0
            for v in vec:
                if v >= B_MIN:
                    ok += 1
                    if ok >= 2:
                        break
            if ok < 2:
                continue
            logmult = LC[m + 1]
            for v in vec:
                logmult -= LC[v + 1]
            for i, k in enumerate(inrange):
                if vec[i]:
                    logmult += vec[i] * lcond[k]
            lt = logpm + logmult
            if lt < CUT:
                continue
            gs = [gfun[inrange[i]][vec[i]] for i in range(len(vec))]
            p = p_at_least_two(gs)
            if p > 0.0:
                acc.append(lt + math.log(p))
    return exp_lse(acc)


def test_size(n):
    return int(math.floor(0.25 * n + 0.5))


def readings(n, masses, inrange, gc, gf):
    M = 0.0
    for k in inrange:
        M += masses[k]
    if M <= 0.0 or len(inrange) < 2:
        return {"struct": True}
    T = test_size(n)
    lcond = {}
    for k in inrange:
        lcond[k] = math.log(masses[k] / M)
    logM = math.log(M)
    log1m = math.log1p(-M)
    use3 = len(inrange) == 3
    K = len(inrange)
    lcN = logcomb(n, T)
    hyp = {}
    HT = {}
    HTmid = {}
    HZ = {}
    for mS in range(n + 1):
        hi = mS if mS < T else T
        row = [0.0] * (hi + 1)
        for t in range(hi + 1):
            lr = logcomb(mS, t) + logcomb(n - mS, T - t) - lcN
            if lr > -745.0:
                row[t] = math.exp(lr)
        hyp[mS] = row
        s8 = 0.0
        sm = 0.0
        for t in range(8, hi + 1):
            s8 += row[t]
            if t <= mS - 8:
                sm += row[t]
        HT[mS] = s8
        HTmid[mS] = sm
        HZ[mS] = row[0]
    fL = {}
    fTl = {}
    fTu = {}

    def get_fL(mS, b):
        key = (mS, b)
        v = fL.get(key)
        if v is None:
            v = 0.0
            row = hyp[mS]
            hi = b if b < len(row) else len(row) - 1
            for t in range(8, hi + 1):
                lr = logcomb(b, t) - logcomb(mS, t)
                if lr > -745.0:
                    v += row[t] * math.exp(lr)
            fL[key] = v
        return v

    def get_fTl(mS, b):
        key = (mS, b)
        v = fTl.get(key)
        if v is None:
            v = 0.0
            row = hyp[mS]
            hi = b if b < len(row) else len(row) - 1
            hi = hi if hi < mS - 7 else mS - 8
            for t in range(8, hi + 1):
                lr = logcomb(b, t) - logcomb(mS, t)
                if lr > -745.0:
                    v += row[t] * math.exp(lr)
            fTl[key] = v
        return v

    def get_fTu(mS, b):
        key = (mS, b)
        v = fTu.get(key)
        if v is None:
            v = 0.0
            row = hyp[mS]
            lo = 8 if 8 > mS - b else mS - b
            hi = mS - 8 if mS - 8 < len(row) - 1 else len(row) - 1
            for t in range(lo, hi + 1):
                d = t - (mS - b)
                if d < 0 or d > b:
                    continue
                lr = logcomb(b, d) - logcomb(mS, t)
                if lr > -745.0:
                    v += row[t] * math.exp(lr)
            fTu[key] = v
        return v

    def inner_L(mS, ns):
        if mS <= 0:
            return 0.0
        v = HT[mS]
        for b in ns:
            v -= get_fL(mS, b)
        return v if v > 0.0 else 0.0

    def inner_T(mS, ns):
        s = len(ns)
        if s < 2 or mS < 16:
            return 0.0
        v = HTmid[mS]
        for b in ns:
            v -= get_fTl(mS, b)
            v -= get_fTu(mS, b)
        if s == 2:
            v += math.exp(logcomb(n - mS, T - ns[0]) - lcN)
            v += math.exp(logcomb(n - mS, T - ns[1]) - lcN)
        return v if v > 0.0 else 0.0

    acc = {k: [] for k in ("lib_c", "trn_c", "nos", "nosF", "lib_f", "trn_f", "nosf", "nosFf")}
    for m in range(n + 1):
        logpm = LC[n + 1] - LC[m + 1] - LC[n - m + 1] + m * logM + (n - m) * log1m
        if logpm < CUT:
            continue
        vecs = iter3(m) if use3 else iter2(m)
        for vec in vecs:
            logmult = LC[m + 1]
            for v in vec:
                logmult -= LC[v + 1]
            for i, k in enumerate(inrange):
                if vec[i]:
                    logmult += vec[i] * lcond[k]
            lt = logpm + logmult
            if lt < CUT:
                continue
            dmap = dict(zip(inrange, vec))
            ns_c = [dmap[k] for k in inrange if dmap[k] >= B_MIN]
            mS = sum(ns_c)
            F = len(ns_c) >= 2
            if ns_c:
                il = inner_L(mS, ns_c)
                if il > 0.0:
                    acc["lib_c"].append(lt + math.log(il))
                it = inner_T(mS, ns_c)
                if it > 0.0:
                    acc["trn_c"].append(lt + math.log(it))
                z = HZ[mS]
                if z > 0.0:
                    acc["nos"].append(lt + math.log(z))
                    if F:
                        acc["nosF"].append(lt + math.log(z))
            else:
                acc["nos"].append(lt)
            gf_v = [gf[k][dmap[k]] for k in inrange]
            for mask in range(1 << K):
                pr = 1.0
                for i, g in enumerate(gf_v):
                    if (mask >> i) & 1:
                        pr *= g
                    else:
                        pr *= 1.0 - g
                if pr <= 0.0:
                    continue
                S = [inrange[i] for i in range(K) if (mask >> i) & 1]
                ns_f = [dmap[k] for k in S]
                mSf = sum(ns_f)
                if ns_f:
                    il = inner_L(mSf, ns_f)
                    if il > 0.0:
                        acc["lib_f"].append(lt + math.log(pr * il))
                    it = inner_T(mSf, ns_f)
                    if it > 0.0:
                        acc["trn_f"].append(lt + math.log(pr * it))
                    z = HZ[mSf]
                    if z > 0.0:
                        acc["nosf"].append(lt + math.log(pr * z))
                        if len(S) >= 2:
                            acc["nosFf"].append(lt + math.log(pr * z))
                else:
                    acc["nosf"].append(lt + math.log(pr))
    out = {"struct": False, "T": T}
    out["cons"] = pass_prob(T, masses, inrange, gc)
    U = n - T
    out["tonl_c"] = pass_prob(U, masses, inrange, gc)
    out["tonl_f"] = pass_prob(U, masses, inrange, gf)
    out["fc"] = pass_prob(n, masses, inrange, gc)
    out["ff"] = pass_prob(n, masses, inrange, gf)
    out["lib_c"] = exp_lse(acc["lib_c"])
    out["trn_c"] = exp_lse(acc["trn_c"])
    out["nos"] = exp_lse(acc["nos"])
    out["nosF"] = exp_lse(acc["nosF"])
    out["lib_f"] = exp_lse(acc["lib_f"])
    out["trn_f"] = exp_lse(acc["trn_f"])
    out["nosf"] = exp_lse(acc["nosf"])
    out["nosFf"] = exp_lse(acc["nosFf"])
    return out


def fmt(x, struct):
    if struct:
        return "0*"
    if x <= 0.0:
        return "0-dag"
    if x < 1e-4:
        return "%.2e" % x
    return "%.6f" % x


def main():
    build_lc(max(N_GRID))
    nmax = max(N_GRID)
    gc = {}
    gf = {}
    for k in (5, 10, 20):
        gc[k] = [1.0 if i >= B_MIN else 0.0 for i in range(nmax + 1)]
        gf[k] = g_full(k, nmax)
    print("feas_prob_test.py (Revision B corrected) - exact fixed-size block readings")
    print("T = floor(0.25*N + 0.5) round-half-up; term cutoff exp(%g)" % CUT)
    print()
    cells = {}
    print("Count-only readings: N, T, F_cnt, CONS, TONL_c, LIB_c, TRN_c, P(F fails), NOSUP|F_c")
    for s in ("a", "b", "c", "d"):
        masses, ir = SCENARIOS[s]
        for n in N_GRID:
            r = readings(n, masses, ir, gc, gf)
            cells[(s, n)] = r
            if r["struct"]:
                print("%-4s N=%-4d STRUCTURAL-ZERO" % (s, n))
                continue
            ffail = 1.0 - r["fc"]
            cond = (r["nosF"] / r["fc"]) if r["fc"] > 0 else 0.0
            print("%-4s N=%-4d T=%-4d F=%s CONS=%s TONL=%s LIB=%s TRN=%s P(Ffail)=%s NOS|F=%s" % (
                s, n, r["T"], fmt(r["fc"], False), fmt(r["cons"], False),
                fmt(r["tonl_c"], False), fmt(r["lib_c"], False), fmt(r["trn_c"], False),
                fmt(ffail, False), fmt(cond, False)))
    print()
    print("Fuller readings: N, T, F_ful, TONL_f, LIB_f, TRN_f, NOSUP|F_f")
    for s in ("a", "b", "c"):
        masses, ir = SCENARIOS[s]
        for n in N_GRID:
            r = cells[(s, n)]
            cond = (r["nosFf"] / r["ff"]) if r["ff"] > 0 else 0.0
            print("%-4s N=%-4d T=%-4d F=%s TONL=%s LIB=%s TRN=%s NOS|F=%s" % (
                s, n, r["T"], fmt(r["ff"], False), fmt(r["tonl_f"], False),
                fmt(r["lib_f"], False), fmt(r["trn_f"], False), fmt(cond, False)))
    print()
    print("O4 sensitivity at budget-mapped points (count CONS/LIB/TRN | fuller LIB/TRN):")
    for s in ("a50", "b3", "c50"):
        masses, ir = O4[s]
        for n in (113, 150, 450, 600):
            r = readings(n, masses, ir, gc, gf)
            print("%-4s N=%-4d T=%-4d F_c=%s CONS=%s LIB_c=%s TRN_c=%s F_f=%s LIB_f=%s TRN_f=%s" % (
                s, n, r["T"], fmt(r["fc"], False), fmt(r["cons"], False),
                fmt(r["lib_c"], False), fmt(r["trn_c"], False), fmt(r["ff"], False),
                fmt(r["lib_f"], False), fmt(r["trn_f"], False)))
    print()
    print("Monotonicity / subset checks (TRN vs TONL omitted: incomparable events -")
    print("TRN's train conjunct counts train bodies in fully-supported buckets,")
    print("TONL counts train buckets with >= 8 train bodies each):")
    ok = [True]

    def chk(name, a, b):
        good = a + 1e-12 >= b
        if not good:
            ok[0] = False
        print("  %s: %.6g >= %.6g %s" % (name, a, b, "OK" if good else "VIOLATION"))

    for key, r in cells.items():
        if r["struct"]:
            continue
        chk("%s CONS<=F" % str(key), r["fc"], r["cons"])
        chk("%s LIB_c<=F" % str(key), r["fc"], r["lib_c"])
        chk("%s TRN_c<=LIB_c" % str(key), r["lib_c"], r["trn_c"])
        chk("%s F_f<=F_c" % str(key), r["fc"], r["ff"])
        chk("%s LIB_f<=F_f" % str(key), r["ff"], r["lib_f"])
        chk("%s TRN_f<=LIB_f" % str(key), r["lib_f"], r["trn_f"])
    print("CHECKS:", "ALL-OK" if ok[0] else "REVIEW-NEEDED")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
