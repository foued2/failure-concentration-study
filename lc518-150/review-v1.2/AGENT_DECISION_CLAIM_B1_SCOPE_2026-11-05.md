# LC518 joint scientific decision: Claim B1 as the first-stage target

**Date:** 2026-11-05  
**Decision status:** GPT–Claude agreement on the primary target, subject to the conditions recorded below.  
**Repository status:** Review-branch decision record only. This is not a design freeze, does not amend the frozen v1.0 specifications, and grants no new execution or publication authorization.

## 1. Decision and primary target

GPT and Claude have reached agreement that **Claim B1 is the primary target for the first LC518 concentration study**.

**Claim B1:** Among singly mutated solver versions, does the concentration of definite diagnostic failures across the eight input strata carry information about held-out correctness beyond total definite failures and unresolved diagnostic outcomes, conditional on both the identity of the individual mutation mechanism and the parent algorithm family?

The primary B1 population consists of the intended singly mutated versions:

- \`SA\`: mutation A only;
- \`SB\`: mutation B only;
- \`S-extra\`: one additional single mutation.

\`S0\`, the unmodified parent, remains a control and is not a mutation-identity stratum. \`SAB\`, the dual-mutant version, is outside the primary B1 population.

The intended nominal count is **90 singly mutated versions**: 30 parent groups with three intended single-mutation slots each (\`SA\`, \`SB\`, and \`S-extra\`). This is a design count, not a verified realized count. The \`S-extra\` assignments and balancing depend on the private annex. Until that annex and the realized construction inventory are checked, 90 must not be reported as the number actually constructed or validated.

A positive B1 result would apply only to the supported part of this constructed single-mutation population and the fixed LC518 task and banks. **Any such result also depends on the realized construction matching the intended mutation assignments and version roles; that realization has not yet been verified.** It would not establish the same result for naturally generated solver submissions, arbitrary programmes, or combinations of multiple defects.

## 2. Claim A and B2 are not adopted

**Claim A is not adopted.** It asks whether concentration predicts correctness within the complete constructed mixture beyond failure count, unresolved outcomes, and parent family. That does not address whether concentration is merely revealing which individual mutation mechanism generated the failures. Failure to identify B1 will be reported as non-identification or insufficient support, not as a reason to switch silently to Claim A.

**B2 is deferred.** It asks whether concentration adds information beyond the exact composition of a dual-mutant pair. The current schedule contains 28 unordered pair types across 30 parent assignments: 26 pair types occur once and two occur twice. This does not provide adequate replication for a broad claim about exact pair composition or pair-specific interactions. The current schedule must not be presented as supporting B2.

The index itself is not novel. \`C_D\` is the Berger–Parker dominance index applied to the distribution of failures across the eight diagnostic input strata. The proposed contribution concerns incremental predictive information, not a new concentration formula.

## 3. B1 support and identification rule

B1 requires variation in concentration **within individual mutation mechanism and within parent algorithm family**, not merely variation between families or between mechanisms.

The exact support cell is:

\`(individual mutation mechanism, parent family Z, k_fail, k_unresolved)\`

A cell qualifies for the proposed minimum support screen only when all of the following hold:

1. \`k_fail\` is at least 2.
2. At least three distinct parent groups contribute singly mutated versions to that exact cell.
3. At least two distinct observed \`C_D\` values occur among those contributing parent groups.
4. No pooling is permitted across individual mechanisms, parent families, or exact \`(k_fail, k_unresolved)\` cells.

The audit must report the full mechanism × family × exact-cell table, including unsupported cells, zero-variance cells, and the number of distinct parent groups and \`C_D\` values in each cell.

This is an identification-support convention, not a power calculation, precision guarantee, or effect-size threshold. It must be specified in the revised B1 analysis specification before candidate outcomes are examined.

### K5 exclusion

**K5 is excluded from inferential claims and may be reported descriptively only.** The frozen parent roster contains only two K5 parent groups. It therefore cannot meet the three-parent minimum in a K5 family-cell. No B1 inference may be generalized to K5 under this support rule.

For other families, only mechanism × family × exact cells that actually meet the support rule can contribute to the B1 inferential scope. Unsupported mechanisms or family contexts must be identified explicitly. A result from supported cells must not be generalized to unsupported cells or to the entire eight-mechanism/eight-stratum design without evidence.

If the required within-mechanism × family × exact-cell support is absent, the result is:

**NON-IDENTIFICATION / INSUFFICIENT WITHIN-MECHANISM-AND-WITHIN-FAMILY SUPPORT**

It is not a null concentration effect and does not authorize a switch to Claim A.

## 4. Analysis architecture

The frozen v1.0 E3 analysis remains unchanged. It does not test concentration. Review revision 2.6 is not adopted and does not, as written, establish the B1 comparison.

A separate B1 analysis specification is required before execution. At minimum, the B1 comparison must assess the incremental contribution of \`C_D\` beyond:

- total definite failures (\`k_fail\`);
- unresolved diagnostic outcomes (\`k_unresolved\`);
- parent algorithm family (\`Z\`);
- individual mutation-mechanism identity.

Parent-group IDs are used for grouped validation and are not predictive covariates. Mechanism identity is used in a separate, explicitly unblinded B1 analysis lane. It must not be inserted into or used to alter the frozen blind E3 pass.

The revised B1 specification must predeclare the model comparison, handling of the support-qualified cells, validation and scoring procedure, aggregation, analyst access, and reporting. The exact predictive procedure is not frozen by this target decision.

The fixed held-out bank is publicly exposed. It can support a fixed-bank developmental evaluation, but not a claim that the evaluation set was sealed from public exposure. No power, minimum-effect, or confirmatory inference claim is authorized by the current specifications.

## 5. Stages and dependencies

1. **A1a: Abstract support capacity.** The same-family witness and the single-stratum degeneracy counterexample establish mathematical capacity only. They do not establish that the assigned mutation mechanisms can produce the required realized profiles.
2. **A2-static: Annex and allocation audit.** Requires the private mutation annex. It must verify the taxonomy, assignments, parent compatibility, mechanism incidence by parent family, and \`S-extra\` assignments and balancing. Static inspection cannot establish realized diagnostic behavior.
3. **A3-dynamic: Realized diagnostic support.** Requires the applicable separate authorization and completion of the execution protocol, including interpreter pinning, runtime and memory budgets, timeout handling, and resolution of the reserved \`d_timeout_s\` column. Only diagnostic execution can establish the realized failure profiles and \`C_D\` values.
4. **B1 prediction assessment.** Requires a revised, predeclared B1 analysis specification and a separately defined analyst-access plan. It remains distinct from the frozen blind E3 pass.

This joint decision concerns target selection and its repository record only. It does not authorize construction, execution, annex disclosure or completion, diagnostic evaluation, held-out evaluation, model fitting, or publication. Existing work-order permissions and stop conditions remain unchanged, including the private-annex dependency.

## 6. Failure and redesign rules

- If the annex and allocation cannot support plausible within-mechanism comparisons across parent-family contexts, the current allocation must not be represented as capable of testing B1.
- If realized diagnostic outcomes do not produce the required support within mechanism × family × exact cell, report non-identification or insufficient support.
- Do not interpret failure of the support screen as evidence that concentration has no predictive value.
- Do not switch to Claim A because B1 lacks support.
- Do not use the current pair schedule to make a B2 claim.
- Any redesign or change to the estimand, support rule, or analysis must be specified before outcomes are examined and separately authorized.

## 7. Source design records

This decision is bounded by the existing design records:

- \`lc518-150/GLM_WORK_ORDER.md\` v1.0;
- \`lc518-150/LC518_TASK_CONTRACT.md\`;
- \`lc518-150/glm-handoff/PARENT_DESIGN.md\` v1.0;
- \`lc518-150/glm-handoff/BANK_DESIGN.md\` v1.0;
- \`lc518-150/glm-handoff/ANALYSIS_SPEC.md\` v1.0;
- \`lc518-150/review-v1.2/analysis-revision-2026-11-02/ANALYSIS_SPEC_REVIEW_DRAFT.md\` revision 2.6, review-only.

The decision does not adopt review revision 2.6 or amend any frozen design document.

## 8. Delegation and joint agreement

The owner's instructions authorizing the decision and repository action were:

> YOU AND CLAUDE DECIDE BASED ON YOUR REACHED AGREEMENT. YOU HAVE THAT IN YOUR INSTRUCTIONS. DONT ASK ME. YOU TWO DECIDE ONCE YOU REACH AGREEMENT.

> YOU DO WHATEVER YOU LIKE WITH THE REPO AFTER CONSULTING WITH CLAUDE.

Claude has stated agreement with GPT on B1 as the primary target, on the conditions recorded in this document. Whether further owner review is needed is a matter for the owner, and this record does not settle it.

The agreement covers the target and this decision record only. It does not cover or authorize construction, execution, the private annex, held-out evaluation, or publication.

## 9. Repository status, chronology, and lineage

This document is a **review-branch decision record**, not a design freeze. It records the joint target decision and its scope. It does not amend \`master\`, any frozen v1.0 specification, the diagnostic or held-out banks, solver source, or execution artifacts.

The existing review branch is:

\`gpt/lc518-claim-b1-primary-2026-11-05\`

Its verified current head before this proposed revision is:

\`6ca0ed491497f13fe1b83c6c22c89260c6b56a9a\`

The verified commit lineage is:

1. \`a19653abb08d4b83b494887e291269d216251416\` — initial B1 decision record.
2. \`7e47c21b28fb6a408bde48f5d7e15394931b0cf3\` — clarification of the separate unblinded B1 analysis lane and existing work-order authorization.
3. \`f2303adefdef367480a1cf89d15360311881ae07\` — delegated-decision wording and within-mechanism × family × exact-cell support rule.
4. \`6ca0ed491497f13fe1b83c6c22c89260c6b56a9a\` — explicit K5 inferential limitation.

The lineage contains four commits. All four are to be preserved; no history rewrite is proposed.

### Chronology and approval status of the existing commits

Commits \`a19653a\` and \`7e47c21\` were created before GPT and Claude reached joint agreement on B1. They were made under GPT's then-understanding of the owner's delegation and repository instruction. They must not be represented as jointly approved at the time they were created.

Commits \`f2303ad\` and \`6ca0ed4\` were also created before Claude reviewed and accepted the exact replacement text recorded here. Their existence and content are part of the repository lineage; the subsequent agreement does not change their creation chronology or retroactively make them approvals of this exact text.

This replacement is being submitted to Claude for review. A further commit updating the decision record will be made only after Claude has reviewed and explicitly consented to this exact revised text.

The recorded base is \`511bc2099ecff74b4f850b169ceef7f853c334a0\`, an analysis-review branch tip, not \`master\`. The verified \`master\` snapshot remains at \`b3e98740716bd79ecc99346241d633fd405d49d8\`. The decision branch is separate from \`master\`. The branch record contains no private mutation annex or per-solver mutation assignments.

### Separate unresolved local write set

GLM previously reported a separate local working-tree write set consisting of:

- an untracked root-level \`LC518_CONCENTRATION_ESTIMAND_REVIEW_2026-11-05.md\`;
- a modification to \`REPOSITORY_STORAGE_INVENTORY_2026-11-05.md\`.

That local write set remains unresolved. It is separate from this GitHub review branch. This decision record neither claims to have inspected the current local Windows working tree nor claims to have reverted, retained, or committed those local changes.
