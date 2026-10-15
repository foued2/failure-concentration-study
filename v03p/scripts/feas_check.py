"""feas_check.py - fast exact reference tests for the Revision B/C arithmetic package.

Deterministic stdlib-only checks (independent implementations where noted):
 T1 logcomb table vs exact integer math.comb.
 T2 closed-form inner_L/inner_T (independent direct code) vs explicit
    hypergeometric split enumeration at fixed compositions (s=2 and s=3).
 T3 end-to-end brute force vs feas_prob_test.readings() count-only fields
    for 2-bucket scenarios at N=32.
 T4 RCS baseline rank minors at the scenario k-sets (exact rcs formula cited
    from study/models.py:17-26; KNOTS study/models.py:8).
 T5 outcome-tail grid convergence re-assert (one mix, 81 vs 161 nodes).
 T6 fuller LIB/TRN wiring: independent mask-sum with T2 closed forms vs
    feas_prob_test.readings() lib_f/trn_f at N=32, scenario (a).
Runs in seconds. Full-script runtime report: Appendix C.
"""

import math

import feas_prob_test as F
from dgp_outcome_tails import tail_fractions

F.build_lc(600)

PASS = [True]


def check(name, cond, detail=""):
    if not cond:
        PASS[0] = False
    print(("PASS " if cond else "FAIL ") + name + (" " + detail if detail else ""))


def close(a, b, rel=1e-9, floor=1e-12):
    return abs(a - b) <= max(floor, rel * max(abs(a), abs(b)))


# T1
t1 = True
for n, r in [(600, 150), (600, 0), (600, 600), (113, 28), (0, 0), (450, 113), (90, 45)]:
    t1 = t1 and abs(F.logcomb(n, r) - math.log(math.comb(n, r))) < 1e-9
check("T1 logcomb vs math.comb", t1)


# T2
def closed_L(N, T, ns):
    from math import comb
    mS = sum(ns)
    CN = comb(N, T)
    tot = 0.0
    for t in range(8, min(mS, T) + 1):
        hyp = comb(mS, t) * comb(N - mS, T - t) / CN
        single = sum(comb(b, t) / comb(mS, t) for b in ns)
        tot += hyp * (1.0 - single)
    return tot


def explicit_L(N, T, ns):
    from math import comb
    mS = sum(ns)
    CN = comb(N, T)
    out = N - mS
    tot = [0.0]

    def rec(i, t_used, cprod, reps, tsum):
        if i == len(ns):
            t_out = T - t_used
            if 0 <= t_out <= out and tsum >= 8 and reps >= 2:
                tot[0] += cprod * comb(out, t_out) / CN
            return
        b = ns[i]
        for t in range(0, min(b, T - t_used) + 1):
            rec(i + 1, t_used + t, cprod * comb(b, t),
                reps + (1 if t >= 1 else 0), tsum + t)

    rec(0, 0, 1, 0, 0)
    return tot[0]


def closed_T(N, T, ns):
    from math import comb
    mS = sum(ns)
    s = len(ns)
    if s < 2 or mS < 16:
        return 0.0
    CN = comb(N, T)
    tot = 0.0
    for t in range(8, min(mS - 8, T) + 1):
        hyp = comb(mS, t) * comb(N - mS, T - t) / CN
        single = sum(comb(b, t) / comb(mS, t) for b in ns)
        pu = 0.0
        for j in range(s):
            d = t - (mS - ns[j])
            if 0 <= d <= ns[j]:
                pu += comb(ns[j], d) / comb(mS, t)
        both = 0.0
        if s == 2:
            for j in range(2):
                if t == ns[j]:
                    both += comb(ns[j], t) / comb(mS, t)
        tot += hyp * (1.0 - single - pu + both)
    return tot


def explicit_T(N, T, ns):
    from math import comb
    mS = sum(ns)
    CN = comb(N, T)
    out = N - mS
    tot = [0.0]

    def rec(i, t_used, cprod, tvec):
        if i == len(ns):
            t_out = T - t_used
            if t_out < 0 or t_out > out:
                return
            ts = sum(tvec)
            if ts < 8 or ts > mS - 8:
                return
            rt = sum(1 for t in tvec if t >= 1)
            if rt < 2:
                return
            ru = sum(1 for k in range(len(ns)) if ns[k] - tvec[k] >= 1)
            if ru < 2:
                return
            tot[0] += cprod * comb(out, t_out) / CN
            return
        b = ns[i]
        for t in range(0, min(b, T - t_used) + 1):
            tvec.append(t)
            rec(i + 1, t_used + t, cprod * comb(b, t), tvec)
            tvec.pop()

    rec(0, 0, 1, [])
    return tot[0]


for N, T, ns in [(600, 150, [60, 30]), (600, 150, [40, 20, 12]),
                 (150, 38, [20, 14]), (150, 38, [10, 8, 8])]:
    a = closed_L(N, T, ns)
    b = explicit_L(N, T, ns)
    check("T2 inner_L N=%d T=%d %s" % (N, T, ns), close(a, b), "closed=%.9g expl=%.9g" % (a, b))
    a = closed_T(N, T, ns)
    b = explicit_T(N, T, ns)
    check("T2 inner_T N=%d T=%d %s" % (N, T, ns), close(a, b), "closed=%.9g expl=%.9g" % (a, b))


# T3
def brute(N, p5, p10):
    from math import comb
    T = int(math.floor(0.25 * N + 0.5))
    CN = comb(N, T)
    Fv = CONS = LIB = TRN = NOS = NOSF = 0.0
    for n5 in range(N + 1):
        w5 = comb(N, n5) * p5 ** n5 * (1 - p5) ** (N - n5)
        if w5 == 0.0:
            continue
        q10 = p10 / (1 - p5)
        qo = (1 - p5 - p10) / (1 - p5)
        for n10 in range(N - n5 + 1):
            w = w5 * comb(N - n5, n10) * q10 ** n10 * qo ** (N - n5 - n10)
            if w == 0.0:
                continue
            n = {5: n5, 10: n10}
            S = [k for k in (5, 10) if n[k] >= 8]
            mS = sum(n[k] for k in S)
            nout = N - n5 - n10
            if len(S) >= 2:
                Fv += w
            for t5 in range(min(n5, T) + 1):
                for t10 in range(min(n10, T - t5) + 1):
                    tout = T - t5 - t10
                    if tout < 0 or tout > nout:
                        continue
                    wt = w * comb(n5, t5) * comb(n10, t10) * comb(nout, tout) / CN
                    t = {5: t5, 10: t10}
                    tS = sum(t[k] for k in S)
                    if tS == 0:
                        NOS += wt
                        if len(S) >= 2:
                            NOSF += wt
                    rt = sum(1 for k in S if t[k] >= 1)
                    if tS >= 8 and rt >= 2:
                        LIB += wt
                        uS = mS - tS
                        ru = sum(1 for k in S if n[k] - t[k] >= 1)
                        if uS >= 8 and ru >= 2:
                            TRN += wt
                    if t5 >= 8 and t10 >= 8:
                        CONS += wt
    return {"fc": Fv, "cons": CONS, "lib_c": LIB, "trn_c": TRN, "nos": NOS, "nosF": NOSF}


gc = {k: [1.0 if i >= 8 else 0.0 for i in range(65)] for k in (5, 10, 20)}
gf = {k: F.g_full(k, 64) for k in (5, 10, 20)}
for s, masses in (("a", {0: 0.80, 5: 0.10, 10: 0.05, 25: 0.05}),
                  ("c", {0: 0.94, 5: 0.03, 10: 0.02, 25: 0.01})):
    r = F.readings(32, masses, [5, 10], gc, gf)
    b = brute(32, masses[5], masses[10])
    for k in ("fc", "cons", "lib_c", "trn_c", "nos", "nosF"):
        check("T3 (%s)@32 %s" % (s, k), abs(r[k] - b[k]) <= 1e-9,
              "script=%.9g brute=%.9g" % (r[k], b[k]))


# T4
KNOTS = [1.0986122886681098, 1.6094379124341003, 2.302585092994046, 2.995732273553991, 3.4339872044851463]


def rcs_cols(x):
    t1, tk = KNOTS[0], KNOTS[-1]
    cols = [x]
    for j in range(1, 4):
        tj = KNOTS[j]
        d = ((x - tj if x - tj > 0 else 0.0) ** 3 - (x - tk if x - tk > 0 else 0.0) ** 3)
        d -= ((tk - tj) / (tk - t1)) * ((x - t1 if x - t1 > 0 else 0.0) ** 3 - (x - tk if x - tk > 0 else 0.0) ** 3)
        cols.append(d / (tk - t1) ** 2)
    return cols


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


x5, x10, x20 = math.log(6), math.log(11), math.log(21)
d2 = abs(x10 - x5)
check("T4 2-point baseline rank exactly 2", d2 > 1e-12, "det[1,x]=%.6f" % d2)
rows = [[1.0] + rcs_cols(x) for x in (x5, x10, x20)]
import itertools
dets = []
for cols in itertools.combinations(range(5), 3):
    dets.append(abs(det3([[r[c] for c in cols] for r in rows])))
check("T4 3-point baseline rank exactly 3", min(dets) > 1e-9,
      "min|minor|=%.3e max|minor|=%.3e" % (min(dets), max(dets)))


# T5
a1, _ = tail_fractions([5, 10], [0.10 / 0.15, 0.05 / 0.15], 81)
a2, _ = tail_fractions([5, 10], [0.10 / 0.15, 0.05 / 0.15], 161)
check("T5 tail grid convergence", max(abs(a1[i] - a2[i]) for i in range(5)) < 1e-9,
      "maxdiff=%.2e" % max(abs(a1[i] - a2[i]) for i in range(5)))

# T6
lib = trn = 0.0
N = 32
T = 8
M = 0.15
logM, log1m = math.log(M), math.log1p(-M)
lcond = {5: math.log(0.10 / M), 10: math.log(0.05 / M)}
LC = F.LC
for m in range(N + 1):
    logpm = LC[N + 1] - LC[m + 1] - LC[N - m + 1] + m * logM + (N - m) * log1m
    if logpm < -46.0:
        continue
    for t in range(m + 1):
        vec = (t, m - t)
        logmult = LC[m + 1] - LC[vec[0] + 1] - LC[vec[1] + 1]
        logmult += vec[0] * lcond[5] + vec[1] * lcond[10]
        lt = logpm + logmult
        if lt < -46.0:
            continue
        w = math.exp(lt)
        gs = [gf[5][vec[0]], gf[10][vec[1]]]
        for mask in range(4):
            pr = 1.0
            S = []
            for i, g in enumerate(gs):
                if (mask >> i) & 1:
                    pr *= g
                    S.append([5, 10][i])
                else:
                    pr *= 1.0 - g
            if pr <= 0.0:
                continue
            ns = [vec[[5, 10].index(k)] for k in S]
            mS = sum(ns)
            if ns:
                lib += w * pr * closed_L(N, T, ns)
                trn += w * pr * closed_T(N, T, ns)
r = F.readings(32, {0: 0.80, 5: 0.10, 10: 0.05, 25: 0.05}, [5, 10], gc, gf)
check("T6 (a)@32 lib_f wiring", abs(r["lib_f"] - lib) <= 1e-9,
      "script=%.9g indep=%.9g" % (r["lib_f"], lib))
check("T6 (a)@32 trn_f wiring", abs(r["trn_f"] - trn) <= 1e-9,
      "script=%.9g indep=%.9g" % (r["trn_f"], trn))

print("REFERENCE-TESTS:", "ALL-PASS" if PASS[0] else "REVIEW-NEEDED")
