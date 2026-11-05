# LC518 scientific decision: Claim B1 as the first-stage target

**Date:** 2026-11-05  
**Status:** Agent decision under the owner's explicit delegation in this conversation. Review-branch record only. This document does not freeze or amend the v1.0 design, adopt review revision 2.6, or authorize construction or execution.

## 1. Decision

The programme target remains **Claim B**, not Claim A.

For the current LC518 iteration, Claim B is operationalized as **Claim B1: concentration information beyond individual mutation-mechanism identity, in the single-mutation population**.

The primary B1 population is the set of singly mutated versions:

- `SA`: mutation A only;
- `SB`: mutation B only;
- `S-extra`: one additional single mutation.

The following are outside the primary B1 estimand:

- `S0`: unmodified parent control; retain it for matched correctness/control analyses, not as a mutation-identity stratum;
- `SAB`: two mutations applied together; retain it for the planned matched interaction description, but do not use it to claim information beyond exact pair composition.

This is an explicit scope restriction, not a silent downgrade to Claim A. It gives the current design a potentially identifiable first question while refusing to claim that the 28+2 schedule supports broad pair-interaction identification.

**Claim B1 question:** among singly mutated solver versions, does the observable concentration of definite diagnostic failures across the eight input strata carry information about held-out correctness beyond total definite failures, unresolved diagnostic outcomes, parent algorithm family/context, and the identity of the one individual mutation mechanism?

A positive B1 result applies only to this constructed single-mutation population and the fixed LC518 task/bank. It does not establish the same result for natural solver submissions, arbitrary programmes, or combinations of multiple defects.

## 2. Why Claim A is not the programme target

Claim A asks whether (C_D) improves prediction within the complete constructed mixture beyond (k_{fail}), (k_{unresolved}), and parent family.

That is a population-internal prediction question. It does not address whether (C_D) is merely revealing which mechanism generated the failures. The natural-solver route failed to identify concentration separately from carrier family/defect identity (see the programme's construct-validity assessment and E02). Repeating the same confounding in a constructed mixture would not answer the programme's central question.

The index itself is not novel. Both (C) over defect-family failures and (C_D) over diagnostic-stratum failures are Berger–Parker dominance indices applied to different distributions. The potential contribution is evidence about incremental information, not a new formula.

## 3. Why B1, not B2, is the first LC518 target

B1 conditions on the identity of one individual mutation mechanism. The frozen pair schedule gives each of the eight mechanisms seven base appearances in the complete graph of 28 unordered pairs. The two repeated pairs add zero to two further appearances to the relevant mechanisms. S-extra assignments are annex-dependent; the number of distinct parent contexts they add cannot be determined without the annex.

This is nominal incidence, not established identifiability. A2-static must check the actual allocation across parent groups and algorithm families. A3-dynamic must establish the realized diagnostic profiles.

B2 would ask whether concentration adds information beyond the exact composition of a dual-mutant pair. The frozen schedule has 28 exact pair types across 30 parent assignments: 26 pair types occur once, and two pair types occur twice. Thus, 26 pair compositions have no parent replication and the remaining two have only (n=2). This is inadequate for a broad claim about pair-specific interactions or generalization across exact dual-mutant compositions. The frozen v1.0 analysis specification itself describes the 28-pair screen as exploratory with limited replication (v1.0 §3 and §8).

Accordingly:

- **B1 is the primary target for this LC518 iteration.**
- **B2 is deferred and excluded from the primary claim.**
- No result from B1 may be described as evidence that (C_D) adds information beyond exact dual-mutant composition or generalizes to arbitrary combinations of defects.
- A future B2 study would require a redesigned allocation with repeated exact pair compositions across independent parent contexts. The current 28+2 schedule is not to be retroactively presented as such a design.

This decision does not claim that B2 is scientifically unimportant. It says the current allocation does not support it adequately.

## 4. B1 identification requirements

The B1 question is not answered merely because the individual mechanisms recur in the allocation. The study must show that concentration varies within mechanism identity.

Before any candidate execution, the annex-dependent A2-static review must map each singly mutated version to its individual mechanism, parent group, and parent family. It must determine whether the schedule provides plausible same-mechanism comparisons across parent contexts. Static review may assess assignments and compatibility; it cannot establish that a mutation triggers or produces a particular failure profile.

After separately authorized diagnostic execution, the B1 support audit must examine, without pooling across mechanisms or exact failure-count cells:

- (k_{fail}\geq 2);
- exact ((k_{fail},k_{unresolved})) cells within each individual mechanism;
- at least three distinct parent groups in a supported mechanism-cell;
- at least two distinct observed (C_D) values within that mechanism-cell;
- representation across at least two parent algorithm families.

This is a proposed minimum *identification-support screen*, not a power calculation, precision guarantee, or effect-size threshold. It must be frozen in the revised analysis specification before execution. The existing revision 2.6 §5.2 support rule is a separate within-parent rule; it does not by itself establish within-mechanism support.

For an aggregate claim across all eight mechanisms, each mechanism must have at least one supported cell under the frozen rule. If only a subset has support, report results only for that subset and do not generalize to all eight mechanisms. If the required support is absent, report **NON-IDENTIFICATION / INSUFFICIENT WITHIN-MECHANISM SUPPORT**, not a null concentration effect.

## 5. Analysis architecture and blinding

The frozen v1.0 E3 analysis remains unchanged and does not test concentration. Review revision 2.6 is not adopted and, as written, does not test B1 because its Model A/Model B comparison does not condition on individual mechanism identity.

A revised analysis specification is required before execution. It must define the B1 conditional comparison and the scoring/validation procedure in advance.

The separately predeclared B1 robustness stage may use the sealed mechanism identities **only to define mechanism strata and conduct within-mechanism scientific diagnostics**. It must not add mutation labels, version-role labels, or other construction ground-truth fields as predictors in the blind E3 model. It must not alter the frozen blind pass or trigger post-result model revision. The B1 stage and its analyst/access rules must be authorized and frozen before candidate outcomes are observed.

The fixed held-out bank is publicly exposed. It can support a fixed-bank developmental evaluation, but not a sealed confirmatory claim. No power or minimum-effect claim is authorized by the current specifications.

## 6. Stages and dependencies

1. **A1a — Abstract Within-Parent Support Capacity.** Retain the corrected same-family witness using two mutation-bearing slots, plus the single-stratum degeneracy counterexample. This proves mathematical capacity only. It does not prove B1 mechanism crossing.
2. **A2-static — Annex and allocation identification audit.** Requires the private mutation annex. Check taxonomy, assignments, parent compatibility, individual-mechanism incidence by parent family, S-extra assignments, and whether the B1 support pattern is plausible. Do not infer realized failure profiles.
3. **A3-dynamic — Realized diagnostic support.** Requires separate authorization and completion of the v1.0 §9 execution protocol, including interpreter pinning, runtime and memory budgets, timeout rule, and resolution of the reserved `d_timeout_s` column. Only execution can establish observed (f_j), (k_{fail}), (k_{unresolved}), and (C_D).
4. **B1 robustness and prediction assessment.** Requires a predeclared analysis specification and authorized analyst/access plan. The blind E3 pass remains separate and unchanged.

No stage in this record authorizes source construction, solver execution, held-out evaluation, fitting, or publication.

## 7. Failure and redesign rules

- If A2-static shows that the annex cannot provide plausible within-mechanism crossing across parent contexts, do not proceed under a claim that the current allocation can test B1. Redesign the allocation or abandon the LC518 concentration claim.
- If A3-dynamic shows no realized within-mechanism, same-cell (C_D) variation under the frozen support rule, report non-identification. Do not call it a negative or null effect.
- Do not silently switch to Claim A if B1 fails.
- Do not use the current pair schedule to make a B2 claim.
- Any redesign, revised estimand, or change to the frozen blind analysis must be recorded before outcomes are examined and separately authorized.

## 8. Source documents

This decision is bounded by the following design records on the base branch:

- `lc518-150/GLM_WORK_ORDER.md` v1.0, especially §§3–5, 9–13;
- `lc518-150/glm-handoff/PARENT_DESIGN.md` v1.0;
- `lc518-150/glm-handoff/BANK_DESIGN.md` v1.0, especially §6;
- `lc518-150/glm-handoff/ANALYSIS_SPEC.md` v1.0, especially §§3–4 and 8–9;
- `lc518-150/review-v1.2/analysis-revision-2026-11-02/ANALYSIS_SPEC_REVIEW_DRAFT.md` revision 2.6, review-only, especially §§2, 5, 7.

**Repository effect:** this file is added on a dedicated review branch. No frozen design document, `master`, bank, solver source, or execution artifact is modified.
