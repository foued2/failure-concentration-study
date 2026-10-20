"""Independent validator for the M2 complete-rule feasibility calculation.

This module deliberately does NOT import `m2_complete_rule_feasibility`. It rebuilds the
declared CK weights from the committed A1 support machinery, enumerates the minimal supports
with its own multinomial weighting, and computes kappa by materializing body-level rows and
using a direct singular-value decomposition. It then compares its values with the recorded
results in `m2_complete_rule_feasibility_2026-10-20.json`.

Run:
    python -B v03p/bridge/m2_complete_rule_feasibility_validate.py

Exit code 0 means all checked values agree within tolerance.
"""

import itertools
import json
import math
import sys

import numpy as np

sys.path.insert(0, "v03p/a1")
import a1_support_comparison as A1  # noqa: E402

def logfact(n):
    return math.lgamma(n + 1.0)


def multinomial_logpmf(counts, probs):
    n = sum(counts)
    t = logfact(n)
    for c, p in zip(counts, probs):
        t -= logfact(c)
        if c:
            if p <= 0.0:
                return float("-inf")
            t += c * math.log(p)
    return t


def design_matrix(k, counts, cvals):
    """Body-level extended matrix: [1, RCS1..RCS4, C]."""
    n = len(cvals)
    x = math.log(1.0 + k)
    # rcs_basis copied from study/models.py semantics, independently implemented here
    def pos(z):
        return z if z > 0.0 else 0.0

    knots = [1.0986122886681098, 1.6094379124341003, 2.302585092994046,
             2.995732273553991, 3.4339872044851463]
    t1, tk = knots[0], knots[-1]
    rcs = [x]
    for j in range(1, len(knots) - 1):
        tj = knots[j]
        d = ((pos(x - tj) ** 3 - pos(x - tk) ** 3)
             - ((tk - tj) / (tk - t1)) * (pos(x - t1) ** 3 - pos(x - tk) ** 3))
        rcs.append(d / (tk - t1) ** 2)
    mat = np.ones((n, 6))
    mat[:, 1:5] = np.tile(np.array(rcs), (n, 1))
    mat[:, 5] = np.array(cvals)
    return mat


def bucket_pass(counts):
    n = sum(counts)
    if n < 8:
        return False
    nz = [i for i, c in enumerate(counts) if c > 0]
    return len(nz) >= 2 and counts[nz[0]] >= 4 and counts[nz[-1]] >= 4


def count_vectors(n, V):
    def rec(i, rem, cur):
        if i == V - 1:
            yield tuple(cur + [rem])
            return
        for c in range(rem + 1):
            yield from rec(i + 1, rem - c, cur + [c])
    yield from rec(0, n, [])


def enumerate_support(nmap):
    ks = sorted(nmap)
    lists = []
    for k in ks:
        vals, probs = A1.CK[k]
        items = []
        for cnt in count_vectors(nmap[k], len(vals)):
            items.append((cnt, multinomial_logpmf(cnt, probs)))
        lists.append(items)
    p_pass = 0.0
    p_viol = 0.0
    total = 0.0
    n_pass = 0
    n_viol = 0
    for combo in itertools.product(*lists):
        logp = sum(x[1] for x in combo)
        if logp <= -745.0:
            continue
        w = math.exp(logp)
        total += w
        ps = [bucket_pass(x[0]) for x in combo]
        if sum(ps) < 2:
            continue
        p_pass += w
        n_pass += 1
        mats = []
        for k, item in zip(ks, combo):
            vals, _ = A1.CK[k]
            cvals = []
            for c, v in zip(item[0], vals):
                cvals.extend([v] * c)
            mats.append(design_matrix(k, item[0], cvals))
        mat = np.vstack(mats)
        kk = float("inf")
        for j in range(1, 6):
            col = mat[:, j]
            mu = col.mean()
            sd = col.std(ddof=0)
            if sd <= 0.0:
                break
            mat[:, j] = (col - mu) / sd
        else:
            sv = np.linalg.svd(mat, compute_uv=False)
            rank = int(np.sum(sv > 1e-9 * sv[0]))
            if rank >= 2:
                kk = float(sv[0] / sv[rank - 1])
        if kk > 30.0:
            p_viol += w
            n_viol += 1
    return {
        "bucket_n": {str(k): nmap[k] for k in ks},
        "P_pass": p_pass,
        "P_pass_and_kappa_gt_30": p_viol,
        "patterns_total_probability": total,
        "patterns_passing": n_pass,
        "patterns_violating": n_viol,
    }


def kappa_recorded_patterns():
    tests = [
        ([5, 10], [(0, 0, 0, 4, 4), (4, 4, 0, 0)], 10.481693469786787),
        ([5, 10], [(0, 0, 0, 4, 12), (12, 4, 0, 0)], 13.395997941033501),
        ([5, 10, 20], [(0, 0, 0, 4, 4), (4, 4, 0, 0), (4, 4)],
         36.08794233527171),
    ]
    out = []
    for ks, counts, want in tests:
        mats = []
        for k, cnt in zip(ks, counts):
            vals, _ = A1.CK[k]
            cvals = []
            for c, v in zip(cnt, vals):
                cvals.extend([v] * c)
            mats.append(design_matrix(k, cnt, cvals))
        mat = np.vstack(mats)
        for j in range(1, 6):
            col = mat[:, j]
            mat[:, j] = (col - col.mean()) / col.std(ddof=0)
        sv = np.linalg.svd(mat, compute_uv=False)
        rank = int(np.sum(sv > 1e-9 * sv[0]))
        got = float(sv[0] / sv[rank - 1])
        out.append({"pattern": counts, "want": want, "got": got,
                    "abs_diff": abs(got - want)})
    return out


def main():
    ref = json.load(open("v03p/bridge/m2_complete_rule_feasibility_2026-10-20.json",
                         encoding="utf-8"))
    ref_small = {tuple(sorted(x["bucket_n"].items())): x
                 for x in ref["small_support_gate"]}
    checks = []
    for nmap in ({5: 8, 10: 8}, {5: 8, 10: 8, 20: 8}):
        got = enumerate_support(nmap)
        key = tuple(sorted((str(k), v) for k, v in nmap.items()))
        want = ref_small[key]
        checks.append({
            "support": got["bucket_n"],
            "P_pass": got["P_pass"],
            "P_pass_ref": want["P_pass"],
            "P_pass_abs_diff": abs(got["P_pass"] - want["P_pass"]),
            "P_viol": got["P_pass_and_kappa_gt_30"],
            "P_viol_ref": want["P_pass_and_kappa_gt_30"],
            "P_viol_abs_diff": abs(got["P_pass_and_kappa_gt_30"]
                                   - want["P_pass_and_kappa_gt_30"]),
            "mass": got["patterns_total_probability"],
        })
    kap = kappa_recorded_patterns()
    ok = (all(x["P_pass_abs_diff"] < 1e-9 and x["P_viol_abs_diff"] < 1e-12
              for x in checks)
          and all(x["abs_diff"] < 1e-8 for x in kap)
          and all(abs(x["mass"] - 1.0) < 1e-9 for x in checks))
    result = {"checks": checks, "kappa_checks": kap, "ok": ok}
    print(json.dumps(result, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
