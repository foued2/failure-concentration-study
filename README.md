# LC518: Diagnostic failure concentration and solver correctness

**Scientific presentation and current research status — 22 November 2026**

LC518 is a research programme, not a validated prediction tool. Its question is whether the distribution of diagnostic failures across eight prespecified input strata adds predictive information about engineered solver variants' correctness on a separate development bank, beyond a defined exact-cell baseline.

The original Doctor/C_genuine project was terminated. LC518 is a clean-room successor, not a rescue or continuation of that project and does not inherit its scientific validity.

## The scientific question

When two versions of an engineered solver have the same number of definite diagnostic failures, could the way those failures are distributed across diagnostic input categories tell us anything more about their correctness on other inputs?

LC518 represents the largest share of definite failures with the Berger–Parker dominance index:

`C_D = max_j(f_j) / k_fail`

where `f_j` is the number of definite failures in diagnostic stratum `j`, and `k_fail = Σ_j f_j`. The index is an established statistic from ecology (Berger & Parker, 1970); it is not claimed as new. Unresolved outcomes are not included in `C_D`; their count is retained separately as `k_unresolved`.

The adopted B1 proposition is narrower than the slogan “concentration predicts correctness”. It tests whether a version-level maximum-share summary adds predictive information about record-level correctness beyond the exact-cell baseline:

`(q, Z, k, ℓ) = (mutation mechanism, parent family, k_fail, k_unresolved)`

The evaluation is leave-one-parent-out within the selected and observed parent implementations. The claim is conditional on those parents. It does not claim generalization to all solvers or to a superpopulation of independently developed parents. Nor does it claim that `C_D` contains information unavailable in the complete failure vector: it is a deterministic summary of that vector.

## Why this is a difficult research question

The central identification problem is not hidden: the programme has repeatedly failed to construct the required equal-failure-count, different-concentration contrast independently of other design variables.

- The earlier Option B profile ladder changed the leading carrier failure count as concentration changed, so the intended contrast was confounded with carrier count.
- A bounded audit examined 257 candidate mechanisms. Fourteen produced the specified five-failure count. Eight cross-mechanism profile matches were found, but all had identical full-domain failure sets. The audit found **zero distinct mechanism matches** under its definition. This is a bounded negative construction result, not proof that no possible mechanism could work. See [the construction-audit result](engineered-study/08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md).
- The later LC518 design also acknowledged that its realization setting and `C_D` varied together rather than establishing independent concentration variation. See the [theory succession audit](reviews/analytical-validity-2026-11-18/concentration-theory-succession-audit-2026-11-18.md), especially §4.

There is also a mathematical support ceiling. With eight diagnostic strata, at most eight distinct `C_D` values can occur at any fixed `k_fail` on the record-level exposure basis. For `9 ≤ k_fail ≤ 16`, the record-level upper bound is seven. These are attainable-value limits, not evidence that a study population realizes the required values. The exact attainable set depends on the exposure basis. See [the measurement and support register](reviews/analytical-validity-2026-11-18/NOVELTY_AND_POSITIONING_REGISTER_2026-11-19.md) §9.3.

These failures do not establish that the scientific hypothesis is false. They establish that the required identifying variation has not yet been demonstrated.

## Population, measurement and provenance

The current target is **engineered solver variants deliberately constructed or modified under a declared study process, nested within selected real parent solver implementations**. The variants are the tested units; parent implementations are the source and grouping units. The inference remains conditional on the selected and observed parents.

The owner clarified this target on 22 November 2026. The decision is recorded in the project conversation and in the repository; the repository does not independently authenticate the conversational act. No parent roster has been selected. The historical feasibility work that used “natural solver” terminology remains part of the record of those particular procedures; it is not a separate current target population. See the [reviewer ledger](reviews/analytical-validity-2026-11-18/REVIEWER_RESPONSE_2026-11-18.md) §33 and the [positioning register](reviews/analytical-validity-2026-11-18/NOVELTY_AND_POSITIONING_REGISTER_2026-11-19.md) §15.

Rev 11 prescribes record-level diagnostic exposure: 64 diagnostic bank records, eight per stratum. A canonical-level calculation using 60 unique inputs is a different statistic and must be recomputed from its own failure vector; it is not an alternative coding to select after results. The held-out bank has 80 raw presentations representing 78 canonical identities. The two H6 reorder pairs still lack an adopted raw-to-canonical correctness aggregation rule. That rule is required before constructing or interpreting the canonical outcome matrix, but it is not an input to a strictly outcome-free diagnostic support census. The held-out bank is publicly exposed development data, not a sealed confirmatory benchmark. See [C_D measurement specification](reviews/analytical-validity-2026-11-18/CD_MEASUREMENT_SPEC_2026-11-19.md) and [B1 identity acceptance addendum](reviews/analytical-validity-2026-11-18/B1_IDENTITY_ACCEPTANCE_ADDENDUM_2026-11-22.md).

Provenance is a substantive requirement, not administrative decoration. A master-branch audit found that the retained v0.2 emitter deterministically wrote 40 literal source-body templates three times each, producing 120 files. The repository does not independently substantiate the claimed model-generation sessions, raw single-shot outputs, or no-selection/no-edit history. This establishes **unverified origin**, not proven human authorship. Hashes establish byte identity, not model origin. Any future parent acquisition must document source identity, authorship/origin where known, lineage, transformations, outcome-blind selection, family assignment, hashes, permissions and custody. A specifically model-generated origin claim must pass the six-point provenance gate in [the master-branch adjudication](reviews/CLAUDE_FULL_REPO_CHALLENGE_ADJUDICATION_2026-11-21.md) §6.

## Gate status

### Gate 0 — CLOSED, limited to positioning and contribution definition

The owner adopted the bounded contribution statement. The scoping review records the closest screened work, the inferential scope and the limits of its search. This is not a systematic review, novelty finding or priority claim. The scientific proposition `P` remains **UNPROVEN**. The supported literature statement is limited to the records screened in the documented OpenAlex pass.

Gate 0 does not establish predictive value, empirical feasibility, statistical power or operational readiness. The owner-adoption and population decisions are recorded as conversational acts; their provenance caveat remains explicit.

### Gate 1 — NEXT: design-only support census

The next prescribed action is an outcome-free census of diagnostic support. For each exact B1 cell, the census must report version count, distinct-parent count, distinct `C_D` values and within-cell variation. Full-population eligibility requires `k_fail ≥ 2`, at least three distinct parents, and at least two distinct `C_D` values. Each leave-one-parent-out training fold must separately meet its frozen estimability conditions. Record-level and canonical-level exposure audits must not be mixed. All exclusions, scored parents, test rows and coverage must be reported. The repository has not established a minimum acceptable overall scored-parent coverage threshold, so finding one eligible cell cannot automatically be called a Gate 1 PASS.

**Gate 1 preflight at the current repository snapshot: BLOCKED / NOT ASSESSABLE.** The current branch contains bank definitions, identity records and historical diagnostic outputs from earlier, different studies. It does not contain an LC518 parent roster, 150 LC518 solver variants, or the per-variant LC518 diagnostic failure vectors needed to populate the exact-cell census. The project record remains at 0/150 LC518 solver bodies and zero LC518 solver outcomes. Historical diagnostic files from other tasks are not substitutes and must not be pooled or relabelled as LC518 evidence.

This is missing input evidence, not a demonstrated scientific failure. The census has not been run. The absence of the H6 outcome-aggregation rule is not the reason it is blocked: H6 gates the canonical outcome matrix, not the outcome-free support census.

The owner's 22 November instruction to move to Gate 1 is treated as authorization to advance to this Gate 1 preflight and the design-only census when its required diagnostic tables exist. It does **not** authorize reconstructing an unestablished mutation allocation, acquiring or selecting parents, constructing or generating solvers, running solvers, collecting outcomes, fitting models or conducting predictive analysis. Any such production work requires its own explicit authorization. The project pause remains in force outside this limited Gate 1 step.

### Gate 4 — NOT STARTED

MDE, power and operating characteristics for the actual B1 pipeline remain unestablished. The analytical pipeline has not demonstrated recovery of a known B1 predictive effect under a matching known-truth design. An unpowered or unsupported null must not be presented as evidence against the hypothesis.

## The adopted null-interpretation rule

A null result must be reported as **inconclusive** unless Gate 1 support and Gate 4 power establish that the design could have detected a stated effect. A null without those conditions is a support failure, not a negative scientific finding. This rule is part of the owner's adopted contribution statement; it is a reporting commitment, not evidence that the required power or known-effect recovery has already been demonstrated.

## Questions we invite researchers to challenge

The project itself records two substantial challenges:

1. Is the conjunction of an established index, a fixed diagnostic partition and grouped evaluation a scientific contribution, or a well-specified ablation?
2. If the exact-cell baseline is beaten, is a one-parameter improvement worth reporting when a flexible model using the full failure vector could perform better? Parsimony, finite-sample stability and interpretability have not yet been measured as practical advantages.

We invite researchers in software testing, program analysis, algorithm engineering and statistical learning to challenge the estimand, measurement alignment, support requirements, provenance controls and contribution claim before any further execution.

**This is an invitation to review a falsifiable research proposition, not a request to buy or adopt a validated tool.**

## Key records

- [Novelty and positioning register](reviews/analytical-validity-2026-11-18/NOVELTY_AND_POSITIONING_REGISTER_2026-11-19.md) — adopted contribution, bounded prior-work comparison, support arithmetic and remaining challenges.
- [Reviewer response ledger](reviews/analytical-validity-2026-11-18/REVIEWER_RESPONSE_2026-11-18.md) — owner decisions, provenance caveats, population scope and gate status.
- [Fundamental research goal](FUNDAMENTAL_GOAL_ANALYTICAL_VALIDITY_2026-11-18.md) — research question and gate structure.
- [C_D measurement specification](reviews/analytical-validity-2026-11-18/CD_MEASUREMENT_SPEC_2026-11-19.md) — record/canonical exposure and unresolved-outcome boundaries.
- [B1 identity acceptance addendum](reviews/analytical-validity-2026-11-18/B1_IDENTITY_ACCEPTANCE_ADDENDUM_2026-11-22.md) — accepted 78-canonical identity chain and explicit measurement non-decisions.
- [Theory succession audit](reviews/analytical-validity-2026-11-18/concentration-theory-succession-audit-2026-11-18.md) — history of the identification and construction failures.
- [Option B construction audit](engineered-study/08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md) — bounded 257-mechanism audit and zero distinct mechanism matches.
- [Master provenance adjudication](reviews/CLAUDE_FULL_REPO_CHALLENGE_ADJUDICATION_2026-11-21.md) — v0.1/v0.2 retained-corpus provenance findings and the six-point future gate.

Repository snapshot used for this README update: branch `audit/analytical-validity-2026-11-18`, prior HEAD `660d3d09e7d1b84d4aec1f40b7fa783635cb8982`. This update changes documentation only; it does not modify frozen protocols, solver sources, banks or experimental data.
