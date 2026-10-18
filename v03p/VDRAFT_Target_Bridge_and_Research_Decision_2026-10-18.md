# VDraft: Target Bridge and Research Decision Plan — Revision 2

**Date:** 2026-10-18  
**Status:** REVIEW DRAFT ONLY (Revision 2). Produced under the owner implementation order `v03p/VDRAFT_IMPLEMENTATION_ORDER_2026-10-18.md` (commit `906dd351e647d3d28a70ae16a01070e34fdca8a6`, from Foued, relayed by GPT, to GLM). Not frozen. No NC2 computation, Phase 1 simulation, solver generation, hidden-outcome collection, spending, NC1 rerun, or protocol freeze/authorization is granted by this document or by that order. The branch remains separate from `master`.  
**Purpose:** Translate the owner's minimum-meaningful predictive target (`δ*`) into the mechanistic signal parameter of the `c*` heuristic — designated **`β_min`** by the owner order — as a reviewable plan, while keeping the original scientific question primary. Revision 2 applies the converged review corrections (GLM, GPT, Claude) recorded in §0. The candidate-grid owner menu (`β ∈ {0.05, 0.10, 0.20}`) is retired: `β_min` is derived through the target-translation procedure, not chosen from the grid.

## 0. Change record (Revision 2)

| Order item (work order `906dd351`) | Reviewer finding source | Edit applied in this revision |
|---|---|---|
| 1 | GLM Q1, GPT Q1 | §2 `β_min` row, §4, A1.3, A2.3, A3 rewritten on the fixed M3 reference unit `s_ref = 0.12703` exactly; "slope per one within-`k` SD of `C`" removed as the definition of `β_min`; within-`k` variation retained as the identification/population input, with the M3 bucket weighting and body-count scaling stated explicitly (A1.3) |
| 2 | GLM Q1, order item 2 | §2 keeps `δ*` / `γ` / `β_min` / `c*` as four distinct quantities; no conversion is asserted as authoritative; the only numeric cross-relations shown are the algebraic restatement of the engine's own `c` definition (A1.3) and a clearly labeled non-authoritative candidate mapping (A2.3) |
| 3 | GLM Q5, GPT Q1 | §2.1 and the new source document `v03p/VDRAFT_M3_SOURCE_DEPENDENCY_2026-10-18.md`: controlling M3 Rev d / engine spec v1 §2 texts are NOT in the repository and the exact text is not available verbatim in the active conversation; the `β_min` numerical mapping is kept **PROVISIONAL-PENDING-SOURCE**; nothing is fabricated or paraphrased as if retrieved. The only verbatim anchors preserved are the in-repo engine docstring excerpts, quoted with file/line/hash provenance |
| 4 | GLM Q2/Q5, GPT Q2 | A2 and A3 declare the population and support family for every `Δ`, `γ`, `β_min`, and spread value; every bucket-local-proxy quantity is labeled **PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE** (Rev F §5A: complete-rule `P(pass) = 0` as drafted, Rev F:175) |
| 5 | GPT Q2, GLM Q2 | A2.2 pins the calibration to Revision F's stated convention (bisection, tolerance `10⁻⁴` on `Δ`, fixed calibration seed, recorded Monte Carlo size — Rev F:364); a deterministic alternative requires its own documented validation on the bridge population before use; A2.3 states that the exact marginal/probability-scale functional for `β_min` comes from the controlling M3 definition (source-pending) |
| 6 | GLM Q3, GPT Q3 | §6 B2 and §8 add the confirmatory-procedure choice as an explicit owner blocker (Revision F held-out log-loss comparison vs the in-chat engine-spec scale-(i) stratified-permutation procedure), with no blending of estimands or operating characteristics |
| 7 | GLM Q3 | §6 B2 word "selected" removed ("- no §5A resolution has been adopted; Rev F:177, 625"); §7 adds the owner decision whether power at `δ*` is gated (Revision F gates power at `2δ*` and only reports power at `δ*`, Rev F:268) |
| 8 | GPT Q5, GLM Q5 | A3 scenario-scope note: NC1's `c` construction covers only its `k=5` and `k=10` buckets (`nc1_calc.py:106-111`), and NC1 evaluated no (b)-family scenario at all (`nc1_calc.py:96`); no NC1 contribution is implied for Revision F scenario (b)'s `k=20` without a separately specified extension; no new NC1 computations fill threshold-grid gaps (A2.4/A3) |
| 9 | CLAUDE Q4, GPT Q4 | §7 adds the optional pre-registered `PILOT-DECIDES` branch and states explicitly that GO or passing a pilot gate does not confirm the theory and never authorizes a later phase automatically |
| 10 | all reviewers | Header/status unchanged in kind: review draft only; contrast list extended ("NC1 rerun" added) |
| — | CLAUDE Q3 | §2 footnote separating Revision F's M1/M2/M3 conditioning candidates from NC1's M1/M2/M3 mutation tests (unrelated namespaces) |

### 0.1 Genuine remaining blockers

1. **Source dependency (blocks only the numerical `β_min` mapping).** The controlling M3 Rev d addendum and engine spec v1 §2 texts are not in the repository, and their exact text is not available verbatim in the active conversation (see §2.1). Committing those texts resolves this; no computation is needed.
2. **§5A M1/M2/M3 resolution and complete-rule recalculation** — owner decision + reviewer verification (Rev F §11 items 13–14). Blocks complete-rule labeling, not this plan's PROVISIONAL rows.
3. **Confirmatory-procedure choice** — owner decision (§8 item added). Required before any Phase 1 gate claim; not required for the bridge.
4. **Power-at-`δ*` gating** — owner decision (§7).
5. **Bridge execution authorization** — the bridge calculation itself (A2/A3) runs only under the owner-authorized work order per §8, after blocker 1 is resolved. No computation was run for this revision.

### 0.2 Post-review correction pass (GPT/ review of Revision 2 at `78d5f36ff09367bc138645d8c8ae130a2f8eb7ef`; CLAUDE/ concurrence)

Two targeted corrections applied, with no computation and no other substantive change:

1. **Correction A — provisional meaning of `β_min`, and symbol disambiguation.** The §2 `β_min` row now labels the probability-scale reading a **provisional working interpretation inferred from the engine normalization**, not the binding M3 definition (the engine anchors fix `s_ref` and the construction of `c`, not the statistical functional of `β_min`). The A2.3 candidate mapping is marked **conditional on that interpretation**. §4 keeps `0.1007` as an illustrative approximation only — not a resolved translation of `δ*` into `β_min`, not a selected minimum-signal value, not sheeted into any decision. Symbols disambiguation added (§2 footnote): Revision F's predictor `x_RCS = log(1+k)` vs the M3 channel `x_M3` = `s_ref`-normalized within-bucket departure; `β_min`'s slope attaches to `x_M3` only, and every former bare-`x` use (§2, §4, A2.3) now carries the distinct name.
2. **Correction B — DGP variance vs realized variance in the offered-mass specification.** A1.3 and A3 now distinguish the DGP variance `σ_k²` (unconditioned) from the realized `t`-denominator variance `V̂ar_k^{(t)}` (identity for the realized bucket: `Σ_i(C_i − C̄_k)² = t_k·V̂ar_k^{(t)}`; for i.i.d. draws at fixed `t_k`: `E[Σ_i(C_i − C̄_k)² | t_k] = (t_k − 1)·σ_k²`, before support conditioning). `E[c]` is specified per-row under the row's declared support/composition rule — empty buckets contribute zero, support conditioning respected — and never as expected bucket sizes × unconditioned DGP variances. Every `Var` occurrence in §2/A1.3/A3 now states which variance it is (A3 variance-notation rule). Specification correction only; no new computation authorized or run.
3. **Correction C — units of `x_M3` (GPT/ sign-off condition on `9aaf3ee`; CLAUDE/ concurrence).** `x_{M3,i} = (C_i − C̄_{k(i)})/s_ref` is **dimensionless by construction** (the raw departure is divided by the constant `s_ref` exactly once). §2, §4, and A2.3 now read: `β_min` is the probability-scale slope per one unit of `x_M3`, equivalently per a raw within-bucket departure of size `s_ref = 0.12703`; `Var(x_M3)` is the plain variance of that dimensionless normalized channel — no further `s_ref²` attribution (which would double-divide; the `s_ref²` factor belongs to the raw→`c` scaling in the `c` construction). The §4 approximation and the A2.3 candidate mapping therefore remain mutually consistent as written. Wording fix only.

## 1. Recommendation in brief

Accept the goal framing. The primary question remains:

> Does the concentration of a solver's diagnostic failures, `C`, predict correctness on unseen inputs beyond the total failure count, `k`, for naturally generated solver bodies?

The natural-solver predictive study should remain the primary route. An engineered mechanistic study is a possible alternative or validation route if the natural population cannot provide enough identifiable support at an acceptable cost. The two routes answer related but different questions; evidence for one must not be presented as evidence for the other.

Before choosing a route, complete the target-translation report that relates the already chosen predictive-score target (`δ*`) to the mechanistic signal parameter (`β_min`) used by the `c*` heuristic. Treat the approximation in §4 as a sanity check, not as the final conversion. The report derives `β_min` through the declared procedure of §5; the submission to its owner is the derived value, not a re-opened candidate menu.

Do **not** redefine NC2 as the v0.3 Phase 1 power simulation. The existing `c*`-heuristic question and the v0.3 predictive-procedure validation are separate work products unless the owner explicitly merges them in a revised protocol. Phase 1 of v0.3 also remains blocked by unresolved design decisions in Revision F, including the §5A conditioning contradiction.

## 2. Terms that must not be conflated

| Symbol | Meaning in this plan | What it is not |
|---|---|---|
| `k` | Total number of diagnostic probe failures | A measure of where failures occur |
| `C` | Largest family's share of failures; a concentration statistic (Rev F §1: `C = max_j f_j / k`) | The mechanistic variance-like quantity `c` calculated in NC1 |
| `Δ` | Held-out predictive log-loss improvement: baseline (`k`) minus extended (`k, C`) (Rev F §1 estimand; oracle form = §1 estimand evaluated on DGP truth) | The mechanistic slope or a threshold-crossing probability |
| `δ*` | Existing proposed minimum meaningful predictive gain, `ln(1.5)/20 = 0.020273255405408218` nats per hidden input (owner decision C, Rev F:121) | A slope on the correctness-probability scale |
| `γ` | Coefficient on raw `C` in Revision F's proposed logit outcome generator, `logit(p) = θ0 + θ1 log(1+k) + γC + u + v` (Rev F:291) | The same parameter as `β_min` without a specified transformation |
| `β_min` | The minimum-signal parameter of the mechanistic `c*` heuristic, **in the fixed M3 reference unit `s_ref = 0.12703 exactly`** (engine, `v03p/nc1/nc1_calc.py:19`). The engine anchors fix `s_ref` and the construction of `c`; they do **not** by themselves fix the exact statistical functional of `β_min`. The reading carried here — "the per-body probability-scale change in correctness rate attributable to one unit of the dimensionless normalized channel `x_M3 = (C_i − C̄_{k(i)})/s_ref`, i.e. to a raw within-bucket departure of size `s_ref = 0.12703` (the `s_ref`-normalized within-bucket departure used in the `c` construction; symbol disambiguation below)" — is a **provisional working interpretation inferred from the engine normalization**, not the binding M3 definition; the exact population functional is prescribed by the controlling M3 Rev d text, pending-source (§2.1) | `Δ`, `δ*`, or the logit coefficient `γ`; nor "a slope per one within-`k` SD of `C`" — that variant substitutes a scenario-dependent SD for the fixed reference unit (Revision 1 wording, corrected here) |
| `c` | NC1 gate statistic (engine, `nc1_calc.py:17-21`): `c = (δ_5²·X_5/t_5 + δ_10²·X_10/t_10)/s_ref²` with `X_k = Σ_{i<j}(g_i−g_j)²`; algebraically, over a realized train block, `c = (t_5·V̂ar₅^{(t)}(C) + t_10·V̂ar₁₀^{(t)}(C))/s_ref² = Σ_i x_{M3,i}²`, where `x_{M3,i} = (C_i − C̄_{k(i)})/s_ref` is the `s_ref`-normalized within-bucket departure and `V̂ar_k^{(t)}` the realized `t`-denominator within-bucket variance (variance-notation rule, A3) — a **body-count-scaled total** in `s_ref²` units, not a per-body variance | A directly measured estimate of predictive gain or statistical power |
| `c*` | Mechanistic threshold `c* = (1.25/β_min)²` under the M3 addendum's stated construction (`σ_max·z_req = 1.25`; `nc1_calc.py:25-26`) | A directly measured estimate of predictive gain or statistical power |

**Namespace footnote:** In Revision F §5A, `M1/M2/M3` denote candidate resolutions of the conditioning (κ) rule for the fitted-model gate. In `v03p/nc1/RUN.txt` and the NC1 verification battery, `M1/M2/M3` denote engine mutation tests. These namespaces are unrelated; this document uses `M1/M2/M3` only for the Revision F conditioning candidates.

**Symbol disambiguation (Correction A, GPT review of this revision):** Revision F's outcome-model predictor is `x_RCS = log(1+k)` (the `θ1·log(1+k)` term, Rev F:291). The M3 mechanistic channel is a distinct quantity: the per-body **dimensionless** `s_ref`-normalized within-bucket departure `x_{M3,i} = (C_i − C̄_{k(i)})/s_ref` (one full unit of `x_M3` corresponds to a raw within-bucket departure of size `s_ref = 0.12703`; `s_ref` is divided into the raw departure exactly once, so `x_M3` carries no further `s_ref` scaling). `β_min`'s slope attaches to `x_M3` (provisional working interpretation, pending the M3 source, §2.1); it must never be mapped to `x_RCS` in any implementation or interpretation — a slope attached to the wrong predictor would pass every otherwise-plausible sanity check.

### 2.1 Source precondition for `β_min` (controlling definitions)

**What is missing.** The controlling texts — "engine spec v1 section 2" and "M3 addendum Rev d" — are not checked into the repository (`nc1_calc.py:14` names them, but only excerpts are carried in its docstring). Their exact text is not available verbatim in the active conversation either: the review-thread quotations are reviewer paraphrases, and the implementation order (item 3 / close-out) forbids paraphrasing missing controlling text as if it had been retrieved.

**What is preserved verbatim (in-repo anchoring, complete quotation).** From `v03p/nc1/nc1_calc.py` lines 14–26 at commits `4551cacb`/`906dd351` (file SHA-256 `c23639b85877161ad97186a6a088655ca7c1cce524aaf0b55464f1653725859d`, rev 3):

```
Definitions (engine spec v1 section 2, M3 addendum Rev d, A1 rev 3):
  C levels: k=5 -> {0.2,0.4,0.6,0.8,1.0}; k=10 -> {0.2,0.3,0.4,0.5}
  integer labels g = C/delta_k: k=5 g in 1..5; k=10 g in 2..5
  X_k = t_k * sum_i n_i g_i^2 - (sum_i n_i g_i)^2 = sum_{i<j} (g_i-g_j)^2
  c = (delta_5^2 * X5/t5 + delta_10^2 * X10/t10) / s_ref^2,
      delta_5^2 = 0.04, delta_10^2 = 0.01, s_ref = 0.12703 exactly
      => s_ref^2 = 161366209/1e10 ; every c>=tau comparison is done in
      exact integer arithmetic (see pooled_R0 / ssfloor_x).
  Engine-spec anchors reproduced as checks:
      c_floor(t) = delta^2 (t-1)/t / s_ref^2   (min nonzero c at size t)
      c_ceil(t)  = R_k^2 floor(t^2/4)/t / s_ref^2
  c* exact values (M3 addendum): c* = (1.25/beta)^2, sigma_max*z_req = 1.25:
      beta .20 -> 625/16 = 39.0625; .10 -> 156.25; .05 -> 625.00
```

Supporting code anchors (same file): `SREF2_NUM = 161366209  # s_ref^2 = SREF2_NUM / 1e10  (0.12703^2, exact)` (line 103), `DELTA2 = {5: 0.04, 10: 0.01}` (line 106), `CSTAR = (39.0625, 156.25, 625.0)` (line 110), `SCENS = ("a-hist", "a-50:50", "c-hist", "c-50:50")` (line 96).

**Consequence.** Until the controlling texts are committed to the repository, the numerical mapping `γ ↔ β_min ← c*` is **PROVISIONAL-PENDING-SOURCE**. Every other element of the bridge procedure is specified below from the in-repo anchors, so this is the only definitional blocker of the bridge (§0.1 item 1); it blocks no other work of this draft revision.

**Exactly what the source must pin** (mechanical checklist for the injection, per A2.3):

1. The exact mechanistic channel relative to which `β_min` is measured — its relation to the per-body within-bucket departure `(C_i − C̄_k)` used in the `c` construction (in `s_ref`-normalized units per the engine excerpts; denoted `x_{M3,i}` in this document).
2. The exact marginal/population functional prescribing `β_min`: the averaging population, whether the slope is a local derivative `γ·p(1−p)` under the declared logistic model or a finite-difference of a population mean, and whether it is evaluated at the null baseline `γ = 0` or at the calibrated effect `γ = γ*`.
3. The roles of `σ_max` and `z_req` in `σ_max·z_req = 1.25` and their relation to `β_min` (how the fixed factor `1.25` is assembled).
4. Any sign/scale conventions linking `γ·C` (Revision F outcome model) and `β_min·x_M3` (M3 mechanistic channel) — with the disambiguation that the slope attaches to `x_M3`, the `s_ref`-normalized within-bucket departure, and never to Revision F's `x_RCS = log(1+k)` — including how suite and body random effects enter the definition, if at all.

The companion document `v03p/VDRAFT_M3_SOURCE_DEPENDENCY_2026-10-18.md` records this dependency statement and the verbatim anchor provenance for review.

## 3. What is already established, and what is not

### Established design target

The current v0.3-P Revision F draft records the owner's earlier choice `r = 1.5`, operationalized as:

\[
\delta^* = \frac{\ln(1.5)}{20} \approx 0.0202733
\]

This is the proposed minimum meaningful *held-out log-loss gain* for prioritizing candidates for an expensive confirmation slot. Revision F also explicitly warns that `exp(20Δ)` is a multiplicative score contrast under the additive scoring interpretation, not a literal joint-vector likelihood ratio (Rev F:121). This target is not a value of `β_min`.

### Established NC1 evaluation grid

Under the current heuristic, the values evaluated in NC1 are:

| `β_min` supplied to heuristic | `c* = (1.25/β_min)²` |
|---:|---:|
| 0.20 | 39.0625 |
| 0.10 | 156.25 |
| 0.05 | 625 |

These three rows are NC1's **evaluation grid** (`CSTAR`, `nc1_calc.py:110`), not the study's design choice: the study's design value is `β_min`, derived by the bridge (§5) — per the owner order, not selected from this grid. NC1 has been technically validated and its validation loop is closed (`v03p/nc1/RUN.txt` through M1b, commit `4551cac`). Its threshold probabilities are conditional on the declared scenario distributions and gates at the engine's two-bucket construction over scenarios `("a-hist", "a-50:50", "c-hist", "c-50:50")` (`nc1_calc.py:96`) — notably, **no (b)-family scenario was evaluated by NC1** (see A3 scope note). They do not establish the distribution of real natural solvers, nor do they constitute power estimates for the v0.3 predictive procedure.

### Still unknown

The value of `β_min` corresponding to `δ*` across the declared baseline probabilities and within-`k` spreads of `C` — derivable through the §5 procedure once the source precondition of §2.1 is met, and provisionally expressible under the labeled candidate mapping of A2.3 in the meantime. A single approximate value cannot be assumed to apply across all scenario families.

## 4. Preliminary bridge: approximation only

For a probability-scale slope `β_min` under the provisional working interpretation of §2 (per one unit of the dimensionless mechanistic channel `x_M3`, equivalently a raw within-bucket departure of size `s_ref`), a centered predictor in `x_M3` units with supported-population second moment `Var(x_M3)` — the plain variance of the dimensionless normalized channel, computed under the row's declared support/composition rule (variance-notation rule in A3) — and a baseline correctness probability near `p`, a small-effect approximation for the population log-score gain is:

\[
\Delta_{\mathrm{oracle}} \approx
\frac{\beta_{\min}^{2}\,\operatorname{Var}(x_{M3})}{2p(1-p)}.
\]

At `p ≈ 0.5` (i.e. `p(1−p) = 0.25`) and `Var(x_M3) = 1`, this becomes `Δ ≈ 2β_min²`. Substituting the existing `δ*` gives:

\[
\beta_{\min} \approx \sqrt{\delta^*/2} \approx 0.1007.
\]

**Unit discipline (Revision 2 correction).** `x_M3` is dimensionless by construction: each raw within-bucket departure is divided by the fixed constant `s_ref = 0.12703` exactly once, so `Var(x_M3)` is the plain supported-population variance of that normalized channel, computed under the row's declared support/composition rule — not a variance "in `s_ref²` units" (the `s_ref²` division has already been applied in forming `x_M3`; quoting it again would double-divide — the `s_ref²` factor belongs to the raw→`c` scaling in the `c` construction, A1.3) — not `Var(C)` measured in per-within-`k`-SD-of-`C` units, and not an unconditioned-DGP variance scaled by an expected bucket size (A1.3 DGP/realized distinction; A3 variance-notation rule). The number `0.1007` is an illustrative approximation for the `Var(x_M3) = 1`, `p(1−p) = 0.25` slice only: it is neither a resolved translation of `δ*` into `β_min` nor a selected minimum-signal value, and it is not sheeted into any decision; the submission value comes from the A2 procedure under the source-defined functional. The approximation can move with baseline probability, the `s_ref`-normalized spread of the supported population, the distribution of `k`, the support gate, and the nonlinear/random-effects outcome model. It is also a population-oracle approximation, not finite-sample power of the fitted procedure.

## 5. Proposed work item A: target-translation report (deriving `β_min`)

**Purpose:** Derive `β_min` from the existing predictive target `δ*` through the declared procedure below, replacing the retired candidate grid; and, where the source precondition of §2.1 is met, map the derived value to `c* = (1.25/β_min)²` and locate it on NC1's evaluation grid.

### A1. Lock the definitions before calculating

1. **Source precondition first.** The controlling M3 Rev d addendum and engine spec v1 §2 texts must be committed to the repository (see §2.1 and the source document) before any `β_min` value or `c*` mapping is treated as more than **PROVISIONAL-PENDING-SOURCE**. This revision reports the dependency; it does not resolve it, because the exact controlling text is not available verbatim in the active conversation (order item 3's otherwise-branch governs here).
2. Keep `δ*`, the logit coefficient `γ`, the exact M3-defined `β_min`, and the mechanistic threshold `c*` as four distinct quantities. Do not invent a conversion and do not call a candidate numeric value authoritative.
3. **Within-`k` variation: identification input, not a redefinition of `β_min`'s unit.** The scientific claim is *incremental prediction beyond `k`*, and the identification channel is within-`k`: a `C` vector varying within one `k`-slice is linearly independent of every `k`-function (Rev F:173), so Revision F's rank-increase condition, §1's `Δ`, and the mechanistic gate statistic all draw on within-`k` variation. `β_min`'s reference unit nevertheless remains the fixed `s_ref = 0.12703`. The spread enters the bridge as inputs to the `c` construction — realized `V̂ar_k^{(t)}` quantities inside the realized identity below, declared-DGP variances `σ_k²` where a row works at the population level (distinction below) — with the M3 bucket weighting and body-count scaling stated explicitly:
   - buckets `k = 5` and `k = 10` only (the construction has no `k = 20` term; `nc1_calc.py:106-111`);
   - each included bucket contributes its realized within-bucket mass: per-bucket `δ_k²·X_k/t_k = Σ_{i∈bucket k}(C_i − C̄_k)² = t_k·V̂ar_k^{(t)}(C)` — an identity for the realized bucket, where `V̂ar_k^{(t)}(C) = Σ_{i∈bucket k}(C_i − C̄_k)²/t_k` is the realized `t`-denominator within-bucket variance;
   - the offered mass of a realized train block is the `δ`-weighted sum normalized by the fixed `s_ref² = 0.0161366209`: `c = (t_5·V̂ar₅^{(t)}(C) + t_10·V̂ar₁₀^{(t)}(C))/s_ref²` — algebraic restatement of the engine's own in-repo definition (`nc1_calc.py:17-21`), including its body-count scaling: doubling an included bucket's size doubles that bucket's contribution at fixed realized within-bucket variance;
   - **DGP variance vs realized variance (Correction B).** The declared-DGP within-`k` variance `σ_k²` — the unconditioned variance of `C` under the declared DGP — is a distinct quantity from the realized `V̂ar_k^{(t)}`: for i.i.d. draws from the unconditioned DGP at a fixed bucket size `t_k`, `E[Σ_{i∈bucket k}(C_i − C̄_k)² | t_k] = (t_k − 1)·σ_k²`, not `t_k·σ_k²` (consistent with the engine's own moment anchor `E[X | t] = t·(t−1)·Var_g`, `nc1_calc.py:389-391`). Support conditioning changes the conditional moments again, and an empty bucket contributes zero to `c`. Consequently the offered mass `E[c]` for every A3 row is computed **under that row's declared support/composition rule** (empty-bucket zeros and support conditioning included), never as `(E[t₅]·σ₅² + E[t₁₀]·σ₁₀²)/s_ref²` or any variant multiplying an expected bucket size by an unconditioned DGP variance. Specification rule only — no computation is authorized now;
   - the `C` values are the engine's grids (`k=5: {0.2,0.4,0.6,0.8,1.0}` with δ_5 = 0.2; `k=10: {0.2,0.3,0.4,0.5}` with δ_10 = 0.1), which match Revision F's declared DGP exactly (Rev F:287); attainable-value discreteness is handled by the declared uniformity `1/Z(k)` machinery.
   If the controlling M3 text prescribes any different scale or weighting, that text governs; the difference is documented here and requires reviewer/owner acceptance before adoption.
4. Separate the population-oracle log-score contrast from the finite-sample score gain of the fitted analysis procedure. Revision F itself says its proposed `γ*` calibration targets the former (Rev F:270, 364); Phase 1 would assess the latter.

### A2. Calculate the bridge under declared cases

For each declared outcome baseline and support/composition scenario, including the documented within-range alternatives where relevant:

1. Use the declared Revision F outcome model as proposed: `logit(p) = θ0 + θ1·log(1+k) + γC + u + v`, with `u ~ N(0, σ_b²)`, `v ~ N(0, σ_s²)`, soft label `s/20` per (body, suite), `s ~ Binomial(20, p)`; proposed `θ0 = 0`, `θ1 = −1`, `σ_b = σ_s = 1` (Rev F:291). These parameters remain **PROPOSED, not validated** (Rev F:362), inherit the recorded §9.1 upper-tail shortfall (Rev F:623), and require reviewer sign-off and owner acceptance per Rev F §11; every row inherits that status.
2. Calibrate `γ` (as `γ*`) to the population-oracle target `Δ = δ*` — and, as a sensitivity case matching Rev F's grid, `Δ = 2δ*` — using Revision F's stated convention: bisection on `γ` with tolerance `10⁻⁴` on `Δ`, a fixed calibration seed, and a recorded Monte Carlo size from DGP truth (Rev F:364). A deterministic computation of `Δ(γ)` may substitute **only if** it is separately validated for the bridge's actual `Δ(γ)` over the intended support population before use and the validation is documented here (a γ=0 tail-calculations agreement does not by itself validate the bridge's `Δ(γ)` path). Report the method, seed, Monte Carlo/replication size, and attained tolerance per row.
3. Compute `β_min` from the calibrated `γ` under **the exact functional prescribed by the controlling M3 definition** (§2.1 checklist item 2). Pending that source, report the row with `γ*`, the declared spread inputs, and the label **PROVISIONAL-PENDING-SOURCE**; the only cross-relation shown meanwhile is the non-authoritative candidate mapping — clearly labeled, not to be sheeted into decisions, and **conditional on the provisional working probability-scale interpretation of §2 (not the binding M3 definition)**: under Revision F's declared logistic model, an average marginal probability slope per one unit of the dimensionless channel `x_M3`, evaluated over the supported population's random-effects mixture in `(u, v)` jointly with the predictors `(k, C)` — where Revision F's `x_RCS = log(1+k)` enters only through the `θ1·x_RCS` term and never carries `β_min`'s slope — would give `β_min ≈ γ*·E[p̃(1−p̃)]·s_ref`, with `p̃(1−p̃)` averaged over that mixture at the evaluation point fixed by the source (candidate only).
4. Map the derived `β_min` values to `c* = (1.25/β_min)²` and locate them **only** where NC1 has quantities: NC1's grid is exactly `{39.0625, 156.25, 625}` (`CSTAR`, `nc1_calc.py:110`). For bridge-implied `c*` values off this grid there is no NC1 row, the cell reports "no NC1 row (grid mismatch)", and no new NC1 computation is triggered to fill it.
5. Report a range/sensitivity across scenarios, not a single pooled value that conceals differences between a-, b-, and c-type populations.

**Precision language:** discrete NC1 probability calculations may be exact under their specified enumerations, but the target bridge involves a nonlinear random-effects outcome model and numerical calibration. Unless the calculation actually proves a closed form, describe this bridge as a *numerically calibrated mapping with declared tolerances*, not simply as "exact."

### A3. Required output

One table with these columns:

| Scenario/support definition | Within-`k` **DGP** variances `σ₅², σ₁₀²` (unconditioned, declared DGP; realized `V̂ar_k^{(t)}` stated separately wherever used) | Expected train sizes `E[t₅], E[t₁₀]` | Offered mass `E[c]` computed under this row's declared support/composition rule (s_ref²-units construction; A1.3) | Baseline correctness range | Target `Δ` | Calibrated `γ*` | Implied `β_min` | Implied `c*` | NC1 quantity at that threshold | Population/support label | Numerical method/tolerance/status |
|---|---|---|---|---|---|---|---|---|---|---|---|

Cell rules:

- **Population and support family declared per row** for every `Δ`, `γ*`, `β_min`, and spread value (order item 4). Any bucket-local-proxy quantity is labeled **PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE** — this applies to `Δ`, `γ`, `β_min`, and variance entries alike, not to a single trailing column; the complete-rule `P(pass) = 0` as drafted (Rev F §5A) is never glossed.
- **Variance-notation rule (Correction B).** Whenever a variance appears in any cell, the cell states which of the two distinct quantities it is: the **DGP variance** `σ_k²` — the unconditioned variance of `C` within bucket `k` under the declared DGP — or the **realized `t`-denominator sample variance** `V̂ar_k^{(t)}(C) = Σ_{i∈bucket k}(C_i − C̄_k)²/t_k`. They are not interchangeable: for i.i.d. draws at a fixed bucket size `t_k`, `E[Σ_i(C_i − C̄_k)² | t_k] = (t_k − 1)·σ_k²`, before support conditioning shifts conditional moments again. `E[c]` is computed under the row's declared support/composition rule, never from expected bucket sizes times unconditioned DGP variances (A1.3).
- **Scenario (b) scope note:** Revision F scenario (b) includes `k=20` (`C ∈ {0.2, 0.25}`), while NC1's `c` construction has only the `k=5` and `k=10` buckets and NC1 evaluated no (b)-family scenario at all (`nc1_calc.py:96, 106-111`). Scenario-(b) rows report bridge quantities and write "**no NC1 comparison defined**" in the NC1 column at every threshold; filling that gap would require a separately specified and authorized extension (a `k=20` bucket term with its own `δ_20 = 0.05` grid, plus a (b)-family scenario run), not an unapproved extra NC1 run.
- If the current support rule cannot be defined because the §5A contradiction makes the complete analysis support empty as drafted, the affected rows say so and carry **PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE**. Bucket-local proxy results are never presented as the probability that the full study passes, in line with Revision F's own proxy-labeling language (Rev F:291, 372).

## 6. Proposed work item B: decide what "NC2" is meant to test

Two questions were bundled in the discussion. Keep them distinct in the draft and in any work order.

**Question B1: Is the `c*` heuristic calibrated to the signal scale that matters?**

This is the mechanistic bridge/NC2 question. It asks whether the threshold mapping is too pessimistic or optimistic under defined signal models, and what the corresponding `c*`-crossing probabilities are under the declared distributions. It does not, by itself, estimate the predictive gain from natural solvers.

**Question B2: Can the proposed `k` versus `k+C` estimator detect `Δ = δ*` with controlled error?**

This is the v0.3 Phase 1 software-simulation question. It requires a frozen simulation DGP, analysis procedure, inference target, support/gate rules, interval procedure, Type I error criterion, power criterion, and explicit owner authorization after protocol freeze. Revision F §5A currently records a structural problem — the conventional condition-number requirement makes the full support rule `P(pass) = 0` as drafted (Rev F:175) — so the **§5A M1/M2/M3 resolution and the recalculation of complete-rule probabilities (computable only after that resolution; Rev F §11 items 13–14) must precede a meaningful Phase 1 power result.** No §5A resolution has been adopted; reviewers recommend, Foued decides (Rev F:625).

Additionally, the two candidate primary analyses must not be blended, and the confirmatory one must be named by an owner decision (order item 6; see §8):

- **Revision F's primary proposal:** the held-out per-cell log-loss comparison between the fitted `k`-only (ridge-IRLS) and `k+C` models, equal-weight over eligible test cells, with the two-way cluster bootstrap interval and the `G6a-fix / G6a-id / G6b` inference-target machinery (Rev F:232-242).
- **The in-chat engine specification's scale-(i) alternative:** an exact stratified permutation test with a probability-slope statistic (in-chat only; not in the repository).

These differ in estimand, calibration, Type I error statement, and power target. The bridge can inform the choice; it cannot resolve it automatically.

Hygiene note: `M1/M2/M3` is used above in Revision F's sense (conditioning-rule candidates), per the §2 namespace footnote; the same three identifiers denote unrelated mutation tests in the NC1 record.

**Recommendation:** Run the target-translation report first. Then decide, on its results, whether a mechanistic NC2 calculation is still needed. Do not start the v0.3 Phase 1 simulation by calling it "NC2"; resolve its separate freeze blockers and authorization boundary first. No solver generation or hidden-outcome collection is part of either work item.

## 7. Decision sheet to prepare before simulation results

The report should end with a decision table whose criteria are agreed before any Phase 1 outputs are examined.

| Outcome | Proposed meaning | Required conditions |
|---|---|---|
| **GO: natural-solver predictive study** | Proceed to the next separately authorized phase aimed at the primary theory question | Complete-rule support is nonzero and adequate under the adopted protocol; the design is evaluable at the approved budget; the interval procedure controls Type I error and meets the owner-approved power/coverage criteria at the owner-approved target level (**see the `δ*`-power decision below**); projected cost is within the owner-approved ceiling |
| **ALTERNATIVE: engineered mechanistic study** | Do not spend the natural-solver budget under the current design; consider a separately chartered controlled-mechanism study | Natural-solver support/power is inadequate at the affordable budget, but the controlled design has a clear, separately stated estimand and can test the mechanism without being misrepresented as evidence about natural solvers |
| **PILOT-DECIDES (optional owner-decision path)** | An intermediate, bounded pilot determines which of the above rows is taken before a full committed spend | Only if the owner elects the pilot path in advance; its pass criterion must be registered before pilot outputs are examined (same pre-registration discipline as §8's two-threshold-set rule, Rev F:248); the pilot's result then feeds the GO/ALTERNATIVE/STOP decision without adding authorization of its own |
| **STOP / redesign decision** | Neither route currently justifies the planned cost, or neither has a valid, evaluable design | State the failed gate and what it implies for feasibility; do not claim that a failed feasibility gate falsifies the scientific theory |

**Standing caveat for every row:** GO, or passing the feasibility gate or an elected pilot's gate, authorizes only the next separately approved step. It does **not** confirm the scientific theory, and it never authorizes a later phase automatically (Rev F §8 authorization sequence; order item 9).

The following are **owner decisions still required before a protocol freeze**, not numbers for reviewers or agents to guess:

- Maximum affordable budget, expressed as attempts, hidden suites, and/or a monetary ceiling.
- Minimum acceptable Phase 1 power and the Type I error ceiling — **and the new decision whether power at `δ*` is gated.** Revision F's binding claim mapping gates power at `2δ*` and reports power at `δ*` without gating it ("Power AT δ* is reported, not gated", Rev F:268). The GO row above must not silently promote the reported-only `δ*` power into a gated requirement: either retain Revision F's existing criterion, or adopt a changed `δ*`-gated criterion as an explicit, owner-approved change recorded in the protocol.
- The final suite-count choice, consistent with Revision F's derived minimum constraints.
- The confirmatory-procedure choice between Revision F's held-out log-loss comparison and the engine-spec scale-(i) stratified-permutation alternative (order item 6; §6/§8).
- Whether an ALTERNATIVE mechanistic study is an acceptable fallback and what result it must deliver to be useful.
- Whether to elect the optional PILOT-DECIDES path and, if so, its pre-registered pass criterion.

Existing Revision F candidate budgets (`150` feasibility attempts and `600` confirmatory attempts) are not treated as final spend approval. The design itself says they require owner approval.

## 8. Required protocol blockers and authorization boundaries

Before the v0.3 predictive procedure can be simulated, the review must close the relevant Revision F items, at minimum:

1. §5A's M1/M2/M3 matrix/conditioning resolution and recalculation of complete-rule support probabilities (owner decision + reviewer verification; Rev F §11 items 13–14).
2. Coordinated O1–O5 resolution, including attempt-versus-valid/unique-body budgeting and the support/replication-grid mapping.
3. G6 inference-target choice and the calibration/coverage-truth method.
4. Support and split eligibility rules, including training-block/test-block behavior.
5. Predeclared FPR, power, coverage, and "not evaluable" criteria — including the `δ*`-power gating decision (§7) and the confirmatory-procedure choice (§6).
6. Owner approval of the estimand narrowing, DGP parameters, suite counts, budget, and proposed decision rule.

Authorization sequence remains:

1. Review and revise this VDraft.
2. Commit the controlling M3 Rev d / engine spec v1 §2 source texts into the repository (the §2.1 precondition); owner approves the target-translation computation and the precise work order.
3. Review the bridge report; decide whether NC2 is justified.
4. Resolve and review the v0.3 simulation-protocol blockers; freeze only after sign-off and owner approval.
5. Obtain separate explicit owner authorization before Phase 1 simulation.
6. Obtain separate authorization for each later study phase. Passing a gate never authorizes the next phase automatically.

NC1 remains closed — no rerun of NC1 computations is authorized to fill threshold-grid gaps or scenario-(b) gaps. Its source artifacts and results are not reopened by this plan. NC2 remains held until explicitly authorized. Phase 1 remains unauthorized until its protocol freeze and separate authorization. Solver generation and hidden-outcome collection remain unauthorized.

## 9. Review questions

Reviewers should respond to these specific questions and to the change record rather than reopening unrelated provenance checks:

1. Does the revised `β_min` framing (fixed `s_ref = 0.12703` unit; within-`k` variation as identification input with explicit bucket weighting and body-count scaling in A1.3) match the controlling M3 definition once its text is committed? If the committed text prescribes anything different, it governs and the bridge re-ghosts accordingly.
2. Is the target bridge's population-oracle estimand correctly aligned with Revision F under the pinned calibration convention (A2.2), and is the candidate mapping of A2.3 correctly quarantined as non-authoritative pending the source?
3. Is the distinction between the mechanistic NC2 question and v0.3 Phase 1 power/Type I error validation correctly stated, including the newly added confirmatory-procedure blocker?
4. Are the GO / ALTERNATIVE / PILOT-DECIDES / STOP conditions logically complete without claiming that a feasibility failure falsifies the theory, and is the `δ*`-power decision correctly routed to the owner?
5. Are there any scientific blockers to the bridge calculation itself beyond the §0.1 list, as distinct from blockers to Phase 1 or real data collection?
6. Does the source document `v03p/VDRAFT_M3_SOURCE_DEPENDENCY_2026-10-18.md` correctly delimit what is preserved verbatim versus what remains an unresolved document dependency?

## 10. Source anchors

- v0.3-P Phase 0 Design, Revision F, especially §§1, 3, 5–5B, 7, 9–12, on branch snapshot `4551cac`: `v03p/PHASE0_DESIGN_2026-10-15_RevF.md` (quoted anchors: :121, :164-175, :232-242, :248, :257-272, :281-287, :291, :362, :364, :623, :625).
- NC1 rev-3 report on branch snapshot `4551cac`: `v03p/nc1/nc1_report.md`.
- NC1 engine definition of `c* = (1.25/β)²`, the `c` construction, `s_ref = 0.12703` exactly, `CSTAR`, and `SCENS`: `v03p/nc1/nc1_calc.py` (lines 14-26, 96, 103-110).
- NC1 RUN record through M1b: `v03p/nc1/RUN.txt`, commit `4551cac`.
- Owner implementation order for this revision: `v03p/VDRAFT_IMPLEMENTATION_ORDER_2026-10-18.md`, commit `906dd351e647d3d28a70ae16a01070e34fdca8a6`.
- Source-dependency record (M3 Rev d / engine spec v1 §2): `v03p/VDRAFT_M3_SOURCE_DEPENDENCY_2026-10-18.md` (created by this revision).

**Status line:** This VDraft (Revision 2) is a proposal produced under the owner implementation order. Its `β_min` numerical mapping is PROVISIONAL-PENDING-SOURCE; no new computation or study phase is authorized by its creation or by the implementation order.
