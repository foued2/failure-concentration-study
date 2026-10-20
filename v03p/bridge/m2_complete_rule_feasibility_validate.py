"""Independent validator for the M2 complete-rule feasibility calculation.

This module deliberately does NOT import `m2_complete_rule_feasibility`. It rebuilds the
declared CK weights from the committed A1 support machinery, enumerates the minimal supports
with its own multinomial weighting, and computes kappa by materializing body-level rows and
using a direct singular-value decomposition. It then compares its values with the recorded
results in `m2_complete_rule_feasibility_2026-10-20.json`.

Run:
    py -3.14 -B v03p/bridge/m2_complete_rule_feasibility_validate.py

Exit code 0 means all checked values agree within tolerance.
"""

import itertools
import json
import math
import os
import re
import sys

import numpy as np

sys.path.insert(0, "v03p/a1")
import a1_support_comparison as A1  # noqa: E402

REPS = 2000
FLOOR = 39
PROB_TARGET = 0.95
REPORT_PATH = "v03p/bridge/M2_COMPLETE_RULE_FEASIBILITY_2026-10-20.md"
TABLE_SCENARIOS = ("a-hist", "b-hist", "c-hist")
TABLE_SIZES = (60, 120, 113, 150, 240, 300, 400, 450, 600)
TABLE_ARMS = {"rho=0 unique": "fixed_unique_rho_0",
              "rho=.25 slots": "attempt_copy_rho_0_25"}
TABLE_LABELS = {"both_rules_ruled_out": "both_candidate_rules_ruled_out",
                "P_rule_ruled_out": "probability_rule_ruled_out",
                "not_certified": "not_certified_no_complete_rule_lower_bound"}
TABLE_ROW_RE = re.compile(
    r"^\|\s*([a-z]-hist)\s*/\s*(\d+)\s*"
    r"\|\s*(rho=0 unique|rho=\.25 slots)\s*"
    r"\|\s*\[([0-9.eE+-]+),\s*([0-9.eE+-]+)\]\s*"
    r"\|\s*([0-9.eE+-]+)\s*"
    r"\|\s*([0-9.eE+-]+)\s*"
    r"\|\s*(both_rules_ruled_out|P_rule_ruled_out|not_certified)\s*\|\s*$"
)


def logfact(n):
    return math.lgamma(n + 1.0)


def binom_pmf_local(n, k, p):
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    if k < 0 or k > n:
        return 0.0
    t = (logfact(n) - logfact(k) - logfact(n - k)
         + k * math.log(p) + (n - k) * math.log1p(-p))
    return math.exp(t) if t > -745.0 else 0.0


def binom_sf_local(m, n, p):
    if m < 0:
        return 1.0
    if m >= n:
        return 0.0
    return sum(binom_pmf_local(n, i, p) for i in range(m + 1, n + 1))


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


_FS0_CACHE = {}


def fs0(k, n):
    key = (k, n)
    if key not in _FS0_CACHE:
        _FS0_CACHE[key] = A1.f_s0(k, n)
    return _FS0_CACHE[key]


_EXACT_CELL_CACHE = {}


def exact_support(scenario, nb):
    """Exact conditions 1-4 probability over all bucket counts (no count box)."""
    key = (scenario, nb)
    if key in _EXACT_CELL_CACHE:
        return _EXACT_CELL_CACHE[key]
    ks = list(A1.INRANGE[scenario])
    if len(ks) < 2:
        _EXACT_CELL_CACHE[key] = 0.0
        return 0.0
    probs = [A1.SCEN[scenario][k] for k in ks]
    p_other = 1.0 - sum(probs)
    total = 0.0

    def rec(i, rem, cur):
        nonlocal total
        if i == len(ks):
            other = rem
            if p_other <= 0.0 and other > 0:
                return
            lp = logfact(nb) - logfact(other)
            for c in cur:
                lp -= logfact(c)
            for c, p in zip(cur, probs):
                if c:
                    lp += c * math.log(p)
            if other:
                lp += other * math.log(p_other)
            if lp <= -745.0:
                return
            fs = [fs0(k, c) for k, c in zip(ks, cur)]
            q = sum(fs[a] * fs[b] for a in range(len(fs))
                    for b in range(a + 1, len(fs)))
            if len(fs) == 3:
                q -= 2.0 * fs[0] * fs[1] * fs[2]
            total += math.exp(lp) * q
            return
        for c in range(rem + 1):
            rec(i + 1, rem - c, cur + [c])

    rec(0, nb, [])
    _EXACT_CELL_CACHE[key] = total
    return total


def check_cell_schema(ref):
    errors = []
    for cell in ref["cells"]:
        if "structural" in cell:
            continue
        tail = cell["box_tail_bound"]
        for name, arm in cell["arms"].items():
            tag = "%s@%s/%s" % (cell["scenario"], cell["N_b"], name)
            pl = arm["P_support_lower"]
            pu = arm["P_support_upper"]
            if not (0.0 <= pl <= pu <= 1.0):
                errors.append(tag + " support interval order")
            if abs(arm["E_support_lower"] - REPS * pl) > 1e-9:
                errors.append(tag + " E lower")
            if abs(arm["E_support_upper"] - REPS * pu) > 1e-9:
                errors.append(tag + " E upper")
            want_lo = binom_sf_local(FLOOR - 1, REPS, pl)
            want_hi = binom_sf_local(FLOOR - 1, REPS, pu)
            if abs(arm["P_N_ge_39_support_lower"] - want_lo) > 1e-9:
                errors.append(tag + " P39 support lower")
            if abs(arm["P_N_ge_39_support_upper"] - want_hi) > 1e-9:
                errors.append(tag + " P39 support upper")
            if arm["P_complete_lower"] != 0.0:
                errors.append(tag + " complete lower not zero")
            if abs(arm["P_complete_upper"] - pu) > 1e-15:
                errors.append(tag + " complete upper != support upper")
            if abs(arm["E_complete_upper"] - REPS * pu) > 1e-9:
                errors.append(tag + " complete E upper")
            if arm["P_N_ge_39_complete_lower"] != 0.0:
                errors.append(tag + " complete P39 lower not zero")
            if abs(arm["P_N_ge_39_complete_upper"] - want_hi) > 1e-9:
                errors.append(tag + " complete P39 upper")
            exp_status = ("ruled_out" if REPS * pu < FLOOR
                          else "not_certified")
            prob_status = ("ruled_out" if want_hi < PROB_TARGET
                           else "not_certified")
            if arm["o3_expected_count_status"] != exp_status:
                errors.append(tag + " expected-count label")
            if arm["o3_probability_status"] != prob_status:
                errors.append(tag + " probability label")
            if name == "fixed_unique_rho_0":
                if arm["rho"] != 0.0 or arm["N_b_semantics"] != "unique_bodies":
                    errors.append(tag + " fixed arm semantics")
                if abs((pu - pl) - tail) > 1e-15:
                    errors.append(tag + " fixed tail interval mismatch")
            else:
                if arm["rho"] != 0.25 or arm["N_b_semantics"] != "attempt_slots":
                    errors.append(tag + " duplicate arm semantics")
                if abs(arm["M_mean"] - (1.0 + (cell["N_b"] - 1) * 0.75)) > 1e-12:
                    errors.append(tag + " M mean")
                if abs(pl - arm["p_lower"]) > 1e-15 or abs(pu - arm["p_upper"]) > 1e-15:
                    errors.append(tag + " duplicate p aliases")
                implied_tail = max(0.0, pu - pl)
                if arm["tail_mixture"] > implied_tail + 1e-15:
                    errors.append(tag + " duplicate tail mixture")
    return errors


def check_exact_cells(ref):
    by_key = {(c["scenario"], c["N_b"]): c for c in ref["cells"]}
    checks = []
    for scenario, nb in (("a-hist", 60), ("a-hist", 120),
                         ("b-hist", 60), ("c-hist", 60),
                         ("c-hist", 120)):
        exact = exact_support(scenario, nb)
        cell = by_key[(scenario, nb)]
        fixed = cell["arms"]["fixed_unique_rho_0"]
        ok_contain = (fixed["P_support_lower"] - 1e-15 <= exact
                      <= fixed["P_support_upper"] + 1e-15)
        gap = exact - fixed["P_support_lower"]
        checks.append({
            "scenario": scenario,
            "N_b": nb,
            "P_exact": exact,
            "P_lower": fixed["P_support_lower"],
            "P_upper": fixed["P_support_upper"],
            "box_tail": cell["box_tail_bound"],
            "contained": ok_contain,
            "outside_box_mass": gap,
            "outside_within_tail": gap <= cell["box_tail_bound"] + 1e-15,
        })
    return checks


def check_exact_duplicate(ref, scenario="a-hist", nb=60):
    cell = next(c for c in ref["cells"]
                if c["scenario"] == scenario and c["N_b"] == nb)
    arm = cell["arms"]["attempt_copy_rho_0_25"]
    mix = 0.0
    mass = 0.0
    for m in range(1, nb + 1):
        pmf = A1.binom_pmf(nb - 1, m - 1, 0.75)
        if pmf == 0.0:
            continue
        mix += pmf * exact_support(scenario, m)
        mass += pmf
    mix = mix + max(0.0, 1.0 - mass)
    return {
        "scenario": scenario,
        "N_b": nb,
        "P_mixture_exact": mix,
        "P_lower": arm["P_support_lower"],
        "P_upper": arm["P_support_upper"],
        "contained": (arm["P_support_lower"] - 1e-15 <= mix
                      <= arm["P_support_upper"] + 1e-15),
        "mixture_mass": mass,
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


def check_report_tables(ref):
    by_key = {(c["scenario"], c["N_b"]): c for c in ref["cells"]}
    expected = {(scenario, nb, arm)
                for scenario in TABLE_SCENARIOS
                for nb in TABLE_SIZES
                for arm in TABLE_ARMS}
    seen = set()
    errors = []
    n_rows = 0
    with open(REPORT_PATH, encoding="utf-8") as handle:
        for line in handle:
            match = TABLE_ROW_RE.match(line.strip())
            if not match:
                continue
            n_rows += 1
            scenario = match.group(1)
            nb = int(match.group(2))
            arm_name = match.group(3)
            lower = float(match.group(4))
            upper = float(match.group(5))
            e_upper = float(match.group(6))
            p_upper = float(match.group(7))
            label = match.group(8)
            key = (scenario, nb, arm_name)
            tag = "%s@%s/%s" % (scenario, nb, arm_name)
            if key not in expected:
                errors.append(tag + " unexpected table row")
                continue
            if key in seen:
                errors.append(tag + " duplicate table row")
                continue
            seen.add(key)
            if (scenario, nb) not in by_key:
                errors.append(tag + " missing JSON cell")
                continue
            arm = by_key[(scenario, nb)]["arms"][TABLE_ARMS[arm_name]]
            if lower > upper:
                errors.append(tag + " report interval order")
            for got, want, floor, field in (
                (lower, arm["P_support_lower"], 5e-15, "P lower"),
                (upper, arm["P_support_upper"], 5e-15, "P upper"),
                (e_upper, arm["E_complete_upper"], 5e-5, "E upper"),
                (p_upper, arm["P_N_ge_39_complete_upper"], 5e-15,
                 "P39 upper"),
            ):
                if abs(got - want) > max(floor, 5e-4 * abs(want)):
                    errors.append(tag + " report " + field)
            if TABLE_LABELS[label] != arm["o3_label"]:
                errors.append(tag + " report O3 label")
    missing = sorted(expected - seen)
    if missing:
        errors.append("missing table rows: %d" % len(missing))
    return {
        "errors": errors,
        "n_rows": n_rows,
        "n_expected": len(expected),
        "missing": ["%s@%s/%s" % x for x in missing],
    }


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
    schema_errors = check_cell_schema(ref)
    exact_cells = check_exact_cells(ref)
    duplicate_check = check_exact_duplicate(ref)
    report_check = check_report_tables(ref)
    ok = (all(x["P_pass_abs_diff"] < 1e-9 and x["P_viol_abs_diff"] < 1e-12
              for x in checks)
          and all(x["abs_diff"] < 1e-8 for x in kap)
          and all(abs(x["mass"] - 1.0) < 1e-9 for x in checks)
          and not schema_errors
          and all(x["contained"] and x["outside_within_tail"] for x in exact_cells)
          and duplicate_check["contained"]
          and not report_check["errors"])
    result = {
        "small_support_checks": checks,
        "kappa_checks": kap,
        "cell_schema_checks": {"errors": schema_errors,
                               "n_cells": len(ref["cells"])},
        "exact_cell_checks": exact_cells,
        "duplicate_mixture_check": duplicate_check,
        "report_table_check": report_check,
        "validated_scope": [
            "independent small-support (8,8) and (8,8,8) pass/violation probabilities",
            "three recorded kappa patterns",
            "cell interval algebra, complete-rule upper bound, O3 labels",
            "exact no-box support at selected cells; exact duplicate mixture at a-hist@60",
            "report candidate/planning table rows against the JSON",
        ],
        "not_validated": [
            "large-n three-bucket complete-rule lower bound",
            "independent enumeration of every cell",
            "natural-solver sampling distribution",
        ],
        "ok": ok,
    }
    print(json.dumps(result, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
