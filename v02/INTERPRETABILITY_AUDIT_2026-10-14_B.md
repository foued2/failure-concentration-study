# v0.2 Interpretability Audit — Addendum B: Confirmatory Instance Variation and the Bootstrap Interval

**Date:** 2026-10-14
**Status:** append-only addition to `v02/INTERPRETABILITY_AUDIT_2026-10-14.md` (commit `da4030d`, preserved unamended). Read-only reconciliation per GPT's review of that note: no solver was executed, no frozen file was edited, no outcome was regenerated, and no v0.3 was started.

## 1. Question (GPT review)

Note A verified that the diagnostic probe suite is seed-invariant (1 graph-content hash across 11 seeds; only the metadata `seed` field varies). GPT correctly identified a tension: if the 40 confirmatory instances share those same outcome-relevant inputs, they would be repeated evaluations of one suite, and a percentile bootstrap over 40 identical instance-level contributions should be near-degenerate — yet the published interval [−1.519 × 10⁻⁶, 1.583 × 10⁻⁶] is non-degenerate. Two explanations were open: (i) the instances differ on an outcome-relevant dimension the probe hash did not cover (e.g. the hidden scoring suite, which note A never hashed), or (ii) the interval width is numerical refit noise rather than instance variation.

## 2. Four checks (explicit counts; script in Appendix A, full output in Appendix B)

Confirmatory instance ids were derived exactly as the frozen runner derives them (from the frozen protocol hash `99a7f7f00d14b98e`): 40 seeds, 40 distinct, 0 overlap with the pilot seeds {101, 102, 103}.

**Check 1 — suite identity across the 40 instance ids.** Built both suites per seed and hashed them separately (probe graphs excluding the metadata `seed` field; hidden inputs have no metadata field — every field is scoring content):

- Diagnostic probe suites: 40 built → **1 unique graph-content hash**. Confirms and extends note A's check (a) to the exact 40 confirmatory seeds.
- Hidden scoring suites: 40 built → **40 unique hashes**. Every instance's hidden suite is distinct. The fields that differ across seeds are `edges`, `n`, and `t` (with `s` fixed at 0 and the `hid` labels fixed); these are outcome-relevant scoring inputs, not metadata.

**Check 2 — per-solver pass/fail outcome vectors across instances: NOT PERFORMABLE from persisted records.** The confirmatory report persists only aggregates (`eligible_pairs`, `delta`, `ci`, relabel statistics) and the 40 instance-level `delta_i` — no per-solver rows (unlike the pilot, which persisted its `fails` vectors). The outcome rows were **not regenerated**, because regeneration would require executing the 120 solvers. This is recorded as a persistence gap, not as a passed check.

**Check 3 — the 40 instance-level leave-one-instance-out score differences.** 40/40 finite, **40 exactly distinct values**; min −9.411 × 10⁻⁶, max 1.572 × 10⁻⁵, range 2.513 × 10⁻⁵, population std 5.009 × 10⁻⁶; persisted CI width 3.101 × 10⁻⁶; range/width ratio 8.10. (Full value table, Appendix B.) The spread sits at the ~10⁻⁶ scale — roughly nine orders of magnitude above floating-point refit noise (~10⁻¹⁵ for these magnitudes). The interval width is **not** explained by numerical noise.

**Check 4 — bootstrap sampling unit and exact reproduction.** `run_confirmatory_v02.py` lines 80–82: `pairs = build_pairs(obs); delta_i, delta = loo_delta_pairs(pairs); ci_lo, ci_hi = bootstrap_ci(delta_i)` — the resampled units are the 40 instance-level LOIO differences. `models_v02.py` lines 114–121: resample 40 values with replacement, B = 10 000, rng seed 99, percentile 2.5/97.5. Recomputing the frozen bootstrap on the **persisted** `delta_i` reproduces the published CI **bitwise** (`−1.5186596329042069e-06`, `1.5827074637819738e-06`). The interval is exactly the frozen procedure's output on these 40 values.

## 3. Disposition

The second row of the reconciliation table applies: **probe hash single, hidden suites differ.** The 40 instances vary in outcome-relevant scoring inputs (hidden suites, 40/40 distinct) but not in diagnostic features (one probe suite repeated 40×).

Consequences:

- The interval is the frozen bootstrap's output over 40 genuinely distinct instance-level contributions. It is **not** an artifact of duplicated instances and **not** dominated by refit noise. Generalization to unseen hidden scoring suites drawn by the frozen generator is partly tested; generalization to unseen diagnostic probe suites is not tested at all (one suite, shared by all instances).
- Component-wise trace: because the probe graphs are identical, each solver's probe fail vector — and therefore its `(k, C)` (functions of that vector alone, `study/features.py`) — is constant across all 40 instances. The only instance-varying component of an eligible row is `successes` (the hidden-suite outcomes), which enter the soft label. The 40 distinct `delta_i` values at the ~10⁻⁶ scale are therefore driven by genuine hidden-suite outcome variation and fold composition, not by numerical noise. (Direct per-solver confirmation via stored outcome rows remains unavailable — check 2 gap.)
- **Scope correction to note A:** the seed-invariance claim in note A §5/§7(a) covered the diagnostic probe graphs (`make_probe_suite`) only; it never covered the hidden suite. This addendum supplies the missing check, and the claim is to be read as scoped to probe graphs.

## 4. Revised statement of what the interval means

The 95% percentile interval [−1.519 × 10⁻⁶, 1.583 × 10⁻⁶] is the frozen procedure's output over 40 instance-level LOIO score differences arising from 40 distinct hidden scoring suites under one shared diagnostic probe suite. Within the frozen scope it is a calibrated uncertainty interval for the mean score difference over the hidden-suite generator's draws. It is not evidence about behavior under unseen diagnostic probe suites, and — because per-solver outcome rows were not persisted — instance-level outcome variation is evidenced through the hidden-suite hash distinctness and the `delta_i` spread rather than through stored pass/fail vectors. The exposure caveat of `v02/REPORT_V02.md` §1 (unblinded execution) continues to apply jointly with these limitations. The frozen **NEGATIVE** (CI upper bound 1.583 × 10⁻⁶ < δ = 0.01) is unchanged, and its margin is not an artifact of instance duplication.

## 5. Scientific status (unchanged)

- v0.2: formally NEGATIVE under its frozen rule.
- Identifiability: no independent variation in C at fixed k on the verified support (note A: 90/90 pilot rows; now additionally: C constant per solver across all 40 instances, since the probe suite is shared).
- Predictive claim: unresolved, neither supported nor refuted.
- Successor study: not authorized by this audit.

## Appendix A — reconciliation script (read-only)

```python
"""v0.2 interpretability audit addendum B — read-only reconciliation (2026-10-14).

GPT's four checks. No solver is executed; no frozen file is written.
Prints explicit counts for every check.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\pakla\PycharmProjects\failure-concentration-study")
sys.path.insert(0, str(ROOT))

from study.instances import make_hidden_suite  # noqa: E402
from study.probes import make_probe_suite  # noqa: E402


def section(t: str) -> None:
    print(f"\n===== {t} =====")


spec = importlib.util.spec_from_file_location("mv2_audit", ROOT / "v02" / "models_v02.py")
assert spec and spec.loader
mv2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mv2)  # frozen analysis module; no side effects

report = json.loads(
    (ROOT / "v02" / "confirmatory_v02" / "confirmatory_v02_report.json").read_text(encoding="utf-8")
)
proto16 = report["proto_hash16"]
PILOT = {101, 102, 103}
seeds = []
for i in range(40):
    s = int.from_bytes(hashlib.sha256(f"{proto16}:confirmatory:{i}".encode()).digest()[:4], "big") % 10**7
    while s in PILOT:
        s += 1
    seeds.append(s)
print(f"proto_hash16={proto16} seeds_n={len(seeds)} distinct={len(set(seeds))} overlap_pilot={len(set(seeds) & PILOT)}")

# ---------------------------------------------------------------- check 1
section("check 1: suite identity across the 40 confirmatory instance ids")
GRAPH_KEYS = ("probe_id", "family", "variant", "n", "edges", "s", "t", "assigned_predicate", "sat_vector")
probe_hashes: list[str] = []
for s in seeds:
    probes = make_probe_suite(s)
    payload = json.dumps([{k: p[k] for k in GRAPH_KEYS} for p in probes], sort_keys=True)
    probe_hashes.append(hashlib.sha256(payload.encode()).hexdigest())
print(f"probe_suites_built={len(probe_hashes)} distinct_probe_graph_hashes={len(set(probe_hashes))} (metadata 'seed' field excluded)")

hid_hashes: list[str] = []
hid_diff_keys: set[str] = set()
baseline = None
for s in seeds:
    hidden = make_hidden_suite(s)
    hid_hashes.append(hashlib.sha256(json.dumps(hidden, sort_keys=True).encode()).hexdigest())
    if baseline is None:
        baseline = hidden
        print(f"hidden_input_keys={sorted(hidden[0].keys())} hidden_suite_len={len(hidden)}")
    else:
        for hb, ho in zip(baseline, hidden):
            for k in set(hb) | set(ho):
                if hb.get(k) != ho.get(k):
                    hid_diff_keys.add(k)
print(f"hidden_suites_built={len(hid_hashes)} distinct_hidden_suite_hashes={len(set(hid_hashes))}")
print(f"hidden_fields_differing_across_seeds={sorted(hid_diff_keys)} (no metadata field exists in hidden inputs)")

# ---------------------------------------------------------------- check 2
section("check 2: per-solver outcome vectors across instances (persistence check)")
print(f"confirmatory_report_keys={sorted(report.keys())}")
has_fail_rows = any(k in report for k in ("obs", "rows", "eligible_observations", "per_solver", "outcomes", "fails"))
print(f"per_solver_pass_fail_rows_persisted={has_fail_rows}")
print("check2_status=NOT PERFORMABLE from persisted records (aggregates + delta_i only); outcomes NOT regenerated (would require executing solvers)")

# ---------------------------------------------------------------- check 3
section("check 3: all 40 instance-level LOIO delta_i values + spread vs CI width")
delta_i = report["delta_i"]
print(f"delta_i_n={len(delta_i)} finite={sum(1 for d in delta_i if d == d)}")
for idx, d in enumerate(delta_i):
    print(f"  i={idx:02d} seed={seeds[idx]} delta_i={d!r}")
print(f"min={min(delta_i)!r} max={max(delta_i)!r} range={max(delta_i) - min(delta_i)!r}")
mean = sum(delta_i) / len(delta_i)
pvar = sum((d - mean) ** 2 for d in delta_i) / len(delta_i)
print(f"mean={mean!r} pop_std={pvar ** 0.5!r}")
print(f"distinct_exact={len(set(delta_i))}")
for tol in (1e-15, 1e-12, 1e-9, 1e-7):
    clusters = 0
    last = None
    for d in sorted(delta_i):
        if last is None or abs(d - last) > tol:
            clusters += 1
            last = d
    print(f"distinct_at_tol>{tol}: {clusters}")
ci = report["ci"]
print(f"persisted_ci={ci!r} width={ci[1] - ci[0]!r} persisted_delta_mean={report['delta']!r}")

# ---------------------------------------------------------------- check 4
section("check 4: bootstrap sampling unit + CI recomputation from persisted delta_i")
lo, hi = mv2.bootstrap_ci(delta_i, n_boot=10000, seed=99)
print(f"recomputed_ci=({lo!r}, {hi!r}) bitwise_matches_persisted={lo == ci[0] and hi == ci[1]}")
print("unit_trace: run_confirmatory_v02.py:80-82 pairs=build_pairs(obs); delta_i,delta=loo_delta_pairs(pairs); ci_lo,ci_hi=bootstrap_ci(delta_i)")
print("unit_trace: models_v02.py:114-121 bootstrap_ci resamples len(delta_i)=40 instance-level values with replacement, n_boot=10000, rng seed=99, percentile 2.5/97.5")
print(f"spread_vs_width: delta_i_range={max(delta_i) - min(delta_i):.3e} ci_width={ci[1] - ci[0]:.3e} ratio_range_over_width={(max(delta_i) - min(delta_i)) / (ci[1] - ci[0]):.3f}")
```

## Appendix B — reconciliation output (2026-10-14)

```text
proto_hash16=99a7f7f00d14b98e seeds_n=40 distinct=40 overlap_pilot=0

===== check 1: suite identity across the 40 confirmatory instance ids =====
probe_suites_built=40 distinct_probe_graph_hashes=1 (metadata 'seed' field excluded)
hidden_input_keys=['edges', 'hid', 'n', 's', 't'] hidden_suite_len=20
hidden_suites_built=40 distinct_hidden_suite_hashes=40
hidden_fields_differing_across_seeds=['edges', 'n', 't'] (no metadata field exists in hidden inputs)

===== check 2: per-solver outcome vectors across instances (persistence check) =====
confirmatory_report_keys=['ci', 'delta', 'delta_i', 'eligible_pairs', 'n_confirmatory_instances', 'outcome', 'proto_hash16', 'relabel_mean', 'relabel_p95', 'threshold', 'timestamp']
per_solver_pass_fail_rows_persisted=False
check2_status=NOT PERFORMABLE from persisted records (aggregates + delta_i only); outcomes NOT regenerated (would require executing solvers)

===== check 3: all 40 instance-level LOIO delta_i values + spread vs CI width =====
delta_i_n=40 finite=40
  i=00 seed=9774360 delta_i=-4.167523369513759e-06
  i=01 seed=197002 delta_i=-7.724499034189591e-06
  i=02 seed=4976410 delta_i=7.62933378695152e-08
  i=03 seed=8282449 delta_i=-1.069481216475765e-06
  i=04 seed=2285332 delta_i=1.7247559931377054e-06
  i=05 seed=4040201 delta_i=2.5179544623776806e-06
  i=06 seed=5047746 delta_i=-5.1244292776919664e-06
  i=07 seed=6283407 delta_i=6.935942994834576e-06
  i=08 seed=9237077 delta_i=-2.3288148078837168e-06
  i=09 seed=8927684 delta_i=-3.851658032627547e-06
  i=10 seed=3914224 delta_i=4.614931289892432e-06
  i=11 seed=1970638 delta_i=7.231197568513537e-07
  i=12 seed=7261847 delta_i=-3.6699566399178707e-06
  i=13 seed=8672265 delta_i=-4.151388433348835e-06
  i=14 seed=9503518 delta_i=-2.3007358940230205e-06
  i=15 seed=1423543 delta_i=5.075307776380988e-06
  i=16 seed=1055675 delta_i=-9.411245243451383e-06
  i=17 seed=6308794 delta_i=4.871783219617676e-06
  i=18 seed=7337101 delta_i=-1.6841098711140035e-06
  i=19 seed=5952838 delta_i=-3.2083073620015057e-07
  i=20 seed=3600035 delta_i=3.0268916331177564e-06
  i=21 seed=4629490 delta_i=9.444363571087244e-06
  i=22 seed=1834717 delta_i=1.1183694262895116e-06
  i=23 seed=3490574 delta_i=-2.7018968620229344e-06
  i=24 seed=5171755 delta_i=7.874426088516628e-06
  i=25 seed=3605375 delta_i=-8.26188460734123e-06
  i=26 seed=8195336 delta_i=2.698397016942522e-08
  i=27 seed=2750535 delta_i=-2.37621352483508e-06
  i=28 seed=2106121 delta_i=8.365444202906858e-07
  i=29 seed=7610233 delta_i=-6.841061361839706e-08
  i=30 seed=157040 delta_i=1.9350953650576486e-07
  i=31 seed=7928323 delta_i=1.5722448520438803e-05
  i=32 seed=3036896 delta_i=-6.6351297552946775e-06
  i=33 seed=3751822 delta_i=1.9350958546660024e-07
  i=34 seed=3284208 delta_i=1.302400689517924e-07
  i=35 seed=2387299 delta_i=3.6179963699423112e-06
  i=36 seed=861348 delta_i=-1.2627494523353988e-06
  i=37 seed=2101043 delta_i=6.194107738721755e-06
  i=38 seed=9420200 delta_i=-2.656753927965383e-06
  i=39 seed=1890265 delta_i=-5.257325645713351e-06
min=-9.411245243451383e-06 max=1.5722448520438803e-05 range=2.5133693763890186e-05
mean=-2.638929627596376e-09 pop_std=5.008826427687712e-06
distinct_exact=40
distinct_at_tol>1e-15: 40
distinct_at_tol>1e-12: 39
distinct_at_tol>1e-09: 39
distinct_at_tol>1e-07: 33
persisted_ci=[-1.5186596329042069e-06, 1.5827074637819738e-06] width=3.1013670966861807e-06 persisted_delta_mean=-2.638929627596376e-09

===== check 4: bootstrap sampling unit + CI recomputation from persisted delta_i =====
recomputed_ci=(-1.5186596329042069e-06, 1.5827074637819738e-06) bitwise_matches_persisted=True
unit_trace: run_confirmatory_v02.py:80-82 pairs=build_pairs(obs); delta_i,delta=loo_delta_pairs(pairs); ci_lo,ci_hi=bootstrap_ci(delta_i)
unit_trace: models_v02.py:114-121 bootstrap_ci resamples len(delta_i)=40 instance-level values with replacement, n_boot=10000, rng seed=99, percentile 2.5/97.5
spread_vs_width: delta_i_range=2.513e-05 ci_width=3.101e-06 ratio_range_over_width=8.104
```

## Operational note

GitHub OAuth token rotation remains **PENDING** (separate security action, owner-side). The exposed token must be revoked and replaced via GitHub's settings; the replacement must never be pasted into chat, scripts, or repository files.
