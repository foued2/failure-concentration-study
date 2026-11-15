# Claude Review Handoff: LC518 Population and Experimental Design v0.12

**Date:** 2026-11-15  
**Status:** READ-ONLY INDEPENDENT REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** gpt/b1-computational-plan-2026-11-14

## 1. Exact review target

Please review the complete v0.12 specification, not only the changed paragraphs:

- **Path:** lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.12.md
- **Branch:** gpt/b1-computational-plan-2026-11-14
- **Git blob SHA-1:** 3fd56b8799722a7d534065955106071e8122d21f
- **Content-changing commit:** 4bd377f1b939133b8edcd4276fbbd05821faecc3
- **Dimensions:** 1,101 lines; final newline present.

The immediate predecessor v0.11 remains unchanged:
- **Path:** lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.11.md
- **Blob:** 00f683f4bed5559399a81cee03de84772e3c9ab8
- **Content-changing commit:** 9ac9fb15581b2772748871e4c3ca53f717b8acab

The v0.10 predecessor remains unchanged with blob fd263e787062ac9377719d58d9d547d162c96683. Accepted predecessor artifacts remain unchanged:
- **Rev 1.4 Amendment E:** blob 3728146356a74363a94fe75a87fd06c483954ee2.
- **Rev 1.4 Amendment E acceptance record:** blob 074b40980eb96d164cd8411c8995bb1db4af0d46.
- **B1 v1.7:** blob 8c666e501a31726c728447d155045c0b20adc178.
- **B1 v1.7 acceptance record:** blob ea51d72f4f85c5d832d72add561b4c93472c364a.

Neither accepted predecessor is an execution GO.

## 2. Version history and review boundary

Claude's v0.10 review was partial. GPT subsequently fetched and reviewed the complete v0.10 specification, adjudicated the findings, and published v0.11. A final consistency scan then identified stale active self-references and a sentence that still described v0.11's publication identity as pending. v0.12 corrects those editorial/provenance defects before this review.

v0.12 does not change the scientific estimand, population rules, lineage rules, statistical conditions, operational requirements or authorization boundaries introduced in v0.11. v0.11 remains preserved unchanged as its predecessor. Do not treat GPT's adjudication, this summary or the change history as authority; inspect the actual v0.12 text.

The v0.12 document remains an **UNREVIEWED DESIGN-ONLY DRAFT**. This is a read-only review request. Do not modify the repository, generate sources or variants, allocate mutations, access diagnostic or protected banks, execute solvers, fit models, simulate, or perform scientific analysis.

## 3. Correction A: November 6 mutation-allocation provenance

The v0.10 statement that the November 6 mutation allocation “was not created” was withdrawn in v0.11.

v0.12 retains the evidence-bounded statement: the existence and contents of any standalone November 6 mutation-allocation artifact are **unproven** in the available record; the allocation is **not established** for this design. This does not assert that an artifact was never privately created, lost, destroyed or recovered. No recovery or reconstruction is undertaken.

Review whether the wording accurately distinguishes an unestablished allocation from proof that no private artifact ever existed. Do not search for or reconstruct a putative allocation.

## 4. Correction B: complete direct pairwise disposition within clusters

Section 2.3.7 requires every unordered pair of distinct candidates within a proposed/finalized cluster to have its own direct disposition or exact identity/mirror evidence. Transitive SAME_IMPLEMENTATION_LINEAGE paths through an intermediate candidate cannot substitute for a direct pair determination.

Review questions:
1. Does the text unambiguously require a direct recorded disposition for every within-cluster pair, not merely a complete similarity-score matrix?
2. Does a missing or UNRESOLVED pair correctly prevent finalization?
3. Is an INDEPENDENT_IMPLEMENTATIONS disposition handled as a conflict without being hidden by transitive closure?
4. Is the singleton diameter convention (NA, no pairwise comparison) correct?
5. Is the direct within-cluster rule consistent with §2.3.6, which reviews every candidate pair proposed to contribute to separate parent groups?

## 5. Correction C: unresolved lineage components and eligible parent counts

An unresolved component may be retained as one provisional grouping solely to prevent false independence. It is not a verified implementation-lineage cluster, contributes zero to eligible G_c, and cannot supply a selected parent until resolved.

Review the consistency of this rule across §§2.3, 2.4, 2.5 and 3.1–3.6. In particular, verify that no unresolved component can satisfy the B1 distinct-parent condition or inflate the parent count.

## 6. Correction D: reference-set independent units and category floors

Section 2.3.4 distinguishes independent lineage units from raw pair rows:
- a positive unit is one documented implementation lineage represented by one predeclared lineage pair;
- a hard-negative unit is one pair of independently developed implementation lineages;
- lineages are not reused across units within a partition unless the predeclared interval method accounts for lineage-level dependence;
- calibration and validation remain disjoint by implementation identity/lineage;
- each applicable positive and hard-negative category requires a numerical minimum independent-unit floor in each partition, declared before examples are assembled or similarity scores examined;
- both the floor and the confidence-interval precision target must be met; otherwise thresholds remain descriptive/triage-only.

Review whether the unit definitions, no-reuse rule, per-category/per-partition floor, precision target and treatment of dependent lineages are statistically coherent. Confirm that a large number of pair rows cannot masquerade as a large independent sample. Verify that similarity scores remain triage-only and never establish lineage or independence.

## 7. Correction E: serial deterministic semantic analysis

Sections 4.1.1b and 4.1.5(B) require serial, single-worker execution for semantic analysis phases contributing nodes, edges, reachability, abstract state or semantic work counters. Parallel worklist processing, work stealing and nondeterministic reductions are prohibited for those phases. Worker count and scheduler settings enter the profile digest.

Counter totals are described as deterministic relative to the pinned analysis implementation and instrumentation, not implementation-independent or directly comparable across different profile digests. Operational resource class, container limits and interruptions remain separate from semantic caps; interrupted work is UNRESOLVED / OPERATIONAL INTERRUPTION.

Review whether this requirement is explicit and enforceable, whether the counter definitions/instrumentation are adequately pinned, and whether the retry rule avoids machine-dependent semantic classifications without turning operational resources into semantic gates.

## 8. Editorial/provenance correction from v0.11 to v0.12

v0.11 contained active passages that still named v0.10 as the current design and a pre-publication sentence that did not yet record v0.11's actual blob/commit identity. v0.12 updates those passages, records the v0.11 predecessor identity, and states that v0.12 is the current unreviewed draft.

Confirm:
1. all active current-document references now name v0.12 or use “this design specification”;
2. remaining references to v0.10 and v0.11 are historical or explicit predecessor references;
3. §0.13 records v0.11's exact blob and commit identity;
4. the terminal statement, §8 review target and repository identity agree on v0.12;
5. this editorial revision did not alter any scientific or authorization rule.

## 9. Full v0.12 review required

Please read every section of v0.12, including all text unchanged from earlier versions:

1. **§§0–1:** provenance language, authorization boundaries, accepted predecessor identities, target population, claim scope, Option B and statistic conventions.
2. **§§2.1–2.5:** parent definition and eligibility, full lineage procedure, calibration, pairwise cluster coherence, unresolved-parent treatment, representative selection and operating parent-count justification.
3. **§§3.1–3.6:** exact B1 cells, full-population support, LOPO folds, discrete C_D, M1-si as an additional design requirement, historical M1 authority and pre-fit rank.
4. **§§4.1.1–4.1.6, 4.2–4.3:** operator-class identity, canonicalization, Stage 1/Stage 2 profile sequencing, predicate/effect catalog, serial deterministic work budgets, diagnostic-blind review, one invocation per variant, floating-point and external-call requirements, target-centred context slices and complete candidate inventory.
5. **§§5.1–5.7:** new protected evaluation set, exposed-data separation, independent custodian, no leakage, B1 amendment, outcome-side reporting and Option B/N5 proxy interpretation.
6. **§§6.1–6.6:** structural lower bounds, non-power boundary, incidence feasibility, shortfall rules and descriptive concordance audit.
7. **§§7–9:** compatibility with accepted B1 and computational plans, all outstanding governance gates, and complete non-authorization wording.

Check all cross-references, current-version self-references, numbering, headings and predecessor pointers. Confirm v0.11, v0.10 and all accepted predecessor artifacts remain unchanged.

## 10. Required deliverable

Return a review table with:
- finding ID;
- severity: blocking, recommended, accepted or contradicted;
- exact v0.12 section;
- technical reason;
- required correction, if any;
- whether it blocks design freeze.

Distinguish genuine resolutions from remaining defects. State explicitly which sections were read in full and which, if any, remain unread. Do not give a whole-document verdict if any section remains unread.

## 11. Boundary

This is a read-only review. v0.12 authorizes no solver-source acquisition, parent selection, mutation allocation, mutation/source generation, compilation, execution, diagnostic probing, bank access, protected-set access, model fitting, sampling, simulation or scientific analysis.

Passing this review would concern only the population/design specification. Separate statistical, computational, consent/provenance, custodian, isolation, data-access and execution gates remain in force. GPT will adjudicate the complete review. Any substantive correction after v0.12 must be a new version with its own identity and review.
