# Concentration research record (2026-10-25)

**Status:** reconciled working record on the review branch. This folder is a research record only, not an approved study protocol. The failure-concentration project remains closed under existing authorization.

## Boundaries

- No solver generation or execution, mutation building, simulation, model calls, new data collection, or experiments are authorized by these files.
- This branch contains only material under `concentration-formulation/`. The base branch `research/concentration-math-spec` remains separate. Preserve the pre-existing `README.md` modification.
- Related material remains elsewhere in the repository, including `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` on `research/concentration-math-spec` and a protocol draft on `review/feasibility-protocol-2026-10-25`.

## Files and roles

| File | Current role | Status |
| --- | --- | --- |
| `02_RESEARCH_FORMULATION_NOTE_2026-10-25.md` | Primary formulation. H3, ranking rejected candidates by `C` at fixed `k` on held-out inputs, is the **working primary hypothesis**, not a demonstrated result or authorized protocol. | Reconciled candidate, revision 4 |
| `03_LITERATURE_SCAN_2026-10-25.md` | Focused scan plus exploratory follow-up on slice/worst-group evaluation, reliability/capture-recapture, and automated grading. | Updated scope; not systematic |
| `01_FEASIBILITY_NOTE_IDEA1_RANDOM_DEFECT_SETS_2026-10-25.md` | Historical paper-only analysis of mutation-site combinations. This population differs from naturally generated solvers and cannot answer primary H3 by itself. | Alternative-only feasibility note; important issues remain open |

Suggested reading order: 02, then 03, then 01.

## Core conclusions and constraints

- At fixed `k`, ranking by `C = max_j f_j / k` is exactly ranking by `max_j f_j`. The claim to test is whether the maximum family-specific failure count adds predictive ranking information conditional on total failure count, not whether the ratio has a distinct ordering property.
- The legacy six-family, `p = 5` partition has been used in v0.2 and Gate 1 with observed failures. Unless records establish that the partition itself was frozen before those outcomes, treat its definition as outcome-exposed. Freezing it now does not remove that history. Reuse supports a prospective replication conditional on the legacy taxonomy; a cleaner confirmatory test requires a new task-semantics partition selected without access to prior failure-profile tables, which is a related but not identical operationalization.
- H3 conditions on B1-rejected candidates (`k > 0`). B1's rejection rule depends only on `k`, but the claim does not generalize to accepted candidates or other selection rules.
- Held-out input-domain construction and any score strata/weights must be defined independently of the diagnostic family partition, with related input clusters kept disjoint.
- The intended primary population is naturally generated rejected solver candidates, but the generator, sampling frame, and task/base-algorithm strata are not yet operationally specified. If the frame spans multiple tasks or base algorithms, H3 comparisons must be within task/base-algorithm/`k` cells, with per-cell concordance reported and a pre-weighted aggregate; cross-task pairs cannot establish the primary effect.
- Mutation-site combinations in file 01 are a different population. A positive result for them would not establish the natural-candidate claim.
- Solver-side dependence groups and input-construction clusters must be controlled separately. Different program text or failure sets alone do not establish independence.
- The archived v0.2 analysis reports `C = 5/k` throughout. Keep its dimensions separate: 1,200 rows correspond to 40 input instances × 30 probes; the solver inventory separately comprises 40 bodies with three replicas each, with ten base bodies eligible. Neither the 1,200 probe/input rows nor the 120 body/replica records are 120 independent candidates. A separate natural-candidate inventory was reported as 90 eligible rows across ten base bodies, also without same-`k`, different-`C` support. Do not conflate these records or their units.
- The alias-check issue in file 01 is not solved: comparing failure behavior over the same domain used for held-out scoring is not outcome-blind.

## Version status

The repository version of file 02 is the active formulation candidate for this branch. A separately reported local file, `CONCENTRATION_RESEARCH_FORMULATION_2026-10-25.md`, was not available in the repository contents for this reconciliation. Its reported hash was not independently reproduced, and byte-for-byte equivalence is not claimed. No additional copy is being created.

## Open items

1. Specify the natural candidate-generation mechanism and sampling frame; establish independent solver-side groups.
2. Define the bounded held-out input domain and scoring target, independently of the diagnostic family partition.
3. Use the fixed group-pair estimand in file 02: average candidate-pair concordance within each eligible pair of distinct dependence groups, then weight group pairs equally within task/base-algorithm/`k` cells; ties receive half credit. Declare cell weights and use a two-way solver-group/input-cluster bootstrap, not pair-row resampling, before held-out outcomes are inspected.
4. Demonstrate support before accessing held-out scores: within each pre-declared task/base-algorithm/`k` cell, require at least two `C` levels, each represented by at least a pre-declared `m_min` distinct solver-side dependence groups. Justify `m_min` from a precision/decision rationale. For six families with five probes each, `C` cannot vary at `k = 1` or `k = 25..30`, and has only two levels at `k = 2`. A footprint-only pilot can establish whether support exists, but cannot by itself establish power or precision. If support is absent, H3 is not estimable with that population/instrument.
5. Resolve alias grouping and separate diagnostic, identity-check, and evaluation input clusters without claiming more equivalence than the domains support.
6. Resolve legacy-partition exposure: either explicitly treat reuse as prospective replication on an outcome-exposed definition, or specify a new task-semantics partition without access to historical failure-profile tables. Freeze the selected partition before new candidate generation, and define evaluation strata/weights independently of it.
7. Specify how pairs drawn from dependence groups containing multiple candidates are weighted so larger groups do not dominate.
8. Treat Yang et al. (ICML 2023) on worst-class-accuracy model selection under subpopulation shift as the closest conceptual precedent identified so far, not a direct match to H3.
9. Search defect prediction and software reliability more systematically; the current scan is exploratory and defect prediction remains unsearched.
10. Record the eventual authorized protocol freeze with an annotated tag and full commit SHA, UTC timestamp, and hashes of the partition, generator/sampling frame, diagnostic/evaluation input manifests, scoring rules, and analysis code. The present formulation branch is not itself a protocol freeze.
11. Conduct a systematic literature review before any novelty claim.
