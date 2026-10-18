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
3. **Bucket support predicate (Rev F conditions 1–4, bucket-local):**
   `I_k ⟺ n ≥ 8 ∧ N_{cmin(k)} ≥ 4 ∧ N_{cmax(k)} ≥ 4`, with `cmin(k) = 0.2` and
   `cmax(k) = 1.0` (`k = 5`) / `0.5` (`k = 10`) — the grid endpoints. Condition 2's "≥ 2 distinct C
   values" is implied by both-extremes-≥4. This is the same predicate whose outcome-blind
   bucket-local probabilities `A.f_s1(k, n, 4)` back NC1's `F5/F10` tables; its use here is the
   bucket-local population proxy only — the complete-rule pass probability stays `P(pass) = 0` as
   drafted (Rev F:175), unchanged.
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
per bucket size `n`, the grouped counts `(A, T, B) = (N_{cmin}, Σ_{mid-levels} N_c, N_{cmax})` are
`Multinomial(n; ρ_{cmin}, ρ_{mid}, ρ_{cmax})` where `ρ_{mid} = Σ_{mid} ρ_{c|k}`; per-`n` support
aggregates depend only on this trinomial plus the within-group split `E[N_c | T] = T·ρ_{c|k}/ρ_{mid}`
(exact multinomial marginalization).

## 3. Production and reference paths (both exact; structurally independent)

- **PRODUCTION** (the bridge machinery, reused later for `γ*` and `β_pop`): per-`n` aggregates
  `P(I_k | n)`, `E[N_c·1{I_k} | n]` by a capped-state dynamic program over the grouped trinomial
  (saturating counters at the predicate thresholds), folded over `n` by the Binomial bucket-size law
  with truncation noted and any dropped mass bounded and reported. Fitting machinery: **unpenalized
  Newton–IRLS** on the restricted parametrizations justified by the Rev F §5A rank table
  (Rev F:166-173): the committed 5-column RCS family restricted to `{5, 10}` spans **all stratum
  functions** (rank exactly 2), and the extended family's restriction = same stratum constants +
  `C` (rank 3); therefore the fitted prediction spaces of both committed families equal the
  restricted parametrizations `{1{k=5}, 1{k=10}}` (baseline) and `{1{k=5}, 1{k=10}, C}` (extended).
  σ = 0 targets: `p̄ = ` truth, `q(k, c, γ) = logit⁻¹(−log(1+k) + γC)` (`θ0 = 0`, `θ1 = −1`).
  σ = 1 targets: `p̄(k, c; γ) = E_{s~N(0,2)}[logit⁻¹(−log(1+k) + γC + s)]` (declared zero-mean
  independent effects; `u + v ~ N(0, σ_u² + σ_v²) = N(0, 2)`), computed by Gauss–Hermite quadrature
  with node doubling 64 → 128 → 256 until the declared convergence criterion holds, plus a seeded
  Monte Carlo cross-check (`2·10⁶` draws of `s`; SE reported). Family-level population losses depend
  on the truth only through `p̄` (`E_{u,v}[−p log q − (1−p) log(1−q)] = CE(Bern(p̄), q)`); check V-2
  validates this equivalence numerically.
- **REFERENCE** (independent; closed forms only; no shared weighting code): same per-`n` aggregates
  by **direct trinomial sums and inclusion–exclusion**
  (`P(I_k|n) = 1 − P(A ≤ 3) − P(B ≤ 3) + P(A ≤ 3 ∧ B ≤ 3)`, moments by truncated-mean algebra),
  folded exactly like production but computed through the different formulation; and
  `Δ_ref(γ) = Σ_k ŵ_k Σ_c π̂_{c|k}·D_KL[Bern(q(k,c,γ)) ‖ Bern(q̄̂_k)]` with
  `q̄̂_k = Σ_c π̂_{c|k}·q(k,c,γ)` — the exact zero-RE benchmark of A2.2, evaluated entirely from the
  reference's own weights.

## 4. Tested `γ` values and frozen tolerances

- `γ_grid` (check i, weight outputs, tables): `(0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0)`.
- **Small-`γ` band** (quadratic-form sanity, reported only): `γ ∈ {0.25, 0.5, 1.0}`.
- **Monotonicity grid** (check ii): `γ = 0, 0.5, 1.0, …, 8.0` (17 points), at σ = 0 (exact) and
  σ = 1 (GH at the frozen node count). Criteria: σ = 0: `Δ(γ_{j+1}) ≥ Δ(γ_j) − 1e-12`;
  σ = 1: `≥ Δ(γ_j) − 5e-10` (quadrature slack).
- **Check (i) zero-RE agreement:** at every `γ_grid` point, `|Δ_prod(γ) − Δ_ref(γ)| ≤ 1e-9`
  (absolute; both paths exact; achieved margins reported).
- **W1 precursor (weights cross-agreement):** production vs reference `w_k`, `π_{c|k}`, and derived
  `Var_k^{sup}(C)` agree to `≤ 1e-10` absolute.
- **Check (ii):** `|Δ(0)| ≤ 1e-12` at σ = 0 and σ = 1.
- **Check (iii) bisection self-test (σ = 0):** solve `Δ(γ) = δ* = 0.020273255405408218` and
  `Δ(γ) = 2δ* = 0.040546510810816436` inside the declared bracket `[0, 8]`; attainment
  `|Δ(γ̂) − target| ≤ 1e-4` (Rev F:364 convention); iterations and achieved margins reported. The
  σ = 1 calibration re-attains the same tolerance per row at calibration time and reports it.
- **GH convergence criterion:** node doubling alters no `p̄`-dependent battery quantity by more than
  `1e-12` absolute; node counts reported per row. **MC cross-check:** `|Δ_MC − Δ_GH| ≤ 5·SE_MC`
  (SE reported; the MC step used for totals at the frozen node count's convergence level).
- **Check (iv) mutation battery** (production path mutated; reference untouched; threshold
  `γ = 2.0`; every mutation must trip its target check, recorded in the report):
  `m1` uniform `C` weights (`π_c = 1/#levels`, stratum weights kept) → must trip check (i)
  (`|Δ_mut − Δ_ref| > 1e-6`); `m2` variant mix swap (c-mix weights substituted into the a-row) →
  must trip check (i); `m3` retained `RIDGE = 1e-6` penalty in the σ = 0 production fit → must trip
  check (i) (validates the unpenalized-optimum rider, round-7); `m4` extended predictions
  substituted by the true marginals `p̄` at σ = 1 → must trip check (v).
- **Check (v) oracle-bound trip-wire (σ = 1):** with the fitted extended family's achieved loss
  `L_ext*`, the gap `g = L_ext* − Σ_k w_k Σ_c π_{c|k} H(p̄(k,c))` must be `> 1e-9` at every `γ_grid`
  point (the marginalized truth is generally not logit-linear in `C` under σ = 1 — GPT round-8);
  the substitution mutation `m4` must drive `g ≤ 1e-12` (trip). A production gap `≤ 1e-9` without a
  mutation **stops the run** for implementation correction before any result is interpreted.
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
