#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O2 exact feasibility calculation -- PRE-FREEZE, TEMPORARY (not published).

Prepared per the 2026-10-17 work order (Foued approved the narrow named
pre-freeze deterministic computation policy).  Temporary location only:
no changes to RevF, the published A1 package, or Git history; no commit.

Event (2-bucket scenarios only; support rule S1-m4; R-a global membership):
  G   : both in-range buckets (k=5 and k=10) pass S1-m4 support
        (n >= 8 and n - max_c n_c >= 4, exact C|k composition model).
  TR  : training block (size NTR = N - (N+2)//4) has tra>=1, trb>=1,
        tra+trb>=8  (A1 TrainRa / global-membership reading).
  CVD : "at least two distinct C values in some included training bucket",
        computed under BOTH readings:
          P_atleastone : exists an included bucket with >=2 distinct C
                         values among its training bodies  (literal reading)
          P_each       : every included bucket has >=2 distinct C values
                         among its training bodies  (stricter reading)
  TN  : test block (size T = (N+2)//4) has tea>=1, teb>=1, tea+teb>=8
        (B_split = 8, as proposed).
  Matrix rank/conditioning criterion (M3): EXCLUDED -- implementation and
  acceptance are not yet specified.

Method (exact, deterministic, stdlib only; no sampling):
  For a fixed-size uniform train/test split, the train and test block class
  compositions are independent multinomials (exact identity).  Per-bucket
  C-composition effects enter through
    F_k(n)      = f_s1(k, n, 4) = P(S1-m4 support | bucket size n)
    H_k(n, t)   = P(S1-m4 support AND all t training bodies of the bucket
                    share one C value | bucket size n, train size t).
  H_k is computed in closed form via binomial tails of the C-value
  distribution (with direct enumeration for small test-block sizes).
  Then, with 1tr = [x>=1][y>=1][x+y>=8], 1tn = [u>=1][v>=1][u+v>=8],
  R = Mult(NTR; x, y, pO), S = Mult(NTE; u, v, pO):
    T0   = sum R S F5(x+u) F10(y+v)
    T_HF = sum R S H5(x+u,x) F10(y+v)      (same-C in bucket 5)
    T_FH = sum R S F5(x+u) H10(y+v,y)      (same-C in bucket 10)
    T_HH = sum R S H5(x+u,x) H10(y+v,y)    (same-C in both)
    P_atleastone = T0 - T_HH
    P_each       = T0 - T_HF - T_FH + T_HH

Validations: small-N direct hypergeometric+composition route; brute vs
analytic F/H; A1 h-table route for T0; bracketing against the published
A1 joint_2bucket S1-m4 lib/cons values.  N=16/20 route comparisons are
recorded as VACUOUS (test block < 8 bodies => complete event mass is
identically zero); N=32 is the first informative small-N comparison.

External dependency: this script imports v03p/a1/a1_support_comparison.py
(A1 rev 3, commit f69cc9b) read-only via the absolute A1DIR path below;
it is NOT self-contained or portable by design.
"""

import sys
import os
import math
import json
import time
import datetime

sys.dont_write_bytecode = True

A1DIR = r"C:\Users\pakla\PycharmProjects\failure-concentration-study\v03p\a1"
sys.path.insert(0, A1DIR)
import a1_support_comparison as A  # noqa: E402

OUTDIR = os.path.dirname(os.path.abspath(__file__))
NB = (113, 150, 450, 600)
SCENS = ("a-hist", "a-50:50", "c-hist", "c-50:50")
NMAX = 600
CHECKS = []


def check(name, ok, detail="", vacuous=False):
    status = "VACUOUS" if vacuous else ("PASS" if ok else "FAIL")
    CHECKS.append({"name": name, "ok": bool(ok), "vacuous": bool(vacuous),
                   "status": status, "detail": str(detail)})
    print(status + " " + name + ((" | " + str(detail)) if detail != "" else ""))
    return bool(ok)


# --------------------------------------------------------------------------
# H_k(n, t): P(S1-m4 support AND all train bodies share one C value)
# --------------------------------------------------------------------------

def _Q_small(pi, u, t, c):
    """Direct enumeration (u <= 5): P(test comp of size u with probs pi has
    t_c <= u-4 and t_i <= t+u-4 for i != c)."""
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
    """P(test multinomial size u satisfies t_c <= u-4 and t_i <= t+u-4, i!=c).

    Exact for all u,t: for u >= 6 the violation events are pairwise disjoint
    (two classes cannot each hold u+t-3 pre-dominantly), so
      Q = 1 - P(Bin(u,pi_c) >= u-3) - sum_{i!=c} P(Bin(u,pi_i) >= u+t-3)
    for t <= 3; for t >= 4 the i!=c constraints are automatic.
    """
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


def build_H(pi, ntrmax=450):
    """H[(n,t)] for n in 8..NMAX, t in 1..min(n,ntrmax); zero entries omitted."""
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


# --------------------------------------------------------------------------
# Main route: independent train/test compositions (exact identity)
# --------------------------------------------------------------------------

def rs_terms(N, p5, p10, F5, H5, F10, H10):
    """Return T0/T_HF/T_FH/T_HH and the two CVD readings; exact."""
    NTR, NTE = A.split_sizes(N)
    pO = 1.0 - p5 - p10
    R = [[0.0] * (NTR + 1) for _ in range(NTR + 1)]
    for x in range(1, NTR + 1):
        for y in range(1, NTR - x + 1):
            if x + y >= 8:
                R[x][y] = A.mpmf2(NTR, x, y, p5, p10, pO)
    S = [[0.0] * (NTE + 1) for _ in range(NTE + 1)]
    for u in range(1, NTE + 1):
        for v in range(1, NTE - u + 1):
            if u + v >= 8:
                S[u][v] = A.mpmf2(NTE, u, v, p5, p10, pO)
    # Sf[y][u] = sum_v S[u][v] F10(y+v);  Xi[y][u] = sum_v S[u][v] H10(y+v,y)
    Sf = [[0.0] * (NTE + 1) for _ in range(NTR + 1)]
    Xi = [[0.0] * (NTE + 1) for _ in range(NTR + 1)]
    h10get = H10.get
    for u in range(1, NTE + 1):
        Su = S[u]
        for v in range(1, NTE - u + 1):
            s = Su[v]
            if s <= 0.0:
                continue
            for y in range(1, NTR + 1):
                s2 = y + v
                fv = F10[s2]
                if fv > 0.0:
                    Sf[y][u] += s * fv
                hv = h10get((s2, y), 0.0)
                if hv > 0.0:
                    Xi[y][u] += s * hv
    T = {"T0": 0.0, "T_HF": 0.0, "T_FH": 0.0, "T_HH": 0.0}
    h5get = H5.get
    for x in range(1, NTR + 1):
        for y in range(1, NTR - x + 1):
            r = R[x][y]
            if r <= 0.0:
                continue
            sfy = Sf[y]
            xiy = Xi[y]
            l0 = l1 = l2 = l3 = 0.0
            for u in range(1, NTE + 1):
                sf = sfy[u]
                xi = xiy[u]
                if sf <= 0.0 and xi <= 0.0:
                    continue
                n = x + u
                f5v = F5[n]
                if sf > 0.0 and f5v > 0.0:
                    l0 += sf * f5v
                h5v = h5get((n, x), 0.0)
                if h5v > 0.0:
                    if sf > 0.0:
                        l1 += sf * h5v
                    if xi > 0.0:
                        l3 += xi * h5v
                if xi > 0.0 and f5v > 0.0:
                    l2 += xi * f5v
            T["T0"] += r * l0
            T["T_HF"] += r * l1
            T["T_FH"] += r * l2
            T["T_HH"] += r * l3
    T["P_atleastone"] = T["T0"] - T["T_HH"]
    T["P_each"] = T["T0"] - T["T_HF"] - T["T_FH"] + T["T_HH"]
    return T


# --------------------------------------------------------------------------
# Validation route 1: small-N direct hypergeometric + composition enumeration
# --------------------------------------------------------------------------

def comp_prob(n, comp, pi):
    lg = A.LFACT[n]
    for x, p in zip(comp, pi):
        lg -= A.LFACT[x]
        if x:
            if p <= 0.0:
                return 0.0
            lg += x * math.log(p)
    return math.exp(lg) if lg > -745.0 else 0.0


def comps_list(n, v):
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


def brute_bucket_tables(N, pi):
    """PF[a] = P(S1-m4 support); PH[(a,ta)] = P(support and train all-same)."""
    v = len(pi)
    NTR, _ = A.split_sizes(N)
    PF = {}
    PH = {}
    for a in range(8, N + 1):
        tmax = min(a, NTR)
        Fv = 0.0
        Hv = [0.0] * (tmax + 1)
        for comp in comps_list(a, v):
            p = comp_prob(a, comp, pi)
            if p <= 0.0:
                continue
            if a - max(comp) < 4:
                continue
            Fv += p
            lca = A.log_comb(a, 1)
            for ta in range(1, tmax + 1):
                s = 0.0
                for cc in comp:
                    if cc >= ta:
                        s += math.exp(A.log_comb(cc, ta))
                Hv[ta] += p * s * math.exp(-A.log_comb(a, ta))
        PF[a] = Fv
        for ta in range(1, tmax + 1):
            PH[(a, ta)] = Hv[ta]
    return PF, PH


def direct_terms(N, p5, p10, pi5, pi10):
    """Exact alternative route: hypergeometric split + composition tables."""
    NTR, NTE = A.split_sizes(N)
    pO = 1.0 - p5 - p10
    PF5, PH5 = brute_bucket_tables(N, pi5)
    PF10, PH10 = brute_bucket_tables(N, pi10)
    T = {"T0": 0.0, "T_HF": 0.0, "T_FH": 0.0, "T_HH": 0.0}
    for a in range(8, N + 1):
        for b in range(8, N - a + 1):
            o = N - a - b
            mult = A.mpmf2(N, a, b, p5, p10, pO)
            if mult <= 0.0:
                continue
            f5 = PF5[a]
            f10 = PF10[b]
            for ta in range(1, min(a, NTR) + 1):
                tea = a - ta
                if tea < 1:
                    continue
                h5 = PH5[(a, ta)]
                for tb in range(1, min(b, NTR - ta) + 1):
                    teb = b - tb
                    if teb < 1 or ta + tb < 8 or tea + teb < 8:
                        continue
                    h = A._hg_ratio(a, b, o, NTR, ta, tb)
                    if h <= 0.0:
                        continue
                    h10 = PH10[(b, tb)]
                    T["T0"] += mult * h * f5 * f10
                    T["T_HF"] += mult * h * h5 * f10
                    T["T_FH"] += mult * h * f5 * h10
                    T["T_HH"] += mult * h * h5 * h10
    T["P_atleastone"] = T["T0"] - T["T_HH"]
    T["P_each"] = T["T0"] - T["T_HF"] - T["T_FH"] + T["T_HH"]
    return T, (PF5, PH5, PF10, PH10)


# --------------------------------------------------------------------------
# Validation route 2: A1-style h-table for the count-only event T0
# --------------------------------------------------------------------------

def htab_T0(N, p5, p10, F5, F10):
    NTR, NTE = A.split_sizes(N)
    tab = {}
    for a in range(8, N + 1):
        for b in range(8, N - a + 1):
            o = N - a - b
            s = 0.0
            for ta in range(1, min(a, NTR) + 1):
                tea = a - ta
                if tea < 1:
                    continue
                for tb in range(1, min(b, NTR - ta) + 1):
                    teb = b - tb
                    if teb < 1:
                        continue
                    if ta + tb >= 8 and tea + teb >= 8:
                        s += A._hg_ratio(a, b, o, NTR, ta, tb)
            if s > 0.0:
                tab[(a, b)] = s
    return A.joint2(N, p5, p10, F5, F10, tab)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def rel_close(a, b, tol=1e-12):
    return abs(a - b) <= tol * max(abs(a), abs(b), 1e-300)


def main():
    t_start = time.time()
    print("interpreter:", sys.version.replace("\n", " "))
    print("executable:", sys.executable)
    print("A1 module:", A.__file__)

    F5 = [A.f_s1(5, n, 4) for n in range(NMAX + 1)]
    F10 = [A.f_s1(10, n, 4) for n in range(NMAX + 1)]
    if ("S1-m4", 5) not in A.FTABLE:
        A.build_ftables()
    ref5 = A.FTABLE[("S1-m4", 5)]
    ref10 = A.FTABLE[("S1-m4", 10)]
    nlim = min(len(ref5), len(ref10), len(F5), len(F10))
    worst5 = max((abs(ref5[n] - F5[n]) for n in range(nlim)), default=0.0)
    worst10 = max((abs(ref10[n] - F10[n]) for n in range(nlim)), default=0.0)
    check("V0 F5,F10 equal A.FTABLE[('S1-m4', k)] (exact)",
          len(ref5) >= len(F5) and len(ref10) >= len(F10) and worst5 == 0.0 and worst10 == 0.0,
          f"worst |dev| k=5 {worst5:.3e}, k=10 {worst10:.3e}; len ref/calc "
          f"{len(ref5)}/{len(F5)} and {len(ref10)}/{len(F10)}")

    t0 = time.time()
    H5 = build_H(A.CK[5][1])
    print(f"H5 built: {len(H5)} entries ({time.time()-t0:.1f}s)")
    t0 = time.time()
    H10 = build_H(A.CK[10][1])
    print(f"H10 built: {len(H10)} entries ({time.time()-t0:.1f}s)")

    # V2: analytic identities on H
    worst = 0.0
    for n in range(8, NMAX + 1):
        worst = max(worst, abs(H5.get((n, 1), 0.0) - F5[n]) / max(F5[n], 1e-300))
    check("V2 H5(n,1) == F5(n) all n (rel)", worst <= 1e-9, f"worst rel dev {worst:.3e}")
    worst = 0.0
    for n in range(8, NMAX + 1):
        worst = max(worst, abs(H10.get((n, 1), 0.0) - F10[n]) / max(F10[n], 1e-300))
    check("V2 H10(n,1) == F10(n) all n (rel)", worst <= 1e-9, f"worst rel dev {worst:.3e}")
    bad = 0
    for (n, t), h in H5.items():
        if h > F5[n] * (1.0 + 1e-12):
            bad += 1
    check("V2 H5 <= F5 pointwise", bad == 0, f"{bad} violations")

    # V1: small N, real and harness tables, direct vs independent-composition
    for N in (16, 20, 32):
        for label, p5, p10, pi5, pi10 in (
            ("real a-hist", 0.10, 0.05, A.CK[5][1], A.CK[10][1]),
            ("harness", 0.30, 0.25, (0.40, 0.30, 0.20, 0.10), (0.50, 0.20, 0.20, 0.10)),
        ):
            Td, (PF5, PH5b, PF10, PH10b) = direct_terms(N, p5, p10, pi5, pi10)
            F5b = [PF5.get(n, 0.0) for n in range(NMAX + 1)]
            F10b = [PF10.get(n, 0.0) for n in range(NMAX + 1)]
            Tr = rs_terms(N, p5, p10, F5b, PH5b, F10b, PH10b)
            ok = True
            dev = 0.0
            for key in ("T0", "T_HF", "T_FH", "T_HH", "P_atleastone", "P_each"):
                d = abs(Td[key] - Tr[key])
                dev = max(dev, d)
                if not rel_close(Td[key], Tr[key], 1e-9) and d > 1e-15:
                    ok = False
            nte_ = A.split_sizes(N)[1]
            vac = nte_ < 8
            vtxt = (f"; VACUOUS: test block {nte_} < 8 => complete event mass "
                    f"is identically zero") if vac else ""
            check(f"V1 direct==RS {label} N={N}", ok, f"max abs dev {dev:.3e}{vtxt}",
                  vacuous=vac)
            if label == "real a-hist":
                wf = max(abs(PF5[a] - F5[a]) for a in range(8, N + 1))
                wh = 0.0
                for a in range(8, N + 1):
                    for ta in range(1, min(a, A.split_sizes(N)[0]) + 1):
                        wh = max(wh, abs(PH5b[(a, ta)] - H5.get((a, ta), 0.0)))
                wf10 = max(abs(PF10[b] - F10[b]) for b in range(8, N + 1))
                wh10 = 0.0
                for b in range(8, N + 1):
                    for tb in range(1, min(b, A.split_sizes(N)[0]) + 1):
                        wh10 = max(wh10, abs(PH10b[(b, tb)] - H10.get((b, tb), 0.0)))
                check(f"V1 brute F5==analytic N={N}", wf <= 1e-12, f"{wf:.3e}")
                check(f"V1 brute H5==analytic N={N}", wh <= 1e-12, f"{wh:.3e}")
                check(f"V1 brute F10==analytic N={N}", wf10 <= 1e-12, f"{wf10:.3e}")
                check(f"V1 brute H10==analytic N={N}", wh10 <= 1e-12, f"{wh10:.3e}")

    # Main grid
    j2path = os.path.join(A1DIR, "out", "a1_tables.json")
    with open(j2path, "r", encoding="utf-8") as fh:
        J2 = json.load(fh)["joint_2bucket"]

    results = {}
    for scen in SCENS:
        p5 = A.SCEN[scen][5]
        p10 = A.SCEN[scen][10]
        for N in NB:
            t0 = time.time()
            T = rs_terms(N, p5, p10, F5, H5, F10, H10)
            ref = J2[f"S1-m4|{scen}|{N}"]
            T["lib_ref"] = ref["lib"]
            T["cons_ref"] = ref["cons"]
            T["scen"] = scen
            T["N"] = N
            T["NTR"] = A.split_sizes(N)[0]
            T["NTE"] = A.split_sizes(N)[1]
            results[f"{scen}|{N}"] = T
            check(f"V4 cons<=T0<=lib {scen}@{N}",
                  T["T0"] >= ref["cons"] * (1 - 1e-12) and T["T0"] <= ref["lib"] * (1 + 1e-12),
                  f"cons={ref['cons']:.6e} T0={T['T0']:.6e} lib={ref['lib']:.6e}")
            check(f"V5 order 0<=P_each<=P_atleastone<=T0 {scen}@{N}",
                  T["P_each"] >= -1e-18 and T["P_each"] <= T["P_atleastone"] + 1e-18
                  and T["P_atleastone"] <= T["T0"] + 1e-18,
                  f"P_each={T['P_each']:.6e} P_one={T['P_atleastone']:.6e} T0={T['T0']:.6e}")
            print(f"  {scen}@{N}: T0={T['T0']:.10g} P_atleastone={T['P_atleastone']:.10g} "
                  f"P_each={T['P_each']:.10g}  [{time.time()-t0:.1f}s]")

    # V3: A1 h-table route for T0 (N=113, two scenarios)
    for scen in ("a-hist", "c-hist"):
        p5 = A.SCEN[scen][5]
        p10 = A.SCEN[scen][10]
        t0 = time.time()
        T0h = htab_T0(113, p5, p10, F5, F10)
        Trs = results[f"{scen}|113"]["T0"]
        check(f"V3 htab-vs-RS T0 {scen}@113", rel_close(T0h, Trs, 1e-11),
              f"htab={T0h:.10g} rs={Trs:.10g} ({time.time()-t0:.1f}s)")

    all_ok = all(c["ok"] for c in CHECKS)
    meta = {
        "status": "TEMPORARY pre-freeze calculation; not published; repo untouched",
        "event": "S1-m4 support + TrainRa + CVD (both readings) + Test (lib1 & total>=8)",
        "excluded": ["matrix rank/conditioning criterion (M3)", "3-bucket scenarios",
                     "attempt-axis budget", "validity/dedup modeling"],
        "interpreter": sys.version,
        "executable": sys.executable,
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "runtime_s": round(time.time() - t_start, 1),
        "NB": list(NB),
        "scenarios": list(SCENS),
        "failures": [c for c in CHECKS if not c["ok"]],
        "checks_total": len(CHECKS),
        "checks_pass": sum(1 for c in CHECKS if c["status"] == "PASS"),
        "checks_vacuous": sum(1 for c in CHECKS if c["status"] == "VACUOUS"),
        "checks_fail": sum(1 for c in CHECKS if c["status"] == "FAIL"),
    }
    out = {"meta": meta, "checks": CHECKS, "results": results}
    outfile = os.path.join(OUTDIR, "o2_results.json")
    with open(outfile, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    # Markdown summary
    lines = []
    lines.append("# O2 exact feasibility calculation (pre-freeze, temporary)")
    lines.append("")
    lines.append("- Status: TEMPORARY. Not published, no repo changes, no commit.")
    lines.append("- Interpreter: " + sys.version.replace("\n", " "))
    lines.append("- Generated (UTC): " + meta["generated_utc"])
    lines.append("- Event: S1-m4 support + TrainRa (tra,tb>=1; tra+tb>=8) + CVD")
    lines.append("  (both readings) + test tea,teb>=1 and tea+teb>=8 (B_split=8).")
    lines.append("- Excluded: matrix rank/conditioning criterion; 3-bucket scenarios;")
    lines.append("  attempt-budget modeling; validity/dedup modeling.")
    lines.append("")
    lines.append("| scen | N | T0 (no CVD) | P(atleastone) | P(each) | A1 lib ref | A1 cons ref |")
    lines.append("|---|---|---|---|---|---|---|")
    for key in sorted(results):
        r = results[key]
        lines.append("| {scen} | {N} | {t0:.10g} | {pa:.10g} | {pe:.10g} | {lib:.10g} | {cons:.10g} |".format(
            scen=r["scen"], N=r["N"], t0=r["T0"], pa=r["P_atleastone"], pe=r["P_each"],
            lib=r["lib_ref"], cons=r["cons_ref"]))
    lines.append("")
    lines.append("## checks")
    lines.append("")
    lines.append(f"- check records: {len(CHECKS)} total; "
                 f"{sum(1 for c in CHECKS if c['status'] == 'PASS')} PASS, "
                 f"{sum(1 for c in CHECKS if c['status'] == 'VACUOUS')} VACUOUS, "
                 f"{sum(1 for c in CHECKS if c['status'] == 'FAIL')} FAIL")
    lines.append("")
    for c in CHECKS:
        lines.append(f"- [{c['status']}] {c['name']}" + (f" -- {c['detail']}" if c["detail"] else ""))
    lines.append("")
    lines.append("## assumptions / limitations")
    lines.append("")
    lines.append("- 2-bucket scenarios only (a-hist, a-50:50, c-hist, c-50:50); the")
    lines.append("  3-bucket scenarios (b-hist, b-thirds) are outside A1's joint scope")
    lines.append("  and are not computed here.")
    lines.append("- Fixed N_b unique valid bodies; 25% holdout with exact fixed split")
    lines.append("  sizes; A1's C|k composition model; no validity/dedup modeling.")
    lines.append("- 'Eligible' test/training bodies = bodies in the included buckets.")
    lines.append("- CVD literal reading: at least one included bucket has >=2 distinct")
    lines.append("  C values among its training bodies (P_atleastone). Stricter reading:")
    lines.append("  every included bucket does (P_each). Both reported; the choice is")
    lines.append("  an owner decision.")
    lines.append("- Matrix conditioning is excluded; results must not be presented as")
    lines.append("  complete-rule feasibility.")
    with open(os.path.join(OUTDIR, "o2_report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("wrote o2_results.json and o2_report.md")
    print("FAILURES:", "none" if all_ok else [c["name"] for c in CHECKS if not c["ok"]])
    print(f"CHECKS: {meta['checks_total']} total = {meta['checks_pass']} PASS + "
          f"{meta['checks_vacuous']} VACUOUS + {meta['checks_fail']} FAIL")
    print(f"total runtime {time.time()-t_start:.1f}s")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
