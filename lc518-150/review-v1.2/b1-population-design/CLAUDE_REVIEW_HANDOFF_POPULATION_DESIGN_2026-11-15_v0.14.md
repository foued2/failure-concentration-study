# Claude Review Handoff: LC518 Population and Experimental Design v0.14

**Date:** 2026-11-15  
**Status:** READ-ONLY INDEPENDENT REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** gpt/b1-computational-plan-2026-11-14

## 1. Exact review target

Please review the complete v0.14 specification, not only the changes:

- **Path:** lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.14.md
- **Branch:** gpt/b1-computational-plan-2026-11-14
- **Git blob SHA-1:** 5d91df2ebf84da28ab559630883702b1ecf44a01
- **Content-changing commit:** 4c40f30c91591a49869d051b6ac33334d3046c18
- **Dimensions:** 1134 lines; final newline present.

The immediate predecessor v0.13 remains unchanged:
- **Path:** lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.13.md
- **Blob:** b15c44549abaea52dc35941fd8f8e181e8f82684
- **Content-changing commit:** 90945225b2285b38a93c2e6e618917b9b79f74a7

The v0.12 predecessor remains unchanged with blob 3fd56b8799722a7d534065955106071e8122d21f. Accepted predecessor artifacts remain unchanged:
- **Rev 1.4 Amendment E:** blob 3728146356a74363a94fe75a87fd06c483954ee2.
- **Rev 1.4 Amendment E acceptance record:** blob 074b40980eb96d164cd8411c8995bb1db4af0d46.
- **B1 v1.7:** blob 8c666e501a31726c728447d155045c0b20adc178.
- **B1 v1.7 acceptance record:** blob ea51d72f4f85c5d832d72add561b4c93472c364a.

Neither accepted predecessor is an execution GO.

## 2. Review history

Claude's targeted v0.12 review marked X1–X6 accepted and X7 blocking. GPT then inspected all of §§0–9 of v0.12, including the portions Claude had not read. GPT accepted X7 and published v0.13 with a bounded, uniform retry/reproducibility rule. A subsequent audit identified that an attempt ceiling of two could not accommodate one interrupted attempt plus the two required complete executions; v0.14 sets the minimum to three. It also replaces future-tense self-publication wording with a timeless repository-provenance statement.

Do not treat GPT's adjudication or this handoff as authority. Inspect the exact v0.14 text and independently assess whether the new protocol is logically sound, operationally implementable and consistent with the earlier deterministic-counter decisions.

The v0.14 specification remains an **UNREVIEWED DESIGN-ONLY DRAFT**. This is a read-only request. Do not modify the repository, generate sources or variants, allocate mutations, access diagnostic or protected banks, execute solvers, fit models, simulate, or perform scientific analysis.

## 3. Primary correction: bounded uniform repeated execution

Section 4.1.1b now defines:
- a maximum total attempt count (A_{\max}\), fixed in the Stage 2 profile before candidate enumeration;
- a minimum (A_{\max}\ge3\), allowing one interrupted attempt plus two complete attempts;
- the same attempt protocol for every syntactically enumerated candidate site in the parent/operator inventory;
- a fresh analysis process for each attempt, from the same immutable source, profile, input manifest and exact execution-environment manifest;
- acceptance only after two independently initiated complete attempts produce byte-identical canonical semantic-result envelopes;
- full attempt logging;
- **UNRESOLVED / NONDETERMINISTIC ANALYSIS OUTPUT** when two complete result envelopes differ;
- **UNRESOLVED / OPERATIONAL INTERRUPTION** if two complete attempts are not obtained within (A_{\max}\);
- no retry after deterministic work-cap exhaustion or a semantic/analysis error under the same profile;
- no attempt-budget reset, selective retry, majority vote or preferred-result selection;
- full reviewed profile change and complete re-enumeration if software profile or execution environment changes.

The canonical semantic-result envelope includes complete context/signature bytes, semantic classification and deterministic counter totals/cap disposition. Operational-only fields such as wall time, memory, machine load and timestamps are excluded.

Review questions:
1. Is requiring two complete, independent runs for every candidate, including candidates later rejected or unselected, the right way to prevent selective retry?
2. Is the distinction between a complete result, deterministic work-cap exhaustion, semantic/analysis error, operational interruption and nondeterministic completed output sufficient?
3. Does (A_{\max}\ge3\) follow as the minimum necessary to permit one operational interruption and two complete verifications? Is the actual profile-level value appropriately left to a predeclared operational rationale?
4. Is the exact execution-environment manifest sufficiently pinned, including any hardware/runtime property that can affect semantic output?
5. Does requiring identical canonical result envelopes, including counter totals and semantic status, provide a meaningful reproducibility check without comparing operational-only fields?
6. Does the rule prevent a candidate from receiving extra attempts because it is favoured or needed for support?
7. Does it avoid changing semantic classification based on resource interruptions, while honestly leaving a candidate unresolved if the frozen attempt budget is exhausted?
8. Is the new disposition in §4.1.5(B) consistent with §4.1.1b and the attempt policy recorded in §4.1.6?

## 4. Calibration-rate clarification

Section 2.3.4 now defines the lower-threshold false-group triage-flag rate as the proportion of independent hard-negative units at or above the lower review-priority threshold, and the missed-lineage triage rate as the proportion of positive SAME_IMPLEMENTATION_LINEAGE units below that threshold. The high-threshold priority-flag rate is reported separately. These are triage rates, not actual grouping errors; similarity scores do not assign lineage labels or replace mandatory pairwise reviewer dispositions.

Review the denominators, units, and consistency with the threshold roles in §2.3.5. Verify that the rates and confidence-interval precision targets are well-defined for each language family, view, and applicable category, without permitting pair-row pseudoreplication.

## 5. Earlier findings retained

Confirm that the following v0.12 corrections remain intact:
- November 6 allocation existence/contents remain unproven; allocation is not established; no recovery or reconstruction is asserted.
- Every within-cluster pair requires its own direct disposition or exact identity/mirror evidence; transitive closure alone cannot finalize a cluster.
- Unresolved candidate components contribute zero to verified (G_c) and cannot supply selected parents.
- Calibration/validation use independent lineage units, disjoint by implementation identity/lineage, with predeclared category floors and confidence-interval precision targets.
- Semantic context analysis is serial and single-worker; counters are reproducible relative to the pinned implementation/profile, not portable across profiles.
- Option B, the realization-proxy limitation, N5 classification, M1-si status as a new design choice, discrete (C_D) arithmetic, pre-fit rank increment and all shortfall protections remain unchanged.
- Protected custodian, joint-consent, trigger-(i), isolation, new B1 amendment and separate execution GO remain open.

## 6. Full v0.14 review required

Please read every section of v0.14, including text unchanged from earlier versions:

1. **§§0–1:** claim scope, provenance, current version and authorization boundaries.
2. **§§2.1–2.5:** parent eligibility, calibration units/rates/floors, direct pairwise lineage clusters, unresolved parents, representative selection and operating parent-count justification.
3. **§§3.1–3.6:** exact B1 cells, full-population and LOPO support, M1-si, distinct runnable artifacts, discrete (C_D), historical authority and pre-fit rank.
4. **§§4.1.1–4.1.6, 4.2–4.3:** operator identity, canonicalization, Stage 1/Stage 2 sequencing, deterministic counters, uniform attempt protocol, predicate/effect catalog, diagnostic-blind review, one invocation per variant, floating-point/external-call rules, context slices and inventory.
5. **§§5.1–5.7:** protected evaluation set, exposed-data separation, independent custodian, leakage, B1 amendment, outcome-side reporting and Option B/N5.
6. **§§6.1–6.6:** lower bounds, incidence feasibility, no-power boundary, shortfall and descriptive concordance audit.
7. **§§7–9:** B1/computational compatibility, open governance gates and explicit non-authorization.

Check all cross-references, current-version self-references, numbering and predecessor identities. Confirm v0.13, v0.12 and all accepted predecessor artifacts remain unchanged.

## 7. Required deliverable

Return a review table with:
- finding ID;
- severity: blocking, recommended, accepted or contradicted;
- exact v0.14 section;
- technical reason;
- required correction, if any;
- whether it blocks design freeze.

State explicitly which sections were read in full and which remain unread. Do not give a whole-document verdict if any section remains unread.

## 8. Boundary

This is a read-only review. v0.14 does not authorize solver-source acquisition, parent selection, mutation allocation, mutation/source generation, compilation, execution, diagnostic probing, bank access, protected-set access, model fitting, sampling, simulation or scientific analysis.

Passing review would concern only the population/design specification. Separate statistical, computational, consent/provenance, custodian, isolation, data-access and execution gates remain in force. GPT will adjudicate the complete review. Any substantive correction after v0.14 must be a new version with its own identity and review.
