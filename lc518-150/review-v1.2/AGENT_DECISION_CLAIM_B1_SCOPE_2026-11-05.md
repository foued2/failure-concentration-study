# LC518 scientific decision: Claim B1 as the first-stage target

**Date:** 2026-11-05  
**Decision authority:** Effective delegated agent decision under the owner's explicit instruction in this conversation. The owner instructed GPT and Claude to decide upon agreement and authorized GPT to act on the repository after consulting Claude. No separate owner ratification is required for this target selection. **Repository status:** Review-branch record only. This document does not freeze or amend the v1.0 design, adopt review revision 2.6, or authorize execution.

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

**Claim B1 question:** among singly mutated solver versions, does the observable concentration of definite diagnostic failures across the eight input strata carry information about held-out correctness beyond total definite failures and unresolved diagnostic outcomes, conditional on both parent algorithm family and the identity of the one individual mutation mechanism? Parent-group IDs define grouped validation folds; they are not predictive covariates. The mechanism-conditional comparison is a separate, unblinded analysis, not the frozen blind E3 model.

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

After separately authorized diagnostic execution, the B1 support audit must assess variation conditional on **both** individual mechanism identity and parent algorithm family. The exact support cell is:

`(individual mechanism, parent family Z, k_fail, k_unresolved)`.

Within a support cell:

- k_fail must be at least 2;
- at least three distinct parent groups must contribute singly mutated versions to that exact cell;
- at least two distinct observed C_D values must occur among those groups;
- no pooling is allowed across mechanisms, parent families, or exact (k_fail, k_unresolved) cells.

This same-family requirement is essential. Variation that appears only between parent families could be explained by family, even if the mechanism identity is held fixed. A mechanism-family-cell with fewer than three parent groups or no C_D variation is unsupported for the proposed minimum screen. The audit must report the complete mechanism × family × exact-cell support table, including unsupported cells and zero-variance cases.

A known structural consequence follows from the frozen parent roster: K5 contains only two parent groups (PARENT_DESIGN.md v1.0 §3). It therefore cannot meet the three-parent minimum within any K5 family-cell. K5 may be reported descriptively, but this B1 support screen cannot support a mechanism-conditional inference generalized to K5. The primary B1 inferential scope is limited to mechanism × family contexts that actually meet the predeclared screen; a claim covering K5 would require a separately justified alternative support rule or a redesigned parent roster, fixed before outcomes.

This is a proposed minimum *identification-support screen*, not a power calculation, precision guarantee, or effect-size threshold. The three-parent floor is an operational support convention only. It must be frozen in the revised analysis specification before execution. The existing revision 2.6 §5.2 support rule is a separate within-parent rule; it does not by itself establish within-mechanism-and-within-family support.

For an aggregate B1 claim, every individual mechanism included in that claim must have at least one supported cell, and the supported cells must cover the parent-family contexts to which the claim is generalized. Report unsupported mechanisms and families separately; do not extrapolate the concentration interpretation into unsupported cells. If only a subset is supported, limit the claim to that subset. If the required support is absent, report **NON-IDENTIFICATION / INSUFFICIENT WITHIN-MECHANISM-AND-WITHIN-FAMILY SUPPORT**, not a null concentration effect.

## 5. Analysis architecture and blinding

The frozen v1.0 E3 analysis remains unchanged and does not test concentration. Review revision 2.6 is not adopted and, as written, does not test B1 because its Model A/Model B comparison does not condition on individual mechanism identity.

A revised analysis specification is required before execution. It must define the B1 conditional comparison and the scoring/validation procedure in advance.

The separately predeclared B1 robustness stage may use sealed individual-mechanism identities as conditioning strata and, if specified before outcomes, as nuisance terms in a separate unblinded conditional predictive comparison. The natural model contrast is a baseline containing the fixed flexible k_fail basis, k_unresolved, parent-family Z, and individual-mechanism identity, versus the same model plus C_D. Parent-group IDs remain fold/grouping variables, not predictors. This is a new analysis lane and does not amend the frozen blind E3 model. It requires a separately appointed analyst, declared access, a frozen estimand, support rule, preprocessing, validation and scoring procedure, and its own reporting. It must not alter the frozen blind pass or trigger post-result model revision. The B1 stage and its analyst/access rules must be authorized and frozen before candidate outcomes are observed.

The fixed held-out bank is publicly exposed. It can support a fixed-bank developmental evaluation, but not a sealed confirmatory claim. No power or minimum-effect claim is authorized by the current specifications.

## 6. Stages and dependencies

1. **A1a — Abstract Within-Parent Support Capacity.** Retain the corrected same-family witness using two mutation-bearing slots, plus the single-stratum degeneracy counterexample. This proves mathematical capacity only. It does not prove B1 mechanism crossing.
2. **A2-static — Annex and allocation identification audit.** Requires the private mutation annex. Check taxonomy, assignments, parent compatibility, individual-mechanism incidence by parent family, S-extra assignments, and whether the B1 support pattern is plausible. Do not infer realized failure profiles.
3. **A3-dynamic — Realized diagnostic support.** Requires separate authorization and completion of the v1.0 §9 execution protocol, including interpreter pinning, runtime and memory budgets, timeout rule, and resolution of the reserved `d_timeout_s` column. Only execution can establish observed (f_j), (k_{fail}), (k_{unresolved}), and (C_D).
4. **B1 robustness and prediction assessment.** Requires a predeclared analysis specification and authorized analyst/access plan. The blind E3 pass remains separate and unchanged.

This decision grants no new authorization. The existing v1.0 work order authorizes construction of the 150 source bodies but requires the private mutation annex before mutation assignments proceed; that stop condition remains binding. Candidate execution, diagnostic evaluation, held-out evaluation, fitting, and publication are not authorized by this decision.

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

## 9. Delegation, consultation, and repository lineage

The owner explicitly instructed GPT and Claude to decide on the scientific target once they reached agreement, and instructed GPT to act on the repository after consulting Claude. This is an explicit delegation of the target decision and repository action within the scope of that instruction. It is not described as the owner personally authoring the scientific conclusion. The delegated decision is effective; it is not awaiting a second ratification.

The consultation record is: Claude selected Claim B as the programme target; GPT narrowed the current LC518 implementation to B1 and deferred B2 on the basis of the pair-composition support; Claude's subsequent review described B1 as the primary single-mutation question and B2 as deferred; GLM verified the committed content and the support framework. The B1 scope is therefore the joint direction under the owner's delegation.

The first B1 branch commit was made before Claude's B1-specific review of the resulting document. That sequence was premature relative to the owner's instruction to consult Claude before repository action. Claude and GLM have now reviewed the branch content. This revision records the post-review corrections; future substantive repository changes will follow review before write.

Repository lineage:

- Base commit: `511bc2099ecff74b4f850b169ceef7f853c334a0` (analysis-review branch tip, not master).
- Initial decision commit: `a19653abb08d4b83b494887e291269d216251416` (adds this decision record).
- Clarification commit: `7e47c21b28fb6a408bde48f5d7e15394931b0cf3` (+2/−2 clarification).
- Current branch: `gpt/lc518-claim-b1-primary-2026-11-05`.
- The branch is separate from `master`; `master` remains at `b3e98740716bd79ecc99346241d633fd405d49d8` in the verified remote snapshot.
- The branch is public, but this decision record contains no private mutation annex or per-solver mutation assignments.

The earlier local working-tree write reported by GLM (the root-level estimand review file and the inventory bullet) is a separate local-state issue. Those paths were not found on the checked remote refs. This GitHub branch update neither removes nor purports to revert local Windows working-tree changes.