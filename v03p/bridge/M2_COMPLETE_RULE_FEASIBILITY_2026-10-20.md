# M2 complete-rule feasibility — bounded calculation (2026-10-20, correction pass 1)

**Status:** REVIEW DRAFT / CORRECTED CALCULATION RECORD. Produced under the owner work orders
"IMPLEMENT CLAUDE'S REVIEW AND DELIVER M2 FEASIBILITY DATA" and "CORRECT M2 FEASIBILITY BOUNDS AND
DUPLICATE-RATE SCOPE" (Foued, 2026-10-20, relayed by GPT/ and Claude/). This record does **not**
execute G6b, Phase 1, solver generation, or hidden-outcome collection; it does **not** adopt M2,
O3, or a duplicate-rate design; it does **not** authorize simulation, a master merge, tags, a
protocol freeze, or publication. All numbers below are deterministic calculations under the
declared support model, except where explicitly labeled as a diagnostic or as unresolved.

**Decision use.** This record answers one bounded question: under the declared Rev F support model
and the proposed M2 complete rule, what are defensible intervals for the number of eligible
replications out of `R = 2000`, and which candidate O3 rules can be ruled out? It does not translate
the answer into a G6b target claim. Support probabilities are intervals from a bounded count box;
complete-rule probabilities are bounded above by the support upper and below by zero, because no
cell-wide gate lower bound is established. The target-translation and authorization blockers remain
in the main decision document.

---

## 1. Inputs and source versions

| Input | Version / hash | Use |
|---|---|---|
| `v03p/PHASE0_DESIGN_2026-10-15_RevF.md` | SHA-256 `BB2B2343E71EF3D57AD738F2BE7CF6F8958590AC5CD1B790750009629EB05658` | controlling support/outcome design; §9.1 declared support, §9.2 grid/O3, §5A rank/κ rule |
| `v03p/a1/a1_support_comparison.py` | SHA-256 `CF3840F108F82E6739CC01DEEDA1623070E2CEC84EB5059F293C4193D3C96C74` | committed CK support machinery, S0/S1/S2 rules, exact `f_s0` cross-check |
| `v03p/bridge/battery.py` | SHA-256 `5E952A202FA0335A305A5110A9D810F86731D9ABAA1D69C12E3E71DD57707A05` | DGP constants `TH0=0`, `TH1=−1`, `SIG_B=SIG_S=1`, `MC_SEED=20261018`; A1 import |
| `study/models.py` | SHA-256 `4E4226FE055DCFDFC4074C77EB5CBF8860F1C747A21DD15DC53A8AF3C6C4C420` | frozen RCS basis / design rows (`rcs_basis`, `KNOTS`) |
| `v03p/VDRAFT_Target_Bridge_and_Research_Decision_2026-10-18.md` | SHA-256 `C1E3D50FB1A5488AF43B6CE3DB0E933A6D6995199DE52B91D23DBC55B27C4FD3` | current Revision 3 decision entry, correction pass 1; the pre-restructure Revision 2 draft is preserved at SHA-256 `24D04F8156866029545615F0FDBC0D7995C7BFB12F9BC039EEB3C66224E2744D` in the review log |
| `v03p/bridge/m2_complete_rule_feasibility.py` | SHA-256 `D1672A01425665333A9F7B176B7FA259AB257877D2D258E68A33C65868FD2B72` | main calculation |
| `v03p/bridge/m2_complete_rule_feasibility_2026-10-20.json` | SHA-256 `0FCCC452DE05C85D27ADD6D597758C1F5764CD8E006211FFC398B65DFC6E1A72` | machine-readable results |
| `v03p/bridge/m2_complete_rule_feasibility_validate.py` | SHA-256 `F83DF288C1E033CF70A317B8F77D89E2DC9AB4D286554B19A2DCF75AB951F38E` | independent validation and report-to-JSON consistency check |

Source files were read, not modified. The calculation uses Python 3.14.0 with NumPy 2.4.6; it does
not import `battery.py` and does not use any sampler. The A1 import was used only for the
independent `f_s0` cross-check reported in §7. The validator also uses the committed A1 support
functions for exact checks.

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
5. **Duplicate semantics are unresolved.** Rev F §3E defines the estimand over unique canonical
   solver bodies; §9.1 defines a slot-copy mechanism with `ρ ∈ {0, .25}`; §9.2 lists duplicate rate
   as a candidate grid factor; §9.3 says the Phase 1 simulation's `N_b` is simulated valid unique
   bodies and calls attempt-axis duplicate modelling O1. This record therefore reports two arms:
   fixed unique bodies (`ρ=0`) and attempt slots (`ρ=.25`). The slot arm replaces `N_b` by
   `M = 1 + Binomial(N_b−1, 1−ρ)` unique bodies, averages `p_support(M)` over the exact `M`
   distribution, and is a sensitivity arm, not an adopted design or budget basis.

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

## 3. Bounded probability of the conditions 1–4 support

The bucket pass probability `f_k(n)` is computed by the exact A1 sum over disjoint
"observed-minimum/observed-maximum" pairs and was cross-checked against
`a1_support_comparison.f_s0` for `k ∈ {5,10,20}` and `n ∈ {8,10,12,16,20,30,60}` (maximum absolute
difference `3.9e-15`). The cell calculation sums over the multinomial in-range bucket counts inside
a ±8 marginal-SD count box. It returns `p_box`, the omitted count tail, and the interval

`p_box ≤ P(conditions 1–4) ≤ p_box + tail`.

The interval is propagated monotonically: `E[N]` and `P(N≥39)` are intervals, and the table reports
their upper ends where a planning threshold is at issue. The omitted tails are small but are **not**
uniformly below `1e-12`; examples are `(a)@60: 4.85e-10`, `(b)@60: 5.3e-9`, `(c)@120: 3.4e-9`.
The complete-rule interval is `[0, P(conditions 1–4 upper)]`, because the κ gate can only reject and
no cell-wide gate lower bound is established. The O3 readings therefore use the complete-rule
upper bounds; an upper bound above a threshold is **not** a passing result.

**Table codes.** `both_rules_ruled_out` = both candidate O3 rules (expected count and
`P(N≥39)≥.95`) are ruled out for that arm. `P_rule_ruled_out` = the candidate probability rule is
ruled out; the expected-count rule is not certified. `not_certified` = no cell-wide complete-rule
lower bound, so the cell is not certified; upper bounds above a threshold are not a pass. The tables
show both duplicate arms; they do not select one.

### 3.1 Candidate sizes (`N_b ∈ {60, 120}`)

| Scenario / `N_b` | Arm | `P(conditions 1–4)` interval | Complete-rule `E[N]` upper | Complete-rule `P(N≥39)` upper | O3 |
|---|---|---:|---:|---:|---|
| a-hist / 60 | rho=0 unique | [5.9587e-06, 5.9591e-06] | 0.0119 | 0.0000e+00 | both_rules_ruled_out |
| a-hist / 60 | rho=.25 slots | [2.6547e-07, 2.6662e-07] | 5.3323e-04 | 0.0000e+00 | both_rules_ruled_out |
| a-hist / 120 | rho=0 unique | [1.5457e-03, 1.5457e-03] | 3.0914 | 0.0000e+00 | both_rules_ruled_out |
| a-hist / 120 | rho=.25 slots | [2.7310e-04, 2.7310e-04] | 0.5462 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 60 | rho=0 unique | [1.5936e-08, 2.1208e-08] | 4.2417e-05 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 60 | rho=.25 slots | [4.3897e-10, 2.8445e-08] | 5.6890e-05 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 120 | rho=0 unique | [3.0110e-05, 3.0113e-05] | 0.0602 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 120 | rho=.25 slots | [2.3715e-06, 2.3761e-06] | 0.0048 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 60 | rho=0 unique | [1.1245e-11, 3.0697e-08] | 6.1394e-05 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 60 | rho=.25 slots | [1.9281e-13, 3.6839e-08] | 7.3679e-05 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 120 | rho=0 unique | [2.0205e-07, 2.0546e-07] | 4.1092e-04 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 120 | rho=.25 slots | [6.0974e-09, 1.2322e-08] | 2.4644e-05 | 0.0000e+00 | both_rules_ruled_out |

Only `60` and `120` are Rev F candidate body counts. They are both far below the O3 planning
thresholds in both arms.

### 3.2 Proposed planning/decision sizes

`113, 150, 240, 300, 400, 450, 600` are proposed O1 re-anchoring/planning sensitivities, not
adopted grid values. `113` and `450` are near the expected unique counts for `150` and `600` slots
at `ρ=0.25` (112.75 and 450.25).

| Scenario / `N_b` | Arm | `P(conditions 1–4)` interval | Complete-rule `E[N]` upper | Complete-rule `P(N≥39)` upper | O3 |
|---|---|---:|---:|---:|---|
| a-hist / 113 | rho=0 unique | [1.1168e-03, 1.1168e-03] | 2.2336 | 0.0000e+00 | both_rules_ruled_out |
| a-hist / 113 | rho=.25 slots | [1.7458e-04, 1.7458e-04] | 0.3492 | 0.0000e+00 | both_rules_ruled_out |
| a-hist / 150 | rho=0 unique | [4.2795e-03, 4.2795e-03] | 8.5590 | 0.0000e+00 | both_rules_ruled_out |
| a-hist / 150 | rho=.25 slots | [1.1258e-03, 1.1258e-03] | 2.2515 | 0.0000e+00 | both_rules_ruled_out |
| a-hist / 240 | rho=0 unique | [2.1882e-02, 2.1882e-02] | 43.7642 | 0.7871 | P_rule_ruled_out |
| a-hist / 240 | rho=.25 slots | [8.5722e-03, 8.5722e-03] | 17.1444 | 3.6427e-06 | both_rules_ruled_out |
| a-hist / 300 | rho=0 unique | [3.9534e-02, 3.9534e-02] | 79.0682 | 1.0000 | not_certified |
| a-hist / 300 | rho=.25 slots | [1.8040e-02, 1.8040e-02] | 36.0804 | 0.3340 | both_rules_ruled_out |
| a-hist / 400 | rho=0 unique | [6.0552e-02, 6.0552e-02] | 121.1031 | 1.0000 | not_certified |
| a-hist / 400 | rho=.25 slots | [3.9576e-02, 3.9576e-02] | 79.1525 | 1.0000 | not_certified |
| a-hist / 450 | rho=0 unique | [6.3514e-02, 6.3514e-02] | 127.0276 | 1.0000 | not_certified |
| a-hist / 450 | rho=.25 slots | [4.9602e-02, 4.9602e-02] | 99.2050 | 1.0000 | not_certified |
| a-hist / 600 | rho=0 unique | [5.6830e-02, 5.6830e-02] | 113.6608 | 1.0000 | not_certified |
| a-hist / 600 | rho=.25 slots | [6.3434e-02, 6.3434e-02] | 126.8681 | 1.0000 | not_certified |
| b-hist / 113 | rho=0 unique | [1.8098e-05, 1.8099e-05] | 0.0362 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 113 | rho=.25 slots | [1.2766e-06, 1.2824e-06] | 0.0026 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 150 | rho=0 unique | [1.5744e-04, 1.5744e-04] | 0.3149 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 150 | rho=.25 slots | [1.8911e-05, 1.8914e-05] | 0.0378 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 240 | rho=0 unique | [1.9394e-03, 1.9394e-03] | 3.8788 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 240 | rho=.25 slots | [4.8355e-04, 4.8355e-04] | 0.9671 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 300 | rho=0 unique | [4.9370e-03, 4.9370e-03] | 9.8741 | 1.4910e-13 | both_rules_ruled_out |
| b-hist / 300 | rho=.25 slots | [1.4676e-03, 1.4676e-03] | 2.9351 | 0.0000e+00 | both_rules_ruled_out |
| b-hist / 400 | rho=0 unique | [1.3897e-02, 1.3897e-02] | 27.7947 | 0.02488 | both_rules_ruled_out |
| b-hist / 400 | rho=.25 slots | [4.9729e-03, 4.9729e-03] | 9.9458 | 5.5567e-13 | both_rules_ruled_out |
| b-hist / 450 | rho=0 unique | [1.9730e-02, 1.9730e-02] | 39.4607 | 0.5514 | P_rule_ruled_out |
| b-hist / 450 | rho=.25 slots | [7.7867e-03, 7.7867e-03] | 15.5735 | 3.8105e-07 | both_rules_ruled_out |
| b-hist / 600 | rho=0 unique | [3.7421e-02, 3.7421e-02] | 74.8419 | 1.0000 | not_certified |
| b-hist / 600 | rho=.25 slots | [1.9767e-02, 1.9767e-02] | 39.5340 | 0.5560 | P_rule_ruled_out |
| c-hist / 113 | rho=0 unique | [9.5592e-08, 9.8056e-08] | 1.9611e-04 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 113 | rho=.25 slots | [2.7019e-09, 1.0009e-08] | 2.0018e-05 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 150 | rho=0 unique | [2.7099e-06, 2.7118e-06] | 0.0054 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 150 | rho=.25 slots | [1.0780e-07, 1.1124e-07] | 2.2248e-04 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 240 | rho=0 unique | [2.2645e-04, 2.2645e-04] | 0.4529 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 240 | rho=.25 slots | [1.9249e-05, 1.9250e-05] | 0.0385 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 300 | rho=0 unique | [1.0749e-03, 1.0749e-03] | 2.1498 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 300 | rho=.25 slots | [1.4017e-04, 1.4017e-04] | 0.2803 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 400 | rho=0 unique | [4.8453e-03, 4.8453e-03] | 9.6905 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 400 | rho=.25 slots | [1.0916e-03, 1.0916e-03] | 2.1833 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 450 | rho=0 unique | [7.8323e-03, 7.8323e-03] | 15.6645 | 4.3872e-07 | both_rules_ruled_out |
| c-hist / 450 | rho=.25 slots | [2.1446e-03, 2.1446e-03] | 4.2893 | 0.0000e+00 | both_rules_ruled_out |
| c-hist / 600 | rho=0 unique | [2.0446e-02, 2.0446e-02] | 40.8927 | 0.6391 | P_rule_ruled_out |
| c-hist / 600 | rho=.25 slots | [7.8631e-03, 7.8631e-03] | 15.7261 | 4.8221e-07 | both_rules_ruled_out |

### 3.3 Immediate feasibility readings

- `(a)@120`: the complete-rule expected-count upper is `3.091` in the fixed-unique arm and `0.546`
  in the slot arm, so the O3 expected-count planning rule (`E[N] ≥ 39`) is **ruled out**. The
  candidate probability rule is also ruled out. This is a bounded negative result, not a
  probabilistic impossibility proof.
- `(a)@240`: fixed-unique `E[N] ≤ 43.764` and `P(N≥39) ≤ 0.787 < 0.95`; the candidate probability
  rule is **ruled out**, while the expected-count rule is not certified. The slot arm rules out both.
  The two O3 rules are **not interchangeable**.
- `(a)@300`: fixed-unique upper bounds exceed both thresholds (`E[N] ≤ 79.068`,
  `P(N≥39) ≤ 1.0`), but the cell is **not certified** because the complete-rule lower bound is 0.
  An upper bound above a threshold is not a pass. The slot arm at 300 rules out both rules.
- `(b)@450`: fixed-unique `E[N] ≤ 39.461` and `P(N≥39) ≤ 0.551`; the probability rule is ruled out,
  the expected-count rule is not certified. The slot arm rules out both.
- `(b)@600`: fixed-unique is not certified (`E[N] ≤ 74.842`, `P(N≥39) ≤ 1.0`); the slot arm rules
  out the probability rule (`E[N] ≤ 39.534`, `P(N≥39) ≤ 0.556`) but not the expected-count rule.
- `(c)@600`: fixed-unique `E[N] ≤ 40.893`, `P(N≥39) ≤ 0.639`; the probability rule is ruled out,
  the expected-count rule is not certified. The slot arm rules out both.
- **No cell is certified and no cell is declared GO.** The shipped JSON contains all 7 scenarios ×
  9 sizes (55 cells) with both arms and intervals; the tables above show the decision-relevant
  candidate and planning sizes. The alternative declared mixes are in the JSON and are not adopted.
- These are eligibility readings under the declared model; they are not G6b target attainability
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

- **Two-bucket (a)/(c) cells:** **no cell-wide complete-rule lower bound is established.** The
  exact minimal-support violation is zero; the population κ is ~2.3; a spot exact count-box
  computation at `(a)@600` (modal counts, ±6 SD) gave a violation probability of `7.1e-28`, with
  omitted count tail below `1e-9`. These are local/small-support diagnostics, not a certificate
  that every (a)/(c) cell has a gate violation probability near zero. The complete-rule interval in
  §3 is therefore `[0, P(conditions 1–4 upper)]`; the cells are `NOT CERTIFIED`.
- **Three-bucket (b) cells:** the exact design-weighted violation is tiny at the enumerable
  supports (above), but the **large-`n` complete-rule probability is not identified** by this
  bounded calculation. The gate is controlled by the near-collinearity of the RCS basis at
  `k=5,10,20`; an exact bound would require the joint large-deviation distribution of the three
  bucket C moments (or a validated approximation), which is outside this task's scope. The
  conditions 1–4 value is therefore an **upper bound** for the b cells, and the lower bound is not
  established. No b cell is certified by this record, and the b `P(N≥39)` values in §3 are upper
  bounds.
- **No cell is declared GO by this record.** The `(a)` cells at `≥300` have upper bounds above the
  candidate planning thresholds, but upper bounds are not passes; the target mapping and the
  remaining protocol blockers are unchanged.

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
  gate-violating tail is `6.2e-13` of total mass. The JSON records the enumeration totals, not a
  full pattern-level distribution and not a cell-wide certificate.
- **Large cells:** the distribution was not exactly enumerated at `N_b ≥ 240`; the structural
  floor and the support conditions are the defensible statements. The design-weighted gate
  calculation at larger cells is unresolved for (b); for (a)/(c) the local evidence is small but
  does not establish a cell-wide lower bound.

---

## 7. Validation

1. **Independent `f_s0` cross-check.** The main script's exact bucket-pass sum was compared with
   the committed `v03p/a1/a1_support_comparison.py::f_s0` for `k ∈ {5,10,20}` and
   `n ∈ {8,10,12,16,20,30,60}`. Maximum absolute difference: `3.9e-15`. This validates the
   probability weights, the disjoint extreme-pair decomposition, and the normalization.
2. **Independent exhaustive validator.**
   `v03p/bridge/m2_complete_rule_feasibility_validate.py` deliberately does not import the main
   module. It rebuilds the CK weights from A1, enumerates each pattern with its own multinomial
   pmf, materializes body-level design rows, and computes κ by direct SVD. It reproduces `(8,8)`
   `P_pass = 0.002201961702875565` vs `0.002201961702875571`; `(8,8,8)`
   `P_pass = 0.0022525697236770456` vs `0.002252569723677053` and
   `P_viol = 2.0817479950533463e-11` vs `2.0817479950533467e-11`; and the three κ spot checks agree
   to `≤8.6e-14`. All checks pass. The validator does not independently enumerate `(10,10,10)`;
   that value remains covered by the main calculation's mass and conjunction checks.
3. **Exact support containment at selected cells.** The validator enumerates the full bucket-count
   distribution without the ±8-SD box for `(a)@60`, `(a)@120`, `(b)@60`, `(c)@60`, `(c)@120` and
   checks that each JSON support interval contains the exact value and that the omitted outside-box
   mass does not exceed the recorded tail. Exact values: `(a)@60 5.95865571915921e-06`,
   `(a)@120 0.0015456987610085503`, `(b)@60 1.5936729430186873e-08`,
   `(c)@60 1.126742005422155e-11`, `(c)@120 2.0204892952003243e-07`.
4. **Duplicate-mixture containment.** For `(a)@60` at `ρ=.25`, the validator enumerates the exact
   `M` distribution and support mixture. `P_mixture_exact = 2.6546846320586415e-07`; the JSON lower
   endpoint is `2.654681888642656e-07`; the exact value is contained.
5. **Cell schema and O3 labels.** The validator checks all 55 cells: interval algebra
   (`p_box ≤ p_upper`, support/complete upper equality, zero lower bounds), monotone `E` and
   `P(N≥39)`, duplicate aliases and `M_mean`, tail-mixture bookkeeping, and the three allowed O3
   labels. No schema errors were found.
6. **κ implementation check.** The Gram/sufficient-statistics implementation reproduces the three
   recorded 2026-10-19 κ values to `≤8.6e-13` (§5.1).
7. **Exact enumeration mass checks.** The small-support enumerations sum to `1 − O(1e-12)` over all
   patterns (§5.2); the complete-rule conjunction is evaluated on the same enumerated objects as
   the pass rule.
8. **Report-to-JSON consistency.** The validator parses the candidate and planning tables in §3 and
   checks the rounded interval endpoints, complete-rule upper bounds, and O3 codes against the JSON.
9. **Commands.** `py -3.14 -B v03p/bridge/m2_complete_rule_feasibility.py` regenerates the JSON and
   the printed cell table. The script is deterministic; it uses no random seed. The independent
   validator is run with
   `py -3.14 -B v03p/bridge/m2_complete_rule_feasibility_validate.py` and exits `0` when all checks
   agree.

**Not validated:** the large-`n` three-bucket κ distribution (unresolved, §5.4); cell-wide
complete-rule lower bounds at any cell; exact enumeration of every cell; the realized power/FPR and
eligibility-conditional error rates (not run, §8); the natural-solver sampling distribution (not
available in this task).

---

## 8. Eligibility, error rates, and what is not estimated

The following are **required before any Phase 1 execution** but were not computed here:

- FPR and power **conditional on eligibility**, with explicit denominators; do not report an
  unconditional rate as if it were the conditional operating characteristic.
- The eligibility + operational outcome profile over **all attempted replications**, with
  `NOT EVALUABLE` as a distinct state; do not count ineligible replications as correct decisions or
  as successful tests.
- The natural-solver vs engineered-support distinction is not resolved by this calculation.
- If the attempt-slot arm were ever adopted, report eligible/attempted and unique-body denominators
  separately; the `ρ=.25` mixture is not interchangeable with a fixed unique-body `N_b`.

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
2. Support probabilities are bounded by a count box, not exact; the omitted tails are small but not
   uniformly below `1e-12`. Every reported `E[N]` and `P(N≥39)` is an interval endpoint, and the
   tables show the upper ends.
3. The exact large-`n` three-bucket complete-rule probability is not identified (§5.4), and no
   cell-wide complete-rule lower bound is established for (a)/(c) either. The report does not
   convert an upper bound into a passing claim.
4. Rev F's duplicate-rate semantics conflict (§9.2 vs §9.3). Both `ρ=0` and `ρ=.25` arms are
   reported; neither is adopted, and no attempt-budget or timing projection is based on the slot
   arm.
5. The κ gate is a proposed M2 resolution; it is not adopted. Rev F §5A remains unresolved, and the
   M2 recommendation still requires reviewer sign-off and owner acceptance as a gate-semantics
   change.
6. The O3 floor/planning rule is a candidate; this record does not adopt it. The 39 floor is not an
   expected-count rule and is not a guarantee.
7. The calculation is outcome-blind and says nothing about FPR, power, or natural-solver effect
   sizes.
8. No G6b execution, Phase 1, solver generation, hidden-outcome collection, or broad sensitivity
   sweep was performed. No master merge, tag, freeze, or publication is authorized.

---

## 11. Recommended owner decisions

1. **Duplicate semantics:** resolve Rev F §9.2 (duplicate rate as a candidate grid factor) versus
   §9.3 (`N_b` as unique bodies; attempt-axis duplicate modelling under O1), including the attempt
   axis and budget. Until resolved, neither arm is a design basis.
2. **M2:** accept or reject the proposed `κ_eff ≤ 30` gate as a gate-semantics change, with the
   reviewer sign-off still required. No cell has a complete-rule lower bound; the (a)/(c) evidence
   is local and the (b) complete-rule probability is not certified at large `n`.
3. **O3:** choose the planning rule — expected count `E[N] ≥ 39`, candidate `P(N≥39) ≥ 0.95`, or
   neither — and confirm whether 39 remains the realized-count floor. The two rules differ at
   `(a)@240`, `(b)@450`, and `(c)@600`; no cell is certified.
4. **Target:** resolve the G6b target mapping/recalibration, or explicitly adopt an
   engineered-support target with a defensible estimand and intervention design. The R1 finding
   alone cannot establish or falsify G6b attainability.
5. **Phase 1:** keep Phase 1 unauthorized until the target mapping, the duplicate-axis decision,
   the M2/O3 dispositions, the confirmatory-procedure choice, the budget/power decision, and the
   eligibility-conditional operating-characteristic plan are resolved.

---

## 12. Reproduction and boundaries

```
py -3.14 -B v03p/bridge/m2_complete_rule_feasibility.py
py -3.14 -B v03p/bridge/m2_complete_rule_feasibility_validate.py
```

The main script writes `v03p/bridge/m2_complete_rule_feasibility_2026-10-20.json` and prints the
cell table. It does not write outside `v03p/bridge/`, does not touch frozen sources, and does not
sample. The validator does not import the main module and exits `0` when its independent
enumeration, schema, duplicate-mixture, exact-support, and report-table checks agree. The `(b)`
large-`n` gate and the cell-wide complete-rule lower bound remain documented unresolved items; no GO
is claimed.

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
