# v0.3-P Phase 0 — Review Response (Revision 5)

**Date:** 2026-10-14
**Status:** Revision 5 — a **one-point targeted amendment** on Revision 4, per GPT's final withheld-sign-off item (the §3B statistic's population must match the §3A(2) outcome-blind analysis support). Nothing else is reopened; Revision 4's two corrections and all previously resolved items stand. Append-only response to independent review of `v03p/PHASE0_DESIGN_2026-10-14.md` (commit `3cd62b8`, preserved unamended; this document does not revise the design). Committed and published on `master` (commit `4018ebd`) after final line-by-line review (GPT, GLM) and explicit owner authorization, 2026-10-14. **C and E may remain OPEN in the committed response document** (GPT explicit); they must be resolved before design freeze. **Not ready to freeze; Phase 1 is not authorized.** No solver generation, no hidden-outcome collection, and no v0.3 Phase 1 simulation has been performed (v0.1 and v0.2 historical analyses are untouched and not obscured by this statement). v0.3 is the first *proposed* design intended to test the predictive question in a new generation population, conditional on passing its design, simulation, and feasibility gates. It is not an adequately identified evaluation and is not described as one.

Terminal-document posture (GLM, concurred by GPT): this document records state and registers open items; it does not close items that require owner decisions (C, E) or simulation/feasibility evidence (A, B). Revision 5 was committed as the terminal response document (commit `4018ebd`, owner-authorized 2026-10-14) after final line-by-line review; OPEN items carry into the revised design as freeze-blockers. Any further revision requires a new substantive line-by-line finding; no additional refinement is warranted otherwise. The post-publication administrative erratum below records publication state only and is not a technical revision.

Revision 5 change (single point, per GPT): §3B's statistic population replaced — the outcome-variation gate is evaluated on feasibility-sample body-suite pairs whose body belongs to the **outcome-blind analysis support defined by the preregistered identifiability gate in §3A(2)**, not on range membership alone, so the gate tests outcome variation for the same target population on which Δ is estimated. Revision 4's corrections (§3A(2) eligibility; k=24 discrete C bounds) are unchanged. Administrative erratum (2026-10-14, post-publication, per GPT's independent verification note): only the self-referential status and posture statements were updated to record publication as commit `4018ebd`; no technical content changed.

## 1. Provenance corrections — RESOLVED

**Error 1 — "no v0.1 per-solver k data exists" (wrong).** The data is `pilot/pilot_report.json`; MIMO's search globbed `study/`, `data/`, and `v01/` and missed `pilot/`. Independent re-aggregation of the persisted JSON: 60 (solver, instance) rows, 20 distinct bodies, k identical across the 3 instances (0 conflicts). Per-body k histogram: **k=0: 16 (80.0%), k=5: 2 (10.0%), k=10: 1 (5.0%), k=25: 1 (5.0%)**; in the potentially identifiable range 2 ≤ k ≤ 24: **3/20 = 15.0%**; observed identifying support: **none** (0 k values with ≥ 2 distinct C). Distinct C per k: k=0→{0.0}, k=5→{1.0} (both bodies), k=10→{0.5}, k=25→{0.2} (instrument-forced 5/25). Terminal INFEASIBLE per `pilot/PILOT_REPORT.md`.

**Non-conflation rule (binding on every later reference).** Two criteria apply to v0.1 and must never be merged:
- *Original pilot feasibility gate (historical):* eligible = k ≥ 2 → **4/20** bodies; all 4 have Y = 0 on every instance; eligible yield 20% against the ≥ 75% gate → INFEASIBLE under the old gate. This figure is a property of the old gate only.
- *Potentially identifiable range (this study):* 2 ≤ k ≤ 24 → **3/20** bodies. The fourth old-gate-eligible body had k = 25, where the instrument forces C = 5/k with zero possible within-k variation; it is outside the range. *Observed identifying support* — realized data with enough distinct bodies and within-k C variation to identify the contrast — was established by neither v0.1 nor v0.2.

**Error 2 — "no generator configuration exists" (wrong for v0.1).** `specs/generator_spec.json` records: model `opencode/mimo-v2.6-flash-free`; one generation session 2026-10-11 by executor (MIMO); sampling at model defaults; the verbatim prompt; **20 distinct approach directives** (one per body); retention rule; pack size 20; snapshot limitation disclosed. The v0.2 pack remains code-constructed (`v02/generate_pack.py` docstring: 20 strategy families × 6 variants, no LLM parameters) — that part of the earlier report stands.

**Arithmetic correction.** v0.2 constructed-pack in-range mass is 45/360 evaluations = **15/120 bodies = 12.5%** (an earlier MIMO statement of "12/120 = 10%" was wrong).

Both errors are MIMO's; GLM's overgeneralization ("all prior evidence was constructed") traced to Error 2 and has been retracted by GLM. Recorded lesson (GLM): reviewers without direct repository access must hedge load-bearing claims that rest on reports of reports.

## 2. Corrected population provenance — RESOLVED

| Study | Population | Status |
|---|---|---|
| v0.1 pilot | **20 LLM-generated bodies, strategy-directed** (one approach directive per body; single-shot, model-default sampling) | INFEASIBLE under its old gate: 80% k=0, 3/20 (15.0%) in the potentially identifiable range, zero within-k C variation, old-gate-eligible Y=0 |
| v0.2 | **120 code-constructed bodies** (20 families × 6 variants) | Formal NEGATIVE under the frozen rule, with the C=5/k identifiability limitation (audit series `da4030d`, `c75fb43`, `11d86b9`) |
| v0.3-P | Proposed single-identical-prompt LLM generation (a **different** sampling procedure) | Untested; first proposed design conditional on its gates; not an identified evaluation |

- The v0.2 formal NEGATIVE does not establish that concentration lacks predictive value: C was mechanically aliased with k in the realized constructed design.
- v0.1's evidence applies to its directed generation process, not to unconditioned LLM output; its old-gate-eligible Y=0 pattern is a feasibility observation, not a predictive result.
- **Recurring shape, with a non-equivalence clause.** Both independent populations show dominant k=0 mass, a thin in-range band, and zero within-k C variation (v0.1: 80%/15.0%/none; v0.2: 75%/12.5%/none). This is recorded as a warning pattern, **not a forecast**: v0.1's directed-prompt generation and v0.3's proposed single-prompt generation are different sampling procedures, and **neither predicts the other**. The shape must not be over-interpreted in either direction when v0.3's gates are read, and the two populations must not be pooled into an estimate of v0.3's generator population.
- **Support-range correction and vocabulary — RESOLVED.** The instrument's *potentially identifiable range* is 2 ≤ k ≤ 24, where within-k variation in C is mathematically possible (k=0 forces C=0; k=1 forces C=1; k ≥ 25 forces C=5/k; at k=24 the **minimum attainable C is 4/24 and the maximum is 5/24** — family counts are discrete, so not every intermediate value is attainable). Design §8's "[1, 24]" is corrected to "[2, 24]" in the next design revision, which will also adopt this two-term vocabulary: *potentially identifiable range* (mathematical possibility) versus *observed identifying support* (realized data with enough distinct bodies and within-k C variation to identify the proposed contrast). The range is maximum possible support only; neither prior population established observed identifying support, and range membership alone never establishes estimator eligibility (§3A(2)).

## 3. Review points A–E — binary status marks

Each point is marked RESOLVED or OPEN. OPEN means the item is a prerequisite still requiring specification sign-off or an owner decision; RESOLVED means the rule below is binding on the next design revision, subject only to diff review.

### A. Crossed evaluation procedure — OPEN

Naming "two-way bootstrap" is not a design (GPT A; CLAUDE 1). The operational specification below is proposed for review and is not yet frozen.

1. **Train/test formation (both axes unseen).** Two-way holdout over solver-body identities and hidden-suite identities. Each repetition draws a held-out subset of body identities and a held-out subset of suite identities. The **training block** is training bodies × training suites; the **test block** is held-out bodies × held-out suites. The **mixed (off-diagonal) blocks** — held-out body × training suite, and training body × held-out suite — are used for neither training nor scoring, so no test body or suite is seen in training in any form.
2. **Primary Δ aggregation (per design §2; adjacent-k clause deleted).** Verified against `PHASE0_DESIGN_2026-10-14.md` §2: the estimand is **Δ = E[ L(baseline) − L(extended) ] over the joint population of solver bodies and hidden suites**, L = held-out log-loss per hidden input, positive Δ meaning C helps; it is **not** a contrast between adjacent-k groups. Scoring: per eligible held-out (body, suite) cell, compute the per-hidden-input log-loss difference; Δ̂ is the **equal-weight mean over all eligible held-out cells**. **Eligibility (GPT's final correction; binding).** The potentially identifiable range is 2 ≤ k ≤ 24, but **range membership alone does not establish eligibility**. The primary estimate uses only the **preregistered analysis support that passes the outcome-blind identifiability gate**. The revised design must define the support-selection rule — including its minimum distinct-body counts, within-k C-variation requirement, and rank/overlap requirement — and specify how that support is applied to held-out cells. **No confirmatory hidden outcomes may be used to select or revise the support.** The precise numerical thresholds remain open (§5). In the crossed test block every held-out body is scored on every held-out suite, so equal weight per cell coincides with equal weight per body among eligible cells; the revised design must still state this aggregation rule explicitly and fix the handling of a body with fewer than all held-out suites (e.g., suite-level exclusions), so the aggregation matches the estimand rather than emerging from scoring code (GPT). Incomplete cells must not be silently reweighted; discard/recompute rules are prespecified in the revised design.
3. **Uncertainty procedure candidates.** *Primary:* two-way cluster bootstrap over body identities and suite identities (resample both axes independently with replacement; score the intersection cells; percentile interval at the nominal level). *Fallback:* crossed random-effects (variance-components) interval with body and suite as crossed factors. Both are evaluated in Phase 1 coverage simulation against the actual crossed target; the procedure carried forward is whichever passes (4). If neither passes, Phase 1 stops with an interval-procedure failure and the predictive question is not tested with intervals under v0.3. The v0.2 overlapping-fold bootstrap remains barred without a coverage test.
4. **Coverage criterion (candidate number; freeze-blocker).** Nominal 95% intervals must achieve empirical coverage ≥ 92.5% in **every** cell of the preregistered simulation grid, including the thin-support cells (scenarios of §5 item 5). Known caveat recorded (CLAUDE): the two-way bootstrap undercovers with few bodies and few suites; those cells exist precisely to expose this. The number 92.5% is proposed here, fixed before any simulation or feasibility data exist, and remains a freeze-blocker until owner/reviewer sign-off. The simulation gate must also prespecify the number of replications and how Monte Carlo uncertainty in the estimated coverage is treated.
5. **Still owed to the revised design (A remains OPEN).** The support-selection rule of (2) — minimum distinct-body counts, within-k C-variation requirement, rank/overlap requirement, application to held-out cells, and its numerical thresholds; split proportions; number of repetitions; deterministic seed policy; aggregation of overlapping test appearances across repetitions; handling of empty or inadequate support within a repetition; simulation-replication count and Monte Carlo-uncertainty treatment for the coverage gate. This is a candidate procedure, not yet a fully operational evaluation protocol.

Closure of A requires the Phase 1 coverage simulation to pass its prespecified criterion; document revision cannot close it (GLM's point, accepted).

### B. Outcome-variation gate — OPEN

The gate must judge variation in the **modeling outcome** — the per-hidden-input soft label s/20 per body-suite pair — not a pooled correct/incorrect rate over hidden inputs (GPT B; CLAUDE 2). A pooled gate can pass while every eligible body-suite pair has the same success fraction; that is useless variation for the estimand. The Phase 0 design currently has no outcome-variation criterion at all (verified: §8, §9). Proposed form, not yet frozen:

- **Sample.** A separate, **predesignated feasibility sample**: its bodies and suites are distinct from all confirmatory material, excluded from confirmatory analysis and from all estimation. Confirmatory outcomes are never inspected to decide feasibility.
- **Statistic (population aligned to §3A(2); GPT's final correction; binding).** Evaluate the soft labels s/20 on the separate feasibility sample, **restricted to body-suite pairs whose body belongs to the outcome-blind analysis support defined by the preregistered identifiability gate in §3A(2)** — not range membership alone, so the gate cannot pass on outcome variation occurring only among bodies outside the analysis support. The binding criterion is **minimum counts in both tails**: at least M pairs with s/20 ≤ θ_lo and at least M pairs with s/20 ≥ θ_hi, where θ_lo < θ_hi. The distinct-body and distinct-suite requirements apply within each tail. Numerical thresholds remain open until preregistration. **Confirmatory hidden outcomes must never be used to choose or revise the support.** Variance of s/20 ≥ v_min remains a secondary diagnostic only; variance alone can be driven by outliers and is not the binding criterion.
- **Crossed-support safeguard (GPT).** Tail pair counts alone are insufficient: many pairs can arise from repeated observations of few body identities, few suite identities, or both, which would not support the crossed generalization. The gate therefore **additionally requires prespecified minimum distinct-body and distinct-suite representation within each tail** — at least D distinct bodies and S distinct suites contributing to the lower tail, and likewise for the upper tail. Numerical values of D and S remain open until preregistration; pair counts alone do not close this issue.
- **Timing.** θ_lo, θ_hi, M, D, S, and v_min are fixed **before** any feasibility-sample hidden outcomes are collected (point D).
- **Precedent, not inheritance.** v0.2's pilot gate2 (≥ 10% correct and ≥ 10% incorrect among pairs' hidden inputs, `run_pilot_v02.py:18-19,72-76`) informs the discussion only; it pools inputs and ignores pair-level variation, and is **not** adopted as sufficient for this estimand.

Closure of B requires feasibility evidence collected under its prespecified thresholds; document revision cannot close it.

### C. δ* minimum meaningful effect — OPEN (freeze-blocker; owner decision required)

Arithmetic verified: δ* = ln(1.5)/20 = 0.020273255405408218 is unit-coherent for the soft-label outcome (per-input log loss; "20" = frozen hidden inputs per suite). **Statistical qualification (GPT; binding on the design document):** ln(1.5)/20 defines the proposed per-input log-loss threshold corresponding to a **1.5-fold multiplicative score contrast over 20 inputs under the stated additive log-loss scoring interpretation** — e^(20Δ) is a multiplicative contrast, **not a literal likelihood ratio for the joint 20-input outcome vector**, and nothing here implies the 20 inputs are independent replications (CLAUDE). The design revision must adopt this qualification in place of design §6's "likelihood ratio" phrasing.

The tie-break rationale explains why the decision matters — prioritizing candidates for an expensive confirmation slot — but it does not derive r = 1.5 from measured costs, and no measured cost ratio exists (GPT; CLAUDE). r = 1.5 can only be a **declared operational policy**, accepted by the owner as the minimum meaningful separation. Proposed owner statement (GPT's template; C stays OPEN until the owner affirms it or substitutes a different r with a stated reason):

> I accept r = 1.5 as my chosen minimum meaningful separation for this study. This is an operational decision threshold for prioritizing candidates for an expensive confirmation slot, not a value derived from measured costs.

Until that affirmation and review acceptance, δ* is not frozen and Phase 1 cannot start. v0.2's δ = 0.01 is not adopted. The proposed r = 1.5 is **not** treated as approved; GPT's recommendation is not the owner's acceptance.

### D. Threshold timing and failure disposition — RESOLVED

- **Timing rule (binding).** Thresholds serving diagnostic/range decisions and thresholds serving hidden-outcome-variation decisions are distinct sets. Each set is frozen before the data it will judge is observed. Neither set may be chosen or adjusted after observing its data.
- **Failure disposition (binding).** A feasibility-gate failure **terminates v0.3**. It is not followed by prompt tuning, switching to constructed solvers, probe-suite redesign, or resubmission. Any such pursuit is a separate owner decision after a deliberate pause, under a new charter — never a permitted continuation of a failed gate.
- **No forecast (GPT; GLM).** The prior populations create a **material feasibility risk** for v0.3 — k=0 dominance and absent within-k C variation appeared in both — but they do not establish the probability of gate failure under the proposed single-prompt generator, consistent with §2's non-equivalence clause. Gate failure is a **possible outcome**; this disposition clause applies **regardless of prior expectation**, expected or surprising. Framing failure as "the likeliest outcome" would weaken the clause (it invites rescue framed as fixing an expected bug rather than overruling a surprising finding) and is withdrawn.

The numerical values these rules govern are freeze-blockers (§5), not resolved by this point.

### E. Invalid and duplicate submissions — OPEN (invalid-body rule settled; estimand unit pending owner)

**Settled (owner decision, GPT §3).** The primary estimand is conditional on compilable, interface-conforming bodies, with the complete rule:

- **Validity.** Compilation and interface conformity determined by a frozen, deterministic check.
- **Retention and reporting.** Every generation attempt is retained in the provenance record; invalid-submission rate and valid-body count are reported. The invalid rate is itself a result about the generation process. Target population: the valid outputs of the specified generator, conditional on the frozen validity criteria — not every attempted output, not LLM solvers generally.
- **Budget.** Fixed generation budget; no best-of selection, no silent replacement, no outcome-driven resubmission. A valid-sample shortfall against preregistered requirements within budget is feasibility failure.
- **Post-validity behavior.** Wrong answers, runtime exceptions, and timeouts after passing validity are behavioral failures, not grounds for exclusion.
- **Provenance of repetition.** Exact-source hashes and duplicate rates are recorded; every generation attempt is kept in the record; repeated draws are not silently deduplicated (silent dedup would alter the target generation population).

**OPEN: the estimand's unit.** Two coherent choices exist (GPT, CLAUDE; the choice changes the estimand and must be disclosed, not treated as bookkeeping):

- **Option 1 — estimand over unique normalized bodies (recommended by GPT; leaned by CLAUDE and GLM).** Deterministic canonicalization limited to specified source-representation normalization; no semantic-equivalence detection. Each unique canonical body identity counts once toward support, independent-body counts, and scoring. All occurrences of an identical body are assigned to the same fold; duplicate occurrences receive no additional scoring weight. Duplicate rate is reported as a generator property. The estimand is explicitly over **unique valid body identities** produced by the specified generation procedure, not over generation attempts weighted by repetition frequency. Rationale (CLAUDE/GLM): the scientific claim is about solver implementations, not about how often a generator happens to repeat one. The normalization rule and the consequences for the target population must be explicitly defined before design freeze (GPT).
- **Option 2 — estimand over generation attempts.** Copies count in scoring; identical copies stay in one fold and count once in support.

The Revision 1 "weight 1/c per copy" rule is **withdrawn** — it fits neither option cleanly (CLAUDE). E is marked RESOLVED only when the owner explicitly adopts one option; reviewers' recommendations are not the owner's adoption.

## 4. Feasibility-before-analysis ordering — RESOLVED (document-first)

GLM's probe-first inversion (Revision 1 §4) is **withdrawn by GLM** after GPT's counter: the proposed 10–20-solver diagnostic probe is solver generation, and running it before the estimand, outcome gate, and inference procedure are specified would let early observations steer choices that must be fixed in advance — the exact pattern pre-registration exists to prevent. The prior populations create a material feasibility risk but do not establish what the probe would show under the proposed generator (§2 non-equivalence clause; no forecast). CLAUDE concurs. Ordering is settled:

- **Document-first.** No probe, no generation, no simulation before this response is reviewed, approved, and committed, and before the Phase 0 design is revised and separately reviewed.
- Any future diagnostic probe is a **separate, explicitly authorized executable phase**, specified inside the revised design under the pre-registered rules of D and E. It is not a shortcut around document completion.
- GLM's deferral point for δ* is moot under document-first: C remains a design-freeze blocker in its own right.

## 5. Freeze-blocker list (all must clear before design freeze)

1. δ* owner affirmation (§3C template or a substitute r with stated reason) plus review acceptance of the rationale paragraph in the revised design.
2. Estimand unit for duplicates (§3E): unique normalized bodies (reviewer recommendation) vs generation attempts — owner choice; disclosed as an estimand change relative to attempt-weighted sampling; normalization rule explicitly defined.
3. Support-selection rule and gate thresholds: the outcome-blind analysis-support rule of §3A(2) — minimum distinct-body counts, within-k C-variation requirement, rank/overlap requirement, application to held-out cells — with its numerical thresholds; outcome-variation gate (θ_lo, θ_hi, M, distinct-body minimum D, distinct-suite minimum S, v_min); minimum effective sample size per analyzed k bucket.
4. Coverage criterion number (§3A(4); candidate 92.5% at nominal 95%, pending sign-off), simulation-replication count and Monte Carlo-uncertainty treatment, and the crossed-procedure selection outcome — the latter requires Phase 1 simulation evidence and cannot be closed by document revision.
5. Thin-support budget statement under **separate historical stress-test scenarios** — explicitly not forecasts, not a pooled estimate, and not an estimate of v0.3's generator population (the non-equivalence clause of §2 bars pooling): (a) in-range mass 15.0% (historical v0.1 figure); (b) in-range mass 12.5% (historical v0.2 figure); (c) a lower-support scenario below both historical figures; (d) a no-usable-support scenario (zero bodies in the potentially identifiable range). For each scenario: expected independent in-range bodies at a candidate generation budget, the minimum per-k counts the design requires, and the budget implied — stated plainly, before any budget is spent, including when that budget is unrealistic.
6. Simulation power/FPR numbers and sample-size scenarios including the de-pooled stress scenarios of item 5 (GPT R4); the crossed-procedure selection rule itself is fixed now (§3A(3)–(4)).

## 6. Status and next steps

- Provenance corrections: **resolved** (§1–§2), including the 4/20 vs 3/20 non-conflation and the range-vs-observed-support vocabulary.
- Invalid-body rule (conditional on valid bodies): **resolved** in substance; the estimand unit for duplicates (§3E) is **open** — owner choice.
- Potentially identifiable range 2 ≤ k ≤ 24: **resolved as a design correction**; it is maximum possible support, not evidence sufficient variation exists in any sampled population. Observed identifying support was established by neither prior population, and range membership alone does not establish estimator eligibility.
- A crossed evaluation: **open** — candidate procedure specified; support-selection rule, operational details, and coverage evidence outstanding.
- B outcome-variation gate: **open** — statistic population aligned to the §3A(2) outcome-blind analysis support (Revision 5); crossed safeguards and timing specified; thresholds and feasibility evidence outstanding.
- C δ*: **open** — awaiting the owner's affirmation statement (§3C).
- D timing and failure disposition: **resolved** — with no-forecast framing.
- E duplicates: **open** — awaiting the owner's estimand-unit choice (§3E).
- Ordering (§4): **resolved** — document-first; any probe is a later, separately authorized phase.
- Estimand integrity: **verified** — design §2's estimand stands; Revision 2's adjacent-k clause was this document's error and is deleted; Revision 4 (GPT's final blocker) additionally fixes eligibility: the estimator's analysis support is the preregistered outcome-blind observed-support rule, not potential-range membership. The design revision must define that rule and adopt the §2 support vocabulary.
- Overall: **not ready to freeze; Phase 1 is not authorized.** No Phase 1 simulation, solver generation, or confirmatory hidden-outcome collection is authorized.
- Pending owner decisions: (1) the §3C affirmation sentence (accept r = 1.5, or supply a different r with a reason); (2) the §3E estimand unit (unique bodies vs attempts). C and E may remain OPEN in the committed response document.
- Posture: Revision 5 is committed and published (`4018ebd`, owner-authorized 2026-10-14) as the terminal response document after final line-by-line review; OPEN items carry into the revised Phase 0 design as freeze-blockers and are not closed by further document iteration. Next sequence: revised design as a new dated document → separate review → separate Phase 1 decision.
- All counts in §1–§2 are MIMO's own aggregations over persisted JSON (`pilot/pilot_report.json`, `v02/pilot_v02/pilot_v02_report.json`), reproducible in a minute by any reviewer.

## Appendix — verified counts

```text
v0.1 (pilot/pilot_report.json, 20 bodies, k solver-stable across 3 instances):
  k_hist: {0: 16, 5: 2, 10: 1, 25: 1}   potentially_identifiable_range(2..24): 3/20 (15.0%)
  distinct C per k: 0->0.0  5->1.0  10->0.5  25->0.2   observed_identifying_support: none
  old_gate_eligible (k>=2): 4 bodies, all Y=0 every instance; yield 4/20 (old gate >= 15/20)
    -> INFEASIBLE under the old gate; the k=25 body is outside the range (C forced)

v0.2 (v02/pilot_v02/pilot_v02_report.json, 120 bodies x 3 instances):
  k_hist per body: {0: 90, 5: 9, 10: 3, 20: 3, 25: 15}
  potentially_identifiable_range(2..24): 15/120 (12.5%)   k>=25: 15/120 (12.5%)   k=0: 90/120 (75.0%)
  within-k C variation in the realized pack: none — all observed eligible rows had C=5/k.
    Property of the realized pack, not a general instrument rule: C=5/k is forced only for
    k>=25; at k=24 the minimum attainable C is 4/24 and the maximum is 5/24 (discrete
    family counts). observed_identifying_support: none.

generator provenance: specs/generator_spec.json (v0.1, LLM, directed) | v02/generate_pack.py (v0.2, constructed)
```
