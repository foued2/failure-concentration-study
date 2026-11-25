# LC518 new mutation-allocation proposal v0.1

**Date:** 25 November 2026  
**Status:** NEW DESIGN PROPOSAL. Not recovered from the original annex, not frozen, not adopted, and not published to the repository.  
**Handling:** owner-side working draft. This directory is not encrypted or cryptographically sealed. Do not put the assignment schedule or mechanism labels in a public repository package.

## 1. Purpose and boundary

This proposal supplies a complete candidate taxonomy and allocation for the frozen LC518 30-parent population. It is a newly authored design, not a reconstruction, recovery, or claim about what was previously assigned. It is submitted for independent scientific and source-compatibility review before any candidate source is written.

The parent roster and family assignments are taken from `PARENT_DESIGN.md` v1.0, commit `3e9a29c9652a6ab4f6bab0919e386757280b2654`, Git blob `fd15338bd511ba479e62efa50ada9d2d233e143a`. The roster is: K1 G01–G07, K2 G08–G15, K3 G16–G23, K4 G24–G28, K5 G29–G30. The frozen bank design specifies 64 diagnostic records, eight in each D1–D8 stratum (`R_j=8`).

The proposal preserves the frozen structure: 30 parents; one pair assignment per parent; every unordered pair among eight mechanisms at least once; two distinct preselected repetitions; SA/SB orientation per assignment; and one S-extra mechanism per parent, balanced six-at-four and two-at-three.

**Not authorized or performed:** no parent source construction, mutation patching, source diff, solver ID assignment, candidate execution, diagnostic execution, held-out evaluation, model fitting, repository change, commit, push, or publication.

## 2. Proposed eight-mechanism taxonomy

These are operational fault operators for the LC518 combination-counting task, not a universal software-defect taxonomy. They are deliberately specified at the level of observable algorithm semantics. Their intended D-stratum reach is a hypothesis to test against actual input rows and concrete parent source. It is not an assertion that every listed stratum contains a triggering row or that a particular complete C6 witness is jointly attainable.

| ID | Mechanism | Defect definition | Trigger condition | Proposed plausible reach |
|---|---|---|---|---|
| M01 | **Empty-combination identity set to zero** | Change the coefficient/base state for amount 0 from 1 to 0. | The correct reference answer is positive; the incorrect zero identity then removes every derivation from the empty state. | D1, D2, D4, D5, D6, D7, D8 |
| M02 | **Unbounded multiplicity reduced to one use** | Replace unlimited reuse of each denomination by at-most-one use per denomination. | At least one valid combination requires using some denomination at least twice, and the at-most-once count is lower than the unbounded count. | D1, D2, D4, D5, D6, D7, D8 |
| M03 | **Largest denomination omitted** | Remove the maximum denomination before evaluating the otherwise unchanged parent. | At least one valid combination uses the maximum denomination, so removing it changes the answer. | D1, D2, D4, D5, D6, D7, D8 |
| M04 | **First denomination processed twice** | Process the first input denomination twice as if the two occurrences were distinct coin types, despite the contract's distinct-denomination set semantics. | The first input denomination participates in at least one representation, and treating it as two distinct types changes the combination count. | D1, D2, D4, D5, D6, D7, D8 |
| M05 | **Target-equal denomination omitted** | Discard any denomination c equal to the target amount A before counting combinations, incorrectly treating an exact denomination match as unusable. | A positive target denomination is present; removing it removes the singleton combination using that denomination. | D1, D2, D4, D6, D7, D8 |
| M06 | **Unsorted prefix early-stop** | Before the parent performs any ordering/normalization, scan the original input sequence and stop at the first denomination greater than amount; retain only the prefix. No sort is performed before this test. | A denomination greater than the target appears before a later denomination that contributes to a valid representation; the premature break then discards that useful suffix. | D1, D2, D4, D6, D7, D8 |
| M07 | **Minimum-denomination divisibility shortcut** | Incorrectly return zero whenever amount is not divisible by min(coins), treating divisibility by the smallest denomination as necessary for reachability. | The target is not divisible by the minimum denomination, but the reference answer is positive because other denominations form a valid combination. | D1, D2, D4, D6, D7, D8 |
| M08 | **Use-transition contribution doubled** | Multiply every non-empty use-transition contribution by two instead of one, overcounting denomination-use paths. | The reference answer is positive; every non-empty transition path receives an extra multiplicity weight, changing the total. | D1, D2, D4, D5, D6, D7, D8 |

### 2.1 Distinction and overlap risks

M03 and M05 are both denomination-omission faults, but their selection rules differ: M03 removes the largest denomination; M05 removes only denomination(s) equal to the target. They can coincide when the target denomination is also the maximum, but they are separately triggerable when a larger-than-target denomination is present. M01 changes the empty-combination identity; M07 adds an invalid divisibility precondition. M02 changes the permitted multiplicity; M08 reweights each use transition. M04 duplicates the first input denomination as a second type; M06 introduces an order-sensitive premature prefix stop.

The taxonomy is still challengeable. It is concentrated on recurrence, denomination selection and input-order handling. It does not include interface/type failures, exceptions, memory behavior or external I/O. The task and work order require a plausible, separable eight-mechanism taxonomy, not necessarily broad coverage of every failure class. Claude should explicitly challenge whether these eight are sufficiently distinct and representative for the research purpose.

### 2.2 Family-level implementation adapters

Each mechanism has a proposed adapter for K1–K5 in the machine-readable JSON. The intended translation is: K1 coin-outer 1-D recurrence; K2 2-D use/skip table; K3 memoized suffix recurrence; K4 generating-function product (including its residue-chain, binary-doubling and sparse-carrier variants); K5 two half-products followed by a Cauchy product.

The parent-level compatibility matrix lists all 30 specific frozen parent tactics and the assigned SA, SB and S-extra adapter. Every entry is currently `PROPOSED_COMPATIBLE` at formulation level only. **No source-specific patch has been reviewed**, because no parent source body exists. In particular, M06 must be inserted before any sorting or normalization; M04 must duplicate the original first input denomination before such normalization; M03/M05 filters and the M07 guard must be ordered as declared below. The matrix additionally flags explicit parent-tactic exceptions: M01 must alter G04/G07's explicit amount-zero return; M02 must use the prior-row value in G06's double-buffer tactic; and order-sensitive mutations must be inserted before sorting/reversing in affected parents.

## 3. Pair schedule, assignment and orientation

The two repeated pairs are preselected in this proposal as M01–M02 and M03–M04. Each appears on two different parent families, and the second occurrence reverses SA/SB orientation. The schedule is not outcome-selected: no source bodies or candidate outcomes have been produced.

The tournament orientation assigns SA to one endpoint and SB to the other. Incidence is balanced: each mechanism appears 3 or 4 times in SA and 3 or 4 times in SB.

| Assignment | Parent | Family | Pair | SA | SB | Pair status | S-extra |
|---|---|---|---|---|---|---|---|
| PAIR-01 | G04 | K1 | M01–M02 | M01 | M02 | BASE | M05 |
| PAIR-02 | G29 | K5 | M01–M03 | M01 | M03 | BASE | M06 |
| PAIR-03 | G11 | K2 | M01–M04 | M01 | M04 | BASE | M03 |
| PAIR-04 | G13 | K2 | M01–M05 | M01 | M05 | BASE | M03 |
| PAIR-05 | G24 | K4 | M01–M06 | M06 | M01 | BASE | M03 |
| PAIR-06 | G08 | K2 | M01–M07 | M07 | M01 | BASE | M02 |
| PAIR-07 | G07 | K1 | M01–M08 | M08 | M01 | BASE | M04 |
| PAIR-08 | G12 | K2 | M02–M03 | M02 | M03 | BASE | M01 |
| PAIR-09 | G14 | K2 | M02–M04 | M02 | M04 | BASE | M05 |
| PAIR-10 | G02 | K1 | M02–M05 | M02 | M05 | BASE | M06 |
| PAIR-11 | G28 | K4 | M02–M06 | M06 | M02 | BASE | M04 |
| PAIR-12 | G09 | K2 | M02–M07 | M07 | M02 | BASE | M06 |
| PAIR-13 | G05 | K1 | M02–M08 | M08 | M02 | BASE | M01 |
| PAIR-14 | G25 | K4 | M03–M04 | M03 | M04 | BASE | M07 |
| PAIR-15 | G06 | K1 | M03–M05 | M03 | M05 | BASE | M02 |
| PAIR-16 | G26 | K4 | M03–M06 | M03 | M06 | BASE | M05 |
| PAIR-17 | G15 | K2 | M03–M07 | M03 | M07 | BASE | M06 |
| PAIR-18 | G27 | K4 | M03–M08 | M08 | M03 | BASE | M01 |
| PAIR-19 | G18 | K3 | M04–M05 | M04 | M05 | BASE | M07 |
| PAIR-20 | G30 | K5 | M04–M06 | M04 | M06 | BASE | M08 |
| PAIR-21 | G20 | K3 | M04–M07 | M04 | M07 | BASE | M08 |
| PAIR-22 | G17 | K3 | M04–M08 | M08 | M04 | BASE | M02 |
| PAIR-23 | G19 | K3 | M05–M06 | M05 | M06 | BASE | M01 |
| PAIR-24 | G16 | K3 | M05–M07 | M05 | M07 | BASE | M03 |
| PAIR-25 | G03 | K1 | M05–M08 | M05 | M08 | BASE | M04 |
| PAIR-26 | G23 | K3 | M06–M07 | M06 | M07 | BASE | M02 |
| PAIR-27 | G22 | K3 | M06–M08 | M06 | M08 | BASE | M04 |
| PAIR-28 | G21 | K3 | M07–M08 | M07 | M08 | BASE | M05 |
| PAIR-29 | G01 | K1 | M03–M04 | M04 | M03 | REPEAT-1 | M07 |
| PAIR-30 | G10 | K2 | M01–M02 | M02 | M01 | REPEAT-1 | M08 |

### 3.1 Assignment totals

| Mechanism | SA | SB | S-extra | Total single-mutation slots |
|---|---:|---:|---:|---:|
| M01 | 4 | 4 | 4 | 12 |
| M02 | 4 | 4 | 4 | 12 |
| M03 | 4 | 4 | 4 | 12 |
| M04 | 4 | 4 | 4 | 12 |
| M05 | 3 | 4 | 4 | 11 |
| M06 | 4 | 3 | 4 | 11 |
| M07 | 3 | 4 | 3 | 10 |
| M08 | 4 | 3 | 3 | 10 |
| **Total** | **30** | **30** | **30** | **90** |

S-extra distribution is M01–M06 four each and M07–M08 three each. No parent receives its S-extra mechanism again as SA or SB.

### 3.2 Parent-family incidence

This is the raw assignment incidence before source-hash deduplication under Rev 11 C4. Counts include SA, SB and S-extra.

| Parent family | Mechanism incidence (total; SA/SB/extra shown) |
|---|---|
| K1 | M01: 3 (SA 1, SB 1, extra 1); M02: 4 (SA 1, SB 2, extra 1); M03: 2 (SA 1, SB 1, extra 0); M04: 3 (SA 1, SB 0, extra 2); M05: 4 (SA 1, SB 2, extra 1); M06: 1 (SA 0, SB 0, extra 1); M07: 1 (SA 0, SB 0, extra 1); M08: 3 (SA 2, SB 1, extra 0) |
| K2 | M01: 5 (SA 2, SB 2, extra 1); M02: 5 (SA 3, SB 1, extra 1); M03: 4 (SA 1, SB 1, extra 2); M04: 2 (SA 0, SB 2, extra 0); M05: 2 (SA 0, SB 1, extra 1); M06: 2 (SA 0, SB 0, extra 2); M07: 3 (SA 2, SB 1, extra 0); M08: 1 (SA 0, SB 0, extra 1) |
| K3 | M01: 1 (SA 0, SB 0, extra 1); M02: 2 (SA 0, SB 0, extra 2); M03: 1 (SA 0, SB 0, extra 1); M04: 4 (SA 2, SB 1, extra 1); M05: 4 (SA 2, SB 1, extra 1); M06: 3 (SA 2, SB 1, extra 0); M07: 5 (SA 1, SB 3, extra 1); M08: 4 (SA 1, SB 2, extra 1) |
| K4 | M01: 2 (SA 0, SB 1, extra 1); M02: 1 (SA 0, SB 1, extra 0); M03: 4 (SA 2, SB 1, extra 1); M04: 2 (SA 0, SB 1, extra 1); M05: 1 (SA 0, SB 0, extra 1); M06: 3 (SA 2, SB 1, extra 0); M07: 1 (SA 0, SB 0, extra 1); M08: 1 (SA 1, SB 0, extra 0) |
| K5 | M01: 1 (SA 1, SB 0, extra 0); M02: 0 (SA 0, SB 0, extra 0); M03: 1 (SA 0, SB 1, extra 0); M04: 1 (SA 1, SB 0, extra 0); M05: 0 (SA 0, SB 0, extra 0); M06: 2 (SA 0, SB 1, extra 1); M07: 0 (SA 0, SB 0, extra 0); M08: 1 (SA 0, SB 0, extra 1) |

## 4. SAB combination rule

For the same parent, the proposed SAB composition order is fixed as follows:

1. Duplicate the original first input denomination as a second distinct coin type (M04), preserving the original input order for this identification.
2. Remove all occurrences of the original maximum denomination (M03).
3. Remove all denominations equal to the target amount (M05).
4. Apply the unsorted prefix break at the first denomination greater than the target (M06), before parent sorting or normalization.
5. Apply the M07 false divisibility guard using the original minimum denomination.
6. Apply recurrence modifiers M01 (zero empty-combination identity), M02 (at-most-once use) and M08 (doubled use contribution).

This precedence is deterministic and tested as a semantic composition rule. It does not establish that each pair's two changes can be cleanly represented as source diffs for every parent. In particular, interactions can mask or overlap on some inputs; this is a scientific property to report, not something the allocation should conceal. The source patch review must ensure each intended component is present in SAB even when its observable effect overlaps the other mutation.

## 5. C6 static feasibility screen: what the proposal suggests

Under raw parent IDs, the schedule places 16 `(mechanism, family)` cells at three or more assigned parent IDs. K5 never reaches three because it has only two parents, consistent with Rev 11 C7. The 16 candidates are listed below.

| Mechanism | Family | Raw parent IDs | Three proposed parents | Witness strata | Illustrative C_D values | Status |
|---|---|---:|---|---|---|---|
| M01 | K1 | 3 | G04, G05, G07 | D1 / D2 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M02 | K1 | 4 | G02, G04, G05 | D1 / D5 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M04 | K1 | 3 | G01, G03, G07 | D2 / D5 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M05 | K1 | 4 | G02, G03, G04 | D1 / D2 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M08 | K1 | 3 | G03, G05, G07 | D2 / D5 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M01 | K2 | 5 | G08, G10, G11 | D1 / D2 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M02 | K2 | 5 | G08, G09, G10 | D1 / D5 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M03 | K2 | 4 | G11, G12, G13 | D2 / D5 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M07 | K2 | 3 | G08, G09, G15 | D2 / D4 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M04 | K3 | 4 | G17, G18, G20 | D2 / D5 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M05 | K3 | 4 | G16, G18, G19 | D1 / D2 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M06 | K3 | 3 | G19, G22, G23 | D2 / D6 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M07 | K3 | 5 | G16, G18, G20 | D2 / D4 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M08 | K3 | 4 | G17, G20, G21 | D2 / D5 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M03 | K4 | 4 | G24, G25, G26 | D2 / D5 | 1, 1/2, 1 | HYPOTHETICAL ONLY |
| M06 | K4 | 3 | G24, G26, G28 | D2 / D6 | 1, 1/2, 1 | HYPOTHETICAL ONLY |

For each listed candidate cell, the JSON includes three arithmetic witness skeletons in the same proposed exact cell `(k_fail=2, k_unresolved=0)`: one parent has `f=(2,0,...)`, another has `f=(1,1,0,...)`, and a third has `f=(0,2,0,...)` across the mechanism's proposed witness strata. These produce C_D values `1`, `1/2`, and `1` respectively, with all eight unresolved entries explicitly zero and each per-stratum total at or below `R_j=8`.

**These are not Rev 11 witnesses and do not make C6 pass.** They are hypothetical arithmetic skeletons only. They lack (i) pinned base-source hashes and effective C4 parent-group deduplication; (ii) actual version/source identities; (iii) exact diagnostic bank record IDs for the proposed failures and unresolved outcomes; (iv) exact, identifiable written mechanism rules tied to each family and assigned version; and (v) evidence that each complete `f` vector is jointly attainable under one coherent application of that mechanism. The candidate C6 cells are feasibility candidates for independent review, not established feasibility.

## 6. Synthetic test design and results

The test script does not import, write or execute any of the 150 planned candidate solver bodies. It runs five generic formulation-level models (K1–K5) on invented, contract-valid inputs. Positive triggers are synthetic examples consistent with the published D1–D8 descriptions, not confirmed frozen-bank records. These tests model the family formulations, not every source-level tactic variant within each family.

Positive fixture coverage:

| Diagnostic stratum | Synthetic input count |
|---|---:|
| D1 | 6 |
| D2 | 14 |
| D3 | 0 |
| D4 | 2 |
| D5 | 8 |
| D6 | 4 |
| D7 | 8 |
| D8 | 8 |
| **Total** | **50** |

D3 is not used as a positive trigger stratum: these proposed operators preserve an unreachable result when the reference answer is zero. D3-like unreachable cases are instead used as negative controls for M01/M08 and other trigger-inactive examples.

The local validation suite completed with **23 tests, 0 failures and 0 errors**. Tests include:

- exact 30-parent/28-pair-plus-two-repetition structure, one-to-one parent mapping and family alignment;
- reverse SA/SB orientation for repeated pairs and balance of 30 SA / 30 SB slots;
- six-at-four / two-at-three S-extra distribution, and no S-extra collision with SA/SB for a parent;
- all 40 mechanism-by-family incidence cells, K5 three-parent impossibility, and the 16 raw candidate support cells;
- 48 witness-skeleton arithmetic checks, including vector lengths, exact sums, per-stratum bounds, reach-set membership, exact rational C_D and distinct parent IDs;
- 50 positive-trigger inputs × five formulation models = 250 baseline/mutant semantic checks;
- 40 negative-control checks (eight named mechanisms × five formulation models);
- agreement of independent 1-D and 2-D DP oracles on all 50 synthetic inputs, and bounded exhaustive multiplicity enumeration on the small-input subset;
- all 30 assigned pair compositions across five family models (150 deterministic composition checks), plus a trigger test requiring each assigned pair to change at least one synthetic input in each family model;
- a D6 permutation metamorphic test showing that M06 can make two orderings of the same mathematical instance behave differently in all five family models;
- 30 parent/tactic compatibility entries, explicitly marked provisional at formulation level and unreviewed at source level.

These tests support internal consistency and semantic realizability of the proposed operators on synthetic cases. They do not verify the exact 30 parent source implementations, prove mutation isolation, test the real 64-record diagnostic bank, establish A2, establish A3, or provide any B1 outcome.

## 7. Limitations and required independent challenges

1. **Taxonomy validity:** Are these eight operational mechanisms sufficiently distinct, separable and scientifically motivated? In particular, is the overlap between M03/M05 and between some recurrence faults acceptable?
2. **Parent-specific compatibility:** Does each assigned operator have a clean source-level patch in every named parent's actual tactic? The present matrix is only formulation-level. Source diff feasibility cannot be certified before source construction.
3. **SAB composition:** Is the proposed precedence correct? Do any pair combinations cancel or silently erase one mutation in source form? The test only checks semantic composition and that a combined output differs from baseline somewhere; it does not establish mutation isolation.
4. **Mechanism reach:** Are the D1–D8 reach claims and witness strata defensible for every family and assigned version? The synthetic fixtures are not actual bank records.
5. **C6 feasibility:** Can the 48 proposed witness skeletons be converted into Rev 11-admissible, source-cited, jointly attainable witness evidence after actual variants and bank records exist?
6. **C4 independence:** Will actual parent source hashes remain distinct after construction? The current 16 candidate cells are raw parent-ID counts only.
7. **Exposure and inferential scope:** The held-out bank was publicly exposed, and candidate screening against that bank is recorded in a later instrument draft. This population must not be described as confirmatory or as independent of all held-out-bank information.

## 8. Status and next controlled gate

**Proposal result:** 30-row allocation, 28 unique pairs plus two repeated pairs, balanced orientations, balanced S-extra, and 16 raw candidate C6 cells.  
**Synthetic validation:** PASS for the 23 listed structural and synthetic checks.  
**A2:** **BLOCKED / NOT ASSESSABLE**.  
**A3:** NOT ASSESSED.  
**B1:** NOT RUN; no correctness outcome matrix established.

The correct next step is independent review of this proposal and its tests, then a separate source-construction work order if the design is adopted. No solver body should be written from this proposal until the mechanism definitions, parent compatibility matrix and SAB precedence are accepted. Dynamic mutation/diagnostic/held-out execution require their own permissions and a pinned execution protocol.

## 9. Deliverable index

- `OWNER_SEALED_NEW_ALLOCATION_v0.1.json`: complete machine-readable proposed taxonomy, schedule, S-extra, parent compatibility mappings, raw incidence and hypothetical witness skeletons.
- `PAIR_AND_PARENT_ALLOCATION_v0.1.csv`: 30-row parent/pair/orientation/S-extra allocation.
- `MECHANISM_FAMILY_INCIDENCE_v0.1.csv`: all 40 family/mechanism cells with role-specific counts.
- `PARENT_COMPATIBILITY_MATRIX_v0.1.csv`: 30 parent/tactic-specific provisional compatibility entries.
- `C6_CANDIDATE_CELLS_v0.1.csv`: 16 raw candidate cells and non-admissible witness skeleton summary.
- `SYNTHETIC_TRIGGER_FIXTURES_v0.1.csv`: all 50 positive synthetic trigger inputs and outputs from the five formulation models plus independent oracle values.
- `NEGATIVE_CONTROL_FIXTURES_v0.1.csv`: eight negative controls and the five family-model results for each.
- `validate_owner_sealed_allocation.py`: reproducible structural and synthetic-semantic test script.
- `VALIDATION_REPORT.txt`: output from the latest test run.
- `SHA256SUMS`: hashes for the proposal artifacts.