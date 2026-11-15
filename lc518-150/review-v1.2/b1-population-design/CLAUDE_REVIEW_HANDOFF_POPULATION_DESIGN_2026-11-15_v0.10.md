# Claude Review Handoff: LC518 Population and Experimental Design v0.10

**Date:** 2026-11-15  
**Status:** READ-ONLY INDEPENDENT REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** \`gpt/b1-computational-plan-2026-11-14\`

## 1. Exact review target

Please review the complete v0.10 specification, not only this handoff:

- **Path:** \`lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.10.md\`
- **Branch:** \`gpt/b1-computational-plan-2026-11-14\`
- **Git blob SHA-1 at handoff preparation:** \`fd263e787062ac9377719d58d9d547d162c96683\`
- **Dimensions:** 1,081 lines; final newline present.

The immediate predecessor v0.9 remains unchanged:
- **Path:** \`lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.9.md\`
- **Blob:** \`c7daf5ba01bfb2a3546393ed9b3cc6b37fce4098\`

Earlier versions v0.7 and v0.8 remain unchanged. Their review handoffs remain separate artifacts.

The accepted predecessor artifacts remain:
- **Rev 1.4 Amendment E:** commit \`b8b8af042c16eeb9e02077c781ab05c582eeb65d\`, blob \`3728146356a74363a94fe75a87fd06c483954ee2\`.
- **Rev 1.4 Amendment E acceptance record:** commit \`ca15a29bd25c4c9c2293394f67cb19e1a18f34bd\`, blob \`074b40980eb96d164cd8411c8995bb1db4af0d46\`.
- **B1 v1.7:** commit \`c3abe107acd2a3f8be58bf933eafcd734823a129\`, blob \`8c666e501a31726c728447d155045c0b20adc178\`.
- **B1 v1.7 acceptance record:** commit \`ac06c6676982eed795db9cb04c6d91803b591ac7\`, blob \`ea51d72f4f85c5d832d72add561b4c93472c364a\`.

Rev 1.4 Amendment E is accepted for the symbolic B1/M1 feasibility specification. B1 v1.7 is accepted and frozen as a symbolic analysis plan. Neither acceptance is an execution GO.

## 2. Review history and adjudication of v0.9

Claude's v0.9 review identified:
- R1, blocking: wall-time/memory limits made static-analysis admissibility potentially hardware-dependent;
- R2: transitive connected-component grouping could chain dissimilar implementations;
- R3: renamed local identifiers might evade source-similarity grouping, while independent implementations of the same algorithm might be over-grouped;
- R4: candidates below the review threshold could be treated as separate without a blinded disposition;
- R5: the calibration reference set had no minimum-composition or label-quality rule;
- R6: distinct runnable artifacts did not imply different behaviour;
- R7–R10: accepted the float-parameter precedence, static-frequency limitation, discrete \(C_D\) grid, and rank-increment gate;
- R11: current-document self-references still named v0.8.

v0.10 attempts to resolve these findings. Please independently challenge every change. Do not treat GPT's adjudication or the v0.10 change history as authority.

## 3. R1: deterministic resource budgets

Sections 4.1.1b and 4.1.5(B) replace semantic wall-time/memory caps with deterministic work counters:
- included semantic nodes and retained edges;
- worklist removals;
- abstract transfer-function applications;
- lattice joins, widening and narrowing;
- alias/points-to query operations.

The worklist order and tie-breaking must be deterministic. Counter definitions and caps enter the Stage 2 profile digest. Wall-clock time, peak memory and machine-load measurements are recorded as operational metadata only. Incomplete closure after an OS/container/hardware interruption is UNRESOLVED / OPERATIONAL INTERRUPTION, not a semantic rejection or partial-slice match.

Review questions:
1. Are all listed counters deterministic and implementation-independent enough to reproduce the same cap disposition?
2. Are the counting points and counter definitions sufficiently specified, or do abstract domains/tools make these totals implementation-dependent?
3. Should the design require serial execution rather than merely saying parallel scheduling must not alter totals/state?
4. Does the pinned environment manifest adequately cover container/image, OS/runtime, architecture, tool binaries and deterministic scheduling?
5. Can an operational interruption still create machine-dependent candidate availability despite not changing semantic pass/fail? Is the retry rule adequate?
6. Are the deterministic caps correctly included in the profile digest and kept separate from semantic context labels?

## 4. R2–R4: lineage clustering, similarity, and pairwise independence

Section 2.3 now defines:
- exact mirrors/copies as one lineage;
- documented solver-specific derivation separately from common frameworks/libraries/standard algorithms;
- raw-symbol and local-alpha-normalized AST-subtree multiset Jaccard views;
- reference-set calibration and validation;
- similarity thresholds as review-priority signals only, not proof of lineage or independence;
- two blinded reviewers for every pair proposed to count as separate parent groups, with third-reviewer adjudication;
- pairwise-coherent clusters, complete disposition matrices and cluster-diameter records;
- one selected pinned source representative per finalized lineage cluster, from which all variants assigned to that parent must derive.

Review questions:

### R2: cluster chaining and diameter
1. Does the rule actually prevent A–B–C similarity chaining from concealing an A–C independent-implementation disposition?
2. Is the pairwise-coherence rule transitive and operationally implementable?
3. Does treating an unresolved connected candidate component as at most one parent group avoid false independence without making a disputed component appear to be one verified implementation?
4. Is the minimum pairwise similarity correctly called the cluster diameter for each similarity view? Should a singleton have an explicit NA convention?
5. Is the cluster-level adjudication and split rule clear enough to resolve conflicting pairwise labels?

### R3: renamed copies and hard negatives
6. Is the local-alpha view adequate for detecting renamed local-variable copies?
7. Are the exceptions for observable names, macros, reflection/stringification, annotations, and unresolved binding adequate?
8. Can local-alpha similarity falsely group independently written implementations of a common algorithm? Are the hard-negative categories sufficient?
9. Should similarity be calculated at multiple AST-subtree depths or include additional source/structural features?
10. Is the lineage-only alpha-normalization cleanly separated from semantic site-equivalence normalization in §4.1.1a?

### R4: pairwise disposition
11. Does the requirement for two reviewers cover every pair that could otherwise be counted as separate parents, including low-similarity pairs?
12. Is the distinction between SAME_IMPLEMENTATION_LINEAGE, INDEPENDENT_IMPLEMENTATIONS, and UNRESOLVED sufficiently objective?
13. Is third-reviewer adjudication adequate, and what happens if disagreement remains?
14. Can any repository name, low similarity score, or common author label still establish independence without implementation-history evidence?

## 5. R5: reference-set composition, sample size and label quality

Section 2.3.4 now requires positive lineage pairs, hard-negative pairs, provenance-based labels, two blinded reviewers, third-reviewer adjudication, and disjoint calibration/validation splits by implementation identity/lineage.

The number of independent examples per category is determined from a predeclared confidence-interval precision target for false-group and missed-lineage rates. If category coverage or precision is inadequate, thresholds are descriptive/triage-only.

Review questions:
1. Are the positive and hard-negative categories complete for the intended language/task family?
2. Are labels genuinely independent of similarity scores?
3. Does splitting calibration and validation by implementation identity prevent pair-level leakage?
4. Is the confidence-interval precision target a sufficient minimum-sample rule, or should a minimum category count also be specified?
5. Are the false-group and missed-lineage rates the correct performance quantities for the proposed triage role?
6. Could a reference set have high pair counts but too few independent implementations, making nominal precision misleading?
7. Is it correct that similarity remains triage-only if the reference-set gate is not met, while mandatory pairwise human review remains in force?

## 6. R6: observed-output and correctness concordance

New §6.6 states that distinct source/runnable-artifact digests do not establish different behaviour or different correctness outcomes. It adds a descriptive concordance audit for:
- identical diagnostic failure/unresolved vectors;
- identical correctness vectors;
- identical canonicalized observable output/process-disposition vectors;
- same correctness but different outputs and vice versa;
- unavailable/censored/withheld records.

The audit cannot affect parent/variant selection, M1-si, B1 eligibility or admissibility; finite-set agreement is not universal equivalence.

Review questions:
1. Does the audit compare enough observable output detail to detect exact replicas without leaking protected records?
2. Is the distinction among failure-vector identity, correctness-vector identity and observable-output identity correct?
3. Is the audit adequately protected from becoming an outcome-informed selection or exclusion rule?
4. Should the audit report diagnostic and protected evaluation concordance separately?
5. Does the custodian-only aggregate disclosure rule preserve the intended descriptive evidence without revealing record-level protected outcomes?

## 7. Accepted and retained findings

Please verify the earlier accepted corrections remain sound in v0.10:

- **F1 / R7:** floating-point parameter levels are admitted only where the frozen model resolves their semantics; otherwise excluded before Stage 2 and enumeration.
- **F4 / R8:** static context equality does not imply equal runtime loop trip counts or execution frequency.
- **F6 / R9:** for fixed \(k\) and eight integer-count strata, \(C_D=m/k\), distinct values differ by at least \(1/k\), and at \(k=2\) only \(1/2\) and \(1\) are possible before capacity restrictions.
- **R10:** the rank-increment requirement precedes fitting; regularization, intervals and duplicated rows cannot substitute for design identifiability.
- One mutation invocation per variant remains a new population-design restriction, not a requirement inherited from B1 v1.7 or Rev 1.4.
- The Option B exact-cell target and N5 proxy-pathway interpretation remain unchanged.

## 8. Complete-specification review required

The v0.9 review did not cover every line of the specification. Please read the complete v0.10 text, including all portions not listed above.

In particular, recheck:
1. §§0–1: claim scope, historical provenance, current-version labels and parent-population meaning;
2. §§2.1–2.5: parent eligibility, source identity, full lineage procedure and parent-count justification;
3. §§3.1–3.6: exact B1 cells, LOPO, M1-si, discrete \(C_D\), distinct source/artifact identities and pre-fit rank;
4. §§4.1.1a–4.1.1c: canonicalization, source identity, abstract domains, profile freeze, predicate/effect catalog;
5. §§4.1.2–4.1.6 and §4.2–4.3: conformance, diagnostic-blind review, one invocation, float and external-call precedence, target-centred context slices, deterministic work limits and frozen inventory;
6. §§5.1–5.7: new protected set, custody, non-leakage, outcome-side variation, Option B and N5;
7. §§6.1–6.6: lower bounds, incidence, no power claim, shortfall and descriptive concordance audit;
8. §§7–9: compatibility with accepted B1, outstanding governance decisions, and the complete non-authorization boundary.

Check all cross-references, current-version self-references, and subsection numbers. The history subsection IDs should each occur once.

## 9. Historical GLM audit context

The independent GLM audit of the historical repository at master commit \`33dca9b61d95b9fb750f750919c32c2e08b2ee90\` reported:
- \(C=5/k\) on all 1,200 eligible v0.2 confirmatory rows;
- 40 base bodies copied three times, with identical outcomes within all 400 replica groups;
- no identifying equal-\(k\), different-\(C\) contrast on that support;
- ridge sensitivity under predictor aliasing;
- a frozen-versus-executed seed-rule deviation and separate generator/RLC-0 provenance issues.

v0.10 imports only the design implications: lineage integrity, distinct source/runnable identity, actual within-cell \(C_D\) variation, rank-increment checks, and descriptive output concordance. It does not import historical seed/generator/RLC-0 corrections into the new population design.

The audit report and index were supplied in prior discussion, but the complete revised scripts/raw-output ZIP was not supplied as an inspectable runnable bundle here. Do not claim independent reproduction of GLM's audit unless those exact artifacts are actually received and run.

## 10. Required deliverable

Return a complete review table with:
- finding ID;
- severity: blocking, recommended, accepted, or contradicted;
- exact v0.10 section;
- technical reason;
- required correction, if any;
- whether it blocks design freeze.

Distinguish corrections that genuinely resolve a prior issue from issues that remain unresolved. Do not mark a finding accepted just because it appears in the change summary.

## 11. Boundary

This is a read-only review. Do not edit the repository, generate sources/variants, allocate mutations, access banks or protected data, run diagnostics, fit models, simulate, or perform any execution.

v0.10 remains an **UNREVIEWED DESIGN-ONLY DRAFT**. GPT will adjudicate the complete review. Any substantive correction after this review must be a new version. No part of this handoff or v0.10 is an execution authorization.
