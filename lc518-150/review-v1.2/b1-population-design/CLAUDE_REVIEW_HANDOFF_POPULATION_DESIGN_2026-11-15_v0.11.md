# Claude Review Handoff: LC518 Population and Experimental Design v0.11

**Date:** 2026-11-15  
**Status:** READ-ONLY INDEPENDENT REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** gpt/b1-computational-plan-2026-11-14

## 1. Exact review target

Please review the complete v0.11 specification, not only the changed paragraphs:

- **Path:** lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.11.md
- **Branch:** gpt/b1-computational-plan-2026-11-14
- **Git blob SHA-1:** 00f683f4bed5559399a81cee03de84772e3c9ab8
- **Content-changing commit:** 9ac9fb15581b2772748871e4c3ca53f717b8acab
- **Dimensions:** 1095 lines; final newline present.

The immediate predecessor v0.10 remains unchanged:
- **Path:** lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.10.md
- **Blob:** fd263e787062ac9377719d58d9d547d162c96683

The v0.9 predecessor remains unchanged with blob c7daf5ba01bfb2a3546393ed9b3cc6b37fce4098. The accepted predecessor artifacts also remain unchanged:
- **Rev 1.4 Amendment E:** blob 3728146356a74363a94fe75a87fd06c483954ee2.
- **Rev 1.4 Amendment E acceptance record:** blob 074b40980eb96d164cd8411c8995bb1db4af0d46.
- **B1 v1.7:** blob 8c666e501a31726c728447d155045c0b20adc178.
- **B1 v1.7 acceptance record:** blob ea51d72f4f85c5d832d72add561b4c93472c364a.

Neither accepted predecessor is an execution GO.

## 2. Review history and scope

Claude's v0.10 review was explicitly partial. It covered selected lineage, counter, concordance and compatibility sections, but did not read all of §§0–9. GPT subsequently fetched the exact v0.10 blob and reviewed the complete specification. v0.11 implements the specific corrections adjudicated below. Do not treat GPT's adjudication or this summary as authority; inspect the actual text.

The v0.11 document remains an **UNREVIEWED DESIGN-ONLY DRAFT**. This handoff requests read-only review. Do not modify the repository, generate sources or variants, allocate mutations, access diagnostic or protected banks, execute solvers, fit models, simulate, or perform analysis.

## 3. Correction A: November 6 mutation-allocation provenance

v0.10 stated that the November 6 mutation allocation “was not created.” That assertion is withdrawn.

v0.11 now states that the existence and contents of any standalone November 6 mutation-allocation artifact are **unproven** in the available record and that the allocation is **not established** for this design. It does not say the artifact was never privately created, lost, destroyed or recovered. No recovery or reconstruction is undertaken.

Review whether the revised statement accurately distinguishes:
1. no complete allocation artifact established by the available evidence;
2. existence of a standalone artifact not proven either way; and
3. no allocation available as an established design input.

Do not search for or reconstruct a putative allocation.

## 4. Correction B: complete direct pairwise disposition within clusters

Section 2.3.7 now states that every unordered pair of distinct candidates within a proposed/finalized cluster must have its own direct disposition or exact identity/mirror evidence. Transitive SAME_IMPLEMENTATION_LINEAGE paths through an intermediate candidate cannot substitute for a direct A–C determination.

Review questions:
1. Does the text unambiguously require a direct recorded disposition for every within-cluster pair, not merely a complete score matrix?
2. Does a missing or UNRESOLVED pair correctly prevent finalization?
3. Is an INDEPENDENT_IMPLEMENTATIONS disposition handled as a conflict without being hidden by transitive closure?
4. Is the singleton diameter convention (NA, no pairwise comparison) correct?
5. Is the direct within-cluster rule consistent with §2.3.6, which reviews every candidate pair proposed to contribute to separate parent groups?
6. Does the provisional unresolved-component rule avoid falsely treating uncertainty as a verified lineage cluster?

## 5. Correction C: unresolved lineage components and eligible parent counts

v0.11 distinguishes a provisional unresolved candidate component from a verified implementation-lineage cluster. The provisional component can be retained as one conservative grouping solely to prevent false independence, but it:
- is not a verified implementation-lineage cluster;
- contributes zero to eligible G_c; and
- cannot supply a selected parent until resolved.

Review the consistency of this rule across §§2.3, 2.4, 2.5 and 3.1–3.6. In particular, verify that no unresolved component can satisfy the B1 distinct-parent condition or inflate the parent count.

## 6. Correction D: reference-set independent units and category floors

Section 2.3.4 now distinguishes independent lineage units from raw pair rows:
- a positive unit is one documented implementation lineage represented by one predeclared lineage pair;
- a hard-negative unit is one pair of independently developed implementation lineages;
- lineages are not reused across units within a partition unless the predeclared interval method accounts for lineage-level dependence;
- calibration and validation remain disjoint by implementation identity/lineage;
- each applicable positive and hard-negative category must have a numerical minimum independent-unit floor in each partition, declared before reference examples are assembled or scores examined;
- both the floor and the confidence-interval precision target must be met; otherwise thresholds remain descriptive/triage-only.

Review questions:
1. Are the proposed positive and hard-negative statistical units genuinely independent under the described construction?
2. Is the no-reuse rule clear enough, including how a cluster-aware interval method would be documented if units share lineages?
3. Does the floor apply to every applicable subcategory, separately in calibration and validation?
4. Is the floor required to be numerically fixed before examples and scores are observed?
5. Are the false-group and missed-lineage rate estimands and their interval method sufficiently specified for the intended triage-only role?
6. Does this avoid treating a large number of dependent pair rows as a large independent sample?
7. Does the revised rule preserve the principle that similarity scores never establish lineage or independence, and that every pair proposed as separate parents receives human review?

## 7. Correction E: serial deterministic semantic analysis

Sections 4.1.1b and 4.1.5(B) now require serial, single-worker execution for every semantic analysis phase contributing nodes, edges, reachability, abstract state or semantic work counters. Parallel worklist processing, work stealing and nondeterministic reductions are prohibited for these phases. Worker count and scheduler settings enter the profile digest.

The text also clarifies that counter totals are deterministic relative to the pinned analysis implementation and instrumentation, not implementation-independent or directly comparable across different profile digests. Operational resource class, container limits and interruptions remain separate from semantic caps; interrupted work is UNRESOLVED / OPERATIONAL INTERRUPTION.

Review questions:
1. Is the serial single-worker requirement explicit and enforceable across the analysis phases that affect signatures and counters?
2. Are the exact work counters and their instrumentation/counting points adequately pinned?
3. Is the limitation on cross-profile counter comparability correct and sufficiently clear?
4. Does the execution-resource-class retry rule avoid machine-dependent semantic classifications without turning operational resources into semantic gates?
5. Is the distinction between deterministic work-cap exhaustion and operational interruption preserved throughout §§4.1.1b, 4.1.5(B) and 4.1.6?

## 8. Full v0.11 review required

Please read every section of v0.11, including all text not changed from v0.10. In particular, recheck:

1. **§§0–1:** provenance language, authorization boundaries, accepted predecessor identities, target population, claim scope, Option B and statistic conventions.
2. **§§2.1–2.5:** parent definition and eligibility, full lineage procedure, category calibration, direct pairwise cluster coherence, unresolved-parent treatment, representative selection and operating parent-count justification.
3. **§§3.1–3.6:** exact B1 cells, full-population support, LOPO folds, discrete C_D, M1-si as an additional design requirement, historical M1 authority and pre-fit rank.
4. **§§4.1.1–4.1.6, 4.2–4.3:** operator-class identity, canonicalization, Stage 1/Stage 2 profile sequencing, predicate/effect catalog, serial deterministic work budgets, diagnostic-blind review, one invocation per variant, floating-point and external-call requirements, target-centred context slices, and complete candidate inventory.
5. **§§5.1–5.7:** new protected evaluation set, exposed-data separation, independent custodian, no leakage, B1 amendment, outcome-side reporting and Option B/N5 proxy interpretation.
6. **§§6.1–6.6:** structural lower bounds, non-power boundary, incidence feasibility, shortfall rules and descriptive concordance audit.
7. **§§7–9:** compatibility with accepted B1 and computational plans, all outstanding governance gates, and complete non-authorization wording.

Check all cross-references, current-version self-references, numbering and predecessor references. Confirm v0.10 and all earlier accepted artifacts remain unchanged.

## 9. Required deliverable

Return a review table with:
- finding ID;
- severity: blocking, recommended, accepted or contradicted;
- exact v0.11 section;
- technical reason;
- required correction, if any;
- whether it blocks design freeze.

Distinguish genuine resolutions from remaining defects. State explicitly which sections you read in full and which, if any, remain unread. Do not give a whole-document verdict if any section remains unread.

## 10. Boundary

This is a read-only review. v0.11 does not authorize solver-source acquisition, parent selection, mutation allocation, mutation/source generation, compilation, execution, diagnostic probing, bank access, protected-set access, model fitting, sampling, simulation or scientific analysis.

Passing this review would concern only the population/design specification. Separate statistical, computational, consent/provenance, custodian, isolation, data-access and execution gates remain in force. GPT will adjudicate the complete review. Any substantive correction after v0.11 must be a new version with its own identity and review.
