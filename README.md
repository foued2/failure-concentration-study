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

Rev 11 prescribes record-level diagnostic exposure: 64 diagnostic bank records, eight per stratum. A canonical-level calculation using 60 unique inputs is a different statistic and must be recomputed from its own failure vector; it is not an alternative coding to select after results. The held-out bank has 80 raw presentations representing 78 canonical identities. The two H6 reorder pairs still lack an adopted raw-to-canonical correctness aggregation rule. That rule is required before constructing or interpreting the canonical outcome matrix, but it is not an input to a strictly outcome-free diagnostic support census. The held-out bank is publicly exposed development data, not a sealed confirmatory benchmark. The owner-adopted 22 November contribution paragraph names this fixed 78-record development set. D0.3, recorded on 21 November, selected a confirmatory-with-consent route subject to consent, custody and B1-amendment gates. The repository record does not contain an explicit owner statement resolving whether the 22 November public-78 adoption superseded that earlier route. The current evaluation-target choice therefore remains unresolved; the public 78-record set is not a protected confirmatory bank. Resolve this route conflict explicitly before confirmatory planning. See the [Gate 1 preparatory reconciliation](reviews/analytical-validity-2026-11-18/GATE1_PREPARATORY_RECONCILIATION_2026-11-22.md) for the census authorization and readiness status. See [C_D measurement specification](reviews/analytical-validity-2026-11-18/CD_MEASUREMENT_SPEC_2026-11-19.md) and [B1 identity acceptance addendum](reviews/analytical-validity-2026-11-18/B1_IDENTITY_ACCEPTANCE_ADDENDUM_2026-11-22.md).

Provenance is a substantive requirement, not administrative decoration. A master-branch audit found that the retained v0.2 emitter deterministically wrote 40 literal source-body templates three times each, producing 120 files. The repository does not independently substantiate the claimed model-generation sessions, raw single-shot outputs, or no-selection/no-edit history. This establishes **unverified origin**, not proven human authorship. Hashes establish byte identity, not model origin. Any future parent acquisition must document source identity, authorship/origin where known, lineage, transformations, outcome-blind selection, family assignment, hashes, permissions and custody. A specifically model-generated origin claim must pass the six-point provenance gate in [the master-branch adjudication](reviews/CLAUDE_FULL_REPO_CHALLENGE_ADJUDICATION_2026-11-21.md) §6.

## Gate status

### Gate 0 — CLOSED, limited to positioning and contribution definition

The owner adopted the bounded contribution statement. The scoping review records the closest screened work, the inferential scope and the limits of its search. This is not a systematic review, novelty finding or priority claim. The scientific proposition `P` remains **UNPROVEN**. The supported literature statement is limited to the records screened in the documented OpenAlex pass.

Gate 0 does not establish predictive value, empirical feasibility, statistical power or operational readiness. The owner-adoption and population decisions are recorded as conversational acts; their provenance caveat remains explicit.

### Gate 1 — CENSUS AUTHORIZED CONDITIONALLY; NOT RUN / BLOCKED

The next prescribed action is an outcome-free census of diagnostic support. For each exact B1 cell, the census must report version count, distinct-parent count, distinct `C_D` values and within-cell variation. Full-population eligibility requires `k_fail ≥ 2`, at least three distinct parents, and at least two distinct `C_D` values. Each leave-one-parent-out training fold must separately meet its frozen estimability conditions. Record-level and canonical-level exposure audits must not be mixed. All exclusions, scored parents, test rows and coverage must be reported. The LOPO reconciliation proposes a three-part minimum-coverage gate: scored-parent fraction `ρ_min`, scored-cell fraction per fold `ρ_cell`, and records-scored fraction per fold `ρ_rec`; the denominators and numeric floors remain an owner decision. Those floors and the `SUPPORTED` / `NOT SUPPORTED` / `NOT ASSESSABLE` verdict rule must be frozen before a realised diagnostic manifest exists. Without them, the census can be descriptive only and cannot receive an overall Gate 1 PASS/FAIL.

**Census readiness at the inspected repository snapshot: BLOCKED / NOT ASSESSABLE.** A read-only recursive tree check of the current review branch returned 3,086 entries (`truncated=false`). It showed no current LC518 parent/variant roster, no current per-variant diagnostic manifest, and no eight-stratum failure/unresolved vectors. The B1 78-record canonical-ID manifest is an evaluation identity list, not a diagnostic-results table. Other diagnostic-looking files belong to `expression_eval_v1`, `paren7_min_insertions`, or the earlier graph/SSSP feasibility work; they cannot be pooled or relabelled as current LC518 evidence. The legacy solver packs also do not establish a current accepted LC518 roster. No LC518 support counts or LOPO decisions have been computed.

The toolchain does not fill this gap. The separate M1-si engineering bundle is an **auditor for an already-produced manifest**, not a data generator. Its README says the bundle contains no study data, and the fixtures are synthetic software tests. Its schema encodes `OC-A`–`OC-D` operator classes, which are not an owner-accepted LC518 q inventory. The validator is not automatically a validated implementation of B1 v1.7. Running it on its fixtures would test software behaviour, not establish realized B1 support.

The upstream design authorities also have distinct limits. B1 analysis plan v1.7 is accepted and frozen as a **symbolic analysis plan**, but its acceptance record explicitly says this is not an execution GO. The v0.21-linked D1–D8 taxonomy v0.4 has an owner-acceptance record for the taxonomy only; its associated diagnostic-bank generation protocol v0.2.1 is not frozen and carries no generation or execution GO. These records do not demonstrate that a current per-variant diagnostic manifest exists.

This is missing input evidence, not a demonstrated scientific failure. The census has not been run. The absence of the H6 outcome-aggregation rule is not the reason it is blocked: H6 gates the canonical outcome matrix, not the outcome-free support census.

On 22 November the owner clarified the earlier instruction by answering **“YES START”** to the question whether it authorized the outcome-blind support census itself once its prerequisites were met. The census is therefore **AUTHORIZED CONDITIONALLY**. No additional census-specific owner GO is required after all prerequisites are satisfied. This does not authorize creation of the missing manifest or any upstream parent acquisition/selection, mutation allocation, bank generation, solver construction/build, compilation, execution, or diagnostic probing; those production steps retain their separate prerequisites and GOs. Gate 1 remains NOT STARTED; the census is NOT RUN / BLOCKED pending inputs. The wider project pause remains in force outside the work expressly authorized.

**What must happen before the conditionally authorized census can execute:** define and freeze actual q mutation identities and parent-family assignments consistent with B1 v1.7 before diagnostic execution; establish the parent/variant roster and provenance, with owner-frozen caps for parents, variants per parent, total variants, compute/runtime, monetary spend and stop conditions before any production GO (all currently unknown); if M1-si is also to be assessed, accept the separate q/a amendment first; complete the population, source, lineage and mutation-operator design under the applicable gates; freeze the diagnostic generation protocol and obtain separate GOs for bank generation, solver construction/build and diagnostic execution; develop a B1 v1.7-specific schema/validator and census script, independently review it, pin its runtime and hash-freeze the instrument before the realised diagnostic manifest exists; freeze the numeric coverage thresholds, their denominators and the verdict rule before the manifest exists; produce and validate a complete per-variant manifest with all eight record-level failure counts and unresolved counts; then exercise the owner's already-granted conditional census authorization. **Do not request another census-specific GO once these prerequisites are met.** The current generation-protocol draft also contains protected-frame/custody preflight requirements that must be reconciled before relying on it for generation. The 21 November D0.3 confirmatory-with-consent selection and the 22 November public-78 contribution wording remain operationally unresolved; that must be reconciled before confirmatory planning or protected-set preflight. It does not alter the arithmetic of a strictly outcome-free support census. The census must report every eligible/excluded cell, LOPO fold, scored parent, test row and coverage result. The census instrument, schema, runtime, inputs and output must be hash-identified.


The outcome-free support census is authorised conditionally by the owner's 22 November clarification (“YES START” in response to GPT's exact question recorded in the reconciliation and reviewer ledger). No additional census-specific GO is required after its prerequisites are satisfied. The authorisation does not cover parent acquisition, mutation allocation, bank generation, solver construction/build or diagnostic execution; those require their own GOs. The readiness finding is limited to the inspected review-branch tree, not a claim that no files exist in any other branch or local workspace.

A valid census cannot be made self-adjudicating after its data exist. Before the realised manifest is produced, the q mapping, the B1 v1.7-specific census/validation implementation and hashes, and the coverage thresholds/verdict rule must all be frozen. If the owner does not set the coverage floors in advance, the census may report descriptive support counts only; it cannot receive an overall Gate 1 PASS/FAIL. Non-overlap of diagnostic and public evaluation identities, if established, must not be described as statistical independence: future predictive claims must disclose diagnostic candidate selection, shared generation lineage and public exposure.

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
- [Master provenance adjudication](https://github.com/foued2/failure-concentration-study/blob/master/reviews/CLAUDE_FULL_REPO_CHALLENGE_ADJUDICATION_2026-11-21.md) — v0.1/v0.2 retained-corpus provenance findings and the six-point future gate. 
- [Accepted B1 v1.7 symbolic analysis plan](https://github.com/foued2/failure-concentration-study/blob/gpt/b1-m1-rev1.2-review-chain-2026-11-14/lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/B1_ANALYSIS_PLAN_2026-11-14_v1.7.md) and [its acceptance record](https://github.com/foued2/failure-concentration-study/blob/gpt/b1-m1-rev1.2-review-chain-2026-11-14/lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/GPT_ACCEPTANCE_RECORD_B1_ANALYSIS_PLAN_V1.7_2026-11-14.md) — symbolic plan accepted/frozen; not an execution GO.
- [Gate 1 preparatory reconciliation](reviews/analytical-validity-2026-11-18/GATE1_PREPARATORY_RECONCILIATION_2026-11-22.md) — reconciles B1/M1-si, q/a, v0.21 taxonomy authority, generation status, operating-count limits and census authorization.
- [M1-si audit utility README](https://github.com/foued2/failure-concentration-study/blob/gpt/lc518-m1si-audit-2026-11-17/lc518-150/engineering/README.md) — specifies that the utility audits an existing manifest and does not generate or execute solver data.
- [Owner acceptance of v0.21 diagnostic-strata taxonomy v0.4](https://github.com/foued2/failure-concentration-study/blob/gpt/lc518-v021-operational-strata-spec-2026-11-21/docs/LC518_V021_V04_OWNER_ACCEPTANCE_2026-11-21.md) and [v0.2.1 generation-protocol amendment](https://github.com/foued2/failure-concentration-study/blob/gpt/lc518-v021-generation-protocol-2026-11-21/docs/LC518_V021_DIAGNOSTIC_BANK_GENERATION_PROTOCOL_2026-11-21_v0.2.1_AMENDMENT.md) — taxonomy acceptance is not a generation-protocol freeze or execution GO.

Repository snapshot used for this README update: audit branch HEAD `cffaf9b34cd9e412ab7b46eb8205ab00058a311a`; reconciliation is recorded on `gpt/gate1-preparatory-reconciliation-2026-11-22`. This update changes documentation only; it does not modify frozen protocols, solver sources, banks or experimental data.
