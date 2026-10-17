"""TEMP PROBE (not part of the O2 package; do not push): M3 conditioning stress.

Verifies the M3 conditioning statistic on the S1-m4-admissible training
patterns for GPT's Options A and B (message of 2026-10-17), under the
CVD-atleastone reading of the complete rule (and the CVD-each variant).

Inputs: A1 rev 3 CK distributions (read-only import).
Output: stdout report + m3_cond_results.json in the same temp folder.

Row set (stated assumption): training design = the t5 + t10 training-block
bodies whose k in {5, 10}; t5,t10 >= 1; t5+t10 >= 8 (TrainRa).
"""
import sys, math, json, time

A1 = r"C:\Users\pakla\PycharmProjects\failure-concentration-study\v03p\a1"
sys.path.insert(0, A1)
import a1_support_comparison as A

OUT = r"C:\Users\pakla\AppData\Local\Temp\opencode\m3_cond"
NTRS = [("N=113", 85), ("N=150", 112), ("N=450", 337), ("N=600", 450)]


# ---------------- moments ----------------
def mom(vals, probs):
    m = sum(v * p for v, p in zip(vals, probs))
    v = sum(p * (x - m) ** 2 for x, p in zip(vals, probs))
    return m, math.sqrt(v)


v5, p5 = A.CK[5]
v10, p10 = A.CK[10]
m5, s5 = mom(v5, p5)
m10, s10 = mom(v10, p10)
m_pool = (m5 + m10) / 2.0
s_pool = math.sqrt(((s5 ** 2 + (m5 - m_pool) ** 2) +
                    (s10 ** 2 + (m10 - m_pool) ** 2)) / 2.0)
s_within = math.sqrt((s5 ** 2 + s10 ** 2) / 2.0)
d5 = min(b - a for a, b in zip(v5, v5[1:]))
d10 = min(b - a for a, b in zip(v10, v10[1:]))

print("== reference moments (A1 rev3, unconditioned C|k) ==")
print(f"k=5 : mean {m5:.5f}  sd {s5:.5f}   (GPT: 0.52857 / 0.16225)")
print(f"k=10: mean {m10:.5f}  sd {s10:.5f}   (GPT: 0.40774 / 0.07712)")
print(f"pooled (equal type weights): mean {m_pool:.5f} sd {s_pool:.5f}"
      f"   (GPT: 0.46816 / 0.14067)")
print(f"pooled within-bucket sd: {s_within:.5f}   (GPT: 0.12703)")
print(f"attainable gaps: d5={d5:.3f}  d10={d10:.3f}")

print("\n== collinearity of pooled C with k10 indicator "
      "(scenario weights w = P(k10 | included)) ==")
rho_rows = []
for w in (1.0 / 3.0, 0.4, 0.5):
    mu_w = (1 - w) * m5 + w * m10
    sw2 = (1 - w) * s5 ** 2 + w * s10 ** 2 + w * (1 - w) * (m5 - m10) ** 2
    sw = math.sqrt(sw2)
    rho = (m10 - mu_w) * math.sqrt(w / (1 - w)) / sw
    vif = 1.0 / (1.0 - rho ** 2)
    rho_rows.append({"w10": w, "rho": rho, "vif": vif})
    print(f"w10={w:.3f}: corr={rho:+.4f}  VIF={vif:.4f}")
print("GPT stated range: corr -0.38..-0.43, VIF 1.17..1.23")
print("(w10 = 1/3 a-hist, 0.4 c-hist, 0.5 50:50 scenarios)")

print("\n== minimum within-bucket residual variation (min-gap, two-point) ==")
print("SS_min per varying bucket of train size t: (delta_k^2)*(t-1)/t")
for t in (2, 8, 43, 225, 449):
    print(f"  t={t:4d}: k5 delta=.2 -> SS={0.04*(t-1)/t:.6f}   "
          f"k10 delta=.1 -> SS={0.01*(t-1)/t:.6f}")
print(f"scaled by 1/s_within^2 = {1.0/s_within**2:.5f}")


# ---------------- 3x3 symmetric eigenvalues ----------------
def eig_bounds(a11, a12, a13, a22, a23, a33):
    tr = a11 + a22 + a33
    q = tr / 3.0
    p1 = a12 * a12 + a13 * a13 + a23 * a23
    p2 = (a11 - q) ** 2 + (a22 - q) ** 2 + (a33 - q) ** 2 + 2.0 * p1
    if p2 <= 0.0:
        return q, q
    p = math.sqrt(p2 / 6.0)
    b11 = (a11 - q) / p
    b12 = a12 / p
    b13 = a13 / p
    b22 = (a22 - q) / p
    b23 = a23 / p
    b33 = (a33 - q) / p
    det = (b11 * (b22 * b33 - b23 * b23)
           - b12 * (b12 * b33 - b23 * b13)
           + b13 * (b12 * b23 - b22 * b13))
    r = max(-1.0, min(1.0, det / 2.0))
    phi = math.acos(r) / 3.0
    e1 = q + 2.0 * p * math.cos(phi)
    e3 = q + 2.0 * p * math.cos(phi + 2.0943951023931953)
    e2 = 3.0 * q - e1 - e3
    return max(e1, e2, e3), min(e1, e2, e3)


# ---------------- Option B: closed form ----------------
def scanB(NTR):
    best = {k: (-1.0, None) for k in ("any_i", "any_ii", "each_i", "each_ii")}
    cnt = {k: 0 for k in best}
    for t5 in range(1, NTR):
        for t10 in range(max(1, 8 - t5), NTR - t5 + 1):
            n = t5 + t10
            v5_ = 0.64 * (t5 * t5 // 4) / t5 / s_within ** 2 if t5 >= 2 else 0.0
            v10_ = 0.09 * (t10 * t10 // 4) / t10 / s_within ** 2 if t10 >= 2 else 0.0
            cands = []
            if t10 >= 2:
                cands.append(0.01 * (t10 - 1) / t10 / s_within ** 2)
            if t5 >= 2:
                cands.append(0.04 * (t5 - 1) / t5 / s_within ** 2)
            c = min(cands)
            cmax = max(v5_, v10_)
            tr = n + t10
            disc = math.sqrt(tr * tr - 4.0 * t5 * t10)
            lp = (tr + disc) / 2.0
            lm = (tr - disc) / 2.0

            def kappa1(cc):
                return math.sqrt(max(lp, cc) / min(lm, cc))

            def kappa2(cc):
                return math.sqrt(max(t5, t10, cc) / min(t5, t10, cc))

            for key, kfun in (("any_i", kappa1), ("any_ii", kappa2)):
                kk = max(kfun(c), kfun(cmax))
                if kk > best[key][0]:
                    best[key] = (kk, (t5, t10, round(c, 4), round(cmax, 4)))
                if kk > 30.0:
                    cnt[key] += 1
            if t5 >= 2 and t10 >= 2:
                c2 = (0.04 * (t5 - 1) / t5 + 0.01 * (t10 - 1) / t10) \
                    / s_within ** 2
                cmax2 = v5_ + v10_
                for key, kfun in (("each_i", kappa1), ("each_ii", kappa2)):
                    kk = max(kfun(c2), kfun(cmax2))
                    if kk > best[key][0]:
                        best[key] = (kk, (t5, t10, round(c2, 4), round(cmax2, 4)))
                    if kk > 30.0:
                        cnt[key] += 1
    return best, cnt


# ---------------- Option A: per-combo aggregates, linear in (t5,t10) ----------
def agg_k10var(u, c5):
    return dict(aS=d10, bS=c5, gS=u,
                aQ=2 * u * d10 + d10 * d10, bQ=c5 * c5, gQ=u * u,
                aS5=0.0, bS5=c5, gS5=0.0, aS10=d10, bS10=0.0, gS10=u)


def agg_k5var(u5, c10):
    return dict(aS=d5, bS=u5, gS=c10,
                aQ=2 * u5 * d5 + d5 * d5, bQ=u5 * u5, gQ=c10 * c10,
                aS5=d5, bS5=u5, gS5=0.0, aS10=0.0, bS10=0.0, gS10=c10)


def agg_both(u5, u10):
    return dict(aS=d5 + d10, bS=u5, gS=u10,
                aQ=2 * u5 * d5 + d5 * d5 + 2 * u10 * d10 + d10 * d10,
                bQ=u5 * u5, gQ=u10 * u10,
                aS5=d5, bS5=u5, gS5=0.0, aS10=d10, bS10=0.0, gS10=u10)


def combos():
    out = []
    for u in (0.2, 0.3, 0.4):
        for c5 in (0.2, 0.6, 1.0):
            out.append((f"k10v u={u} c5={c5}", agg_k10var(u, c5), False, True))
    for u5 in (0.2, 0.4, 0.8):
        for c10 in (0.2, 0.5):
            out.append((f"k5v u={u5} c10={c10}", agg_k5var(u5, c10), True, False))
    for u5, u10 in ((0.2, 0.2), (0.2, 0.3), (0.4, 0.3), (0.8, 0.3)):
        out.append((f"both u5={u5} u10={u10}", agg_both(u5, u10), True, True))
    return out


COMBOS = combos()


def scanA(NTR, centered=True):
    best_i = (-1.0, None)
    best_ii = (-1.0, None)
    best_ni = (-1.0, None)
    best_nii = (-1.0, None)
    cnt_i = cnt_ii = cnt_ni = cnt_nii = 0
    for t5 in range(1, NTR):
        for t10 in range(max(1, 8 - t5), NTR - t5 + 1):
            n = t5 + t10
            bi = bii = bni = bnii = -1.0
            for name, c, need5, need10 in COMBOS:
                if (need5 and t5 < 2) or (need10 and t10 < 2):
                    continue
                S = c["aS"] + c["bS"] * t5 + c["gS"] * t10
                Q = c["aQ"] + c["bQ"] * t5 + c["gQ"] * t10
                S5 = c["aS5"] + c["bS5"] * t5 + c["gS5"] * t10
                S10 = c["aS10"] + c["bS10"] * t5 + c["gS10"] * t10
                if centered:
                    Z = (S - n * m_pool) / s_pool
                    Z5 = (S5 - t5 * m_pool) / s_pool
                    Z10 = (S10 - t10 * m_pool) / s_pool
                    ZQ = (Q - 2.0 * m_pool * S + n * m_pool ** 2) / s_pool ** 2
                else:
                    Z = S / s_pool
                    Z5 = S5 / s_pool
                    Z10 = S10 / s_pool
                    ZQ = Q / s_pool ** 2
                lm, lmn = eig_bounds(n, t10, Z, t10, Z10, ZQ)
                kk = math.sqrt(lm / lmn) if lmn > 0 else float("inf")
                if kk > bi:
                    bi, bi_name = kk, name
                lm2, lmn2 = eig_bounds(t5, 0.0, Z5, t10, Z10, ZQ)
                kk2 = math.sqrt(lm2 / lmn2) if lmn2 > 0 else float("inf")
                if kk2 > bii:
                    bii, bii_name = kk2, name
                d1, d2, d3 = n, t10, ZQ
                if d1 > 0 and d2 > 0 and d3 > 0:
                    s1, s2, s3 = math.sqrt(d1), math.sqrt(d2), math.sqrt(d3)
                    lm3, lmn3 = eig_bounds(1.0, t10 / (s1 * s2), Z / (s1 * s3),
                                           1.0, Z10 / (s2 * s3), 1.0)
                    kk3 = math.sqrt(lm3 / lmn3) if lmn3 > 0 else float("inf")
                    if kk3 > bni:
                        bni, bni_name = kk3, name
                d1, d2, d3 = t5, t10, ZQ
                if d1 > 0 and d2 > 0 and d3 > 0:
                    s1, s2, s3 = math.sqrt(d1), math.sqrt(d2), math.sqrt(d3)
                    lm4, lmn4 = eig_bounds(1.0, 0.0, Z5 / (s1 * s3),
                                           1.0, Z10 / (s2 * s3), 1.0)
                    kk4 = math.sqrt(lm4 / lmn4) if lmn4 > 0 else float("inf")
                    if kk4 > bnii:
                        bnii, bnii_name = kk4, name
            if bi > best_i[0]:
                best_i = (bi, (t5, t10, bi_name))
            if bii > best_ii[0]:
                best_ii = (bii, (t5, t10, bii_name))
            if bni > best_ni[0]:
                best_ni = (bni, (t5, t10, bni_name))
            if bnii > best_nii[0]:
                best_nii = (bnii, (t5, t10, bnii_name))
            if bi > 30.0:
                cnt_i += 1
            if bii > 30.0:
                cnt_ii += 1
            if bni > 30.0:
                cnt_ni += 1
            if bnii > 30.0:
                cnt_nii += 1
    return (best_i, best_ii, best_ni, best_nii, cnt_i, cnt_ii, cnt_ni, cnt_nii)


results = {"moments": {"m5": m5, "s5": s5, "m10": m10, "s10": s10,
                       "m_pool": m_pool, "s_pool": s_pool,
                       "s_within": s_within, "d5": d5, "d10": d10},
           "rho_vif": rho_rows, "B": {}, "A": {}}

print("\n== Option B worst case over admissible (t5,t10) and min-variation "
      "patterns ==")
print("coding i  = [1, I(k10), C_perp/s_within]   "
      "coding ii = [I(k5), I(k10), C_perp/s_within]")
print("variant 'any' = CVD-atleastone; 'each' = both buckets vary")
for label, NTR in NTRS:
    t0 = time.time()
    best, cnt = scanB(NTR)
    dt = time.time() - t0
    print(f"\n{label} (NTR={NTR}, {dt:.1f}s)")
    for k in ("any_i", "any_ii", "each_i", "each_ii"):
        kk, arg = best[k]
        flag = " ** >30 **" if kk > 30.0 else ""
        print(f"  {k:8s}: max kappa2 = {kk:7.2f} at (t5,t10,c)={arg}"
              f"  grid points>30: {cnt[k]}{flag}")
    results["B"][label] = {k: {"max": best[k][0], "arg": best[k][1],
                               "n_gt30": cnt[k]} for k in best}

print("\n== Option B, unit-column-scaled (pure collinearity view) ==")
print("coding i : kappa2 = sqrt((1+r)/(1-r)), r = sqrt(t5*t10)/(t5+t10) "
      "(pattern-independent, max sqrt(3)=1.732 at balanced split)")
print("coding ii: kappa2 = 1.0 exactly (C_perp orthogonal to both dummies)")

print("\n== Option A worst case (standardized by pooled reference moments; "
      "min-gap pattern family; 'raw' vs unit-column-scaled design) ==")
for label, NTR in NTRS:
    t0 = time.time()
    (bi, bii, bni, bnii, ci, cii, cni, cnii) = scanA(NTR, centered=True)
    dt = time.time() - t0
    print(f"\n{label} (NTR={NTR}, {dt:.1f}s)")
    for nm, (kk, arg), cn in (("A_i  raw ", bi, ci), ("A_ii raw ", bii, cii),
                              ("A_i  norm", bni, cni), ("A_ii norm", bnii, cnii)):
        flag = " ** >30 **" if kk > 30.0 else ""
        print(f"  {nm}: max kappa2 = {kk:7.2f} at {arg}"
              f"  grid points>30: {cn}{flag}")
    results["A"].setdefault(label, {})["i_centered"] = {"max": bi[0], "arg": bi[1], "n_gt30": ci}
    results["A"][label]["ii_centered"] = {"max": bii[0], "arg": bii[1], "n_gt30": cii}
    results["A"][label]["i_normalized"] = {"max": bni[0], "arg": bni[1], "n_gt30": cni}
    results["A"][label]["ii_normalized"] = {"max": bnii[0], "arg": bnii[1], "n_gt30": cnii}

t0 = time.time()
(biu, _, _, _, ciu, _, _, _) = scanA(450, centered=False)
print(f"\nSensitivity, N=600, coding i without centering (raw): max kappa2 = "
      f"{biu[0]:7.2f} at {biu[1]} (grid>30: {ciu})  [{time.time()-t0:.1f}s]")
results["A"].setdefault("N=600", {})["i_uncentered"] = {"max": biu[0], "arg": biu[1], "n_gt30": ciu}
results["B"]["normalized"] = {"coding_i_max": math.sqrt(3.0), "coding_ii": 1.0}

with open(OUT + r"\m3_cond_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=1)
print("\nsaved: m3_cond_results.json")
