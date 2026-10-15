"""feas_prob.py (Revision B, corrected) - exact full-population feasibility arithmetic.

Exact deterministic log-space computation (stdlib only; no sampling, no simulation).

For each candidate Section 9.1 scenario, with N unique valid bodies:
 (1) count-only bound: P(at least two in-range k-buckets each hold >= B_MIN bodies).
     The event is "at least two of" (three-bucket case: any two may satisfy it;
     the prior three-bucket branch requiring all three is superseded).
 (2) fuller gate: P(at least two in-range k-buckets pass the full Section 5
     rule, conditions 1-4, observed-extremes reading), exact under the
     conditioned Dirichlet-multinomial C law (uniform over feasible
     compositions; cross-checked against dgp_counts_v2.py below).
 (3) expected body counts: in-range, count-rule support, full-rule support.

Method: m ~ Bin(N, M) in-range count; given m, bucket counts ~ Mult(m, cond);
bucket pass events are conditionally independent given counts and use the
indicator (count-only) or the exact g_k(n) (fuller) pass probabilities.
g_k(n) sums, over each candidate observed-extreme pair (i, j), the exact
probability that the bucket minimum is c_i with >= 4 bodies, the maximum is
c_j with >= 4 bodies, and every other body lies strictly between them.

Omissions (stated, not hidden): the duplicate mechanism (rho) and the validity
rate are not modeled; N denotes unique valid bodies (budget mapping printed
below). Test/train-block readings are in feas_prob_test.py. Summation terms
with log-weight below CUT are dropped; omitted mass is bounded by 1e-13.
Structural zeros print as 0*; log-space underflow prints as 0-dagger.

N grid: 60 and 120 (current Section 9 grid points); 113 and 450 (attempt
budgets 150/600 mapped to expected unique bodies at rho = 0.25); 150 and 600
(budget points at rho = 0); 240/300/400 (continuity with the prior table).
"""

import math
import sys

B_MIN = 8
EXT_MIN = 4
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

OLD_COUNT = {
    ("a", 60): 0.001679, ("a", 120): 0.229011, ("a", 240): 0.915980,
    ("a", 300): 0.984032, ("a", 400): 0.999380, ("a", 600): 1.000000,
    ("c", 120): 0.000065, ("c", 240): 0.045907, ("c", 300): 0.170091,
    ("c", 400): 0.499715, ("c", 600): 0.910291,
}
OLD_B_LOW = {
    ("b", 60): 0.000000, ("b", 120): 0.000051, ("b", 240): 0.061576,
    ("b", 300): 0.222695, ("b", 400): 0.611372, ("b", 600): 0.966303,
}

LC = []


def build_lc(nmax):
    global LC
    LC = [float("-inf")] * (nmax + 2)
    for i in range(1, nmax + 2):
        LC[i] = math.lgamma(i)


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


def exp_support(nmax, masses, inrange, gfun):
    tot = 0.0
    for k in inrange:
        pk = masses[k]
        lpk = math.log(pk)
        l1m = math.log1p(-pk)
        for nn in range(nmax + 1):
            lg = LC[nmax + 1] - LC[nn + 1] - LC[nmax - nn + 1] + nn * lpk + (nmax - nn) * l1m
            g = gfun[k][nn]
            if g != 0.0 and lg > -745.0:
                tot += nn * g * math.exp(lg)
    return tot


def compute_cell(masses, inrange, n, gc, gf):
    M = 0.0
    for k in inrange:
        M += masses[k]
    if M <= 0.0 or len(inrange) < 2:
        return {"struct": True}
    lcond = {}
    for k in inrange:
        lcond[k] = math.log(masses[k] / M)
    logM = math.log(M)
    log1m = math.log1p(-M)
    use3 = len(inrange) == 3
    lt_cnt = []
    lt_ful = []
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
            gs = [gc[inrange[i]][vec[i]] for i in range(len(vec))]
            pc = p_at_least_two(gs)
            if pc > 0.0:
                lt_cnt.append(lt + math.log(pc))
            fs = [gf[inrange[i]][vec[i]] for i in range(len(vec))]
            pf = p_at_least_two(fs)
            if pf > 0.0:
                lt_ful.append(lt + math.log(pf))
    return {
        "struct": False,
        "p_cnt": exp_lse(lt_cnt),
        "p_ful": exp_lse(lt_ful),
        "e_cnt": exp_support(n, masses, inrange, gc),
        "e_ful": exp_support(n, masses, inrange, gf),
    }


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
    print("feas_prob.py (Revision B corrected) - exact full-population feasibility")
    print("B_MIN=8, EXT_MIN=4, term cutoff exp(%g); structural zeros = 0*; underflow = 0-dag" % CUT)
    print()
    print("C-law cross-checks (conditioned Dirichlet-multinomial vs dgp_counts_v2.py):")
    for k, zexp in ((5, 252), (10, 2247), (20, 2247)):
        dist, z = c_dist(k)
        flag = "OK" if z == zexp else "MISMATCH"
        print("  k=%d Z=%d expected=%d support-size=%d %s" % (k, z, zexp, len(dist), flag))
    print()
    nmax = max(N_GRID)
    gc = {}
    gf = {}
    for k in (5, 10, 20):
        gc[k] = [1.0 if i >= B_MIN else 0.0 for i in range(nmax + 1)]
        gf[k] = g_full(k, nmax)
    print("Budget mapping (attempts -> E[unique canonical bodies] = 1 + (A-1)(1-rho),")
    print("fresh-draw-uniqueness assumed; validity not modeled):")
    for A in (150, 600):
        print("  attempts=%d: rho=0 -> %.1f ; rho=0.25 -> %.2f" % (A, 1 + (A - 1), 1 + (A - 1) * 0.75))
    print()
    print("Table 1: count-only P(>=2 in-range buckets each >= 8 bodies), full population")
    print("%-9s %12s %s" % ("scenario", "N", " ".join("%12d" % v for v in N_GRID)))
    res = {}
    for s in ("a", "b", "c", "d"):
        masses, ir = SCENARIOS[s]
        row = []
        for n in N_GRID:
            r = compute_cell(masses, ir, n, gc, gf)
            res[(s, n)] = r
            row.append(fmt(r.get("p_cnt", 0.0), r["struct"]))
        print("%-9s %12s %s" % (s, "", " ".join("%12s" % v for v in row)))
    print()
    print("Table 2: fuller P(>=2 buckets pass full Section 5 rule, cond 1-4, observed extremes)")
    for s in ("a", "b", "c", "d"):
        row = []
        for n in N_GRID:
            r = res[(s, n)]
            row.append(fmt(r.get("p_ful", 0.0), r["struct"]))
        print("%-9s %12s %s" % (s, "", " ".join("%12s" % v for v in row)))
    print()
    print("Table 3: expected body counts (E[in-range] = N*M exact; support = exact sums)")
    print("%-9s %-5s %10s %14s %14s" % ("scenario", "N", "E[inrange]", "E[cnt-support]", "E[full-support]"))
    for s in ("a", "b", "c"):
        masses, ir = SCENARIOS[s]
        M = sum(masses[k] for k in ir)
        for n in N_GRID:
            r = res[(s, n)]
            print("%-9s %-5d %10.1f %14.2f %14.2f" % (s, n, n * M, r["e_cnt"], r["e_ful"]))
    print()
    print("Table 4: O4 within-range-mix sensitivity (count-only | fuller)")
    for s in ("a50", "b3", "c50"):
        masses, ir = O4[s]
        print("  [%s] in-range masses: %s" % (s, {k: masses[k] for k in ir}))
        for n in N_GRID:
            r = compute_cell(masses, ir, n, gc, gf)
            print("    N=%-5d count=%s fuller=%s" % (n, fmt(r.get("p_cnt", 0.0), r["struct"]), fmt(r.get("p_ful", 0.0), r["struct"])))
    print()
    print("Regression vs CLAUDE-verified count-only figures (tolerance 5e-7):")
    allok = True
    for key in sorted(OLD_COUNT):
        s, n = key
        old = OLD_COUNT[key]
        new = res[key]["p_cnt"]
        d = abs(new - old)
        flag = "OK" if d <= 5e-7 else "DIFF"
        if flag != "OK":
            allok = False
        print("  (%s @%d) old=%.6f new=%.6f %s" % (s, n, old, new, flag))
    for key in sorted(OLD_B_LOW):
        s, n = key
        old = OLD_B_LOW[key]
        new = res[key]["p_cnt"]
        flag = "OK(superset)" if new + 1e-12 >= old else "VIOLATION"
        if flag != "OK(superset)":
            allok = False
        print("  (%s @%d) buggy-old=%.6f corrected=%.6f %s" % (s, n, old, new, flag))
    print("  count >= fuller in every cell:", end=" ")
    mono = True
    for key, r in res.items():
        if not r["struct"] and r["p_ful"] > r["p_cnt"] + 1e-12:
            mono = False
            allok = False
    print("OK" if mono else "VIOLATION")
    print("REGRESSION:", "ALL-OK" if allok else "REVIEW-NEEDED")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
