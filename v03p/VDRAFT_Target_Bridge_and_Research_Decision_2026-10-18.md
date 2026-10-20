# VDraft: Target Bridge and Research Decision Plan — Revision 3 (decision entry)

**Date:** 2026-10-20
**Status:** REVIEW DRAFT ONLY (Revision 3). Decision entry for the 2026-10-20 owner work order
("IMPLEMENT CLAUDE'S REVIEW AND DELIVER M2 FEASIBILITY DATA", Foued via GPT/). This document is
**not frozen**. It does not grant NC2, Phase 1, G6b execution, solver generation, hidden-outcome
collection, a master merge, tags, a protocol freeze, or publication. The full review history is
preserved in `v03p/VDRAFT_REVIEW_LOG_2026-10-20.md`; the bounded M2 feasibility calculation is in
`v03p/bridge/M2_COMPLETE_RULE_FEASIBILITY_2026-10-20.md` and its JSON.

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
| Established | `δ* = ln(1.5)/20 = 0.020273255405408218`; NC1 evaluation grid `c* ∈ {39.0625, 156.25, 625}` as an evaluation grid only; M2 identifiability facts (null-space dimension 3 for (a)/(c) and 2 for (b); rank increase +1 on every admissible pattern); exact conditions 1–4 eligibility under the declared support model (2026-10-20 calculation); `κ_eff` implementation validated against the 2026-10-19 spot values. |
| Untested | G6b target attainment; finite-sample power/FPR; natural-solver eligibility and effect sizes; complete-rule probability for the three-bucket (b) design at large `n`; the engineered-support estimand. |
| Blocked | G6b target mapping/recalibration; the `β_min` value from `δ*` (source-mapping provisional); M2 adoption; O3 planning-rule choice; confirmatory-procedure choice; budget/power decision; Phase 1 authorization. |

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
EVALUABLE as currently specified; Phase 1 is not authorized.** The 2026-10-20 calculation sharpens
the feasibility picture (below) but does not resolve the target mapping or the (b) complete-rule
probability. The immediate next actions are the owner decisions in §7, in this order:

1. Resolve the G6b target mapping/recalibration (or adopt an engineered-support target with an
   approved estimand).
2. Decide M2 adoption (with reviewer sign-off) and the O3 planning rule.
3. Decide the confirmatory procedure and the budget/power rule.
4. Only then consider a separate Phase 1 authorization.

---

## 1. Recommendation in brief

Keep the natural-solver predictive study as the primary route. Do not redefine NC2 as the v0.3
Phase 1 power simulation. Do not execute G6b or Phase 1. The 2026-10-20 eligibility calculation
shows that the proposed O3 expected-count rule rules out `(a)@120` and that `(a)@300+` meets the
candidate planning arithmetic; it also shows that the expected-count rule and the candidate
`P(N≥39) ≥ 0.95` rule are not interchangeable. The proposed M2 gate is non-material for the
two-bucket (a)/(c) design; for the three-bucket (b) design the large-`n` complete-rule probability
remains **unidentified**, so no (b) cell is certified. None of this authorizes a GO or a Phase 1
run.

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
- The exact conditions 1–4 eligibility results under the declared support model (2026-10-20), and
  the bounded κ evidence. See §5 and the feasibility record.

### Still unknown

- The `β_min` value corresponding to `δ*` across the declared baseline probabilities and
  within-`k` spreads of `C`; the exact `γ ↔ β_min` functional.
- The G6b finite-procedure target mapping and the realized attainability of the target.
- The natural-solver population distribution, natural eligibility, and natural effect sizes.
- The large-`n` three-bucket complete-rule probability (§5.3).
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
> eligible replications are probabilistically impossible. O3 rule adoption and the exact
> complete-rule support probability remain unresolved.

The phrase "unattainable" in the earlier draft is scoped only to a realized eligible count `< 39`
under the all-success CP bound; it is not a claim that the support or the G6b target is
impossible. The 2026-10-20 feasibility record makes the `(a)@120` reading exact (3.09 expected) and
adds the probability-rule distinction below.

---

## 5. M2 complete-rule feasibility (2026-10-20)

The full calculation, assumptions, validation, and limitations are in
`v03p/bridge/M2_COMPLETE_RULE_FEASIBILITY_2026-10-20.md`; the numbers below are the decision-facing
summary. The model is the declared Rev F §9.1 simulation support (A1 CK marginals, independent
replications, `R = 2000`), not the natural-solver population.

### 5.1 Exact conditions 1–4 eligibility (selection of the grid)

| Scenario / `N_b` | `E[N_eligible]` (exact) | `P(N≥39)` | Reading |
|---|---:|---:|---|
| (a)@120 | 3.09 | 0 | Ruled out by the expected-count rule |
| (a)@240 | 43.76 | 0.787 | Meets `E≥39`; fails candidate `P≥0.95` |
| (a)@300 | 79.07 | 1.0 | Meets both candidate rules |
| (a)@450 | 127.03 | 1.0 | Meets both; near the high point of the curve |
| (b)@450 | 39.46 | 0.551 | Meets `E≥39`; fails candidate `P≥0.95` |
| (b)@600 | 74.84 | 1.0 | Meets both (upper bound; see §5.3) |
| (c)@600 | 40.89 | 0.639 | Meets `E≥39`; fails candidate `P≥0.95` |

The expected-count rule and the candidate `P(N≥39) ≥ 0.95` rule differ materially at `(a)@240`,
`(b)@450`, and `(c)@600`. Under `Binomial(2000, p)`, the 95% probability rule needs `p ≥ 0.024831`;
the expected-count rule needs `p ≥ 0.0195`. The O3 floor of 39 is a floor on the **realized**
eligible count; it is not a guarantee and not an expected-count rule. Sensitivity: 90% CP → 29;
95% CP → 59.

### 5.2 O3 arithmetic

- `0.05^(1/38) = 0.924192 < 0.925`; `0.05^(1/39) = 0.926062 ≥ 0.925`. The minimum realized
  eligible count for the all-success 95% CP lower bound to reach 92.5% is **39**.
- `P(N≥39) ≥ 0.95` is a candidate planning rule for owner consideration only. It is not adopted.
  `E[N] ≥ 39` is not interchangeable with it.

### 5.3 The κ gate

- **Two-bucket (a)/(c):** the gate is not material. Population κ is ~2.26–2.29; the exact
  minimal-support violation is zero; a spot exact count-box computation at `(a)@600` gave a
  violation probability of `7.1e-28` with an omitted tail below `1e-9`.
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
  158,938 passing patterns; the gate-violating tail is `6.2e-13` of total mass. The full
  distinct-level/variance distribution is in the JSON.
- **Large cells:** the distribution was not exactly enumerated at `N_b ≥ 240`; the structural floor
  and the support conditions are the defensible statements. The gate correction is the unresolved
  item in §5.3 for (b); for (a)/(c) it is negligible.
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
| 2 | M2 adoption | Accept the `κ_eff ≤ 30` gate as a gate-semantics change (reviewer sign-off required), reject it, or defer | Not adopted; (a)/(c) non-material, (b) large-`n` unresolved |
| 3 | O3 planning rule | `E[N] ≥ 39`, candidate `P(N≥39) ≥ 0.95`, or neither; confirm the 39 realized-count floor | Not adopted; the rules differ at `(a)@240`, `(b)@450`, `(c)@600` |
| 4 | Confirmatory procedure | Rev F held-out log-loss comparison vs the scale-(i) stratified-permutation procedure | Open |
| 5 | Budget / power | Decide whether power at `δ*` is gated, and the planning budget | Open; post-examination timing evidence only |
| 6 | Untrained-`k` claim | Restrict the default claim to trained `k`-levels, or approve a separate untrained-`k` target | Recommend restriction |
| 7 | Phase 1 authorization | Separate explicit authorization after 1–6 and the operating-characteristic plan | **Not granted** |

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
- M2 and O3 are **not adopted**.
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
2. Is the `κ_eff ≤ 30` gate accepted as a gate-semantics change, given that the (a)/(c) gate is
   non-material and the (b) large-`n` probability is not certified? (Owner decision 2.)
3. Which planning rule governs the design: expected count, candidate probability, or neither?
   (Owner decision 3.)
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
