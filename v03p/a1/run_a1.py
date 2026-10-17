"""Run A1: self-tests, RevF regression, full grids, joint train/test.

Deterministic, stdlib only. Writes out/a1_tables.json and out/a1_report.md.
Exit code 0 only if every self-test and regression check passes.
"""

import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a1_support_comparison import (
    CK, CK_Z, S2_STRATA, NMAX, LFACT, SCEN, INRANGE, RULES, FTABLE,
    build_ftables, f_s0, f_s1, f_s2, brute_probs, global2, global3_full,
    global3_box, bucket_marginals, split_sizes, h_joint_lib, h_joint_cons,
    joint2, _hg_ratio,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
NB = [113, 150, 450, 600]
TOL = 1e-9
fails = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (" | " + str(detail) if detail else ""))
    if not cond:
        fails.append(name)


# ---- 1. C|k distributions -------------------------------------------------
check("Z5==252", CK_Z[5] == 252, CK_Z[5])
check("Z10==2247", CK_Z[10] == 2247, CK_Z[10])
check("Z20==2247", CK_Z[20] == 2247, CK_Z[20])
check("Z24==456", CK_Z[24] == 456, CK_Z[24])
v5, p5 = CK[5]
check("k5 values", v5 == [0.2, 0.4, 0.6, 0.8, 1.0], v5)
check("k5 P extremes", abs(p5[0] - 6 / 252) < 1e-15 and abs(p5[-1] - 6 / 252) < 1e-15)
v10, p10 = CK[10]
check("k10 values", v10 == [0.2, 0.3, 0.4, 0.5], v10)
v20, p20 = CK[20]
check("k20 values", v20 == [0.2, 0.25], v20)
check("k20 P(0.25)", abs(p20[1] - 2121 / 2247) < 1e-12, p20[1])
# E[C] spot checks vs RevF
e5 = sum(v * p for v, p in zip(v5, p5))
check("E[C|5]=0.528571", abs(e5 - 0.528571) < 1e-6, e5)
e10 = sum(v * p for v, p in zip(v10, p10))
check("E[C|10]=0.407744", abs(e10 - 0.407744) < 1e-6, e10)
# S2 strata nonempty + disjoint for k=5,10,20
for k in (5, 10, 20):
    s = S2_STRATA[k]
    check(f"S2 strata k={k}",
          len(s["low_vals"]) > 0 and len(s["high_vals"]) > 0
          and max(s["low_vals"]) < min(s["high_vals"])
          and s["p_low"] > 0 and s["p_high"] > 0,
          (s["low_vals"], s["high_vals"], round(s["p_low"], 4),
           round(s["p_mid"], 4), round(s["p_high"], 4)))

# ---- 2. brute-force cross-checks of f_s0/f_s1/f_s2 -------------------------
t0 = time.time()
worst = 0.0
for k in (5, 10, 20):
    for n in range(0, 11):
        b = brute_probs(k, n)
        d0 = abs(b["s0"] - f_s0(k, n))
        worst = max(worst, d0)
        check(f"brute S0 k={k} n={n}", d0 < TOL, d0)
        for m in (2, 4, 6):
            d1 = abs(b["s1"][m] - f_s1(k, n, m))
            d2 = abs(b["s2"][m] - f_s2(k, n, m))
            worst = max(worst, d1, d2)
            if d1 >= TOL or d2 >= TOL:
                check(f"brute S1/S2 k={k} n={n} m={m}", False, (d1, d2))
print(f"brute-force block worst abs diff: {worst:.3e} ({time.time()-t0:.1f}s)")
check("brute worst<1e-9", worst < TOL, worst)

# ---- 3. f-tables + RevF S0 regression --------------------------------------
t0 = time.time()
build_ftables()
print(f"f-tables built ({time.time()-t0:.1f}s)")

REVF_BL = {  # (scen, N) -> (F_bl from RevF full-population table, sig figs)
    ("a-hist", 60): (6.0e-06, 2), ("a-hist", 113): (0.001117, 4), ("a-hist", 120): (0.001546, 4),
    ("a-hist", 150): (0.004279, 4), ("a-hist", 240): (0.021882, 5), ("a-hist", 300): (0.039534, 5),
    ("a-hist", 400): (0.060552, 5), ("a-hist", 450): (0.063514, 5), ("a-hist", 600): (0.056830, 5),
    ("b-hist", 60): (1.6e-08, 2), ("b-hist", 113): (1.8e-05, 2), ("b-hist", 120): (3.0e-05, 2),
    ("b-hist", 150): (0.000157, 3), ("b-hist", 240): (0.001939, 4), ("b-hist", 300): (0.004937, 4),
    ("b-hist", 400): (0.013897, 5), ("b-hist", 450): (0.019730, 4), ("b-hist", 600): (0.037421, 5),
    ("c-hist", 60): (1.1e-11, 2), ("c-hist", 113): (9.6e-08, 2), ("c-hist", 120): (2.0e-07, 2),
    ("c-hist", 150): (2.7e-06, 2), ("c-hist", 240): (0.000226, 3), ("c-hist", 300): (0.001075, 4),
    ("c-hist", 400): (0.004845, 4), ("c-hist", 450): (0.007832, 4), ("c-hist", 600): (0.020446, 5),
}
REVF_O4 = {  # O4 rows (F_bl, sig figs)
    ("a-50:50", 150): (0.013341, 5), ("a-50:50", 600): (0.070041, 5),
    ("b-thirds", 150): (0.000450, 3), ("b-thirds", 600): (0.111332, 6),
    ("c-50:50", 150): (3.8e-06, 2), ("c-50:50", 600): (0.033809, 5),
}
REVF_E = {  # E[bl-support]
    ("a-hist", 150): 2.09, ("a-hist", 600): 25.66,
    ("b-hist", 150): 1.13, ("b-hist", 600): 10.30,
    ("c-hist", 150): 0.06, ("c-hist", 600): 4.71,
}


def global_s0(scen, N):
    ks = INRANGE[scen]
    if not ks:
        return 0.0
    if len(ks) == 2:
        p = SCEN[scen]
        return global2(N, p[ks[0]], p[ks[1]], FTABLE[("S0", ks[0])], FTABLE[("S0", ks[1])])
    p = SCEN[scen]
    probs = (p[5], p[10], p[20])
    ft = (FTABLE[("S0", 5)], FTABLE[("S0", 10)], FTABLE[("S0", 20)])
    if N <= 200:
        return global3_full(N, probs, ft)
    v, _ = global3_box(N, probs, ft)
    return v


t0 = time.time()
# Reference tables are rounded (1-4 sig figs); tolerances below are far
# tighter than any scientifically relevant difference (rules differ by
# orders of magnitude) and only accommodate reference rounding.
def sf_tol(ref, sf):
    """Half a unit in the reference's last significant place + fp epsilon."""
    return 0.51 * 10.0 ** (math.floor(math.log10(ref)) - sf + 1) + 1e-15


for (scen, N), (ref, sf) in sorted(REVF_BL.items()):
    got = global_s0(scen, N)
    ok = abs(got - ref) <= sf_tol(ref, sf)
    check(f"RevF F_bl {scen}@{N}", ok, f"got={got:.6g} ref={ref:.6g}")
for (scen, N), (ref, sf) in sorted(REVF_O4.items()):
    got = global_s0(scen, N)
    ok = abs(got - ref) <= sf_tol(ref, sf)
    check(f"RevF O4 {scen}@{N}", ok, f"got={got:.6g} ref={ref:.6g}")
print(f"S0 regression ({time.time()-t0:.1f}s)")


def e_support(scen, N):
    tot = 0.0
    for k in INRANGE[scen]:
        _, E = bucket_marginals(N, SCEN[scen][k], FTABLE[("S0", k)])
        tot += E
    return tot


for (scen, N), ref in sorted(REVF_E.items()):
    got = e_support(scen, N)
    check(f"RevF E[bl] {scen}@{N}", abs(got - ref) / ref < 5e-2, f"got={got:.4f} ref={ref}")

# ---- 4. full sensitivity grid ----------------------------------------------
t0 = time.time()
GRID = {}
for rule in RULES:
    for scen in SCEN:
        ks = INRANGE[scen]
        for N in NB:
            key = (rule, scen, N)
            if not ks:
                GRID[key] = {"F": 0.0, "structural": True}
                continue
            if len(ks) == 2:
                p = SCEN[scen]
                F = global2(N, p[ks[0]], p[ks[1]],
                            FTABLE[(rule, ks[0])], FTABLE[(rule, ks[1])])
                GRID[key] = {"F": F, "structural": False}
            else:
                p = SCEN[scen]
                probs = (p[5], p[10], p[20])
                ft = (FTABLE[(rule, 5)], FTABLE[(rule, 10)], FTABLE[(rule, 20)])
                if N <= 200:
                    GRID[key] = {"F": global3_full(N, probs, ft), "structural": False}
                else:
                    v, omit = global3_box(N, probs, ft)
                    GRID[key] = {"F": v, "structural": False, "omit_bound": omit}
print(f"global grid ({time.time()-t0:.1f}s)")

# bucket-marginal expectations + P(bucket passes) per (rule, scen, N, k)
MARG = {}
for rule in RULES:
    for scen in SCEN:
        for N in NB:
            for k in INRANGE[scen]:
                P, E = bucket_marginals(N, SCEN[scen][k], FTABLE[(rule, k)])
                MARG[(rule, scen, N, k)] = {"P": P, "E": E}

# ---- 5. fixed-size split: marginals (fresh-sample) + joint (2-bucket) -------
t0 = time.time()
SPLIT = {}
for N in NB:
    NTR, T = split_sizes(N)
    SPLIT[N] = {"NTR": NTR, "T": T}
    print(f"N={N}: NTR={NTR} T={T}")
check("split 113->28", SPLIT[113]["T"] == 28)
check("split 150->38", SPLIT[150]["T"] == 38)
check("split 450->113", SPLIT[450]["T"] == 113)
check("split 600->150", SPLIT[600]["T"] == 150)

# h-tables (scenario- and rule-independent): key (variant, N) -> dict
print("building h-tables (exact hypergeometric inclusion-exclusion)...")
HT = {}
for N in NB:
    NTR, T = SPLIT[N]["NTR"], SPLIT[N]["T"]
    for variant, fn in (("lib", h_joint_lib), ("cons", h_joint_cons)):
        t1 = time.time()
        tab = {}
        # only (a,b) with a,b>=8 contribute (f=0 elsewhere); bound other>=0
        for a in range(8, N + 1):
            for b in range(8, N - a + 1):
                o = N - a - b
                if NTR > N or NTR < 0:
                    h = 0.0
                else:
                    h = fn(a, b, o, NTR)
                if h > 0.0:
                    tab[(a, b)] = h
        HT[(variant, N)] = tab
        print(f"  h_{variant} N={N}: {len(tab)} entries ({time.time()-t1:.1f}s)")

t0 = time.time()
JOINT = {}
for rule in RULES:
    for scen in ("a-hist", "a-50:50", "c-hist", "c-50:50"):
        ks = INRANGE[scen]
        p = SCEN[scen]
        for N in NB:
            jl = joint2(N, p[ks[0]], p[ks[1]],
                        FTABLE[(rule, ks[0])], FTABLE[(rule, ks[1])],
                        HT[("lib", N)])
            jc = joint2(N, p[ks[0]], p[ks[1]],
                        FTABLE[(rule, ks[0])], FTABLE[(rule, ks[1])],
                        HT[("cons", N)])
            F = GRID[(rule, scen, N)]["F"]
            JOINT[(rule, scen, N)] = {"lib": jl, "cons": jc,
                                      "cond_lib": (jl / F if F > 0 else 0.0),
                                      "cond_cons": (jc / F if F > 0 else 0.0)}
print(f"joints 2-bucket ({time.time()-t0:.1f}s)")

# marginal train/test (re-application reading = fresh-sample globals)
MARG_SPLIT = {}
for rule in RULES:
    for scen in SCEN:
        ks = INRANGE[scen]
        for N in NB:
            NTR, T = SPLIT[N]["NTR"], SPLIT[N]["T"]
            if not ks:
                MARG_SPLIT[(rule, scen, N)] = {"train": 0.0, "test": 0.0}
                continue
            def _g(NN):
                if len(ks) == 2:
                    p = SCEN[scen]
                    return global2(NN, p[ks[0]], p[ks[1]],
                                  FTABLE[(rule, ks[0])], FTABLE[(rule, ks[1])])
                p = SCEN[scen]
                probs = (p[5], p[10], p[20])
                ft = (FTABLE[(rule, 5)], FTABLE[(rule, 10)], FTABLE[(rule, 20)])
                return global3_full(NN, probs, ft)
            MARG_SPLIT[(rule, scen, N)] = {"train": _g(NTR), "test": _g(T)}

# ---- 6. diagnostics ---------------------------------------------------------
DIAG = {}
for k in (5, 10, 20):
    vals, probs = CK[k]
    s = S2_STRATA[k]
    # P(bucket passes) at n = round(E[n_k]) for a scenario containing k
    rows = {}
    for N in (150, 600):
        scen = "b-hist" if k == 20 else "a-hist"
        pk = SCEN[scen][k]
        en = N * pk
        nn = int(round(en))
        # E[#distinct C] and P(observe global min/max) at nn
        e_dist = sum(1.0 - (1.0 - pv) ** nn for pv in probs)
        p_min = 1.0 - (1.0 - probs[0]) ** nn
        p_max = 1.0 - (1.0 - probs[-1]) ** nn
        rows[f"{scen}@{N}"] = {"E_n": en, "n": nn,
                               "E_distinct": e_dist,
                               "P_min": p_min, "P_max": p_max,
                               "f": {r: FTABLE[(r, k)][nn] for r in RULES}}
    DIAG[k] = {"vals": vals, "probs": probs,
               "low_vals": s["low_vals"], "high_vals": s["high_vals"],
               "p_low": s["p_low"], "p_mid": s["p_mid"], "p_high": s["p_high"],
               "rows": rows}

# redundancy: same global probability with vs without the B_min>=8 conjunct.
# S0 and S2(m>=4) imply n>=8 through disjoint >=4 counts, so B_min is
# redundant there; S1 and S2(m=2) do not imply it. Exact comparison.
from a1_support_comparison import f_s0_nomin, f_s2_nomin
RED = {}
FT_NOMIN = {}
for k in (5, 10, 20):
    FT_NOMIN[("S0", k)] = [f_s0_nomin(k, n) for n in range(NMAX + 1)]
    for m in (2, 4, 6):
        FT_NOMIN[(f"S2-m{m}", k)] = [f_s2_nomin(k, n, m) for n in range(NMAX + 1)]
for scen in ("a-hist", "b-hist", "c-hist"):
    ks = INRANGE[scen]
    p = SCEN[scen]
    for N in (150, 600):
        row = {}
        for rule in ("S0", "S2-m2", "S2-m4", "S2-m6"):
            if len(ks) == 2:
                g0 = global2(N, p[ks[0]], p[ks[1]],
                             FT_NOMIN[(rule, ks[0])], FT_NOMIN[(rule, ks[1])],
                             n_lo=0)
            else:
                probs = (p[5], p[10], p[20])
                ft = (FT_NOMIN[(rule, 5)], FT_NOMIN[(rule, 10)], FT_NOMIN[(rule, 20)])
                g0 = global3_full(N, probs, ft) if N <= 200 else global3_box(N, probs, ft)[0]
            g1 = GRID[(rule, scen, N)]["F"]
            row[rule] = {"with_Bmin": g1, "without_Bmin": g0}
        RED[(scen, N)] = row
print("redundancy done")

# ---- 7. outputs -------------------------------------------------------------
os.makedirs(OUT, exist_ok=True)


def jkey(t):
    return "|".join(str(x) for x in t)


tables = {
    "meta": {"rules": RULES, "scenarios": list(SCEN), "Nb": NB,
             "note": "N_b = fixed unique valid bodies; 113/450 plug-in proxies; "
                     "no sampling; exact enumeration (3-bucket N>200 truncated "
                     "with union-bound omission <=3e-15)."},
    "F_global": {jkey(k): v for k, v in GRID.items()},
    "marginal_bucket": {jkey(k): v for k, v in MARG.items()},
    "marginal_split": {jkey(k): v for k, v in MARG_SPLIT.items()},
    "joint_2bucket": {jkey(k): v for k, v in JOINT.items()},
    "redundancy_Bmin": {jkey(k): v for k, v in RED.items()},
    "split": {str(N): SPLIT[N] for N in NB},
    "diagnostics": DIAG,
}
with open(os.path.join(OUT, "a1_tables.json"), "w") as fh:
    json.dump(tables, fh, indent=1)

lines = []
lines.append("# A1 support-rule comparison — candidate results (deterministic)")
lines.append("")
lines.append("Scope: S0 vs S1(m) vs S2(m), m in {2,4,6}; B_min=8; 2<=k<=24.")
lines.append("S2 strata are the attainable-C candidate operationalization in the")
lines.append("module docstring (low z<=1/3, high z>=2/3 per k); NOT an owner decision.")
lines.append("N_b = fixed unique valid bodies. 113/450 are rho=0.25 plug-in proxies.")
lines.append("No rank/conditioning conjunct is applied: these are SUPPORT-ONLY")
lines.append("probabilities, not complete-rule or full-study feasibility.")
lines.append("")
for scen in SCEN:
    lines.append(f"## scenario {scen} (in-range buckets {INRANGE[scen] or 'none'})")
    lines.append("")
    lines.append("| rule | " + " | ".join(f"N={N}" for N in NB) + " |")
    lines.append("|---|---|---|---|---|")
    for rule in RULES:
        cells = []
        for N in NB:
            v = GRID[(rule, scen, N)]
            cells.append("0*" if v.get("structural") else f"{v['F']:.6g}")
        lines.append(f"| {rule} | " + " | ".join(cells) + " |")
    lines.append("")
lines.append("0* = structural zero (scenario (d) has no in-range mass).")
lines.append("3-bucket N=450/600 cells carry omission bound <=3e-15 (in JSON).")
lines.append("")
lines.append("## joint global/train/test (2-bucket scenarios; R-a + count-based test)")
lines.append("")
lines.append("TrainRa: training block has >=1 body in each globally-included bucket")
lines.append("and >=8 total in-support training bodies (global-membership reading).")
lines.append("TestLib1: >=1 test body per globally-included bucket.")
lines.append("TestCons8: >=8 test bodies per globally-included bucket (count-rule")
lines.append("re-application). Joint uses the exact fixed-size hypergeometric split;")
lines.append("marginals are never multiplied.")
lines.append("")
for scen in ("a-hist", "a-50:50", "c-hist", "c-50:50"):
    lines.append(f"### {scen}: P(Global & TrainRa & Test) and P(Test|Global)")
    lines.append("")
    lines.append("| rule | " + " | ".join(f"N={N} lib" for N in NB) + " |")
    lines.append("|---|---|---|---|---|")
    for rule in RULES:
        cells = [f"{JOINT[(rule, scen, N)]['lib']:.6g}" for N in NB]
        lines.append(f"| {rule} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("| rule | " + " | ".join(f"N={N} P(lib\\|G)" for N in NB) + " |")
    lines.append("|---|---|---|---|---|")
    for rule in RULES:
        cells = [f"{JOINT[(rule, scen, N)]['cond_lib']:.6g}" for N in NB]
        lines.append(f"| {rule} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("| rule | " + " | ".join(f"N={N} cons" for N in NB) + " |")
    lines.append("|---|---|---|---|---|")
    for rule in RULES:
        cells = [f"{JOINT[(rule, scen, N)]['cons']:.6g}" for N in NB]
        lines.append(f"| {rule} | " + " | ".join(cells) + " |")
    lines.append("")
lines.append("## B_min redundancy (exact: with vs without the >=8 conjunct)")
lines.append("")
lines.append("| scen@N | rule | with B_min | without B_min | redundant? |")
lines.append("|---|---|---|---|---|")
for key in sorted(RED):
    for rule in ("S0", "S2-m2", "S2-m4", "S2-m6"):
        w = RED[key][rule]["with_Bmin"]
        wo = RED[key][rule]["without_Bmin"]
        lines.append(f"| {key[0]}@{key[1]} | {rule} | {w:.6g} | {wo:.6g} | "
                     + ("yes" if abs(w - wo) <= 1e-12 * max(1.0, abs(w)) else "NO") + " |")
lines.append("")
lines.append("## exact-calculation limitations")
lines.append("")
lines.append("- 3-bucket joint global/train/test is NOT computed (C-subsample")
lines.append("  dependence across blocks needs full composition enumeration).")
lines.append("  Reported: exact marginals at NTR/T plus Frechet bounds")
lines.append("  [max(0,PG+PTR+... ), min(...)] in review text, not as estimates.")
lines.append("- R-b (within-block re-application of C conditions) joint likewise")
lines.append("  not computed; marginals at NTR/T are exact fresh-sample values.")
lines.append("- Double-precision log-space; terms < ~5e-324 recorded as 0-dagger")
lines.append("  (underflow), distinct from 0* structural zeros.")
with open(os.path.join(OUT, "a1_report.md"), "w") as fh:
    fh.write("\n".join(lines) + "\n")

print("wrote out/a1_tables.json and out/a1_report.md")
print("FAILURES:", fails if fails else "none")
sys.exit(1 if fails else 0)

