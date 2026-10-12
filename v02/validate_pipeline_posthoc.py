"""POST-HOC SOFTWARE DIAGNOSTIC (2026-10-12). Synthetic data only.

Run after primary-statistic exposure (see INTEGRITY_REVIEW_2026-10-12.md §1).
Does not read real study observations, does not alter the real-data model,
threshold, classification rule, or results. Per GPT GO §3: if a check fails,
stop and report the limitation — do not adapt the analysis.

Checks:
  P1 positive control  — planted C-signal beyond k must be detected (delta > delta_threshold, ci_lo > threshold)
  P2 count-only control — y depends only on k, C uninformative: |delta| < threshold
  P3 classify()        — frozen decision branches, exact expected labels
  P4 bootstrap         — degenerate input -> degenerate CI
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from models_v02 import bootstrap_ci, build_pairs, classify, loo_delta_pairs, relabel_control

DELTA = 0.01
RESULTS: list[dict] = []


def _fails(k: int, spread: bool) -> list[bool]:
    """30-slot fail vector. spread=False: all fails inside family 1 (C=1.0).
    spread: one fail per family (C=1/k). Special k=2/C=0.5: split across two families."""
    f = [False] * 30
    if k == 2 and not spread:  # C = 2/2 = 1.0
        f[0] = f[1] = True
    elif k == 2 and spread:  # one in F1, one in F2 -> C = 1/2
        f[0] = f[5] = True
    elif not spread:  # k=4, all in family 1 -> C = 1.0
        for i in range(k):
            f[i] = True
    else:  # k=6, one per family -> C = 1/6
        for i in range(6):
            f[i * 5] = True
    return f


def check(name: str, passed: bool, detail: dict) -> None:
    RESULTS.append({"check": name, "pass": bool(passed), **detail})
    print(f"  {name}: {'PASS' if passed else 'FAIL'}  {detail}")


def p1_positive_control() -> None:
    # y = 0.05 + 0.9*C exactly, independent of k; C in {1.0, 0.5, 1/6}
    rows = [
        (2, 1.0, 19, False), (2, 0.5, 10, True),
        (4, 1.0, 19, False), (6, 1 / 6, 4, True),
    ]
    obs = [
        {"instance": inst, "k": k, "C": c, "fails": _fails(k, spread), "successes": s}
        for inst in range(1, 9)
        for (k, c, s, spread) in rows
    ]
    pairs = build_pairs(obs)
    delta_i, delta = loo_delta_pairs(pairs)
    ci_lo, ci_hi = bootstrap_ci(delta_i)
    rel = relabel_control(obs, r_max=20)
    p95 = sorted(rel)[int(0.95 * len(rel))]
    label = classify(delta, ci_lo, ci_hi, p95, DELTA)
    check(
        "P1_positive_control",
        delta > DELTA and ci_lo > DELTA and len({round(d, 9) for d in delta_i}) >= 1,
        {"delta": delta, "ci": [ci_lo, ci_hi], "relabel_p95_r20": p95, "classify": label,
         "n_instances": len(delta_i)},
    )


def p2_count_only_control() -> None:
    # y depends only on k (0.8/0.5/0.2); C varies within k with no relation to y
    rows = [(2, 1.0, 16), (2, 0.3, 16), (4, 1.0, 10), (6, 0.3, 4)]
    obs = [
        {"instance": inst, "k": k, "C": c, "fails": _fails(k, k == 6), "successes": s}
        for inst in range(1, 9)
        for (k, c, s) in rows
    ]
    pairs = build_pairs(obs)
    delta_i, delta = loo_delta_pairs(pairs)
    ci_lo, ci_hi = bootstrap_ci(delta_i)
    check(
        "P2_count_only_control",
        abs(delta) < DELTA,
        {"delta": delta, "ci": [ci_lo, ci_hi], "max_abs_di": max(abs(d) for d in delta_i)},
    )


def p3_classify_branches() -> None:
    cases = [
        ((0.02, 0.015, 0.03, 0.005), "POSITIVE"),
        ((0.005, -0.001, 0.009, 0.005), "NEGATIVE"),
        ((0.015, 0.005, 0.03, 0.02), "AMBIGUOUS"),
        ((0.01, 0.005, 0.02, 0.005), "INCONCLUSIVE (CI straddles threshold)"),
        ((0.004, 0.0005, 0.009, 0.001), "NEGATIVE"),
    ]
    got = [classify(c[0], c[1], c[2], c[3], DELTA) for (c, _) in cases]
    expected = [e for (_, e) in cases]
    check("P3_classify_branches", got == expected, {"got": got, "expected": expected})


def p4_bootstrap_degenerate() -> None:
    ci_lo, ci_hi = bootstrap_ci([0.1] * 8)
    check("P4_bootstrap_degenerate", abs(ci_lo - 0.1) < 1e-12 and abs(ci_hi - 0.1) < 1e-12,
          {"ci": [ci_lo, ci_hi]})


def main() -> None:
    print("POST-HOC DIAGNOSTIC (synthetic only; not part of prespecified analysis)")
    p1_positive_control()
    p2_count_only_control()
    p3_classify_branches()
    p4_bootstrap_degenerate()
    all_pass = all(r["pass"] for r in RESULTS)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "label": "post-hoc software diagnostic; synthetic data only; no effect on real-data analysis",
        "checks": RESULTS,
        "all_pass": all_pass,
    }
    out = ROOT / "v02" / "posthoc_diagnostics_v02.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"all_pass": all_pass}))
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
