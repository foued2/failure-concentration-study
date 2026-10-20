# VDraft: Target Bridge and Research Decision Plan — Revision 3 (decision entry)

**Date:** 2026-10-20
**Status:** REVIEW DRAFT ONLY (Revision 3, correction pass 1). Decision entry for the 2026-10-20
owner work orders ("IMPLEMENT CLAUDE'S REVIEW AND DELIVER M2 FEASIBILITY DATA" and "CORRECT M2
FEASIBILITY BOUNDS AND DUPLICATE-RATE SCOPE", Foued via GPT/ and Claude/). This document is **not
frozen**. It does not grant NC2, Phase 1, G6b execution, solver generation, hidden-outcome
collection, a master merge, tags, a protocol freeze, or publication. The full review history is
preserved in `v03p/VDRAFT_REVIEW_LOG_2026-10-20.md`; the corrected bounded M2 feasibility
calculation is in `v03p/bridge/M2_COMPLETE_RULE_FEASIBILITY_2026-10-20.md` and its JSON.

---

## 0. Decision summary (read this first)

### 0.1 The scientific question and the target population

> Does the concentration of a solver's diagnostic failures, `C`, predict correctness on unseen
> inputs beyond the total failure count, `k`, for naturally generated solver bodies?

- **Natural-solver target (primary):** the population of naturally generated solver bodies, with
  its own `k` distribution and concentration structure. This is the primary route.
- **Engineered-support target (legitimate alternative, not a lesser question):** a specified
  held-out engineered-input population where the `k` mix is controlled and the concentration signal
  is manipulated. A candidate estimand is given in §6. It is **not adopted** and requires owner
  approval and a defensible intervention design. Evidence from one target must not be presented as
  evidence for the other.

### 0.2 R1 versus G6b

- **R1** is the population-level predictive-signal/calibration quantity: the oracle-effect curve
  under the declared generator and target population. It is a **population** quantity.
- **G6b** is the intended **full-procedure** objective: the finite-sample predictive procedure,
  including support selection, estimation, and the proposed gate. R1 is not a substitute for G6b,
  and the gap between them is not identified by R1 alone.
- The calibrated R1 curves peak **below `2δ* = 0.040546510810816436`** across the four declared
  scenarios. That means the R1 quantity does not attain that level within the declared calibration
  domain. It does **not** establish that the finite-sample G6b procedure cannot meet its target.
  Preserve `E[Δ_proc] = Δ_R1 + ε_B − ε_E` with the ordering of `ε_B` and `ε_E` unknown; R1 cannot
  by itself establish attainability or non-attainability of the full-procedure target.

### 0.3 What is established, untested, and blocked

| Status | Item |
|---|---|
| Established | `δ* = ln(1.5)/20 = 0.020273255405408218`; NC1 evaluation grid `c* ∈ {39.0625, 156.25, 625}` as an evaluation grid only; M2 identifiability facts (null-space dimension 3 for (a)/(c) and 2 for (b); rank increase +1 on every admissible pattern); bounded conditions 1–4 eligibility intervals and both duplicate-rate arms under the declared support model (2026-10-20 corrected calculation); `κ_eff` implementation validated against the 2026-10-19 spot values. |
| Untested | G6b target attainment; finite-sample power/FPR; natural-solver eligibility and effect sizes; complete-rule probability for the three-bucket (b) design at large `n`; cell-wide complete-rule lower bounds for any cell; the engineered-support estimand. |
| Blocked | G6b target mapping/recalibration; the `β_min` value from `δ*` (source-mapping provisional); M2 adoption; O3 planning-rule choice; duplicate-rate/attempt-axis semantics (Rev F §9.2 vs §9.3); confirmatory-procedure choice; budget/power decision; Phase 1 authorization. |

### 0.4 Terminal interpretations (use these labels)

1. **SUPPORTED** — the approved procedure meets the prespecified predictive criterion on the
   approved target population.
2. **NOT DEMONSTRATED** — a valid, evaluable study does not establish the prespecified predictive
   gain. This is not proof of universal absence and is not a theory verdict.
3. **INCONCLUSIVE / NOT EVALUABLE** — design infeasibility, insufficient eligible observations,
   unresolved target mapping, or another prespecified failure prevents a defensible test.

A failed feasibility gate is **not** falsification of the underlying scientific hypothesis.

### 0.5 Current decision and immediate next action

**Current status: GO remains blocked; NO-GO is not established; the study is INCONCLUSIVE / NOT
EVALUABLE as currently specified; Phase 1 is not authorized.** The corrected 2026-10-20 calculation
sharpens the feasibility picture (below) but does not resolve the target mapping, the complete-rule
probability, or the duplicate-rate semantics. The immediate next actions are the owner decisions in
§7, in this order:

1. Resolve the G6b target mapping/recalibration (or adopt an engineered-support target with an
   approved estimand).
2. Resolve the O1 duplicate-rate/attempt-axis semantics (Rev F §9.2 vs §9.3) and decide M2 adoption
   (with reviewer sign-off) and the O3 planning rule.
3. Decide the confirmatory procedure and the budget/power rule.
4. Only then consider a separate Phase 1 authorization.

---

## 1. Recommendation in brief

Keep the natural-solver predictive study as the primary route. Do not redefine NC2 as the v0.3
Phase 1 power simulation. Do not execute G6b or Phase 1. The corrected 2026-10-20 calculation shows
that the proposed O3 expected-count rule rules out `(a)@120`; that no cell is certified under the
complete rule because no cell-wide complete-rule lower bound is established; and that the
expected-count rule and the candidate `P(N≥39) ≥ 0.95` rule are not interchangeable. Support-only
upper bounds at `(a)@300+` exceed the planning thresholds, but an upper bound above a threshold is
not a passing result. The two-bucket (a)/(c) gate evidence is local and small at the enumerated
supports, not a cell-wide certificate; for the three-bucket (b) design the large-`n` complete-rule probability
remains **unidentified**. The `ρ=0.25` attempt-slot arm is less favorable than the fixed-unique-body
arm at the candidate and many planning sizes; the Rev F duplicate-rate semantics are unresolved. None
of this authorizes a GO or a Phase 1 run.

---

## 2. Terms and corrections that must not be conflated

| Symbol | Meaning | What it is not |
|---|---|---|
| `k` | Total number of diagnostic probe failures | A measure of where failures occur |
| `C` | Largest family's share of failures, `C = max_j f_j/k` (Rev F §1) | The mechanistic variance-like quantity `c` |
| `Δ` | Held-out predictive log-loss improvement: baseline (`k`) minus extended (`k, C`) (Rev F §1) | A slope or a threshold-crossing probability |
| `δ*` | Proposed minimum meaningful predictive gain, `ln(1.5)/20 = 0.020273255405408218` nats per hidden input (owner decision C, Rev F:121) | A correctness-probability-scale slope |
| `γ` | Coefficient on raw `C` in the proposed logit outcome generator, `logit(p) = θ0 + θ1 log(1+k) + γC + u + v` (Rev F:291) | `β_min` without a specified transformation |
| `β_min` | The minimum-signal parameter of the mechanistic `c*` heuristic, in the fixed M3 reference unit `s_ref = 0.12703` exactly. The reading used here is provisional: the probability-scale slope per one unit of the dimensionless `x_M3 = (C_i − C̄_{k(i)})/s_ref`. The bridge functional is **`β_pop`**, the population counterpart under the declared generator; the mapping remains **PROVISIONAL** (source-committed as-found, unfrozen) | `Δ`, `δ*`, or the logit coefficient `γ`; nor a slope per one within-`k` SD of `C` |
| `c*` | Mechanistic threshold `c* = (1.25/β_min)²` under the M3 construction (`σ_max·z_req = 1.25`). The constants `39.0625 / 156.25 / 625` are illustrative, not frozen | A measured predictive gain or a power estimate |

**`0.1007` correction (2026-10-20).** The old §4 approximation `0.1007` is retained, if at all, only
as an explicitly assumption-dependent illustration. Its derivation assumes `p(1−p) = 0.25` and
`Var(x_M3) = 1`; those assumptions do **not** describe the declared support rows, whose marginal
probabilities are `p_k = 1/(k+2)` in the relevant calibration (e.g. `p_5 = 1/7`, `p_10 = 1/12`). It
therefore does **not** independently support `β_min = 0.10`, is not a selected minimum-signal
value, and is not sheeted into any decision. `β_min = 0.10` remains a provisional owner-controlled
anchor, not a conclusion of this document. The `c*` mapping remains provisional. No broad
sensitivity sweep was run.

**Source precondition (unchanged, condensed).** The controlling M3 texts are preserved as-found at
`v03p/source/` and are not frozen; the exact `γ ↔ β_min` functional and the reviewer disposition of
the committed texts remain open. The source record is
`v03p/VDRAFT_M3_SOURCE_DEPENDENCY_2026-10-18.md`; the historical detail is in the review log.

**Chronology note.** The budget/min-power entries were post-examination planning decisions made on
2026-10-19/20, after the bridge results were known. They are not preregistered and must not be read
as having an earlier date.

---

## 3. What is established and what is not

### Established

- The design target `δ*` and the NC1 evaluation grid (above). NC1's grid is not the study's design
  choice and does not establish a natural-solver distribution.
- The M2 identifiability facts from the 2026-10-19 analysis: the null space of the extended design
  has dimension 3 for (a)/(c) and 2 for (b); trained-`k` rows are orthogonal to the null space; the
  rank increase is +1 on every admissible pattern. These are linear-algebra facts, not target
  attainability.
- The bounded conditions 1–4 eligibility intervals and both duplicate-rate arms under the declared
  support model (2026-10-20 corrected calculation), and the local κ evidence. See §5 and the
  feasibility record.

### Still unknown

- The `β_min` value corresponding to `δ*` across the declared baseline probabilities and
  within-`k` spreads of `C`; the exact `γ ↔ β_min` functional.
- The G6b finite-procedure target mapping and the realized attainability of the target.
- The natural-solver population distribution, natural eligibility, and natural effect sizes.
- The large-`n` three-bucket complete-rule probability and any cell-wide complete-rule lower bound
  (§5.3).
- The Rev F duplicate-rate semantics: fixed unique-body `N_b` versus attempt-slot copying (§5.1).
- The FPR/power conditional on eligibility and the operational outcome profile.

---

## 4. R1 vs G6b and the GO/STOP repair

### 4.1 The R1 finding and what it does not say

The calibrated R1 population curves peak below `2δ* = 0.040546510810816436` in all four declared
scenarios. The R1 quantity therefore does not reach that level within the declared calibration
domain. This is a statement about the **population-level oracle-effect curve**, not about the
finite-sample G6b procedure. In particular:

- Do not conclude "G6b cannot meet the target" from R1 alone.
- Preserve the decomposition `E[Δ_proc] = Δ_R1 + ε_B − ε_E`; the ordering of `ε_B` and `ε_E` is
  unknown.
- R1 cannot by itself establish attainability; a target mapping/recalibration of the full procedure
  is required. The population-calibration curve may be retained as an explicit **oracle-effect
  stress test** if the owner chooses that route; it must not be relabeled as full-procedure
  validation.

### 4.2 Accepted GO-status wording (2026-10-19/20 correction pass)

> GO remains blocked: under the proposed O3 expected-count planning rule, the required `(a)@120`
> cell is ruled out because `E[N_eligible] ≤ 3.09 < 39`; this does not establish that 39 realized
> eligible replications are probabilistically impossible. O3 rule adoption and the cell-wide
> complete-rule lower bound remain unresolved.

The phrase "unattainable" in the earlier draft is scoped only to a realized eligible count `< 39`
under the all-success CP bound; it is not a claim that the support or the G6b target is
impossible. The corrected 2026-10-20 feasibility record bounds the support-only `(a)@120` expected
count at `≤ 3.09` (and the complete-rule expected count at no more than that), which is enough to
rule out the expected-count planning rule for that cell; it adds the probability-rule distinction
below.

---

## 5. M2 complete-rule feasibility (2026-10-20)

The full calculation, assumptions, validation, and limitations are in
`v03p/bridge/M2_COMPLETE_RULE_FEASIBILITY_2026-10-20.md`; the numbers below are the decision-facing
summary. The model is the declared Rev F §9.1 simulation support (A1 CK marginals, independent
replications, `R = 2000`), not the natural-solver population.

### 5.1 Bounded conditions 1–4 eligibility and duplicate arms

The corrected calculation reports an interval
`p_box ≤ P(conditions 1–4) ≤ p_box + tail`, where the tail is all count-box mass omitted by the
±8-SD truncation. The interval is propagated monotonically to `E[N]` and `P(N≥39)`. The complete rule
adds `κ_eff ≤ 30`; the gate can only reject, so this record reports
`0 ≤ P(complete rule) ≤ P(conditions 1–4 upper)` and does not claim a cell-wide complete-rule lower
bound. The complete-rule expected-count and probability upper bounds are used for the O3 readings;
an upper bound above a threshold does **not** certify the cell.

**Duplicate scope.** The fixed-unique-body arm treats `N_b` as unique canonical bodies (Rev F §9.3).
The attempt-slot arm treats `N_b` as generated slots; each slot after the first copies an earlier
body with probability `ρ=0.25`, so `M = 1 + Binomial(N_b−1, 0.75)` unique bodies and the support
probability is `E_M[p(M)]` (Rev F §9.1 and §3E). Rev F §9.2 lists duplicate rate as a grid factor,
while §9.3 says the Phase 1 simulation's `N_b` is simulated valid unique bodies and duplicate-rate
modelling at the attempt axis is O1. That conflict is unresolved: both arms are shown, neither is
adopted, and no attempt-budget or timing projection is drawn from the slot arm.

| Scenario / `N_b` | Arm | `P(conditions 1–4)` interval | Complete-rule `E[N]` upper | Complete-rule `P(N≥39)` upper | O3 reading |
|---|---|---:|---:|---:|---|
| (a)@120 | `ρ=0` unique | 1.546e-3–1.546e-3 | 3.091 | 2.3e-29 | Both candidate rules ruled out |
| (a)@120 | `ρ=.25` slots | 2.731e-4–2.731e-4 | 0.546 | 1.1e-57 | Both candidate rules ruled out |
| (a)@240 | `ρ=0` unique | 2.188e-2–2.188e-2 | 43.764 | 0.787 | `P(N≥39)≥.95` ruled out; expected count not certified |
| (a)@240 | `ρ=.25` slots | 8.572e-3–8.572e-3 | 17.144 | 3.6e-6 | Both candidate rules ruled out |
| (a)@300 | `ρ=0` unique | 3.953e-2–3.953e-2 | 79.068 | 1.000 | Not certified; complete-rule lower bound is 0 |
| (a)@300 | `ρ=.25` slots | 1.804e-2–1.804e-2 | 36.080 | 0.334 | Both candidate rules ruled out |
| (b)@450 | `ρ=0` unique | 1.973e-2–1.973e-2 | 39.461 | 0.551 | `P(N≥39)≥.95` ruled out; expected count not certified |
| (b)@450 | `ρ=.25` slots | 7.787e-3–7.787e-3 | 15.573 | 3.8e-7 | Both candidate rules ruled out |
| (b)@600 | `ρ=0` unique | 3.742e-2–3.742e-2 | 74.842 | 1.000 | Not certified; complete-rule lower bound is 0 |
| (b)@600 | `ρ=.25` slots | 1.977e-2–1.977e-2 | 39.534 | 0.556 | `P(N≥39)≥.95` ruled out; expected count not certified |
| (c)@600 | `ρ=0` unique | 2.045e-2–2.045e-2 | 40.893 | 0.639 | `P(N≥39)≥.95` ruled out; expected count not certified |
| (c)@600 | `ρ=.25` slots | 7.863e-3–7.863e-3 | 15.726 | 4.8e-7 | Both candidate rules ruled out |

The two candidate O3 rules differ at `(a)@240`, `(b)@450`, and `(c)@600` in the fixed-unique arm.
Under `Binomial(2000, p)`, the 95% probability rule needs `p ≥ 0.024831`; the expected-count rule
needs `p ≥ 0.0195`. The O3 floor of 39 is a floor on the **realized** eligible count; it is not a
guarantee and not an expected-count rule. Sensitivity: 90% CP → 29; 95% CP → 59.

The calculation covers 7 scenarios × 9 sizes, with both arms, in the companion JSON. Only `60` and
`120` are Rev F candidate body counts. `113, 150, 240, 300, 400, 450, 600` are proposed O1
re-anchoring/planning sensitivities, not adopted grid values; `113` and `450` are close to the
expected unique counts for `150` and `600` slots at `ρ=0.25` (112.75 and 450.25), which is why they
appear in the historical discussion. No size is adopted or claimed to pass.

### 5.2 O3 arithmetic

- `0.05^(1/38) = 0.924192 < 0.925`; `0.05^(1/39) = 0.926062 ≥ 0.925`. The minimum realized
  eligible count for the all-success 95% CP lower bound to reach 92.5% is **39**.
- `P(N≥39) ≥ 0.95` is a candidate planning rule for owner consideration only. It is not adopted.
  `E[N] ≥ 39` is not interchangeable with it.

### 5.3 The κ gate

- **Two-bucket (a)/(c):** no cell-wide complete-rule lower bound is established. The population κ
  is ~2.26–2.29; the exact minimal-support violation is zero; a spot exact count-box computation at
  `(a)@600` gave a violation probability of `7.1e-28` with an omitted tail below `1e-9`. These are
  local and small-support diagnostics, not a cell-wide certificate. The complete rule therefore
  remains `NOT CERTIFIED` at every (a)/(c) cell; the gate is *not* declared non-material.
- **Three-bucket (b):** the design-weighted violation is tiny at the enumerable supports
  (`9.2e-9` of passing mass at `(8,8,8)`; `7.3e-11` at `(10,10,10)`), and the population κ is
  ~11.3–12.4 (margin ~2.4× below the gate). **The large-`n` complete-rule probability is not
  identified** by the bounded calculation; the conditions 1–4 value is an upper bound for the
  `(b)` cells and the lower bound is not established. No `(b)` cell is certified. The large
  unweighted pattern fractions in the 2026-10-19 sweep (e.g. 1.67% at `(8,8,8)`) are not design
  probabilities and must not be used as such.
- **No cell is declared GO by this record.**

### 5.4 Within-`k` C variation and eligibility versus informativeness

- **Mass at zero:** exactly zero. Conditions 3–4 require at least two distinct `C` levels and at
  least four bodies at each observed extreme; a bucket with zero within-bucket variance cannot
  pass. This is a rule property, not an empirical result.
- **Structural lower bound:** for a passing bucket with observed range `r`, the within-bucket
  variance is `≥ 2r²/n_k` (attained only by the `4 / (n_k−4)` extreme split). With the level gaps
  (`k=5: 0.2`, `k=10: 0.1`, `k=20: 0.05`) this is a deterministic floor.
- **Exact small-support distribution:** at `n_k=8`, conditions 3–4 force exactly four bodies at
  the minimum and four at the maximum, so every passing bucket has exactly two distinct levels and
  the minimum-variance configuration. At `(10,10,10)` the exact design-weighted enumeration covers
  158,938 passing patterns; the gate-violating tail is `6.2e-13` of total mass. The JSON records the
  enumeration totals, not a cell-wide certificate and not the full pattern distribution.
- **Large cells:** the distribution was not exactly enumerated at `N_b ≥ 240`; the structural floor
  and the support conditions are the defensible statements. No cell-wide complete-rule lower bound
  is established for (a)/(c) or (b); the local evidence in §5.3 does not certify any cell.
- **Eligibility is not informativeness.** Passing the support rule does not guarantee that the
  fitted contrast is informative; the rank/conditioning diagnostics and the `κ_eff` gate are
  separate from the eligibility count. Do not report eligible counts as effective information.

---

## 6. Natural-solver target versus engineered-support target

This calculation is under the declared **engineered/simulation support model** (CK marginals, fixed
in-range `k` mix). It does not establish the natural-solver target. The two routes answer related
but different questions:

- **Natural-solver target (primary):** predictive gain for `C` beyond `k` on naturally generated
  solver bodies, on the natural `k` distribution.
- **Engineered-support target (legitimate alternative, not a lesser question):** predictive gain
  on a specified held-out engineered input distribution where the `k` distribution is controlled
  and the concentration signal is manipulated. A **candidate estimand for owner review** is the
  out-of-sample proper-score gain of the extended model over the `k`-only baseline on held-out
  engineered inputs, under a stated generator and target population. This is a candidate, not an
  adopted estimand; it requires a defensible intervention design and owner approval, and it carries
  no causal identification. The study design would need to isolate concentration variation while
  controlling the `k` distribution; evidence from this route is not evidence for the natural route.

**N2/O2 recommendation:** restrict the default generalization claim to the trained `k`-levels
unless the owner approves and the protocol supports a separate untrained-`k` target. Predictions at
untrained `k` remain an unresolved generalization issue, not a result settled by M2.

---

## 7. Owner decision sheet

| # | Decision | Options / needed input | Current status |
|---|---|---|---|
| 1 | G6b target mapping | Map/recalibrate the full-procedure target, or adopt an engineered target with an approved estimand | **Blocked**; primary blocker |
| 2 | M2 adoption | Accept the `κ_eff ≤ 30` gate as a gate-semantics change (reviewer sign-off required), reject it, or defer | Not adopted; no cell-wide complete-rule lower bound; (a)/(c) evidence local only, (b) large-`n` unresolved |
| 3 | O3 planning rule | `E[N] ≥ 39`, candidate `P(N≥39) ≥ 0.95`, or neither; confirm the 39 realized-count floor | Not adopted; the rules differ at `(a)@240`, `(b)@450`, `(c)@600`; no cell certified |
| 4 | Confirmatory procedure | Rev F held-out log-loss comparison vs the scale-(i) stratified-permutation procedure | Open |
| 5 | Budget / power | Decide whether power at `δ*` is gated, and the planning budget | Open; post-examination timing evidence only |
| 6 | Untrained-`k` claim | Restrict the default claim to trained `k`-levels, or approve a separate untrained-`k` target | Recommend restriction |
| 7 | Phase 1 authorization | Separate explicit authorization after 1–6 and the operating-characteristic plan | **Not granted** |
| 8 | O1 duplicate-rate semantics | Resolve Rev F §9.2 (duplicate rate as grid factor) versus §9.3 (unique-body `N_b`; attempt-axis modeling under O1); choose the attempt axis and budget | Not resolved; both arms reported, neither adopted |

**Before Phase 1, the protocol must specify:** FPR and power **conditional on eligibility**, with
explicit denominators; the eligibility + operational outcome profile over all attempted
replications, with `NOT EVALUABLE` as a distinct state; and the rule that ineligible replications
are not counted as correct decisions. No Phase 1 run or outcome-rate estimation was performed here.

---

## 8. Protocol blockers and authorization boundaries

**Preserved holds (unchanged by the 2026-10-20 calculation):**

- G6b is the intended full-procedure objective; it is **not** execution authorization.
- NC1 remains closed; NC2, Phase 1, solver generation, hidden-outcome collection, spending, and a
  master merge remain unauthorized.
- The study is not frozen; the branch remains separate from `master`. No tags, publication, or
  protocol freeze is authorized.
- The `β_min = 0.10` anchor is provisional; the `β_pop` mapping and `c*` conversion are
  provisional.
- M2 and O3 are **not adopted**. No cell is certified under the complete rule; support-only upper
  bounds above a threshold are not passing results.
- The Rev F duplicate-rate/attempt-axis semantics are unresolved; the `ρ=0.25` slot arm is a
  sensitivity arm, not an adopted design or budget basis.
- No additional broad parameter sweep is authorized by this record.
- A failed feasibility gate must not be presented as falsification of the underlying scientific
  hypothesis.

**Bridge authorization (2026-10-18, unchanged):** matched-population bridge computation for
scenarios (a)/(c) only, in the battery-first order already recorded; this does not extend to NC2,
Phase 1, G6b, or solver generation.

---

## 9. Review questions for the next round

1. Is the G6b target mapping now specified, or should the study adopt the engineered-support target
   under a new estimand? (Owner decision 1.)
2. Is the `κ_eff ≤ 30` gate accepted as a gate-semantics change, given that no cell has a complete-
   rule lower bound, the (a)/(c) evidence is local rather than cell-wide, and the (b) large-`n`
   probability is not certified? (Owner decision 2.)
3. Which planning rule governs the design: expected count, candidate probability, or neither?
   (Owner decision 3.) Does the owner resolve Rev F §9.2 versus §9.3 on duplicates before any
   attempt-budget or timing claim? (Owner decision 8.)
4. Does the `0.1007` illustration have any remaining decision role? (Recommendation: none; retain
   only as an assumptions-labeled sanity check.)
5. Are the untrained-`k` claims restricted to trained levels? (Owner decision 6.)

The full sequence of prior review rounds, disagreements, and dispositions is preserved verbatim in
`v03p/VDRAFT_REVIEW_LOG_2026-10-20.md`. No history was deleted or reordered.

---

## 10. Source anchors

| Anchor | Location | Role |
|---|---|---|
| `δ* = ln(1.5)/20 = 0.020273255405408218` | Rev F:121 | Design target; not a `β_min` value |
| `2δ* = 0.040546510810816436` | Rev F | Gate/reporting level; R1 curves peak below it |
| Outcome generator `logit(p) = θ0 + θ1 log(1+k) + γC + u + v` | Rev F:291 | Defines `γ`; distinct from `β_min` |
| Rank check / `κ_eff` / M2 | Rev F:150–154, 179 | M2 gate; body-level rows; `κ_eff = s_1/s_r` |
| M3 ridge / `β_min` source | Rev F:185 | M3 reference unit `s_ref = 0.12703` |
| G6b objective | Rev F:239 | Full-procedure target; not execution authorization |
| O3 / support floor | Rev F:257–272 | 39 realized-count floor; planning rule |
| Duplicate scope | Rev F §3E, §9.1, §9.2, §9.3 | Unique canonical bodies; `ρ∈{0,.25}` slot-copy mechanism; unresolved attempt-axis reading |
| Levels `k ∈ {5,10,20}` | Rev F:287 | In-range support |
| CK / S0 / S1 / S2 / `f_s0` | `v03p/a1/a1_support_comparison.py` | Committed support machinery |
| DGP constants `TH0=0`, `TH1=−1`, `SIG_B=SIG_S=1` | `v03p/bridge/battery.py:41–48`, `:69–70` | Declared generator anchors |
| RCS basis / design rows | `study/models.py:17–34` | Frozen design path |
| Feasibility calculation | `v03p/bridge/m2_complete_rule_feasibility.py` | Deterministic main calculation |
| Feasibility record | `v03p/bridge/M2_COMPLETE_RULE_FEASIBILITY_2026-10-20.md` | Assumptions, tables, validation, limitations |
| Machine-readable results | `v03p/bridge/m2_complete_rule_feasibility_2026-10-20.json` | Per-cell numbers and checks |

Controlling-source status: the M3 engine text and addendum are preserved as-found at `v03p/source/`,
unfrozen; the source record is `v03p/VDRAFT_M3_SOURCE_DEPENDENCY_2026-10-18.md`. The companion
implementation-order and source-dependency documents remain at their committed states; no §5A
resolution has been adopted.

---

## 11. Document history

- **Revision 2 (2026-10-18):** full review draft and correction history. Preserved verbatim in
  `v03p/VDRAFT_REVIEW_LOG_2026-10-20.md` (SHA-256 of the preserved pre-restructure draft:
  `24D04F8156866029545615F0FDBC0D7995C7BFB12F9BC039EEB3C66224E2744D`).
- **Revision 2 correction pass (2026-10-19):** O3 floor wording, grid rulings, complete-rule
  status, M1 wording, GO status. Accepted by GPT/; recorded in the log.
- **Revision 3 (2026-10-20):** this decision entry. Restructures the document, preserves the
  history in the log, applies the `0.1007` and GO/STOP repairs, adds the bounded M2 feasibility
  results and the three terminal interpretations, and adds the natural/engineered target section.
  No computation, solver run, Phase 1, or authorization was added beyond the bounded feasibility
  calculation.
- **Revision 3 correction pass 1 (2026-10-20):** applies the GPT/ and Claude/ correction work order:
  count-box intervals replace exact claims; complete-rule probability is bounded above by the
  support upper with no cell-wide lower bound; the `ρ=0` unique-body and `ρ=.25` attempt-slot arms
  are reported side by side; O3 readings are corrected; the Rev F §9.2/§9.3 duplicate-semantics
  conflict is recorded. No new sampling, solver run, Phase 1, or authorization.
