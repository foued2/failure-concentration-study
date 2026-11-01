# GLM Work Order: LC518 150-Body Construction Study

**Version:** 1.0
**Date:** 2026-11-01
**Study folder:** `lc518-150/`
**Owner authorization:** Construction of exactly 150 source bodies and the supporting design/package files is authorized. Execution of candidate solver bodies is not authorized.
**Status labels:** All candidate bodies must remain `GENERATED_NOT_EXECUTED`; intended mutations must remain `DESIGNED_NOT_VERIFIED`.

## 1. Purpose and scientific boundary

Construct a controlled population of 150 Coin Change II solver bodies so that the study can describe failure behaviour, compare matched correctness outcomes, and later investigate whether diagnostic failure information adds predictive information about correctness.

Correctness is the research target. Failure records, defect hypotheses, interactions and concentration are explanatory or predictive instruments. Do not present failure counts or concentration as the final scientific objective.

This is a deliberately constructed LC518 population. It is not a sample of arbitrary programs, naturally occurring submissions, or every possible solver. A result applies only to the declared construction process, task contract, execution protocol and input distribution.

## 2. Repository separation is mandatory

The existing file `engineered-study/03_TASK_SPEC.md` defines `paren7_min_insertions`, the length-seven parenthesis task. It is not LC518. This study has its own contract in `LC518_TASK_CONTRACT.md` and must remain in this separate `lc518-150/` directory.

Do not edit, replace, reuse, or reinterpret the parenthesis-task specification, its diagnostic/evaluation banks, its 30/98 split, its family labels, or its results as LC518 evidence.

Do not cite the earlier 90-solver clustering claim unless its primary record is separately verified. It is not needed to complete this construction package.

## 3. Population design: 30 matched parent groups, 150 bodies

Create exactly 30 distinct parent implementations, each intended to be correct under `LC518_TASK_CONTRACT.md`. Each parent must have five matched versions:

| Role | Construction |
|---|---|
| S0 | Unmodified parent control |
| SA | Parent with mutation A only |
| SB | Parent with mutation B only |
| SAB | Same parent with mutations A and B together |
| S-extra | Parent with one additional single mutation |

This yields 30 controls, 90 single-mutation variants and 30 two-mutation variants: exactly 150 bodies.

Target at least four genuinely distinct correct algorithmic formulations. Each parent requires a written correctness argument and complexity analysis under the full LC518 constraints. Do not call cosmetic rewrites different algorithm families. If four defensible formulations cannot be produced, stop and report the limitation rather than manufacturing diversity.

Every body receives an opaque identifier S001 through S150. Source filenames and source comments must not reveal mutation identities.

## 4. Private mutation design and ground-truth custody

The owner will supply GLM a separate private mutation-design annex containing the approved eight-mechanism taxonomy and the fixed pair-allocation schedule. Use that annex exactly. If GLM has not received it, stop and request it; do not invent, rename, merge or substitute mechanisms.

The fixed schedule must cover all 28 unordered pairs of the eight mechanisms once, plus two preselected pair replications. The two replicated pairs must be chosen before source construction, not after outcomes are observed. S-extra assignments must be balanced across the eight mechanisms as closely as integer counts permit.

The repository branch and public construction package must not contain the per-solver mechanism assignments or defect labels. The sealed ground-truth manifest must be delivered separately to the owner, with its own SHA-256 file. It must map opaque solver IDs to parent group, version role, mechanism identities, mutation details and source hashes.

The owner retains custody of the sealed manifest. Claude may receive a review copy solely to audit whether the source diffs match the declared construction. That makes Claude unblinded; Claude must not conduct any later blinded predictive analysis.

A later predictive analysis must be performed by a separately appointed analyst who has not seen the sealed manifest, mutation assignments or solver source code. That analyst may receive opaque solver IDs, parent-group IDs needed for grouped validation, the frozen observable feature table and correctness outcomes. Mutation labels and version-role labels must be excluded from predictive features.

## 5. Freeze the design before writing solver bodies

Before generating any candidate solver source, GLM must produce and freeze the following design files:

1. `BANK_DESIGN.md`: exact diagnostic and held-out input-bank sizes, deterministic seeds, input strata, target input distribution, weighting, canonical identity rule, and rationale for coverage.
2. `ANALYSIS_SPEC.md`: the estimands, feature definitions, primary and secondary analyses, grouping, loss, reporting rules and limitations set out below.
3. `PARENT_DESIGN.md`: the 30 parent implementations, their algorithm families, correctness arguments and complexity arguments.
4. The private mutation annex and pair schedule, retained outside the repository and public package.

These documents must be frozen before solver mutations are constructed. No test case, feature, mechanism, pair assignment, model setting or exclusion rule may be added because of observed candidate outcomes.

Do not run a power calculation or a new power simulation in this phase. The previous power figures and thresholds remain invalidated. Thirty parent groups define an exploratory construction screen, not a claim of adequate statistical power. Any later confirmatory sample-size or feasibility study requires separate owner authorization and its own justified assumptions.

## 6. Diagnostic and held-out input banks

Construct two disjoint, valid LC518 input banks:

- The diagnostic bank characterizes observable solver behaviour and supplies the candidate enriched features.
- The held-out bank measures correctness on inputs not used to construct those diagnostic features.

Freeze both banks before constructing solver bodies. Use the same banks and the same oracle outputs for all 150 bodies.

Every input must meet the LC518 contract. Include coverage for amount zero, exact denomination matches, unreachable amounts, repeated use of a denomination, multiple distinct combinations, non-greedy counterexamples, varied denomination counts, large amounts, and reordered coin arrays.

Input order is not guaranteed by the contract. Include reordered versions of selected denomination sets to test order invariance. For bank separation, canonicalize an instance by `(amount, sorted coin denominations)`: all permutations of the same mathematical instance must remain in one bank and must not cross from diagnostic to held-out.

The held-out bank defines a finite, explicit target distribution. Report its strata and weights. Conclusions may generalize only to that declared LC518 input distribution; do not describe it as representative of all real LeetCode submissions or all possible LC518 inputs.

Choose bank size for declared coverage, not by claiming statistical power. State clearly that no sample-size or power guarantee is made.

## 7. Oracle construction and validation

Provide a primary reference implementation using one-dimensional dynamic programming with coins in the outer loop and amounts updated in increasing order.

Provide an algorithmically distinct cross-check using a two-dimensional coin-index/amount dynamic-programming formulation. Also implement exhaustive multiplicity enumeration for small inputs only.

Cross-check the two dynamic-programming implementations over the complete finite input banks. Compare both against exhaustive enumeration on a predeclared bounded small-input set.

Record source hashes, recurrences, test domains and outputs. If one agent writes both implementations, describe them as algorithmically distinct, not independently authored. Claude's review is a separate logical inspection, not an external oracle certification.

Oracle tests may execute the oracle implementations only. They must never import, instantiate, call or otherwise execute any of the 150 candidate solver bodies.

## 8. Failure-observation record

Preserve one record per solver/input execution in the later, separately authorized execution phase. The schema must support:

- opaque solver ID and input ID;
- task contract and execution-environment references;
- expected output and actual output, when available;
- status: PASS, FAIL or UNRESOLVED;
- failure manifestation: wrong answer, invalid return type, exception, timeout/resource breach, or other explicitly defined status;
- signed and absolute numerical deviation where meaningful;
- elapsed time and memory only when measured under a pinned environment;
- raw trace/artifact reference and integrity hash.

Preserve successful executions as well as failures. UNRESOLVED is neither PASS nor FAIL. Record unresolved counts separately from failed counts.

Keep observed outcomes separate from injected defect labels and hypotheses about causes. A source mutation's intended label is not evidence that the resulting solver actually exhibits that behaviour.

Do not reduce exceptions, wrong types, wrong values and timeouts to one bit in the retained record. Binary summaries may be derived later, but the underlying typed record must remain available.

### Resource-related behaviour

The LC518 statement does not provide this study with a wall-clock or memory cutoff. Do not invent one. M08-style resource inefficiency may be documented as a designed performance-risk candidate, but it cannot be labelled an observed timeout until a separate execution protocol declares the runtime, memory budget and timeout rule.

## 9. Primary analysis: matched within-parent correctness contrasts

The primary analysis is the matched comparison within each of the 30 parent groups. All five versions of a parent use identical diagnostic inputs, held-out inputs, oracle outputs and execution conditions.

For group g and version v, define held-out error loss:

    L(g,v) = mean over the frozen held-out bank of 1[the solver is incorrect].

Report the following contrasts for each parent group:

- A-only contrast: L(g,SA) - L(g,S0).
- B-only contrast: L(g,SB) - L(g,S0).
- S-extra contrast: L(g,S-extra) - L(g,S0).
- Pair contrast: I(g,A,B) = L(g,SAB) - L(g,SA) - L(g,SB) + L(g,S0).

Also preserve the per-input interaction contrast:

    i(g,A,B,x) = loss(g,SAB,x) - loss(g,SA,x) - loss(g,SB,x) + loss(g,S0,x).

Do not infer 'no interaction' merely because the aggregate I is zero: positive and negative per-input interactions can cancel in the aggregate. Preserve the per-input distribution and the aggregate result.

These are construction- and parent-specific matched contrasts. Because most mechanism pairs occur on only one parent, the 28-pair screen is exploratory. The two repeated pairs provide only limited replication. Do not claim that the design estimates general interaction laws across all solver implementations.

Defect interactions are UNKNOWN until all four matched versions have been dynamically evaluated under the same declared conditions. Before that point, the formulas are planned estimands, not measured results.

## 10. Secondary analysis: baseline versus enriched prediction

The secondary question is whether diagnostic failure information predicts held-out correctness better than the total diagnostic failure count and context.

Target: the solver's mean correctness score Q on the fixed held-out bank, with unresolved held-out outcomes reported separately and accompanied by coverage/bounds. Do not silently count unresolved outcomes as wrong or discard them without reporting coverage.

Baseline predictors:

- diagnostic failed-event count k, with unresolved diagnostic observations counted and reported separately rather than coerced into failure;
- parent algorithm family as the prespecified context variable Z.

Enriched predictors:

- all baseline predictors;
- prespecified diagnostic status counts by the frozen input strata;
- numerical deviation summaries for wrong integer outputs, where defined;
- typed exception/invalid-return counts;
- timeout features only if a later execution protocol has first fixed a resource budget.

Do not use source code, mutation labels, version roles, sealed-manifest fields, solver IDs, or raw output text as predictive features. Preserve raw outputs and traces separately as evidence.

Use the same regularized linear prediction procedure for both arms. Standardization and any tuning must be conducted inside training data only. Outer validation must leave out one complete parent group at a time; all five versions of a parent stay in the same outer fold. Any inner tuning must also group by parent. No random row-level split is permitted.

Use held-out squared prediction error and report the paired out-of-group error difference between the two arms. Report group-level results and the overall descriptive difference. Because there are only 30 parent groups and no power calculation is authorized, label this predictive comparison EXPLORATORY. Do not apply an invented meaningful-effect threshold, claim adequate power, or declare confirmatory support.

The within-parent contrasts and the baseline-versus-enriched prediction comparison answer different questions. Do not merge their estimates or describe a predictive gain as a causal effect of a mutation.

## 11. Algorithm diversity, duplicate checks and taxonomy limits

Report the parent algorithm family for every group. Identify exact duplicate source hashes and plausible near-duplicate parent implementations. Duplicates do not count as distinct parent designs.

Report which intended mutation patterns are compatible with each parent family. A mutation that cannot be applied without changing unrelated logic must be marked incompatible for that parent; do not silently rewrite the mutation or substitute a different mechanism.

List taxonomy coverage limits explicitly. The eight owner-supplied mechanisms are not universal. LC518-specific coverage does not include every possible program failure, and the study does not cover unrelated systems issues such as concurrency or external I/O unless they are separately defined in scope.

## 12. Static validation allowed in this phase

Allowed:

- verify exactly 150 source files and 30 parent groups;
- verify opaque IDs, file counts, hashes and manifest consistency;
- parse source files with Python's AST parser and compile source text for syntax checking without importing or executing it;
- inspect diffs and verify that each source diff matches its declared mutation instructions;
- verify the 28-pair schedule and two preselected replications;
- verify input-bank validity, canonical disjointness, deterministic seeds and oracle provenance;
- execute oracle-only cross-checks as described in Section 7.

Static inspection cannot establish that a mutant is semantically different from S0, that a defect is triggered, that two defects interact, or that an intended-correct parent is actually correct over the full domain. Do not use the phrase 'mutation isolation verified' for static evidence. Report these properties as DESIGNED_NOT_VERIFIED.

## 13. Execution and repository boundaries

This work order authorizes construction of source files, contracts, manifests, banks, oracle files, design documents and hashes. It does not authorize execution of any generated solver body, dynamic mutation validation, diagnostic/evaluation runs, model fitting, power simulation, further generation beyond 150 bodies, or any runtime/resource stress test.

All candidate files must remain marked GENERATED_NOT_EXECUTED. All intended mutations must remain marked DESIGNED_NOT_VERIFIED.

GLM delivers two separate archives to the owner:

1. PUBLIC_CONSTRUCTION_PACKAGE: solver files with opaque IDs, public input banks, oracle files, schemas, hashes and non-sensitive design documentation. It contains no per-solver defect labels or mutation assignments.
2. OWNER_SEALED_GROUND_TRUTH: the private mapping of solver IDs to parent group, version role, mechanism assignments, source mutations and hashes. This archive is delivered separately and is not committed to GitHub.

GLM does not push or commit generated solver packages. Claude performs a static construction audit using the public package and, if supplied by the owner, a review copy of the sealed manifest. Claude is thereby unblinded and is not the later blind predictive analyst.

Any dynamic execution requires a separate written owner authorization specifying the isolated environment, input banks, resource limits, timeout handling and exact execution cap. Any GitHub push of the generated package requires separate owner approval after review and must target a new branch.

## 14. Required deliverables

Create a self-contained output directory with at least:

- LC518_TASK_CONTRACT.md;
- README.md;
- PARENT_DESIGN.md;
- BANK_DESIGN.md;
- ANALYSIS_SPEC.md;
- DESIGN_MATRIX_150.csv, without defect labels;
- 150 solver source files with opaque identifiers;
- public execution-record schema;
- diagnostic and held-out input banks with oracle outputs;
- primary and cross-check oracle implementations;
- oracle cross-check report;
- generation report;
- parent-diversity and duplicate report;
- coverage and taxonomy-limit report;
- static-validation report;
- SHA256SUMS for every delivered file;
- the separate owner-sealed ground-truth archive and its separate hash list.

Do not fabricate execution results, failure observations, correctness scores, timeout labels or interaction estimates.

## 15. Acceptance and stop conditions

Package acceptance for Claude's static review requires:

1. Exactly 150 source files and exactly 30 parent groups.
2. Every group has exactly one S0, SA, SB, SAB and S-extra as recorded in the sealed manifest.
3. The 28-pair schedule and two replications match the pre-frozen private annex.
4. At least four genuinely distinct intended-correct algorithm families, with arguments and complexity justifications; otherwise stop and report.
5. The diagnostic and held-out banks are frozen before source mutation, valid under the contract and canonically disjoint.
6. The oracle checks pass on their declared test domains.
7. Static source checks, source hashes and manifest references reconcile.
8. No per-solver defect labels appear in public source files or the repository package.
9. No generated solver has been executed.
10. All limitations and unverified properties are reported without upgrading design intentions into findings.

If a required item fails, do not silently repair the design after seeing solver outcomes, generate replacement bodies, or exceed 150. Stop and report the exact blocker to the owner.

## 16. Final scientific restriction

This 150-body population can help characterize the specified LC518 failure mechanisms and examine matched correctness changes under the declared construction process. It cannot establish a universal taxonomy of failure, a universal law of solver correctness, or transport to natural/independently generated solver populations or other tasks.

The central question remains: does structured information about how a solver fails help us understand or predict its correctness on separate inputs, beyond what the baseline failure count and declared context already tell us?