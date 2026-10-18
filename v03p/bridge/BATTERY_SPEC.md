# Bridge verification battery — frozen declaration, part 1 (definitions)

**Date:** 2026-10-18. **Status:** FREEZE PART 1 of the pre-registered verification battery under the
owner bridge authorization (Foued, 2026-10-18; bridge draft §0.2 item 12; source record §8 part 5).
This file fixes, before any battery code is run: the declared support-conditioned weight definitions
(W-DEF), the tested `γ` values, the tolerances, and the required method declarations. The battery
code (freeze part 2) is committed with its blob hash referencing this file before any executed run.
Per the symmetric-stop rules (CLAUDE round-7; GPT concurrence; owner reiterated): **any tolerance or
code change after first official numbers exist voids the pass** and forces a re-run with the original
record intact; **no number from a battery run exists in this commit.**

## 1. Scope

Rows: matched-population scenarios (a) and (c), variants `a-hist`, `a-50:50`, `c-hist`, `c-50:50`
(`SCEN` in-ranged mixes from the committed A1 source `v03p/a1/a1_support_comparison.py:391-402`), at
the declared confirmatory scale `N = 600`. Scenario (b) is out of scope (bridge NOT DEFINED there,
draft A2.3). Every battery number carries **PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE**.

## 2. Declared weight definitions (W-DEF) — support-conditioned, bucket-local proxy

Per bucket `k ∈ {5, 10}` and variant with in-range mix shares `p_k` (from `SCEN`; out-of-range mass
`p_0 + p_25` does not enter the two-bucket scope):

1. **Bucket size law:** `n_k ~ Binomial(N = 600, p_k)` (Revision F DGP `k`-mix, Rev F:281-287).
   Variant mixes: `a-hist` (0.10, 0.05); `a-50:50` (0.075, 0.075); `c-hist` (0.03, 0.02);
   `c-50:50` (0.025, 0.025) — in the order `(p₅, p₁₀)`.
2. **C-level law within bucket `k`:** per-level marginals `ρ_{c|k} = CK[k][1]` of the committed A1
   source (`a1_support_comparison.py:59-66`): the exact Rev F DGP marginals (uniform over feasible
   count vectors, Rev F:287). `k = 5`: levels `{0.2, 0.4, 0.6, 0.8, 1.0}`, `Z = 252`;
   `k = 10`: levels `{0.2, 0.3, 0.4, 0.5}`, `Z = 2247`. Level weights are **not equiprobable** in
   general.
3. **Bucket support predicate (Rev F conditions 1–4, bucket-local; AMENDED before code freeze —
   amendment note below):** the rule is Revision F:145-148 — a bucket is included iff
   (1) `2 ≤ k ≤ 24` (in-range by construction here), (2) `n ≥ 8` distinct canonical bodies,
   (3) `≥ 2` distinct `C` values, and (4) **both C extremes of the bucket are represented by ≥ 4
   distinct bodies each** — the OBSERVED extremes of the realized bucket (whatever values they
   are), not the grid endpoints. This is exactly the committed A1 source's `S0` rule
   (`a1_support_comparison.py:10-13`: `S0: n >= 8, >= 2 distinct C values, >= 4 bodies at each
   OBSERVED C extreme`); conditions 2–3 are implied by the both-extremes-≥4 clause. Its use here
   is the bucket-local population proxy only — the complete-rule pass probability stays
   `P(pass) = 0` as drafted (Rev F:175), unchanged. **Amendment audit trail:** the initial
   declaration (commit `a527828`, 2026-10-18) stated a grid-endpoint reading
   (`N_{0.2} ≥ 4 ∧ N_{cmax-grid} ≥ 4`), citing NC1's `F5/F10` (`A.f_s1`) as precedent; that was a
   transcription error — `f_s1` is NC1's own `S1(m)` proxy ("≥ m bodies outside the modal value",
   `a1_support_comparison.py:190-206`), a different rule within NC1's closed scope, and grid-endpoint
   counts are mathematically neither necessary nor sufficient for the observed-extremes condition.
   The error was caught by the pre-code predicate re-verification (WW pin) before any battery code
   was written or run; nothing was computed under the erroneous reading.
4. **Stratum weights:** `w_k = E[n_k·1{I_k}] / Σ_{k'∈{5,10}} E[n_{k'}·1{I_{k'}}]` — normalized over
   the two strata (equal weight per eligible test cell reduces to equal weight per eligible body
   among eligible cells, Rev F:232; suite effect marginalized symmetrically — A2.2 rider).
5. **Within-stratum C-level weights:** `π_{c|k} = E[N_c·1{I_k}] / E[n_k·1{I_k}]` — explicitly
   support-conditioned and non-uniform.
6. All supported-population quantities used by the battery and downstream bridge
   (`Var_k^{sup}(C)`, `E_k^{sup}(C)`, the `Δ` sums, and later `β_pop` inputs) are computed from
   these same `w_k`, `π_{c|k}`.
7. **Caveat (carried on every row):** `I_k` is the bucket-local proxy under Rev F §5A as drafted;
   these weights are **PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE** and support no claim about the
   real study's population (draft A2.3, CLAUDE caveat).

**Grouping identity used by both paths (declared here once):** under the multinomial composition law
per bucket size `n`, for each ordered pair of levels `a < b` (candidate observed extremes) the
grouped counts `(N_a, T_{ab}, N_b) = (N_a, Σ_{a<c<b} N_c, N_b)` are
`Trinomial(n; ρ_a, ρ_{ab}, ρ_b)` with `ρ_{ab} = Σ_{a<c<b} ρ_{c|k}` (exact multinomial
marginalization), and the within-group split is `E[N_c | T_{ab}] = T_{ab}·ρ_{c|k}/ρ_{ab}` for
`a < c < b`. The predicate `I_k` decomposes over pairs disjointly:
`P(I_k | n) = Σ_{a<b} P(all draws within [a,b] ∧ N_a ≥ 4 ∧ N_b ≥ 4 | n)`.

## 3. Production and reference paths (both exact; structurally independent)

- **REFERENCE** (independent; closed forms only; no shared weighting code): per-`n` aggregates by
  the **observed-pair sums** above — `P(I_k|n) = Σ_{a<b} Σ_{c_a ≥ 4, c_b ≥ 4, c_a + c_b ≤ n}
  C(n; c_a, c_b, n − c_a − c_b)·ρ_a^{c_a}·ρ_b^{c_b}·ρ_{ab}^{n − c_a − c_b}`, and per level `c`
  `E[N_c·1{I_k}|n]` split into c-as-left-endpoint (`c = a`, own count term), c-as-right-endpoint
  (`c = b`), and c-strictly-inside (`(n − c_a − c_b)·ρ_c/ρ_{ab}`) contributions over the same
  pair/trinomial cells — the same mathematical formulation as the committed A1 `f_s0` implementation
  (A1:239-257), plus
  `Δ_ref(γ) = Σ_k ŵ_k Σ_c π̂_{c|k}·D_KL[Bern(q(k,c,γ)) ‖ Bern(q̄̂_k)]` with
  `q̄̂_k = Σ_c π̂_{c|k}·q(k,c,γ)` — the exact zero-RE benchmark of A2.2, evaluated entirely from the
  reference's own weights.
- **PRODUCTION** (the bridge machinery, reused later for `γ*` and `β_pop`): per-`n` aggregates
  `P(I_k | n)`, `E[N_c·1{I_k} | n]` by the **first-nonzero-block decomposition** — a level-ordered
  closed-form scheme conditioned on which level is the bucket's smallest occupied level, with the
  tails evaluated by disjoint-block multinomial disaggregation (prefix/left-tail sums
  `LA(u) = Σ_a Σ_{c_a ≥ 4} C(u; c_a)·ρ_a^{c_a}·(1 − ρ_{≤a})^{u − c_a}` and the mirrored
  right-tail `RC(w)`, combined over a binomial split of the remaining mass) — an independent
  derivation whose only basis is the W-DEF predicate above, sharing no weight code with the
  reference, folded over `n` by the Binomial bucket-size law. Fitting machinery: **unpenalized
  Newton–IRLS** on the restricted parametrizations justified by the Rev F §5A rank table
  (Rev F:166-173): the committed 5-column RCS family restricted to `{5, 10}` spans **all stratum
  functions** (rank exactly 2), and the extended family's restriction = same stratum constants +
  `C` (rank 3); therefore the fitted prediction spaces of both committed families equal the
  restricted parametrizations `{1{k=5}, 1{k=10}}` (baseline) and `{1{k=5}, 1{k=10}, C}` (extended).
  Reported fit metric `grad` = per-parameter exact column score `|Σ_cells Ω_j (t_j − q̂_j) x_{ji}|∞`
  at the reported parameter vector (definition clarified pre-code-freeze, 2026-10-18).
  σ = 0 targets: `p̄ = ` truth, `q(k, c, γ) = logit⁻¹(−log(1+k) + γC)` (`θ0 = 0`, `θ1 = −1`).
  σ = 1 targets: `p̄(k, c; γ) = E_{s~N(0,2)}[logit⁻¹(−log(1+k) + γC + s)]` (declared zero-mean
  independent effects; `u + v ~ N(0, σ_u² + σ_v²) = N(0, 2)`), computed by Gauss–Hermite quadrature
  with node doubling 64 → 128 → 256 until the declared convergence criterion holds, plus a seeded
  Monte Carlo cross-check (`2·10⁶` draws of `s`; SE reported). Family-level population losses depend
  on the truth only through `p̄` (`E_{u,v}[−p log q − (1−p) log(1−q)] = CE(Bern(p̄), q)`); check V-2
  validates this equivalence numerically.
- **W0 brute-force validation (both paths, small `n`):** explicit enumeration over all C-count
  vectors (`C(n + V − 1, V − 1)` compositions, e.g. 8008 at `n = 12, k = 5`) gives the exact
  predicate probabilities and per-level moments; both paths must agree with brute force on every
  aggregate to `≤ 1e-12` per `n ≤ 12`, and (consistent with A1's own precedent) spot-checks at
  slightly larger `n`.

## 4. Tested `γ` values and frozen tolerances

- `γ_grid` (check i, weight outputs, tables): `(0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0)`.
- **Small-`γ` band** (quadratic-form sanity, reported only): `γ ∈ {0.25, 0.5, 1.0}`.
- **Monotonicity grid** (check ii): `γ = 0, 0.5, 1.0, …, 8.0` (17 points), at σ = 0 (exact) and
  σ = 1 (GH at the frozen node count). Criteria: σ = 0: `Δ(γ_{j+1}) ≥ Δ(γ_j) − 1e-12`;
  σ = 1: `≥ Δ(γ_j) − 5e-10` (quadrature slack).
  **Amendment (post-freeze run 2, 2026-10-18, symmetric-stop protocol: run stopped at
  `ii-s0-mono` on the `c` rows, record archived; amendment committed before the re-run):** the
  single-peaked shape discovered at the check-(iii) amendment has row-dependent `γ_peak`; for the
  `c` rows the peak lies INSIDE the declared `[0, 8]` grid (run-2 evidence: `c-hist`
  `Δ` rises through `γ = 7.5` and declines by `−1.96e-4` at `γ = 8.0`, peak `≈ 3.97e-2` at
  `γ ≈ 7.6`), so a rising-through-8 contract cannot hold there. Amended contract for both σ = 0
  and σ = 1 monotonicity checks: **single-peak behavior on the grid** — successive grid diffs
  stay `≥ Δ(0) − rising_slack` (`σ = 0: 1e-12`, `σ = 1: 5e-10`) until the first negative diff
  (recorded as the peak location), and **no further rise beyond `+5e-10`** after that point
  (declines of any size belong to the falling branch); dip-below-slack on the rising branch or a
  second rise past the falling slack trips the check. The declared thresholds and grids are
  otherwise unchanged.
- **Check (i) zero-RE agreement:** at every `γ_grid` point, `|Δ_prod(γ) − Δ_ref(γ)| ≤ 1e-9`
  (absolute; both paths exact; achieved margins reported).
- **W1 precursor (weights cross-agreement):** production vs reference `w_k`, `π_{c|k}`, and derived
  `Var_k^{sup}(C)` agree to `≤ 1e-10` absolute (and per-`n` `P(I_k|n)`, `E[N_c·1{I}|n]` at every
  `n ≤ 600`).
- **W2 artifact cross-check (vs the committed A1 source):** the battery's per-`n`
  `P(I_k|n)` (reference path) agrees with `A1.f_s0(k, n)` (`a1_support_comparison.py`, the committed
  conditions-1–4 computation) to `≤ 1e-10` at every `n ≤ 600`; a mismatch beyond the tolerance is a
  stop-level defect.
- **W3 brute-force agreement:** the W0 enumeration checks both paths at small `n` to `≤ 1e-12`
  per aggregate.
- **Check (ii):** `|Δ(0)| ≤ 1e-12` at σ = 0 and σ = 1.
- **Check (iii) bisection self-test (σ = 0):** solve `Δ(γ) = δ* = 0.020273255405408218` and
  `Δ(γ) = 2δ* = 0.040546510810816436` inside the declared bracket `[0, 8]`; attainment
  `|Δ(γ̂) − target| ≤ 1e-4` (Rev F:364 convention); iterations and achieved margins reported. The
  σ = 1 calibration re-attains the same tolerance per row at calibration time and reports it.
  **Amendment (pre-code-freeze, 2026-10-18, feasibility probe — no battery run executed, no
  battery-run number in any commit):** the zero-RE benchmark `Δ(γ)` is single-peaked in `γ`: rising
  on `[0, γ_peak ≈ 7.5–9]` (per row), then declining toward 0 as `γ → ∞` (all level truths saturate
  to a common limit, so the marginal spread vanishes again). Row shape evidence from the probe:
  `Δ_peak` ∈ `[3.74e-2, 3.97e-2]` < `2δ* = 0.04055` for all four rows, with `γ_peak` in `[7.5, 9]`;
  the declared `[0, 8]` mono grid lies inside the rising branch (monotonicity unaffected).
  Consequently the `2δ*` target **has no real solution in any bracket** and the amended PASS
  criterion of check (iii) is: *for every target, the solver behaves correctly per the amended
  contract — either (a) attainment on a solvable target with `|Δ(γ̂) − target| ≤ 1e-4`, or (b)
  not-attained **with the exact bracket evidence** `(Δ(lo) < target) ∧ (Δ(hi) < target)` recorded.*
  The `δ*` row solves are real (probe: `γ̂ ≈ 3.78–4.94` by row, attained well inside tolerance);
  the `2δ*` rows report the (b) arm with evidence. Unattainability of `2δ*` is a **finding** to be
  restated in the later bridge report (γ*/β_pop stage), not a machinery failure.
- **GH convergence criterion:** node doubling alters no `p̄`-dependent battery quantity by more than
  `1e-12` absolute; node counts reported per row. **MC cross-check:** `|Δ_MC − Δ_GH| ≤ 5·SE_MC`
  with an absolute float-noise floor `+ 1e-12` — **amended pre-code-freeze (2026-10-18),
  feasibility probe**: at `γ = 0` both `Δ` values are float-scale (`SE ≈ 1e-19`, margins at the
  `1e-18` float level), so the bare `5·SE` expression is below quadrature/float noise at the
  degenerate point; `5·SE + 1e-12` matches the declared V-2 expression form (criterion verified
  PASS for the probe row at every `γ_grid` point with margins up to `≈ 1e-5` vs `5·SE` limits
  `≈ 1e-4`).
- **Check (iv) mutation battery** (production path mutated; reference untouched; threshold
  `γ = 2.0`; every mutation must trip its target check, recorded in the report):
  `m1` uniform `C` weights (`π_c = 1/#levels`, stratum weights kept) → must trip check (i)
  (`|Δ_mut − Δ_ref| > 1e-6`); `m2` variant mix swap (c-mix weights substituted into the a-row) →
  must trip check (i); `m3` retained `RIDGE = 1e-6` penalty in the σ = 0 production fit → must trip
  check (i) (validates the unpenalized-optimum rider, round-7); `m4` extended predictions
  substituted by the true marginals `p̄` at σ = 1 → must trip check (v).
  **Amendment (post-freeze run 3, 2026-10-18, symmetry-of-record protocol): run 3 completed with
  the m1–m3 gates silently bypassed — a surplus argument placed `MUT_TOL = 1e-6` into the
  `report_only` positional slot of the check recorder, whose truthiness disabled stop-on-fail and
  recorded verdicts `n/a` while every margin stayed the real measured value; run 3's report is
  archived intact as `BATTERY_REPORT_2026-10-18_run3_mutations_report_only_bypass.md` with
  measured margins m1 `5.917e-3 / 4.906e-3 / 1.180e-2 / 7.256e-3`, m2
  `1.912e-3 / 2.485e-3 / 2.515e-17 / 1.816e-3`, m3 `7.887e-6 / 7.896e-6 / 7.908e-6 / 7.871e-6`
  (a / a-50:50 / c-hist / c-50:50), and the amendment is committed before the re-run. Two
  corrections, jointly declared: (a) **gating restored** — the m1–m3 recorder calls drop the
  surplus argument, so mutation failures stop the run like every other declared check (a direct
  consequence is that run 3's `PASS` banner does not stand; the standing record will be the
  post-amendment run); (b) **m2 amended to cross-substitution per row** — the mutation substitutes
  the OTHER declared mix into the row's truth table (`c-hist` on `a`-rows, as originally declared;
  `a-hist` on `c`-rows). The original one-directional wording cannot trip on `c`-rows by
  construction: substituting a mix into a row that already IS that mix leaves `Δ` unchanged at
  float scale (`2.515e-17`, run-3 evidence), which is not a mutation. Cross-substitution preserves
  the intent (the mix choice must be detectable in `Δ`) symmetrically; the run-3 margins put the
  expected cross-substitution effects of order `1e-3`, far above `1e-6`. `m1`, `m3`, `m4` are
  unchanged by this amendment.
- **Check (v) oracle-bound trip-wire (σ = 1):** with the fitted extended family's achieved loss
  `L_ext*`, the gap `g = L_ext* − Σ_k w_k Σ_c π_{c|k} H(p̄(k,c))` must be `> 1e-9` at every
  `γ_grid` point (the marginalized truth is generally not logit-linear in `C` under σ = 1 — GPT round-8);
  the substitution mutation `m4` must drive `g ≤ 1e-12` (trip). A production gap `≤ 1e-9` without a
  mutation **stops the run** for implementation correction before any result is interpreted.
  **Amendment (post-freeze run 1, 2026-10-18, symmetric-stop protocol: run stopped at this check,
  original record archived; amendment committed before the re-run):** at `γ = 0` the σ = 1 truth has
  no `C`-dependence at all (`p̄(k,c,0)` is constant per stratum), so the extended restricted family
  represents it **exactly** (the fit places `β_C = 0`; run-1 evidence: `g(0) = 0` at float scale
  `≈ 1.9e-18`, per-stratum constant fitted predictions) and the round-8 wire cannot hold there.
  The amended gate applies the `> 1e-9` criterion to the **`C`-bearing points** `γ ∈ γ_grid ∩ [0.25, 8]`
  (`run-1` evidence: `g` ∈ `[1.09e-8, 3.81e-5]` across those points, all above the threshold with
  margin) and records `γ = 0` as a report-only row (exact-representability evidence), which matches
  the round-8 wording ("generally not logit-linear"). The substitution mutation `m4` at `γ = 2.0`
  is unchanged.
- **Q-check (quadratic form, sanity only, no gate):** report
  `|Δ_prod(γ) − Δ_quad(γ)|` across the small-`γ` band, where
  `Δ_quad(γ) = (γ²/2)·Σ_k w_k·p_k(1−p_k)·Var_k^{sup}(C)` (A2.2 scope paragraph, zero-RE only).
- **V-1 (σ-transition check):** production `p̄` at σ = 0 computed by direct `logit⁻¹(η)` equals the
  GH machinery evaluated with a point-mass scale to `≤ 1e-12`.
- **V-2 (marginal-equivalence check, σ = 1, `γ = 2.0`):** seeded MC over realized `(u, v)` draws and
  Bernoulli outcomes of the population loss equals the `p̄`-CE computation within `5·SE + 1e-12`.

## 5. Execution rules (owner order; draft battery block; symmetric-stop)

Results and margins for **every** check are reported, including passes. Any failed check stops the
run as a blocker with the concrete failure reported; no post-hoc tolerance or code change without
voiding the pass and re-running with the original record intact. Only after a passing battery:
`γ*` calibration at `δ*` and `2δ*`, then `β_pop` → provisional `c*` mapping → gap report;
method, convergence, node counts, MC SE, achieved tolerances, and limitations published in a
separate committed report. `0.10` (→ `c* = 156.25`) is the owner's comparison anchor only — never a
tuning target. Every output **PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE**; scenario (b) NOT
DEFINED.
