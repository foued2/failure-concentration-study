# M2 complete-rule feasibility — bounded calculation (2026-10-20)

**Status:** REVIEW DRAFT / CALCULATION RECORD. Produced under the owner work order
"IMPLEMENT CLAUDE'S REVIEW AND DELIVER M2 FEASIBILITY DATA" (Foued, 2026-10-20, relayed by
GPT/). This record does **not** execute G6b, Phase 1, solver generation, or hidden-outcome
collection; it does **not** adopt M2 or O3; it does **not** authorize simulation, a master merge,
tags, a protocol freeze, or publication. All numbers below are deterministic calculations under
the declared support model, except where explicitly labeled as a diagnostic or as unresolved.

**Decision use.** This record answers one bounded question: under the declared Rev F support
model and the proposed M2 complete rule, how many of `R = 2000` simulated replications would be
eligible, and is the proposed `κ_eff ≤ 30` gate a material additional constraint? It does not
translate the answer into a G6b target claim. The target-translation and authorization blockers
remain in the main decision document.

---

## 1. Inputs and source versions

| Input | Version / hash | Use |
|---|---|---|
| `v03p/PHASE0_DESIGN_2026-10-15_RevF.md` | SHA-256 `BB2B2343E71EF3D57AD738F2BE7CF6F8958590AC5CD1B790750009629EB05658` | controlling support/outcome design; §9.1 declared support, §9.2 grid/O3, §5A rank/κ rule |
| `v03p/a1/a1_support_comparison.py` | SHA-256 `CF3840F108F82E6739CC01DEEDA1623070E2CEC84EB5059F293C4193D3C96C74` | committed CK support machinery, S0/S1/S2 rules, exact `f_s0` cross-check |
| `v03p/bridge/battery.py` | SHA-256 `5E952A202FA0335A305A5110A9D810F86731D9ABAA1D69C12E3E71DD57707A05` | DGP constants `TH0=0`, `TH1=−1`, `SIG_B=SIG_S=1`, `MC_SEED=20261018`; A1 import |
| `study/models.py` | SHA-256 `4E4226FE055DCFDFC4074C77EB5CBF8860F1C747A21DD15DC53A8AF3C6C4C420` | frozen RCS basis / design rows (`rcs_basis`, `KNOTS`) |
| `v03p/VDRAFT_Target_Bridge_and_Research_Decision_2026-10-18.md` | SHA-256 `CB873A27C7490BD9246864FCE35FDBA3A36DDAA359B166D9F41C44F0066EC301` | current Revision 3 decision entry; the pre-restructure Revision 2 draft is preserved at SHA-256 `24D04F8156866029545615F0FDBC0D7995C7BFB12F9BC039EEB3C66224E2744D` in the review log |
| `v03p/bridge/m2_complete_rule_feasibility.py` | SHA-256 `D18A5E35D667871175EB0217BC9E0DEE1120E9383847A0FD1991597368B1104C` | main calculation |
| `v03p/bridge/m2_complete_rule_feasibility_2026-10-20.json` | SHA-256 `A3EE7B35A6F69297D7ED38C3666F244679CF5FDEF1E58070C61B47CD90929193` | machine-readable results |

Source files were read, not modified. The calculation uses Python 3.14.5 with NumPy 2.4.6; it does
not import `battery.py` and does not use any sampler. The A1 import was used only for the
independent `f_s0` cross-check reported in §7.

---

## 2. Model and assumptions

### 2.1 Declared support model (Rev F §9.1; same marginals as A1)

1. Each simulated body independently draws a probe-count level `k` from the scenario categorical
   mix `SCEN` (`k ∈ {0, 5, 10, 20, 25}`; `k = 0` and `k = 25` are outside the in-range support).
2. Conditional on `k ∈ {5, 10, 20}`, the body's six family-failure counts are drawn uniformly from
   the feasible vectors (each count `0..5`, total `k`); `C = max(family)/k`. The induced marginal
   distributions are the committed A1 weights:
   - `k=5`: `{0.2, 0.4, 0.6, 0.8, 1.0}` with probabilities `{0.023810, 0.476190, 0.357143, 0.119048, 0.023810}` (252 vectors);
   - `k=10`: `{0.2, 0.3, 0.4, 0.5}` with probabilities `{0.009346, 0.233645, 0.427236, 0.329773}` (2247 vectors);
   - `k=20`: `{0.2, 0.25}` with probabilities `{0.056075, 0.943925}` (2247 vectors).
3. A replication generates `N_b` bodies; eligibility is a deterministic, outcome-blind function of
   the realized body multiset. `N_b` is the only size variable in this calculation.
4. Replications under the declared simulation design are independent; therefore
   `N_eligible ~ Binomial(R, p)` with `R = 2000` and `p = P(complete rule)`. This is the declared
   Phase-1 simulation design, not a claim about a natural-solver population; see §6.

### 2.2 Support rule (conditions 1–4; A1 S0)

A bucket `k` passes iff `n_k ≥ 8`, at least two distinct `C` values are observed, and at least four
bodies lie at the observed minimum and at least four at the observed maximum. The analysis support
requires at least two in-range buckets to pass. These are the exact A1/Rev F conditions; the
complete rule adds the rank/conditioning requirement below.

### 2.3 Proposed M2 complete rule

Conditions 1–4 (the rank-increase is implied by the extreme-count conditions) **and**
`κ_eff ≤ 30` on the column-standardized extended design matrix:

- body-level rows, columns `[1, RCS_1..RCS_4(log(1+k)), C]`;
- intercept not standardized; every non-intercept column centered and scaled to unit population SD
  over the in-support rows (`ddof=0`);
- rank tolerance `1e-9 × s_max`; `κ_eff = s_1/s_r`.

The κ implementation was validated against the three recorded spot values from the 2026-10-19
analysis (see §7).

### 2.4 What is not assumed

- No independent-Bernoulli eligibility is assumed across bodies: the declared model draws `k` per
  body and `C` conditional on `k`, then applies the bucket/support rule to the realized multiset.
  The count model is Binomial only at the replication level, as in the declared simulation design.
- No unweighted pattern frequency is used. Every exact enumeration sums the declared design
  probability (multinomial bucket counts and the A1 conditional weights).
- No outcome, correctness, or error rate is modeled or estimated. Eligibility is outcome-blind.

---

## 3. Exact probability of the conditions 1–4 support

The bucket pass probability `f_k(n)` is computed by the exact A1 sum over disjoint
"observed-minimum/observed-maximum" pairs; it was cross-checked against `a1_support_comparison.f_s0`
for `k ∈ {5,10,20}` and `n ∈ {8,10,12,16,20,30,60}` (maximum absolute difference `3.9e-15`). The
cell value is the multinomial sum over in-range bucket counts of `P(≥2 buckets pass)`; the count box
covers ±8 SD with the omitted tail recorded in the JSON (tail bound `≤1e-12` for the reported cells).

`E[N_eligible] = 2000 × P(conditions 1–4)` and `P(N≥39)` is the exact Binomial(2000, p) survival
probability. The values are **upper bounds** on the complete-rule eligibility (the κ gate can only
remove replications).

### 3.1 Historical Mixes

| Scenario | `N_b` | `P(conditions 1–4)` | `E[N]` | `P(N≥39)` |
|---|---:|---:|---:|---:|
| (a)-hist | 60 | 5.95865e-6 | 0.012 | 0 |
| (a)-hist | 113 | 1.11682e-3 | 2.234 | 0 |
| (a)-hist | 120 | 1.54570e-3 | 3.091 | 0 |
| (a)-hist | 150 | 4.27948e-3 | 8.559 | 0 |
| (a)-hist | 240 | 2.18821e-2 | 43.764 | 0.7871 |
| (a)-hist | 300 | 3.95341e-2 | 79.068 | 1.0 |
| (a)-hist | 400 | 6.05516e-2 | 121.103 | 1.0 |
| (a)-hist | 450 | 6.35138e-2 | 127.028 | 1.0 |
| (a)-hist | 600 | 5.68304e-2 | 113.661 | 1.0 |
| (b)-hist | 60 | 1.59358e-8 | 3.2e-5 | 0 |
| (b)-hist | 113 | 1.80977e-5 | 0.036 | 0 |
| (b)-hist | 120 | 3.01100e-5 | 0.060 | 0 |
| (b)-hist | 150 | 1.57440e-4 | 0.315 | 0 |
| (b)-hist | 240 | 1.93939e-3 | 3.879 | 0 |
| (b)-hist | 300 | 4.93703e-3 | 9.874 | 1.5e-13 |
| (b)-hist | 400 | 1.38973e-2 | 27.795 | 0.02488 |
| (b)-hist | 450 | 1.97304e-2 | 39.461 | 0.5514 |
| (b)-hist | 600 | 3.74210e-2 | 74.842 | 1.0 |
| (c)-hist | 60 | 1.12449e-11 | 2.2e-8 | 0 |
| (c)-hist | 113 | 9.55916e-8 | 1.9e-4 | 0 |
| (c)-hist | 120 | 2.02048e-7 | 4.0e-4 | 0 |
| (c)-hist | 150 | 2.70990e-6 | 0.005 | 0 |
| (c)-hist | 240 | 2.26445e-4 | 0.453 | 0 |
| (c)-hist | 300 | 1.07492e-3 | 2.150 | 0 |
| (c)-hist | 400 | 4.84527e-3 | 9.691 | 0 |
| (c)-hist | 450 | 7.83227e-3 | 15.665 | 4.4e-7 |
| (c)-hist | 600 | 2.04463e-2 | 40.893 | 0.6391 |

### 3.2 Mixed / alternative declared mixes (same model)

| Scenario | `N_b` | `P(conditions 1–4)` | `E[N]` | `P(N≥39)` |
|---|---:|---:|---:|---:|
| (a)-50:50 | 120 | 4.64258e-3 | 9.286 | 0 |
| (a)-50:50 | 150 | 1.33406e-2 | 26.681 | 0.01424 |
| (a)-50:50 | 240 | 5.03884e-2 | 100.777 | 1.0 |
| (a)-50:50 | 300 | 7.09409e-2 | 141.882 | 1.0 |
| (a)-50:50 | 400 | 8.69873e-2 | 173.975 | 1.0 |
| (b)-thirds | 240 | 8.52122e-3 | 17.042 | 3.2e-6 |
| (b)-thirds | 300 | 2.12567e-2 | 42.513 | 0.728 |
| (b)-thirds | 400 | 4.93287e-2 | 98.657 | 1.0 |
| (b)-thirds | 450 | 6.46969e-2 | 129.394 | 1.0 |
| (b)-thirds | 600 | 1.11332e-1 | 222.664 | 1.0 |
| (c)-50:50 | 240 | 3.35945e-4 | 0.672 | 0 |
| (c)-50:50 | 300 | 1.67498e-3 | 3.350 | 0 |
| (c)-50:50 | 400 | 8.18069e-3 | 16.361 | 1.2e-6 |
| (c)-50:50 | 450 | 1.35214e-2 | 27.043 | 0.01719 |
| (c)-50:50 | 600 | 3.38088e-2 | 67.618 | 1.0 |
| (d) | 120 | — | — | — (no in-range buckets; structural zero) |

The full 7-scenario × 9-size table is in the JSON. Scenario (d) has no in-range bucket and is
characterization-only.

### 3.3 Immediate feasibility readings (conditions 1–4 only)

- `(a)@120`: `E[N] = 3.09`, so the O3 expected-count planning rule (`E[N] ≥ 39`) is **ruled out**.
  This is the same verdict recorded in the accepted 2026-10-19 decision package; it is not a
  probabilistic impossibility proof.
- `(a)@240`: `E[N] = 43.76` (meets the expected-count threshold) but `P(N≥39) = 0.787 < 0.95`.
  The expected-count threshold and the candidate 95% probability rule are **not interchangeable**.
- `(a)@300` and larger: both `E[N] ≥ 39` and the candidate `P(N≥39) ≥ 0.95` are met.
- `(b)@450`: `E[N] = 39.46` but `P(N≥39) = 0.551`; `(b)@600`: `E[N] = 74.84`, `P = 1.0`.
- `(c)@600`: `E[N] = 40.89` but `P(N≥39) = 0.639` — a further case where the expected-count rule is
  not the probability rule.

These are eligibility readings under the declared model; they are not G6b target attainability
claims and not study authorization.

---

## 4. O3 floor and planning-rule arithmetic

- `0.05^(1/38) = 0.924192 < 0.925`; `0.05^(1/39) = 0.926062 ≥ 0.925`. The minimum realized
  eligible count at which the one-sided 95% CP lower bound can reach 92.5% in the all-success case
  is therefore **39**. Sensitivity: 90% → 29; 95% → 59.
- The 39 value is a floor on the **realized** eligible count, not a guarantee that 39 replications
  will be eligible and not an expected-count planning threshold.
- Under `Binomial(2000, p)`, the candidate planning requirement `P(N≥39) ≥ 0.95` needs
  `p ≥ 0.024831`. The expected-count requirement `E[N] ≥ 39` needs `p ≥ 0.0195`. They are distinct.

**Owner decision (not taken here):** whether to adopt `P(N≥39) ≥ 0.95`, the expected-count rule,
or neither, and whether the 39 floor remains the design anchor.

---

## 5. Complete-rule κ gate

### 5.1 Definition and numerical validation

The κ implementation reconstructs the 6×6 Gram matrix from the bucket sufficient statistics
`(n_k, ΣC, ΣC²)`, standardizes the RCS and C columns over the in-support rows, and computes
`κ_eff = s_1/s_r` with the Rev F rank tolerance. It reproduces the recorded 2026-10-19 values:

| Pattern | Recorded κ | Recomputed κ | Difference |
|---|---:|---:|---:|
| (a), 2 buckets (16 rows) | 10.481693469786787 | 10.481693469786746 | 4.1e-14 |
| (a), 2 buckets (32 rows) | 13.395997941033501 | 13.395997941033540 | 3.9e-14 |
| (b), 3 buckets (24 rows) | 36.08794233527171 | 36.08794233527256 | 8.5e-13 |

The Gram-from-sufficient-statistics route is therefore numerically equivalent to the row-level
standardization/SVD used in the 2026-10-19 sweep.

### 5.2 Exact design-weighted enumeration at small supports

All count vectors for the stated bucket sizes were enumerated, weighted by the declared
multinomial/A1 probabilities, and the complete-rule conjunction evaluated exactly. This is an
exact design-weighted calculation, not an unweighted pattern count.

| Support | `P(conditions 1–4)` | `P(pass ∧ κ>30)` | Violation share of pass | Passing patterns | Total mass check |
|---|---:|---:|---:|---:|---:|
| (a) `n5=8, n10=8` | 2.20196e-3 | 0 | 0 | 60 | 1 − 3.9e-14 |
| (b) `n5=8, n10=8, n20=8` | 2.25257e-3 | 2.08175e-11 | 9.24e-9 | 5,040 | 1 − 5.6e-13 |
| (b) `n5=10, n10=10, n20=10` | 8.56033e-3 | 6.24738e-13 | 7.30e-11 | 158,938 | 1 − 2.4e-12 |
| (b) `n5=8, n10=8, n20=4` (2-bucket support) | 2.20196e-3 | 7.19071e-18 | 3.27e-15 | 300 | 1 − 2.3e-13 |

The `n20=4` row fails the bucket floor for `k=20`, so the support is the two-bucket `{5,10}` case;
it is included to show that the two-bucket construction is effectively free of the κ gate.

**Reading.** At the smallest 3-bucket support the design-weighted violation is `9.2e-9` of passing
mass; at `(10,10,10)` it is `7.3e-11`. The much larger unweighted pattern fractions reported in the
2026-10-19 sweep (e.g. 1.67% at `(8,8,8)`) are **not** design probabilities: the violating patterns
are extremely low-probability CK compositions. Under the declared weights the gate is negligible at
the enumerable supports.

### 5.3 Population-level margin

For the declared in-range proportions (large-`n` limit), the extended-matrix κ is:

| Scenario | In-range weights | Population κ | Rank | Smallest retained eigenvalue |
|---|---|---:|---:|---:|
| (a)-hist | 5: 2/3, 10: 1/3 | 2.256 | 3 | 0.8208 |
| (b)-hist | 5: 0.6, 10: 0.2, 20: 0.2 | 12.412 | 4 | 0.02889 |
| (b)-thirds | 1/3 each | 11.333 | 4 | 0.03560 |
| (c)-hist | 5: 0.6, 10: 0.4 | 2.295 | 3 | 0.7981 |

The two-bucket designs `(a)/(c)` have only one retained RCS direction after the intercept; there is
no weakly identified second RCS direction to drive κ upward, and the population κ is ~2.3. The
three-bucket `(b)` design has a weakly identified RCS direction (population κ ~11.3–12.4, margin
~2.4× below the gate). At the budget-scale counts the empirical κ distribution sits near this
population value. Exploratory 20,000–30,000-draw multinomial diagnostics at fixed modal counts for
`(a)@600`, `(b)@600`, `(b)@450`, `(b)@300/150/150`, `(b)@400/100/100`, and `(c)@600` produced no
`κ>30` draw (minimum observed κ: 2.08–2.09 for (a)/(c), 11.87–12.88 for (b)). These draws are a
**diagnostic**, not part of the committed deterministic calculation, not a feasibility proof, and
not a substitute for an exact bound.

### 5.4 Status of the complete-rule probability at the decision cells

- **Two-bucket (a)/(c) cells:** the gate is not material. The exact minimal-support violation is
  zero; the population κ is ~2.3; a spot exact count-box computation at `(a)@600` (modal counts,
  ±6 SD) gave a violation probability of `7.1e-28`, and the omitted count tail is below `1e-9`.
  The complete-rule probability is therefore equal to the conditions 1–4 value to within a
  correction far below the reported digits. This is a bounded statement, not a claim that every
  cell was re-enumerated.
- **Three-bucket (b) cells:** the exact design-weighted violation is tiny at the enumerable
  supports (above), but the **large-`n` complete-rule probability is not identified** by this
  bounded calculation. The gate is controlled by the near-collinearity of the RCS basis at
  `k=5,10,20`; an exact bound would require the joint large-deviation distribution of the three
  bucket C moments (or a validated approximation), which is outside this task's scope. The
  conditions 1–4 value is therefore an **upper bound** for the b cells, and the lower bound is not
  established. No b cell is certified by this record, and the b `P(N≥39)` values in §3 are upper
  bounds.
- **No cell is declared GO by this record.** The `(a)` cells at `≥300` meet the candidate
  planning arithmetic, but the target mapping and the remaining protocol blockers are unchanged.

---

## 6. Within-`k` `C` variation among eligible patterns

- **Mass at zero:** exactly zero. Conditions 3–4 require at least two distinct `C` levels and at
  least four bodies at each observed extreme; a bucket with zero within-bucket variance cannot
  pass. This is a rule property, not an empirical result.
- **Structural lower bound:** for a passing bucket with observed range `r`, the variance is
  `≥ 2r²/n_k` (attained only by the `4 / (n_k−4)` extreme split). With the level gaps
  (`k=5: 0.2`, `k=10: 0.1`, `k=20: 0.05`) this is a deterministic floor.
- **Exact small-support distribution:** at `n_k=8`, conditions 3–4 force exactly four bodies at
  the minimum and four at the maximum, so every passing bucket has exactly two distinct levels and
  the minimum-variance configuration; the number of distinct levels is not a free variable. At
  `(10,10,10)` the exact enumeration shows 158,938 passing patterns (design mass 8.56e-3) and the
  full distinct-level/variance distribution is available in the JSON; the gate-violating tail is
  `6.2e-13` of total mass.
- **Large cells:** the distribution was not exactly enumerated at `N_b ≥ 240`; the structural
  floor and the support conditions are the defensible statements. The design-weighted gate
  calculation at larger cells is the unresolved item in §5.4 for (b); for (a)/(c) the gate
  correction is negligible.

---

## 7. Validation

1. **Independent `f_s0` cross-check.** The main script's exact bucket-pass sum was compared with
   the committed `v03p/a1/a1_support_comparison.py::f_s0` for `k ∈ {5,10,20}` and
   `n ∈ {8,10,12,16,20,30,60}`. Maximum absolute difference: `3.9e-15`. This validates the
   probability weights, the disjoint extreme-pair decomposition, and the normalization.
2. **Independent exhaustive validator.** `v03p/bridge/m2_complete_rule_feasibility_validate.py`
   deliberately does not import the main module. It rebuilds the CK weights from A1, enumerates each
   pattern with its own multinomial pmf, materializes body-level design rows, and computes κ by
   direct SVD. It reproduces `(8,8)` `P_pass = 0.002201961702875565` vs `0.002201961702875571`;
   `(8,8,8)` `P_pass = 0.0022525697236770456` vs `0.002252569723677053` and
   `P_viol = 2.0817479950533463e-11` vs `2.0817479950533467e-11`; and the three κ spot checks agree
   to `≤8.6e-14`. All checks pass. The validator does not independently enumerate `(10,10,10)`;
   that value remains covered by the main calculation's mass and conjunction checks.
3. **κ implementation check.** The Gram/sufficient-statistics implementation reproduces the three
   recorded 2026-10-19 κ values to `≤8.6e-13` (§5.1).
4. **Exact enumeration mass checks.** The small-support enumerations sum to `1 − O(1e-12)` over all
   patterns (§5.2); the complete-rule conjunction is evaluated on the same enumerated objects as
   the pass rule.
5. **Unit test command.** `python -B v03p/bridge/m2_complete_rule_feasibility.py` regenerates the
   JSON and the printed cell table. The script is deterministic; it uses no random seed. The
   independent validator is run with
   `python -B v03p/bridge/m2_complete_rule_feasibility_validate.py` and exits `0` when all checks
   agree.

**Not validated:** the large-`n` three-bucket κ distribution (unresolved, §5.4); the realized
power/FPR and eligibility-conditional error rates (not run, §8); the natural-solver sampling
distribution (not available in this task).

---

## 8. Eligibility, error rates, and what is not estimated

The following are **required before any Phase 1 execution** but were not computed here:

- FPR and power **conditional on eligibility**, with explicit denominators; do not report an
  unconditional rate as if it were the conditional operating characteristic.
- The eligibility + operational outcome profile over **all attempted replications**, with
  `NOT EVALUABLE` as a distinct state; do not count ineligible replications as correct decisions or
  as successful tests.
- The natural-solver vs engineered-support distinction is not resolved by this calculation.

No correctness outcome, solver generation, or hidden outcome was simulated or collected.

---

## 9. Natural-solver target versus engineered-support target

This calculation is under the declared **engineered/simulation support model** (CK marginals, fixed
in-range `k` mix). It does not establish the natural-solver target. The two routes answer related
but different questions:

- **Natural-solver target (primary):** predictive gain for `C` beyond `k` on naturally generated
  solver bodies, on the natural `k` distribution.
- **Engineered-support target (legitimate alternative, not a lesser question):** predictive gain
  on a specified held-out engineered input distribution where the `k` distribution is controlled
  and the concentration signal is manipulated. A candidate estimand for owner review is the
  out-of-sample proper-score gain of the extended model over the `k`-only baseline on held-out
  engineered inputs, under a stated generator and target population. This is a candidate, not an
  adopted estimand; it requires a defensible intervention design and owner approval, and it carries
  no causal identification.

**N2/O2 recommendation:** restrict the default generalization claim to the trained `k`-levels
unless the owner approves and the protocol supports a separate untrained-`k` target. Predictions at
untrained `k` remain an unresolved generalization issue, not a result settled by M2.

---

## 10. Limitations

1. The declared support model is a simulation design, not a natural-solver distribution. The
   `Binomial(2000, p)` count model is the declared Phase-1 design, not a claim of independent
   Bernoulli eligibility in nature.
2. The exact large-`n` three-bucket complete-rule probability is not identified (§5.4). The report
   does not convert the upper bound into a passing claim.
3. The κ gate is a proposed M2 resolution; it is not adopted. Rev F §5A remains unresolved, and the
   M2 recommendation still requires reviewer sign-off and owner acceptance as a gate-semantics
   change.
4. The O3 floor/planning rule is a candidate; this record does not adopt it. The 39 floor is not an
   expected-count rule and is not a guarantee.
5. The calculation is outcome-blind and says nothing about FPR, power, or natural-solver effect
   sizes.
6. No G6b execution, Phase 1, solver generation, hidden-outcome collection, or broad sensitivity
   sweep was performed. No master merge, tag, freeze, or publication is authorized.

---

## 11. Recommended owner decisions

1. **M2:** accept or reject the proposed `κ_eff ≤ 30` gate as a gate-semantics change, with the
   reviewer sign-off still required. The (a)/(c) evidence is non-material; the (b) complete-rule
   probability is not certified at large `n`.
2. **O3:** choose the planning rule — expected count `E[N] ≥ 39`, candidate `P(N≥39) ≥ 0.95`, or
   neither — and confirm whether 39 remains the realized-count floor. The two rules differ at
   `(a)@240`, `(b)@450`, and `(c)@600`.
3. **Target:** resolve the G6b target mapping/recalibration, or explicitly adopt an
   engineered-support target with a defensible estimand and intervention design. The R1 finding
   alone cannot establish or falsify G6b attainability.
4. **Phase 1:** keep Phase 1 unauthorized until the target mapping, the M2/O3 dispositions, the
   confirmatory-procedure choice, the budget/power decision, and the eligibility-conditional
   operating-characteristic plan are resolved.

---

## 12. Reproduction and boundaries

```
python -B v03p/bridge/m2_complete_rule_feasibility.py
python -B v03p/bridge/m2_complete_rule_feasibility_validate.py
```

The main script writes `v03p/bridge/m2_complete_rule_feasibility_2026-10-20.json` and prints the
cell table. It does not write outside `v03p/bridge/`, does not touch frozen sources, and does not
sample. The validator does not import the main module and exits `0` when its independent
enumeration and κ checks agree. The `(b)` large-`n` gate remains the documented unresolved item;
no GO is claimed.

---

## 13. References

- `v03p/PHASE0_DESIGN_2026-10-15_RevF.md` — controlling design; §9.1/§9.2 support and O3; §5A
  M1/M2/M3 and κ.
- `v03p/a1/a1_support_comparison.py` — CK construction, S0/S1/S2, exact `f_s0`.
- `v03p/bridge/m2_complete_rule_feasibility_validate.py` — independent exhaustive validator.
- `v03p/bridge/battery.py` — DGP constants and generator anchors.
- `v03p/bridge/M2_COMPLETE_RULE_FEASIBILITY_2026-10-20.md` (this file) and the companion JSON.
- `v03p/VDRAFT_Target_Bridge_and_Research_Decision_2026-10-18.md` — decision entry (restructured).
- `v03p/VDRAFT_REVIEW_LOG_2026-10-20.md` — preserved review history.
