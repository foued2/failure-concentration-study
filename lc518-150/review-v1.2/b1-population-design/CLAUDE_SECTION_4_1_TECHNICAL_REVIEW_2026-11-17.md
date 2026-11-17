# Claude Bounded Technical Review: v0.21 §4.1 and Stage 2 Test-Battery Design

**Scope:** v0.21 §§4.1.1–4.1.6 (blob `8af908f6b0ad4cd060194a0a63f4914939f07756`, lines 739–1027), with supporting reads of §§3.4, 4.2–4.3, 5.1, 5.7, 8, 9 and the attempt-protocol passages at lines 230 and 833.
**Repository ref:** `gpt/b1-computational-plan-2026-11-14` at `1e894fe7e6c0b8f33a8e8534d4b717e260f4c000`.
**Independence:** Read from the blob directly. GPT's draft review was checked against the text, not adopted. Each GPT finding is marked confirmed, partly confirmed, or not confirmed.
**Limits:** Read-only and document-only. No toolchain selection or execution, no software install, no source acquisition, no candidate enumeration, no construction, no diagnostics, no outcomes, no simulation, no repository write.

## 1. Verdict

The architecture is internally coherent. The main rules fit together: staged freeze order, byte-exact equivalence after hashing, a target-centred context slice, fail-closed handling of unsupported constructs, uniform attempts with no majority vote (v0.21 lines 230 and 833 prohibit it), and a per-operator catalog frozen before the abstract domain is chosen.

It is not executable yet. The document specifies properties but does not specify how to test the analyser, its terminal statuses are named but not defined, the input contract it depends on is never defined, and the toolchain is not pinned to binaries. Stage 2 feasibility is unestablished.

## 2. Confirmation of GPT's four findings

**F1, no Stage 2 test battery. Confirmed, and blocking.** §4.1.2 and §4.1.3 require reviewers to approve a profile, but nothing in §4.1 requires fixtures, expected outputs, or pass criteria. Two runs agreeing show reproducibility, not correctness; a consistently wrong analyser passes that check. Section 2 of this review gives the battery.

**F2, semantic/analysis-error disposition. Partly confirmed; GPT overstated the gap.** §4.1.1b (line 833) states that a deterministic work-cap hit or semantic/analysis error is not retryable under the same profile, and that an unresolved candidate cannot be admitted. §8 item 13 requires these dispositions to be "distinct." So the names and the downstream consequence exist. What is missing is their definitions, the evidence each requires, and a rule separating a semantic error in the analysed program from a defect in the analyser, from an unsupported construct, and from a malformed external summary. Those are different cases and currently share one label. Blocking before Stage 1 contract review.

**F3, input contract is undefined. Confirmed, and the strongest finding.** I searched §4.1 and the surrounding text. "Declared input contract" appears more than a dozen times, including as the basis for abstract-domain adequacy (lines 126, 827, 843–853, 913, 944), and it is never defined. Its contents, sources, and assumption labels are not specified anywhere.

I add a point GPT did not raise. §5.1 requires the protected evaluation set to have "the formal input domain and admissibility constraints," and §4.1 requires a static input contract. Nothing requires these two objects to coincide. If they differ, the abstract values are sound over one domain while the evaluation runs over another. Blocking before Stage 1 contract review, and a reconciliation requirement belongs in §5.1 as well.

**F4, search-inventory completeness. Confirmed.** §4.1.6 hashes the inventory, which proves identity, not completeness. "Complete relative to the frozen predicate" is circular when the same team writes the predicate and the check. Remedy: a separately implemented reference enumerator over the same frame, a known-answer corpus, and a reported disagreement count. Blocking before Stage 2 acceptance.

## 3. Findings

Classes: **B1** blocking before Stage 1 contract review; **B2** blocking before Stage 2 profile acceptance; **M** material clarification; **N** non-blocking.

| ID | Class | Section | Finding | Proposed correction |
|---|---|---|---|---|
| R1 | B1 | §§4.1.1a–c, 5.1 | Input contract undefined; not reconciled with the §5.1 protected-set input domain | Define the contract (schemas, preconditions, ranges, environment, out-of-contract handling, assumption labels) in Stage 1; require §5.1 to state that its domain is contained in it |
| R2 | B1 | §4.1.1b, line 833; §8 item 13 | Terminal statuses named, not defined; analyser defect, semantic error, unsupported construct, and malformed summary share one label | Adopt a closed status set (see Section 4) with an entry condition, evidence requirement, and next step for each |
| R3 | B2 | §4.1.1b, 4.1.2 | No fixture battery, expected outputs, or pass criteria | Adopt the battery in Section 2; freeze criteria before running it |
| R4 | B2 | §4.1.5 B.1 | "First relevant observable boundary" not defined; two implementers could cut slices differently | Define the boundary: propagate through return values, writes to escaped or shared state, IO, exceptions, and callbacks until each is discharged; a cut point needs a documented rule |
| R5 | B2 | §4.1.1a–b | Only tool version strings and profile digest; no binary or source hashes for parser, canonicaliser, abstract interpreter, serialiser, or external-summary library, although these can change independently | Require hashes of each analyser binary or source release and each dependency, recorded in the profile manifest |
| R6 | B2 | §4.1.6 | Search completeness not independently testable | Require a second, separately implemented enumerator over the same frame, a known-answer corpus, and a disagreement count reported as an output |
| M1 | M | §4.1.5 | Unions, unsafe pointers, inline assembly, and dynamic loading are absent from §4.1 (zero matches). The generic fail-closed rule for unmodelled control-flow constructs and unknown effects probably covers them, but this is not stated | Add an explicit list of unsupported classes, each defaulting to UNRESOLVED |
| M2 | M | §4.1.5 B.7, C | Concurrency treated only as "unresolved unless modelled." No memory model, data-race, or synchronisation abstraction | State that concurrent code is outside Stage A scope unless and until a memory model is specified and validated |
| M3 | M | §4.1.1b | Deterministic counters are relative to the pinned implementation (line 206), but cap values are UNKNOWN, and the spec requires them pinned before enumeration without saying who calibrates them or on what data | Calibrate caps on fixture-only data, never on the parent code or candidate frame; record the calibration corpus hash |
| M4 | M | §4.1.1b, 4.1.6 | Cross-profile comparability is stated (re-enumeration required). What is missing is an explicit prohibition on joining old and new inventories | Add the joinability prohibition as a sentence in §4.1.6 |
| M5 | M | §4.1.5 C | Strict float rules and havoc-by-default for external calls may leave most sites with floating-point or I/O unresolved | Not a defect, but a feasibility risk; measure in a pilot before any count is set |
| M6 | M | §4.1.4 (catalog) | Per-operator catalogs are required but the schema has no worked example | Add one worked example per operator class in the Stage 1 contract |
| N1 | N | §4.1.1a | Edge vocabulary completeness depends on the language; the spec already requires a generic OTHER edge to be prohibited | No change needed |
| N2 | N | §4.1.1b | Analysis-profile manifest will be long; hashing is fine | No change needed |

## 4. Attempt-status set (proposed closed set for R2)

| Status | Entry condition | Retryable? | Site admission |
|---|---|---|---|
| PASS | Two byte-identical complete envelopes within A_max | n/a | Eligible |
| FAIL_CONFORMANCE | Structural mismatch after masking W_q | No | Excluded |
| FAIL_CONTEXT | Canonical context bytes differ | No | Excluded |
| FAIL_VALUE / FAIL_EFFECT | Abstract value or effect profile differs | No | Excluded |
| UNRESOLVED_WORK_CAP | Deterministic cap reached before closure | No | Inadmissible |
| UNRESOLVED_UNSUPPORTED | Construct or summary outside the profile's model | No | Inadmissible |
| UNRESOLVED_SEMANTIC_ERROR | Deterministic error in the analysed program's abstract semantics, with evidence | No | Inadmissible |
| UNRESOLVED_ANALYSER_DEFECT | Analyser crash, exception, or instrumentation fault | No (under this profile) | Inadmissible until a new profile passes the battery |
| UNRESOLVED_HASH_MISMATCH | Hash equal, bytes differ | No | Inadmissible; defect logged |
| UNRESOLVED_NONDETERMINISTIC | Two complete envelopes differ | No | Inadmissible |
| OPERATIONAL_INTERRUPT | Interruption before closure; environment reproducible | Yes, within A_max | Not a semantic result |
| ENVIRONMENT_MISMATCH | Recorded environment cannot be reproduced | No substitute environment | Unresolved |

Each status needs an evidence record that names the artefact and hash it relies on.

## 5. Stage 2 test battery (design only)

Each family must have: an ID; the property tested; a fixture source and hash, written before any tool runs on it; positive and negative cases; the expected result, fixed in advance; the pass criterion; the failure disposition; and a named reviewer independent of profile construction.

| Family | Fixture classes | Expected assertion | Fail-closed disposition |
|---|---|---|---|
| T1 Canonical labelling | Isomorphic graphs with permuted IDs; non-isomorphic graphs differing in label, edge type, multiplicity, or attribute | Isomorphic: identical bytes. Non-isomorphic: different bytes | Profile rejected |
| T2 Serialisation | Permuted unordered sets; ordered arrays; large integers; rationals; intervals; Unicode; floats (must be rejected) | Stable JCS output; typed values exact | Profile rejected |
| T3 Normalisation | Alpha-renamable locals; observable names; overloads; macros; generated code; ambiguous source maps | Only declared unobservable names normalise; ambiguous maps fail | Site unresolved |
| T4 Control flow | Branch polarity; loops; switch fall-through; throw/catch; cleanup; RAII; non-local jumps; coroutines; traps | Distinct edge types retained; unsupported forms unresolved | Site unresolved |
| T5 Data, alias, effect | Reaching definitions; aliases; pointer targets; escapes; callbacks; unknown calls | Sound over-approximation; unknown effects havoced | Site unresolved if effects can matter |
| T6 Predicate catalog | Boundary values; congruence and relational cases; each allowed parameter level | Each required partition receives the expected true/false/both/unresolved result | Parameter level excluded before enumeration |
| T7 Floating point | Signed zero; NaN classes; infinities; subnormals; rounding; overflow; FMA; fast-math | Exact bit semantics preserved; unsupported distinctions unresolved | Float-sensitive use inadmissible |
| T8 Determinism and caps | Just under cap; at cap; over cap; repeated runs; interruption; environment change; deliberate semantic error | Correct status from Section 4; no cap extension | Per status |
| T9 Search completeness | Known complete tree; nested and macro patterns; generated files; exclusions; malformed files; reordered filesystem; deliberately missing match | Complete relative to predicate; no duplicates; byte-stable inventory; seeded miss detected | Inventory unresolved |
| T10 Analyser defect detection | Seeded faults in canonicaliser, context slice, and abstract transfer functions | Each seeded fault is detected by at least one family | Battery insufficient; profile rejected |
| T11 Envelope stability | Two fresh processes, same input; deliberate profile change; deliberate nondeterminism | Equal envelopes for equal inputs; mismatch terminal; changed profile has new digest | Per status |

T10 is the one family GPT's review does not propose. Without it, a battery can pass while detecting none of the defects that matter.

## 6. What finite fixtures can and cannot establish

Fixtures can show that a defect exists in the tested constructs and can measure detection power against seeded faults. They cannot establish soundness for untested constructs or for programs in general. Soundness needs a separate argument: a proof sketch or formal reference for the abstract domain and transfer functions, plus assurance that the tool release is the one that was tested. A passed battery licenses only the conformance it actually covers. Any report should separate three things: formal or design argument, test coverage, and residual limitation.

## 7. Recommendation

The §4.1 architecture is suitable for a design-level review but not for Stage 2 acceptance. Before Stage 1 contract review: R1 and R2. Before Stage 2 profile acceptance: R3 through R6 and the Section 4 status set. Material clarifications M1 through M6 should be resolved before any concrete profile is instantiated. No profile may be instantiated, and no enumeration may run, until the battery in Section 5 is written, frozen, and executed under its own authorization.
