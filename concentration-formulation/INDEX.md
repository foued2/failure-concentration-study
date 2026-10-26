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
- The intended primary population is naturally generated rejected solver candidates, but the generator and sampling frame are not yet operationally specified.
- Mutation-site combinations in file 01 are a different population. A positive result for them would not establish the natural-candidate claim.
- Solver-side dependence groups and input-construction clusters must be controlled separately. Different program text or failure sets alone do not establish independence.
- The archived v0.2 table is reported as 1,200 rows from 40 solver bodies with three replicas each, with `C = 5/k` throughout. A separate natural-candidate inventory was reported as 90 eligible rows across ten base bodies, also without same-`k), different-`C` support. Do not conflate these records or their independent units.
- The alias-check issue in file 01 is not solved: comparing failure behavior over the same domain used for held-out scoring is not outcome-blind.

## Version status

The repository version of file 02 is the active formulation candidate for this branch. A separately reported local file, `CONCENTRATION_RESEARCH_FORMULATION_2026-10-25.md`, was not available in the repository contents for this reconciliation. Its reported hash was not independently reproduced, and byte-for-byte equivalence is not claimed. No additional copy is being created.

## Open items

1. Specify the natural candidate-generation mechanism and sampling frame; establish independent solver-side groups.
2. Define the bounded held-out input domain and scoring target.
3. Specify the practical ranking-gain threshold, tie rule, stratum weighting, and uncertainty procedure before held-out outcomes are inspected.
4. Demonstrate adequate same-`k`, varying-`C` support among independent groups; if absent, primary H3 is not estimable with that population/instrument.
5. Resolve alias grouping and separate diagnostic, identity-check, and evaluation input clusters without claiming more equivalence than the domains support.
6. Conduct a systematic literature review before any novelty claim.
