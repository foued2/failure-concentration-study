# GPT Adjudication: Claude's Bounded Review of v0.21 §4.1 and Stage 2 Test-Battery Design

**Date:** 2026-11-17  
**Artifact class:** GPT technical adjudication of a one-time owner-authorized Claude review, plus design-level disposition of Stage 2 test-battery requirements. Not a v0.21 replacement, not a freeze, not a toolchain approval, not a test-execution authorization, and not a general reinstatement of the Claude review route.  
**Target:** `POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.21.md`, blob `8af908f6b0ad4cd060194a0a63f4914939f07756`, §§4.1.1–4.1.6 (lines 739–1027), with supporting §§3.4, 4.2–4.3, 5.1, 5.7, 8, and 9.  
**Review input:** `CLAUDE_SECTION_4_1_TECHNICAL_REVIEW_2026-11-17.md`, as uploaded in this conversation; SHA-256 `96e919b50419ba9788601917d79af48b52cb2b836ff19d57bd801fc293ed86c8`, 92 lines, final newline.  
**Protocol comparison input:** `CLAUDE_EXPLORATORY_PROTOCOL_ALTERNATIVE_DRAFT_2026-11-17.md`, as uploaded; SHA-256 `c6b869a47b1b8832ff33ad3f9742a43a8f43586fd5fec3cc39f69f4aa3a6bb8e`, 92 lines, final newline.  
**GPT drafts compared:** `LC518_SECTION_4_1_TECHNICAL_REVIEW_DRAFT.md`, SHA-256 `57ba80ce09a5d46f9677a0da88ae9fcb7476c2e5b3a8bb91921fe0debc8f763a`; and exploratory protocol draft 0.1, SHA-256 `a0ea61a452dff891d4c7bc7772f63dec9df002021b52f0c782aaf0ceebdd78f5`.  
**Scope:** Read-only adjudication and document consolidation. No toolchain selection/execution, source acquisition, candidate enumeration, construction, diagnostics, outcomes, simulation, or restricted data access was performed under this review.

## 1. Overall disposition

**CONCUR with Claude's central verdict: §4.1 has a coherent and conservative architecture, but Stage 2 is not executable or validated yet.** The section has unusually strong requirements for canonical graph representation, target-centred context closure, operator-relevant abstract values/effects, static-analysis profile pinning, deterministic resource budgets, repeated-run consistency and fail-closed treatment. It nevertheless states properties that an implementation must satisfy without yet providing the validation battery, status taxonomy, input-contract definition, binary provenance or independent search verification needed to demonstrate those properties.

Claude's review materially improves GPT's initial four-finding review. I accept the additional distinction about the extent of the existing semantic/analysis-error rule, the input-domain reconciliation issue, the proposed second enumerator, the test-battery additions, and the operational clarifications below. I do not accept every proposed formulation literally; the qualifications in this note govern.

## 2. Adjudication of GPT's four original findings

### F1. No Stage 2 test battery — CONFIRMED, BLOCKING BEFORE STAGE 2 ACCEPTANCE

v0.21 specifies desired static-analysis properties and two byte-identical complete attempts, but no fixture battery with predeclared expected results, positive/negative cases, coverage claims, pass criteria and failure dispositions. Repeated identical outputs establish reproducibility of the observed computation, not correctness of the analyser: a deterministic defect can reproduce itself.

A finite test battery, combined with a separate soundness/assurance argument, is required before accepting a concrete Stage 2 profile. The battery must be designed and reviewed before execution; its expected outcomes must be fixed before tools run. Tool execution on fixtures requires a separate owner GO and does not authorize analysis of parent source code or candidate sites.

### F2. Semantic/analysis-error disposition — PARTLY CONFIRMED; GPT'S ORIGINAL WORDING WAS TOO BROAD

Claude is correct that v0.21 §4.1.1b already states a deterministic work-cap hit or semantic/analysis error is not retryable under the same profile, and §8 item 13 requires distinct dispositions. Therefore the rule is not wholly absent. What is missing is an operational taxonomy: entry conditions, evidence records, retryability, scope (attempt/site/pair/profile), and downstream admission consequences. A deterministic source/front-end semantic error, unsupported construct, malformed external summary, analyser crash/defect, instrumentation fault and operational interruption cannot share one undifferentiated status.

Adopt a closed status taxonomy before Stage 1 contract review. The proposed taxonomy in §4 is a design disposition, not an amendment to v0.21. It separates profile/attempt/site outcomes from pairwise site-equivalence decisions. In particular, different context bytes mean two sites are **not equivalent for a site-relocation contrast**; they do not necessarily invalidate either site for a predeclared fixed-site parameter-variation design.

### F3. Input contract — CONFIRMED, HIGHEST-PRIORITY STAGE 1 BLOCKER

The phrase “declared input contract” is repeatedly used as the basis for abstract-domain soundness and site-value classification, but v0.21 does not define its contents, provenance, or out-of-contract treatment. This is a substantive gap, not editorial polish. A sound over-approximation relative to an unstated or post hoc narrowed input domain is not meaningful.

The Stage 1 input contract must include input schemas/types/encodings, preconditions and invariants, legal value ranges and relations, external/environment assumptions, observable outputs and side effects, invalid/out-of-contract handling, and provenance or assumption labels. It must be frozen independently of candidate yields, diagnostics, `C_D`, support and correctness.

Claude identifies a further necessary reconciliation: v0.21 §5.1 requires a formal input domain and admissibility constraints for the protected evaluation set, while §4.1 relies on the static-analysis input contract. The future Stage B protected input domain must be reconciled with the relevant solver input contract. For Stage A, the diagnostic inputs and correctness-evaluation corpus must also be within, or explicitly reconciled to, the frozen Stage A solver input contract. This does not require Stage A and future Stage B to use the same dataset; it requires that neither be evaluated outside the domain for which the static-analysis assumptions are claimed.

### F4. Search-inventory completeness — CONFIRMED, BLOCKING BEFORE CANDIDATE ENUMERATION ACCEPTANCE

A hash establishes the identity of an inventory, not that the enumerator found all matches within the frozen search frame and predicate. The phrase “complete relative to the frozen predicate” requires an independently testable implementation and fixture-based verification.

Require a known-answer corpus with positive, negative, nested, macro/generated-source, excluded-file and malformed-input cases, plus a separately implemented reference enumerator applying the same normative predicate over the same frozen frame. Compare canonical match identities and report misses, extras and duplicates. All discrepancies must be explained and resolved before enumeration is accepted. This second enumerator is a cross-check, not a proof of universal completeness; its own test coverage and shared dependencies must be documented.

## 3. Adjudication of Claude's additional findings

| ID | GPT disposition | Adjudication |
|---|---|---|
| R4: “first relevant observable boundary” | **ACCEPT, Stage 2 blocker** | Define the observable-boundary schema and propagation/cut rule before accepting a profile. Include return values through callers, writes to escaped/shared/global state, IO, exceptions/unwind, callbacks, synchronization and termination where relevant. A cut is allowed only at a declared boundary with a sound summary. Unbounded/unknown effects remain unresolved. |
| R5: tool binary/source hashes | **ACCEPT, Stage 2 blocker** | Pin cryptographic hashes for the parser/front end, compiler components that affect semantic output, graph canonicalizer, abstract interpreter, serializer, instrumentation, relevant libraries and external-call summaries. Record binary digests or source-release/build provenance when binaries are not directly attestable. Version strings alone are insufficient. |
| R6: independent search enumerator | **ACCEPT WITH SCOPE LIMIT** | Require a separately implemented enumerator plus known-answer corpus and disagreement report. It is an independent cross-check of the declared predicate, not a proof that the predicate itself captures every conceivable mutation opportunity. |
| M1: unsupported language/features | **ACCEPT** | Explicitly list unions/union punning, unsafe pointer operations, inline assembly, dynamic loading, reflection, FFI/native boundaries, generated/dynamic code and other unsupported constructs. Each defaults to unresolved unless the profile explicitly models it soundly. |
| M2: concurrency | **ACCEPT** | Distinguish serial execution of the analyser from concurrency semantics in the analysed solver. Stage A excludes concurrent/shared-memory code unless a language/runtime memory model, atomics, happens-before/synchronization, data-race and shared-state treatment are specified and validated. |
| M3: deterministic cap calibration | **ACCEPT WITH SCOPE LIMIT** | Calibrate deterministic work-counter caps on a predeclared fixture-only corpus, never on selected parent source or candidate-site counts/yield. Hash the calibration fixtures, tooling and rationale. Caps are profile-specific and frozen before enumeration. |
| M4: cross-profile inventory joining | **ACCEPT** | State expressly that inventories/equivalence conclusions from different profile digests are not joinable as one candidate pool or one support result. Each new profile requires full re-enumeration; earlier inventories remain separately archived. This sharpens, rather than reverses, v0.21's existing re-enumeration rule. |
| M5: stringent float/havoc feasibility | **ACCEPT AS FEASIBILITY RISK, NOT A REASON TO RELAX RULES** | Record unresolved rates and excluded site classes under the authorized Stage A protocol. Do not weaken float or unknown-call rules to improve candidate yield. Any feasibility measurement is descriptive and cannot drive post-freeze site selection or alter the same cohort. |
| M6: worked operator-catalog example | **ACCEPT WITH SEQUENCING CORRECTION** | Stage 1 should include a generic worked example of the catalog schema. A worked example for each actual operator class belongs at that operator's contract gate, after `q` and operand types are defined but before Stage 2 domain selection and site enumeration. Stage 1 cannot invent examples for operator classes not yet specified. |
| N1: language-specific edge vocabulary | **NO CHANGE** | v0.21 already requires a language-complete vocabulary and rejects collapsing semantically distinct control transfers into a generic `OTHER` edge. |
| N2: long profile manifest | **NO CHANGE** | Length is not a substantive defect; canonicalization, hashing and complete provenance are appropriate. |

## 4. Proposed terminal-status taxonomy

Claude's table is directionally correct, but it mixes attempt-level, site-level, profile-level and pairwise outcomes. The following scope separation is required. It is a proposed status model for the Stage 1 contract and Stage 2 test plan.

| Scope | Status | Entry condition | Retry / next step | Admission consequence |
|---|---|---|---|---|
| Attempt | `COMPLETE` | Analysis closes without deterministic cap, error or interruption | No retry implied | Not sufficient alone; needs the second independent complete envelope |
| Attempt | `OPERATIONAL_INTERRUPT` | Predeclared OS/container/hardware interruption before closure, with exact environment reproducible | Retry only within frozen `A_max` and identical profile/environment | Not a semantic result |
| Attempt | `ENVIRONMENT_MISMATCH` | Required pinned environment cannot be reproduced or environment manifest differs | No substitute environment; restore exact environment only under a predeclared rule | No result/admission |
| Site/profile | `PASS_STABLE` | Two fresh complete attempts within `A_max` yield byte-identical canonical semantic-result envelopes; all conformance requirements pass | No extra attempts after a completed mismatch | Site may be classified under that profile, subject to pairwise comparison and review |
| Site | `FAIL_Q_CONFORMANCE` | Unmasked structural/operator fingerprint differs from frozen `F(q)` | No retry; a different `q` requires prospective reviewed design before construction | Not valid under that `q` |
| Site pair | `NOT_EQUIVALENT_FOR_SITE_RELOCATION` | Complete context/value/effect bundles differ between proposed alternative sites | No retry; do not claim a site-only contrast | Pair cannot be used as a site-relocation pair; an individually admissible fixed-site design may remain separately eligible |
| Site | `UNRESOLVED_WORK_CAP` | Deterministic semantic work cap reached before closure | No retry by enlarging cap under same profile | Site inadmissible for relocation under that profile |
| Site | `UNRESOLVED_UNSUPPORTED` | Relevant construct/effect cannot be modelled soundly under the frozen profile | No retry under same profile; a changed scope/profile needs review and full re-enumeration | Site inadmissible under that profile |
| Site/profile | `UNRESOLVED_INPUT_OR_PROFILE_DEFECT` | Input contract, profile manifest, or required assumption is missing/inconsistent | Stop; correct and review before any new run | No admission under defective profile |
| Site/profile | `UNRESOLVED_SUMMARY_INVALID` | External-call/effect summary is malformed, unversioned or outside its declared soundness scope | No retry using the defective summary; replace only through a reviewed profile update | Affected site unresolved |
| Site/profile | `UNRESOLVED_SOURCE_OR_FRONTEND_SEMANTICS` | Parser/front-end cannot establish a valid, supported semantic representation for the source under declared language/build rules | No retry under same profile; diagnose source/build versus front-end issue | No admission until prospectively resolved |
| Profile | `UNRESOLVED_ANALYSER_DEFECT` | Internal analyser exception/crash, instrumentation defect, contradictory result, or seeded defect detection | No retry under same profile; repair, rehash, review and rerun the full battery under a new profile | All affected outputs under defective profile unresolved |
| Site/profile | `UNRESOLVED_HASH_MISMATCH` | Hash comparison indicates equality but canonical bytes differ, or manifest/hash integrity fails | No retry to select a preferred result; investigate integrity defect | No admission |
| Site/profile | `UNRESOLVED_NONDETERMINISTIC` | Two complete canonical result envelopes differ | Terminal under same profile; no majority vote or extra attempts | No admission |

A deterministic work-cap hit, unsupported construct, analyser defect, malformed summary, source/front-end semantics issue and operational interruption are not interchangeable. The exact error taxonomy, evidence packet and scope propagation must be frozen before Stage 2. An analyser defect discovered after testing invalidates affected results under that profile; a replacement profile requires review, a complete test-battery pass, and complete candidate re-enumeration. Do not mix old and new inventories.

## 5. Stage 2 fixture test-battery requirements

Every test family must have a stable ID, tested property, fixture source and hash, expected output/status fixed before execution, positive and negative cases, coverage rationale, command/tool digest, pass criterion, failure disposition, reviewer, and report reference. Unsupported constructs included as negative fixtures must return the predeclared unresolved status; that expected fail-closed result is a passing test assertion, not a test failure.

| Test family | Minimum fixtures | Required assertion |
|---|---|---|
| T1 Canonical graph labelling | Isomorphic graphs with permuted IDs/order; non-isomorphic graphs differing in node/edge labels, multiplicity or semantic attributes | Isomorphic inputs have identical canonical bytes; each declared material graph difference produces different bytes |
| T2 Canonical serialization | Ordered/unordered arrays, set permutations, large integers, rationals, intervals, Unicode/source encodings, prohibited JSON float values | Pinned JCS output is stable; typed exact values preserve specified semantics; unsupported representations fail closed |
| T3 Source and identifier normalization | Alpha-normalizable locals, observable names/literals, overloads, macros, generated code, ambiguous source-origin maps | Only declared unobservable names normalize; observable identities remain; ambiguous mappings are unresolved |
| T4 Control-flow and exceptional flow | Branch polarity, loops, switch fall-through, throws/catches, cleanup/finally/defer/RAII, indirect calls, callbacks, non-local jumps, async/coroutines, termination | Required edge types/propagation are retained; unsupported forms produce expected unresolved status |
| T5 Data, alias, state and effects | Reaching definitions, aliases/points-to, pointer targets, escapes, writes, IO, callbacks, synchronization and unknown calls | Expected over-approximation and havoc effects are produced; relevant unknown effects resolve to unresolved rather than omission |
| T6 Operator predicate/effect catalog | Exact and boundary values, intervals, congruence/relational cases, each parameter level and effect partition | Every catalog item produces its predeclared true/false/both/unresolved classification and effect profile |
| T7 Floating-point semantics | Signed zero, NaN classes/payload observability, infinities, subnormals, rounding, conversions, overflow/underflow, FMA/contraction and compiler modes | Exact bit-level distinctions are preserved; unsupported semantics yield expected unresolved status |
| T8 External summaries and unknown effects | Valid/invalid summaries, unknown return, memory, IO, exceptions, callbacks, concurrency and termination effects | Valid summaries match declared contract; malformed/out-of-scope summaries fail closed; havoc covers declared unknown effects |
| T9 Work caps and attempt protocol | Just-under/at/over deterministic caps; fresh-run tests; interruption; exact environment reproduction; changed environment; semantic/frontend error; analyser fault | Correct status, retryability and evidence packet; no cap extension, majority vote or selective retries |
| T10 Search completeness | Known-answer source trees; nested syntax; macros/generated files; exclusions; malformed files; filesystem order; seeded missed and extra matches | Primary and independent enumerator agree on canonical matches; known expected matches found, negatives excluded; discrepancy count zero or fully adjudicated before enumeration |
| T11 Seeded analyser-defect detection | Deliberately seeded canonicalizer, context-slice, abstract-transfer and instrumentation defects | Each seeded defect in the declared fault set is detected by at least one preassigned test; otherwise the battery is inadequate and the profile is rejected |
| T12 Envelope stability/profile separation | Same inputs in fresh processes; deliberate nondeterminism; deliberate profile/version change | Same frozen profile/input yields identical complete envelope; mismatch terminal; new profile digest cannot reuse/join old inventory |

The battery must also report the declared supported feature set and map each feature to fixtures and evidence. It must not imply that every possible language construct is tested. Finite fixtures can reveal defects and assess detection against the seeded fault set; they cannot prove universal soundness. A separate assurance argument is required for abstract-domain soundness, transfer functions, external summaries, and the soundness scope of the selected tools. Reports must distinguish formal/design arguments, tool/release assurance, fixture coverage/results and residual limitations.

### 5.1 Explicit unsupported-feature and concurrency rules

Unless a concrete Stage 2 profile explicitly supports and validates them, the following are unsupported and default to `UNRESOLVED_UNSUPPORTED` whenever they may affect the target context: union/union-punning semantics, unsafe pointer arithmetic or aliasing, inline assembly, dynamic loading, reflection, FFI/native calls, runtime code generation, unresolved callbacks/dispatch, and language-specific extensions absent from the model.

Serial single-worker execution of the static analyser is not a memory model for a concurrent program. Stage A must exclude concurrent/shared-memory solver code unless the profile declares and validates the relevant language/runtime memory model, atomics, synchronization/happens-before, data races, callbacks and shared-state effects. An unmodelled concurrent effect cannot be approximated by a sequential CFG merely to retain a site.

### 5.2 Observable-boundary rule

The operator effect closure must propagate through the first boundary that is observable under the frozen input/output and execution contract. The boundary schema must identify at least: returned values and their caller-visible propagation; writes to globals, escaped objects or shared/external state; IO and other external effects; exception/cleanup/unwind propagation; callbacks and re-entrant calls; synchronization/termination effects where in scope; and process exit/output channels. A cut is permitted only where the effect is discharged at a declared observable boundary or captured by a versioned, sound summary. If relevant effects cannot be bounded, the context is unresolved.

## 6. Gate order, authorizations, and protocol consolidation

The consolidated protocol in `LC518_EXPLORATORY_FEASIBILITY_PROTOCOL_DRAFT_0.2.md` incorporates GPT's original scope/non-adaptation/budget protections and Claude's additions: input-contract reconciliation, explicit diagnostic-probe design/freeze, an independent correctness oracle and validation, a separate owner GO for fixture-battery execution, OWNER-SET feasibility thresholds, and explicit Stage B boundaries.

The essential order is: owner route decision and protocol adoption; solver input contract and data-domain reconciliation; source frame/acquisition under GO; lineage and outcome-blind parent selection under separate GO; `q`/realization/catalog freeze; Stage 1 contract review; provisional Stage 2 profile and fixture-battery design; separate GO for fixture-only test execution; Stage 2 profile acceptance; frozen candidate search and independent-enumerator verification under separate GO; complete inventory freeze; variant schedule and source-diff freeze; diagnostic instrument/probe/capacity freeze; isolation probe under separate GO; mutation generation under separate GO; build/solver execution under separate GO; diagnostics under separate GO; correctness oracle generation/independent validation under separate GO; correctness evaluation under separate GO; closeout.

No GO may be inferred from protocol adoption, review completion, a Stage 2 test design, a GLM/Claude technical concurrence, or a successful earlier gate. Stage A outcomes are not used to justify Stage B's operating count or to adapt Stage A. No protected set, exposed 78-record bank, source repository, or solver is accessed by this adjudication.

## 7. Governance and route status

The owner instruction “DO ALL THREE” specifically authorized Claude to prepare the alternative protocol, complete this bounded §4.1 review, and later verify GPT's publication. This adjudication accepts that work as a one-time bounded review input. It does not generally reinstate the suspended Claude review route. The formal review path for the protocol remains governed by v0.21 §0.23 and the current owner decision, with GLM as the active formal route unless the owner separately changes it. Claude's review remains a separately attributed, one-time analytical input.

## 8. Final disposition and next actions

1. **Protocol:** use consolidated draft 0.2 as the current working draft. It remains inactive until the owner chooses exploratory and adopts the completed protocol; all owner-set ceilings remain blank/UNKNOWN.
2. **§4.1:** architecture is coherent, but Stage 1 remains blocked on the input contract and closed status taxonomy. Stage 2 remains blocked on a reviewed/frozen battery, soundness/assurance argument, tool/binary provenance, independent inventory check, observable-boundary rule and unsupported-feature scope.
3. **Testing:** no fixtures have been executed, no toolchain has been selected, and no site has been enumerated. A fixture-execution GO is still required.
4. **Execution:** no source, parent, mutation, solver, diagnostic, correctness, protected-data or analysis activity is authorized by this review.
5. **Repository:** the supplied Claude review and protocol alternative are preserved as separate historical inputs; the consolidated GPT documents are separate adjudication/draft artifacts. v0.21 is not edited. Master is not changed.

**Disposition:** GPT accepts Claude's central technical findings with the qualifications recorded above. No Stage 2 profile is approved, no new population specification version is created, and no execution authorization is issued.
