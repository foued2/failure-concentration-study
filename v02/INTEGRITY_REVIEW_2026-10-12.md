# v0.2 Integrity Review — 2026-10-12

Separate dated record per GPT's GO decision. `FREEZE_V02.md`, the `v0.2-freeze` tag, and
all frozen hashes are untouched by this file. This review is the record of: what was
observed before completion, what was repaired, what the prespecified rules say, and why
execution proceeded.

## 1. Exposure ledger — what was seen before the run completed

**Primary statistic partially observed before the confirmatory run finished.** This is
stated here and must be stated in the final report. The final result must not be
described as a fully blind confirmation.

| # | Attempt | Outcome | Metrics observed |
|---|---|---|---|
| 1 | After freeze, before pack | Crashed: `TypeError: cannot unpack non-iterable function object` (harness unpack of `load_solver` return) — before any scoring | none |
| 2 | Retry | Crashed: `NameError: _norm_ref is not defined` — before any scoring completed | none |
| 3 | Retry | Scored 40/40 instances (1200 eligible pairs), printed `real delta=-0.000000 CI=(-0.000002, 0.000002)`, entered relabel loop, killed at 30-min tool timeout | **real Δ and 95% CI** |
| 4 | Timing profile (read-only) | Confirmed LOIO cost ~15.5 s on full data; called `relabel_control(obs, r_max=3)` | **3 relabel draws: [0.0021378, −2.898e-7, 0.0021378]**; full-data LOIO Δ = −2.6389e-9 |
| 5 | Retry with 70-min timeout | Re-scored, printed same Δ and CI, entered relabel loop, aborted by user | Δ and CI re-observed (same values) |
| — | p95 of 200 relabels, `classify()` outcome, report files | **never computed; `v02/confirmatory_v02/` did not exist at review time** | none |

Also observed, as legitimate prespecified inputs (not exposure violations): pilot gate
results (PASS), G3 on 40 confirmatory hidden sets (0 mismatches), format-failure rate 0.

## 2. Frozen-artifact verification (SHA-256, computed at review time)

| Artifact | Frozen record | Computed | Match |
|---|---|---|---|
| `v02/PROTOCOL_V02.md` | `99a7f7f00d14b98e48a9606da78d909981359630f9b0838c3eba6312c01921ae` | same | yes |
| `v02/spec_v02.json` | `c5aa8fe2bc52b3e692dcb81899f694f8805b33c17d745693870752167d398eac` | same | yes |
| `v02/models_v02.py` (analysis) | `65d4b15764cc9890985e6de5a063208623df43d7829588da33d6af6cef8b0730` | same | yes |
| `v02/run_gates_v02.py` | `34f6270352a54adc5c1da46aab5fa806f81e7803a095af8d5125a13d8e8ce304` | same | yes |
| `v02/run_pilot_v02.py` | `737b3440a641741932a40a36939e34543ad604cc1d898a314650271fa41346af` | same | yes |
| `v02/generate_pack.py` | `d7c3f86fbdd9cb162b8c619f3e358f6fad87765e877e6158b22973e084f8a907` (recorded pre-emission) | same | yes |
| `v02/run_confirmatory_v02.py` (frozen) | `19c4104759038dcc5bcd6977baca6e73412f3b08f9f14565c23620e48953845e` | — | record only |
| `v02/run_confirmatory_v02.py` (executed) | — | `b2c02ddeb0af529b4458393f460516975bdf6faa2668d1a9e7ecf2fd666e6cdf` | differs only by repair diff below |

The statistical calculations (`models_v02.py`: eligibility k ≥ 2, soft labels s/20,
instance weights, LOIO, bootstrap 10 000 / seed 99 / two-sided 95%, R = 200 relabel
partitions, `classify`) are the frozen bytes. No rule, threshold, or constant changed
after freeze.

## 3. Post-freeze runner repairs (moved here from FREEZE_V02.md working-tree edit)

`run_confirmatory_v02.py` had harness bugs that crashed before any scoring occurred.
Repaired pre-run; this document replaces the earlier FREEZE_V02.md working-tree addendum
(that file restored to its committed state). Exact diff:

```diff
--- a/v02/run_confirmatory_v02.py (frozen, 19c41047)
+++ b/v02/run_confirmatory_v02.py (executed, b2c02dde)
@@ -13,7 +13,7 @@
-from study.features import _norm_ref, load_solver
+from study.features import _norm_ref, concentration, load_solver, run_probes
@@ -57,8 +57,8 @@
-        for name, fn in solvers:
-            from study.features import concentration, run_probes
+        for p, fn in zip(pack, solvers):
+            name = p.stem
@@ -66,6 +66,7 @@
+                ok = False
                 try:
                     out = fn(...)
```

Repairs restore the intended execution path (`load_solver` returns the function directly;
loop must zip file paths with functions; `run_probes`/`concentration` imported at module
top; `ok` init defensive — try/except already assigned it). No frozen statistical
calculation is touched. Committed as `a6a8439`.

## 4. Prespecified rules vs. observed exposure

The frozen decision function (`models_v02.classify`, hash above):

- POSITIVE: `ci_lo > δ AND delta > relabel_p95`
- NEGATIVE: `ci_hi < δ`
- AMBIGUOUS: `δ ≤ delta ≤ relabel_p95`
- else INCONCLUSIVE

with δ = 0.01, CI = percentile two-sided 95% (10 000 resamples, seed 99), `relabel_p95`
= 95th percentile of R = 200 prespecified balanced relabel partitions.

**Constraint implied by the observed exposure:** if the completed run reproduces the
observed interval (−0.000002, 0.000002), then `ci_hi < 0.01` and the frozen classifier
returns NEGATIVE regardless of the relabel percentile. This is a consequence of the
prespecified rule, not a surprise. The completed run still produces the full relabel
distribution and the terminal report.

## 5. Review of substantive objections (Claude/GLM), resolved against frozen code

1. **Terminal rules** — deterministic in frozen `classify` + `bootstrap_ci` (two-sided
   95%, seed 99). "Beats reference" = `delta > relabel_p95`; "meaningful" = point
   estimate ≥ δ; straddling CI → INCONCLUSIVE. Gate-failure label mismatch
   (INFEASIBLE vs Inconclusive) is moot: the gate passed.
2. **Model form** — frozen exactly: RCS(log(1+k)), knots ln3…ln31, ridge 1e-6, max_iter
   50; C appended linearly, **no C×k interaction** (noted, not changeable post hoc).
3. **C mechanically tied to k** — its failure mode is false *positive* (k-nonlinearity
   absorbed by C). Observed Δ ≈ 0 with tight CI → NEGATIVE direction not threatened;
   a richer k-baseline would only shrink Δ. Sensitivity checks → exploratory only.
4. **Power** — observed CI width ~4e-6 vs δ = 0.01 (~5000× margin): the design can
   assess the threshold; a Negative here is not an underpowered null. Post-hoc
   precision statement, labeled as such.
5. **Gate variation pooled** — passed with margin (30 ≥ 15 eligible pairs/instance;
   correct 0.40–0.61, incorrect 0.39–0.60). k-stratified variation → exploratory report.
6. **Gate fragility / eligibility definition** — passed on all instances; eligibility
   (k ≥ 2) identical to v0.1.
7. **Correct definition** — §3 frozen: crash or wrong output = 0, bool excluded, probe
   crash = failure; no timeouts occurred (scoring completes in seconds).

**G2 limitation noted:** chain checks validate mechanics, not signal recovery. A
synthetic positive control (does the pipeline detect planted C-signal?) runs as a
post-hoc software diagnostic, per GPT's §3: strictly diagnostic; if it exposes a
defect, stop and report — do not alter the analysis.

## 6. Governance record

v0.2 is structural choice **(a)**: after v0.1's terminal INFEASIBLE (`1612b87`,
immutable), Foued explicitly authorized this separate study with a different outcome
definition. Motivation derived from v0.1's failure to reach the predictive comparison;
that lineage is disclosed rather than disguised. This authorization extends to
completing v0.2 once — **not** to any successor study. No v0.3.

## 7. Decision

**GO, with full disclosure** (GPT, adjudicated with Claude's freeze objections and
GLM's governance objection). Binding order: document (this file) → complete the frozen
analysis once → report the actual outcome with the exposure disclosure → stop. If a
post-hoc diagnostic exposes a pipeline defect: stop and report the limitation instead
of altering the analysis.
