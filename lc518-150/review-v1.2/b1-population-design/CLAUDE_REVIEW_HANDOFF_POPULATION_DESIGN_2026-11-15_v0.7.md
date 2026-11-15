# Claude Review Handoff: LC518 Population and Experimental Design v0.7

**Date:** 2026-11-15  
**Status:** READ-ONLY REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** \`gpt/b1-computational-plan-2026-11-14\`

## 1. Exact review target and controlling references

Please review the complete population and experimental design specification v0.7:

- **Path:** \`lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.7.md\`
- **Commit:** \`32bebbff605c2204f24ad400ba6d8d48bab81235\`
- **Blob:** \`81f4a4dba051883916958713cfa9ee1acd69fc03\`
- **Dimensions:** 111,637 UTF-8 bytes; 901 LF-delimited lines; 0 CR; final newline.

The immediate predecessor v0.6 remains unchanged:
- last content-changing commit \`66c6117d65b20179c29fb95bb9d43ed87de2f75b\`;
- blob \`367f3fc12956a546e85b39a749bbaf16b8a95fb4\`;
- later branch snapshot \`a592fd532e6e7b5e281af955d5553639096b4611\` added the final-newline correction to the v0.6 handoff without changing the v0.6 specification blob.

The controlling accepted predecessor artifacts are:
- **Rev 1.4 Amendment E:** commit \`b8b8af042c16eeb9e02077c781ab05c582eeb65d\`, blob \`3728146356a74363a94fe75a87fd06c483954ee2\`.
- **Rev 1.4 Amendment E acceptance record:** commit \`ca15a29bd25c4c9c2293394f67cb19e1a18f34bd\`, blob \`074b40980eb96d164cd8411c8995bb1db4af0d46\`.
- **B1 v1.7:** commit \`c3abe107acd2a3f8be58bf933eafcd734823a129\`, blob \`8c666e501a31726c728447d155045c0b20adc178\`.
- **B1 v1.7 acceptance record:** commit \`ac06c6676982eed795db9cb04c6d91803b591ac7\`, blob \`ea51d72f4f85c5d832d72add561b4c93472c364a\`.

Rev 1.4 Amendment E is accepted for the symbolic B1/M1 feasibility specification. B1 v1.7 is accepted and frozen as a symbolic analysis plan. Neither acceptance is an execution GO.

## 2. Domain clarification

**LC518 is a computer-science and software-engineering study.** “Mutation,” “mutation operator,” “variant,” “parent,” and “realization setting” refer to source-code transformations and derived software implementations. There are no biological, genetic, or organism-level meanings.

A mutation is a controlled transformation of solver source code; a parent is an original solver implementation; a variant is a traceable modified implementation; and a realization setting specifies a permitted within-operator-class setting.

## 3. Decision history: Option A versus Option B

Please preserve this history exactly:

- In the review of v0.3, Claude recommended **Option A**, conditioning the primary analysis on \(\mathbf a(v)\), with identifiability reported.
- Claude also said Option B could be acceptable if the claim explicitly named the realization-setting limitation.
- GPT independently chose **Option B** for v0.4: retain the exact-cell primary target \((q,Z,k,\ell)\), leave \(\mathbf a(v)\) outside the baseline, and prohibit direct, causal or parameter-independent interpretation of a positive result.
- Claude's v0.4 review accepted that Option B was consistently stated and its proxy/non-identifiability limitation was correct. Claude did not retract its original preference for A.

Option B remains GPT's adjudicated decision, not a joint preference.

## 4. Main changes in v0.7

### 4.1 Canonical graph form and source normalization

Section 4.1.1a now requires a genuine canonical-labelling algorithm for typed, directed, edge-labelled multigraphs. The algorithm must return byte-identical canonical forms if and only if the labelled graphs are isomorphic under the declared graph semantics. A deterministic traversal or a hash of arbitrary traversal order is not sufficient.

The specification pins RFC 8785 JCS as the canonical JSON serialization contract, prohibits floating-point values in signatures, and defines typed exact encodings for large integers, rationals and intervals.

It also defines source/symbol normalization:
- fully qualified semantic identities for global, external, member, type and overload symbols;
- alpha-normalization for local bindings only where local names are unobservable under the declared language/runtime contract;
- preservation of semantically observable identifiers and literals;
- explicit macro expansion/source mapping and generated-code provenance;
- source path/line/column metadata retained in the candidate manifest but excluded from canonical graph labels, with target position represented structurally.

Please challenge whether any naming, macro, generated-code, Unicode, graph-automorphism or source-mapping edge case remains unresolved.

### 4.2 Two-stage profile freeze

Section 4.1.1b separates two gates.

**Stage 1** freezes the design-level static-analysis contract before population/design freeze: required outputs, graph/canonical-form properties, language-transfer coverage, normalization rules, abstract-domain adequacy criteria, fail-closed rules and the permitted selection procedure for tools.

**Stage 2** instantiates actual compiler/front-end/parser versions, build configuration, call-graph/points-to/alias configuration, CFG/exception model, abstract domain, graph-labelling implementation and serializer for each selected parent/operator. This happens after the parent/source revision is selected but **before candidate-site enumeration**. The actual profile is hashed and independently reviewed before the syntactic search begins.

The design does not claim that any Stage 2 profile has already been instantiated: no parent language or build environment has yet been selected. Please assess whether the Stage 1 contract and Stage 2 instantiation rule resolve the apparent tension between freezing the design now and selecting compatible tools later.

### 4.3 Control-flow completeness

Section 4.1.5(B) adds a language-specific edge inventory, including exception propagation through callees, cleanup/finally/defer/finalizers, destructor/RAII unwinding, non-local jumps, coroutine/async continuation and language-specific trap/termination behaviour. Unsupported or unresolved relevant control flow excludes site relocation.

Please identify missing language-level transfers or cases where the rule still permits unlike contexts to be treated as equivalent.

### 4.4 Abstract-domain adequacy

Section 4.1.5(C) requires the abstract domain to be selected from operator semantics, operand types, parameter levels and the declared input contract before candidate-site enumeration. Each operator class must list the relevant predicates/effect partitions that the domain is required to resolve.

The site comparison requires exact equality at the frozen abstraction and matching truth/possibility/effect profiles for all declared operator-relevant predicates. TOP/unknown or unresolved relevant information fails closed. The text explicitly states that this is equality under the declared abstraction, not proof of concrete program or observational equivalence.

Please challenge:
- whether the domain is sufficiently discriminating for value-sensitive operators;
- whether the pre-enumeration selection rule prevents candidate-driven tuning;
- whether the abstraction-level limitation is honest and sufficient;
- whether any rule would be unimplementable or over-restrictive for plausible languages.

### 4.5 Parameter variation, inventory and one invocation

Every intended literal/threshold/extent level must record its abstract relation to the reachable input range and its abstract transfer/effect profile. Site relocation remains a separate coordinate and must pass context/value equivalence at shared parameter settings.

Section 4.1.6 freezes the syntactic search frame before enumeration, enumerates every site meeting the frozen predicate, retains rejected/unresolved candidates and reasons, and hashes the complete inventory before construction.

The one-operator-invocation-per-version rule is explicitly labelled as a **new population-design restriction**, not as an inherited requirement of B1 v1.7 or Rev 1.4. Multiple coordinated edit hunks may implement one atomic operator invocation; independent invocations may not be composed in one variant.

Please assess whether this restriction is compatible with the B1/M1 identity structure and whether the interaction clause correctly treats coordinated edit hunks without becoming a multi-operator review.

## 5. Requested review

Please read the exact v0.7 text, not only this handoff. Classify each finding as **blocking**, **recommended**, or **accepted**, and identify the precise section/wording:

1. Canonical-labelling property and graph/serialization uniqueness.
2. Local-name normalization, semantic symbol identity, macros, generated code, Unicode and source mapping.
3. Language-complete control-flow edge vocabulary, including exception/cleanup/unwind and non-local transfer.
4. Abstract-domain adequacy, operator-relevant predicate/effect partitions, fail-closed conditions and protection from candidate-driven tuning.
5. Whether equality under the frozen abstraction is described honestly and without implying concrete behavioural equivalence.
6. Parameter-level abstract range/effect reporting and separation from site relocation.
7. Stage 1/Stage 2 profile timing, review and hash provenance.
8. Completeness of the syntactic search frame and candidate inventory, including rejected/unresolved sites and reasons.
9. Call-graph resolution-integrity role.
10. One operator invocation per version, including compatibility with B1/M1 and atomic multi-hunk edits.
11. Consistency with accepted Rev 1.4 Amendment E and B1 v1.7.
12. Any remaining scientific, governance, or execution blockers.

## 6. Current boundary

v0.7 is an unreviewed, design-only draft, not frozen and not an execution authorization. The Stage 2 profile is not instantiated because parents have not been selected. The independent custodian remains unappointed. Trigger-(i) ratification and joint-consent provenance remain open. No parent, operator class, site, realization setting, variant or allocation has been selected. No solver construction, diagnostics, protected-set access, fitting, sampling, simulation or analysis is authorized.

Please provide a read-only review only. No repository changes or execution are part of this request.