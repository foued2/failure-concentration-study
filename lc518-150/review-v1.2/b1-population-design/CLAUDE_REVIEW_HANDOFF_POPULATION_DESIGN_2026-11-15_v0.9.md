# Claude Review Handoff: LC518 Population and Experimental Design v0.9

**Date:** 2026-11-15  
**Status:** READ-ONLY INDEPENDENT REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** \`gpt/b1-computational-plan-2026-11-14\`

## 1. Exact review target

Please review the complete v0.9 specification, not only this handoff:

- **Path:** \`lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.9.md\`
- **Branch:** \`gpt/b1-computational-plan-2026-11-14\`
- **Git blob SHA-1 at handoff preparation:** \`c7daf5ba01bfb2a3546393ed9b3cc6b37fce4098\`
- **Dimensions:** 1,026 lines; final newline present.

The immediate predecessor v0.8 remains unchanged:
- **Path:** \`lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.8.md\`
- **Blob:** \`8e2ddd2cf4316c1cd68d60edd2dd6c167af29825\`

The v0.8 review handoff remains a separate read-only artifact. v0.7 and its handoff also remain unchanged.

The accepted predecessor artifacts remain:
- **Rev 1.4 Amendment E:** commit \`b8b8af042c16eeb9e02077c781ab05c582eeb65d\`, blob \`3728146356a74363a94fe75a87fd06c483954ee2\`.
- **Rev 1.4 Amendment E acceptance record:** commit \`ca15a29bd25c4c9c2293394f67cb19e1a18f34bd\`, blob \`074b40980eb96d164cd8411c8995bb1db4af0d46\`.
- **B1 v1.7:** commit \`c3abe107acd2a3f8be58bf933eafcd734823a129\`, blob \`8c666e501a31726c728447d155045c0b20adc178\`.
- **B1 v1.7 acceptance record:** commit \`ac06c6676982eed795db9cb04c6d91803b591ac7\`, blob \`ea51d72f4f85c5d832d72add561b4c93472c364a\`.

Rev 1.4 Amendment E is accepted for the symbolic B1/M1 feasibility specification. B1 v1.7 is accepted and frozen as a symbolic analysis plan. Neither acceptance is an execution GO.

## 2. Review history and v0.9 changes

Claude's v0.8 review identified two blockers and four recommendations:

- F1: conflict between the floating-point fail-closed rule and general parameter-level permission;
- F2: underspecified parent-lineage grouping;
- F3: no resource cap for target-centred dependency closure;
- F4: static context equivalence did not imply equal runtime execution frequency;
- F5: "distinct source artifacts" was undefined;
- F6: discrete \(C_D\) granularity was not explicit;
- F7 and F8: the Operator Contract Gate and one-invocation restriction were accepted;
- F9: duplicate subsection numbering, a repeated sentence, and D/E subsection ordering.

v0.9 attempts to resolve F1–F6 and the confirmed editorial defects. Please independently challenge the corrections rather than treating GPT's adjudication as authoritative.

### F1: floating-point parameter precedence

The parameter-setting rule in §4.1.5(C) now explicitly subordinates parameter admission to the frozen operator catalog and floating-point model. A float-sensitive parameter level that cannot be analysed soundly must be excluded at the Operator Contract Gate, before Stage 2 and site enumeration.

Please check for any remaining path by which the general parameter-variation language could override that exclusion.

### F2: operational lineage grouping

Sections 2.1–2.4 now define the parent-counting unit as an implementation-lineage cluster, not a repository or archive. The grouping procedure includes:

- exact source copies, mirrors and repackagings;
- documented direct forks, ports and derivatives;
- a same-language canonical AST-subtree multiset Jaccard comparison;
- per-language grouping/review thresholds calibrated on an independent labelled reference set and frozen before the study candidate frame is scored;
- blinded two-reviewer disposition for intermediate-similarity and derived pairs;
- connected-component lineage clusters, each counted at most once in \(G_c\).

Please challenge whether this procedure is scientifically adequate and operationally reproducible. In particular:

1. Is canonical AST-subtree multiset Jaccard an adequate near-identity measure, or can it both over-group independently developed solvers and under-group copied derivatives?
2. Is the external calibration-set requirement sufficient? What minimum composition and labelling quality should it have?
3. Are the threshold definitions and boundary cases unambiguous?
4. Does connected-component grouping create unacceptable chaining, where A is similar to B and B to C even though A and C are materially different?
5. Is the rule for common upstream frameworks correctly distinguished from direct solver-code inheritance?
6. Is the conservative treatment of unresolved cross-language ports and lineage pairs correct?
7. Is the fact that numeric thresholds are to be frozen before study-candidate scoring sufficient, or must more be fixed at the current design-specification stage?

The aim is not to maximize the number of parent groups. Ambiguous copies must not be split merely to obtain \(G_c\ge3\).

### F3: context-slice resource budget

Sections 4.1.1b and 4.1.5(B) now require Stage 2 to pin node, edge, worklist/expansion, time and memory caps before enumeration. A cap hit means UNRESOLVED. Partial slices cannot be compared as complete contexts, and the cap cannot be raised for a preferred candidate.

Please check whether these budgets can be set without candidate-driven tuning, whether any relevant resource limit is missing, and whether the rule accidentally makes a resource cap part of the semantic equivalence definition.

### F4: runtime frequency limitation

Sections 1.2 and 4.1.5(D) now state that static context equality does not imply equal loop trip counts, invocation frequency or hot-path exposure. These are not dynamically measured or matched.

Please assess whether the limitation is clear enough for the stated predictive claim and whether any part of the target-centred slice still implies a stronger frequency match.

### F5: source and runnable-artifact distinctness

Sections 3.4 and 4.1.4 now require each M1-si version to carry:

- a raw source-tree digest;
- a canonical semantic-source digest over solver-relevant build-input source;
- a reproducible runnable-artifact digest;
- a build/package manifest and dependency/runtime identity.

A pair contributes distinct variants only when both its semantic-source digest and runnable-artifact digest differ, as well as its predeclared \(\mathbf a\) setting and realized \(C_D\). Source-different pairs that produce the same runnable artifact are recorded but do not count as separate runnable variants. Source-identical pairs producing different runnable artifacts under the same frozen build profile are unresolved as a reproducibility or uncontrolled-input defect.

Please challenge:
1. whether the runnable-artifact definition works for compiled and interpreted solvers;
2. whether metadata normalization can accidentally erase executable distinctions;
3. whether the two-digest distinctness requirement is too strict or still too permissive;
4. how deterministic builds and runtime/dependency identity must be pinned;
5. whether duplicate aliases can still enter \(\mathcal V_{g,c}\), \(\mathcal A_{g,c}\), or the parent count;
6. whether identical runnable artifacts must always be treated as one variant for this M1-si purpose.

### F6: discrete \(C_D\) granularity

Section 3.2 records that with eight strata and integer failure counts, for fixed \(k\), \(C_D=m/k\), where \(m\) is an integer and \(m\ge\lceil k/8\rceil\). Distinct values differ by at least \(1/k\); at \(k=2\), the only mathematical possibilities are \(1/2\) and \(1\), before stratum-capacity restrictions.

Please verify the arithmetic and whether the distinction between the theoretical grid and the actually attainable subset is accurately stated.

## 3. Historical GLM audit implications

The independent GLM audit of the historical repository at master commit \`33dca9b61d95b9fb750f750919c32c2e08b2ee90\` reported:

- \(C=5/k\) on all 1,200 eligible v0.2 confirmatory rows;
- 40 base bodies copied three times, with identical outcomes within all 400 replica groups;
- no identifying equal-\(k\), different-\(C\) contrast on that support;
- a ridge-sensitive residual model contrast on an aliased design;
- a frozen-versus-executed seed-rule discrepancy and separate generator/RLC-0 provenance issues.

v0.9 imports only the implications relevant to the new population specification: lineage-level parent counting, distinct semantic/runnable variant identity, actual within-cell concentration variation, and a pre-fit rank-increment/identifiability gate.

It does **not** import the old seed formula, generator corrections or RLC-0 C2 manifest repair into the population specification. Those remain historical-record issues.

The audit report and evidence index were supplied, but the full revised ZIP, scripts and raw outputs were not supplied as a runnable bundle in this review context. Do not claim that you executed or independently reproduced the GLM audit unless you actually receive and run those artifacts.

Please check whether the v0.9 safeguards really prevent the design from repeating the old pseudoreplication and aliasing failures.

## 4. Complete review of the remaining specification

Claude's v0.8 fetch was incomplete at §5.1. This review must cover the complete v0.9 file, including §§5.2–5.7, §6, §7, §8 and §9.

In particular:

1. **§5.6 outcome-side variation:** confirm the reporting audit is descriptive only and cannot be used to select variants or define admissibility.
2. **§5.7 Option B:** verify that the exact-cell predictive target remains distinct from a direct or parameter-independent concentration effect.
3. **N5:** verify that it remains a proxy-pathway operating-characteristic scenario, not Type-I error calibration for the broad B1 permutation null.
4. **§6:** verify that the count minima remain support bounds, not sample-size or power claims, and that no old 90/150 architecture has reappeared.
5. **§7:** verify compatibility with accepted B1 v1.7 and Rev 1.4 Amendment E, including the requirement for a separate B1 amendment for a new protected evaluation set.
6. **§8:** check all open decisions and whether any new issue identified in this review is missing.
7. **§9:** verify the complete non-authorization boundary remains intact.

## 5. Additional technical checks

Please also review:

1. Whether the rank-increment requirement in §3.6 is appropriately specified before fitting, and whether the required baseline-column projection and scaling/parameterization checks are sufficient to stop ridge regularization or a narrow interval from being mistaken for identification.
2. Whether the full-parent lineage cluster, unique runnable-variant identity and unique record/variant incidence are consistently used in every support count.
3. Whether the discrete \(C_D\) grid interacts with the M1-si requirement in a way that needs a further feasibility warning or mathematical bound.
4. Whether all version references, section headings and cross-references are internally consistent. v0.9 renumbers the duplicated v0.8 history headings as §0.8, §0.9, §0.10 and §0.11; confirm there is now one of each.
5. Whether §4.1.5(D) before §4.1.5(E) is the appropriate sequence and no cross-reference was broken.

## 6. Required review deliverable

Return a complete review table with:

- finding ID;
- severity: blocking, recommended, accepted, or contradicted;
- exact v0.9 section;
- technical reason;
- required correction, if any;
- whether it blocks design freeze.

Distinguish findings actually fixed from residual concerns. Do not mark a point accepted merely because it appears in the change summary.

## 7. Boundary

This is a read-only review. Do not edit the repository, generate sources/variants, allocate mutations, access banks or protected data, run diagnostics, fit models, simulate, or perform any execution.

v0.9 remains an **UNREVIEWED DESIGN-ONLY DRAFT**. GPT will adjudicate the full review. Any substantive correction after this review must be a new version. No part of this handoff or v0.9 is an execution authorization.
