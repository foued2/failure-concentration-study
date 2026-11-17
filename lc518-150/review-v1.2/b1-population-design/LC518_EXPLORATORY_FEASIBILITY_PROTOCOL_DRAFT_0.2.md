# LC518 Exploratory Feasibility Protocol

**Draft:** 0.2 (consolidated GPT/Claude working draft)  
**Date:** 2026-11-17  
**Status:** Document-only proposal. The owner has not selected the exploratory route. This is not an owner decision, protocol freeze, source-access authorization, execution GO, B1 analysis-plan amendment, or protected-set authorization.  
**Repository basis:** `POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.21.md`, blob `8af908f6b0ad4cd060194a0a63f4914939f07756`; working branch baseline `1e894fe7e6c0b8f33a8e8534d4b717e260f4c000`; master baseline `33dca9b61d95b9fb750f750919c32c2e08b2ee90`.  
**Purpose:** Define a bounded, non-confirmatory feasibility study that could test whether the parent-lineage, operator-definition, static-analysis, construction, diagnostic, and correctness-evaluation pipeline can be executed reproducibly and safely. Adoption and every execution stage remain separately owner-gated.

## 1. Decision status and governing principle

This is a conditional proposal for Stage A, an exploratory feasibility study. The owner must separately choose whether to adopt the exploratory route. Until that choice and the protocol are recorded as adopted, this draft is inactive.

Exploratory status does not relax source licensing, provenance, privacy, isolation, safety, input-domain, data-access, or execution requirements. This document authorizes no source acquisition, parent selection, mutation allocation or generation, source modification, software installation, tool execution, solver construction, build, solver run, diagnostic probing, correctness-oracle creation, correctness evaluation, bank/protected-set access, fitting, simulation, or statistical analysis.

Every activity that accesses sources, runs software, modifies code, builds or executes a solver, probes diagnostics, creates or accesses outcomes, or processes study data requires a separate, explicit owner-issued GO. Each GO must identify the exact operation; repository/source/input identities and hashes; tool and environment hashes; operator; data boundary; input/output locations; permitted outputs; resource ceilings; logging requirements; and stop conditions. A GO for one stage does not authorize a later stage. Missing hashes, mismatched inputs, or an unapproved change to scope means no execution.

The study concerns deliberately engineered variants nested within selected, provenance-traceable parent implementations. It does not target the distribution of naturally occurring solvers and cannot support a parent-superpopulation claim.

The one-time owner instruction “DO ALL THREE” authorized Claude to prepare a document-only protocol alternative, conduct a bounded §4.1 review, and verify a later GPT publication. It is not a general reinstatement of the suspended Claude review route. The formal review route remains the one recorded in v0.21 unless the owner changes it separately.

## 2. Research purpose and claim boundary

### 2.1 Feasibility question

Can the project prospectively freeze and reproducibly implement a set of valid variants nested within independently verified parent lineages; define operator identity and realization settings without outcome-informed choices; satisfy the declared static-analysis contract; construct and build the planned solvers reproducibly; run a frozen diagnostic instrument; and collect correctness outcomes under an authorized, auditable evaluation protocol?

A central structural feasibility question is whether the realized design can satisfy the adopted M1-si condition: at least three distinct verified parents each contribute at least two unique valid variants to the same exact B1 cell, with distinct predeclared realization settings, distinct realized values of `C_D`, and distinct semantic-source and runnable-artifact digests. This condition is conditional on the separate B1 amendment retaining the proposed operator-class `q` coding. The requirement `P >= 3` is a mathematical support floor, not an operating-count recommendation. The selected Stage A parent count and maximum roster remain **UNKNOWN** until prospectively declared and bounded; neither three nor the historical 30-parent/150-variant logistics scenario is adopted as an adequate cohort.

### 2.2 Scientific interpretation boundary

The adopted primary target is Option B: incremental predictive information from `C_D` beyond the exact B1 cell `(q, Z, k_fail, k_unresolved)`, without conditioning the primary model on the realization-setting vector `a(v)`.

A positive Option B result may include predictive information carried through `a(v)`. It is not evidence of a direct, causal, or realization-setting-independent concentration effect. The adjusted sensitivity can address the direct/parameter-independent question only if sufficient residual `C_D` variation exists at fixed `a(v)` and exact cell. If that sensitivity is not estimable, the direct question remains unanswered; failure of that sensitivity does not invalidate the broader proxy-inclusive estimand.

Stage A is a feasibility study, not a confirmatory B1 test. It does not establish confirmatory predictive evidence, confirmatory precision or power, natural-solver generalization, or a direct concentration effect. Any Stage A descriptive correctness summary must be frozen in advance and labelled exploratory and conditional on the realized Stage A parents and variants. A formal exploratory predictive model or test is not authorized by this protocol; it would require a separate analysis plan, independent review, and owner GO.

### 2.3 Permitted Stage A conclusions

Subject to the applicable GOs, Stage A may report whether source provenance and lineage verification were operationally achievable; whether the Stage 1/Stage 2 static-analysis requirements could be instantiated without weakening them; whether the planned operator definitions and realization schedules could be applied reproducibly; whether planned variants built and executed under the frozen environment; whether every planned variant received an auditable diagnostic disposition; whether M1-si support was realized or shortfalled; whether correctness outcomes could be obtained under the frozen data/oracle protocol; and the observed operational costs, failures, unresolved cases, deviations, and stop-rule triggers.

A Stage A failure to realize M1-si is a design-feasibility result, not evidence that concentration has no predictive value. B1 support, M1-si realization, LOPO estimability, score coverage, fit availability, and outcome-side informativeness must be reported as separate statuses.

## 3. Input contract and evaluation-domain reconciliation

Before defining the per-operator predicate/effect catalogs or selecting a Stage 2 abstract domain, freeze a versioned **solver input contract**. At minimum it must state:

1. input schemas, types, encodings, dimensions, and admissible formats;
2. preconditions, invariants, legal ranges, boundary conditions, and any relations among input fields;
3. the source or elicitation basis for each constraint, with each statement labelled as established, assumed, or unknown;
4. relevant runtime, platform, locale, environment-variable, filesystem, external-state, nondeterminism, and resource assumptions;
5. observable outputs, process dispositions, and externally visible side effects relevant to correctness;
6. handling of malformed, invalid, or out-of-contract inputs; and
7. how the contract is represented, versioned, hashed, independently reviewed, and changed prospectively.

The contract must be frozen independently of candidate-site yields, diagnostic outcomes, `C_D`, support, correctness results, or preferred operator behaviour. A sound abstract-state claim is meaningful only relative to this declared domain and its assumptions.

Every input actually supplied to a candidate solver during Stage A diagnostics or correctness evaluation must be admissible under the frozen solver input contract, unless a distinct, explicitly defined input interface and contract is frozen for that stage. The Stage A diagnostic input set and correctness-evaluation corpus must be identified and hashed separately; their domains must be subsets of, or explicitly reconciled with, the applicable solver input contract. Out-of-contract inputs cannot be silently ignored or excluded after results are known. If the intended study operation requires a wider domain, widen and review the contract before Stage 2 profile instantiation and before construction.

The future Stage B protected-set domain is a separate B1 design input. Its formal domain and admissibility constraints must be reconciled with the Stage B solver input contract in the B1 amendment and protected-set specification. The Stage A exploratory corpus is not presumed to be the future protected set, and no protected-set equivalence is implied.

## 4. Non-adaptive design and outcome firewall

Before any candidate construction, diagnostic probing, or correctness evaluation, freeze and hash the complete applicable design package, including:

- the candidate source frame and licensing/provenance rules;
- lineage procedures, pairwise dispositions, cluster-coherence rules, and outcome-blind parent-selection procedure;
- selected parent roster, immutable source revisions, and source-tree digests;
- the solver input contract and the Stage A diagnostic/evaluation input specifications;
- each `q` specification, invariant semantics, canonical fingerprint, and permitted realization fields;
- each per-`q` predicate/effect catalog and its rationale;
- Stage 1 requirements and each Stage 2 profile, binary/dependency manifest, environment, deterministic counters, work caps, `A_max`, and test-battery results;
- syntactic candidate-site search predicate, independent-enumerator procedure, complete candidate inventories, and all rejected/unresolved site dispositions;
- complete mutation/realization schedule, planned variant roster, source diffs, validity/build/duplicate/exclusion rules;
- diagnostic strata, capacity vector, probe/instrument set, input hashes, scoring rules, and output schema;
- correctness-evaluation corpus, oracle/reference method, independent validation, scoring rules, and disclosure boundary; and
- resource ceilings, logs, GO records, deviations, and stop conditions.

Every planned variant remains in the accounting register. No parent, mechanism, identity, realization coordinate, parameter level, site, pair, or variant may be chosen, removed, replaced, reassigned, retuned, pooled, or selectively paired because of realized `C_D`, failure totals, unresolved totals, exact-cell membership, correctness outcomes, or model results. The complete planned roster and assignment schedule are frozen before construction and before diagnostics.

The realized-cell audit is descriptive over the complete planned and valid variant register. It is not a selection rule. A shortfall is reported under v0.21 §6.5; it cannot be repaired by pooling cells, selecting favourable pairs, replacing variants, or changing the mechanism schedule. A redesigned study requires a new reviewed design and separate authorization, with no pooling as though the original design had remained unchanged.

Stage A outcomes are not used to select or tune Stage A parents, mechanisms, variants, realization settings, or models. They are not estimates of the new study's between-parent predictive-loss variation and are excluded from the Stage B operating-count justification under v0.21 §2.5. Any external evidence transported into a later count justification must be labelled as an assumption, sourced, justified for transferability, and independently reviewed. Stage A records are not pooled with Stage B as though both arose under one frozen design. Any other proposed reuse must be specified prospectively in a separately reviewed and authorized Stage B plan.

## 5. Predeclared feasibility criteria

The final protocol must contain, before adoption, one evidence artifact, measurement rule, threshold, reviewer, and failure disposition for each criterion. Owner-set values must be supplied before adoption and cannot be inferred from prior counts. Criteria inherited from v0.21 (for example, M1-si's three qualifying parents, complete planned-variant accounting, and the two-complete-identical-envelope rule) are not relaxed by owner choice.

| ID | Criterion | Measurement and required evidence | Threshold/disposition |
|---|---|---|---|
| C1 | Independent parent lineages | Pairwise-coherent lineage clusters; provenance, licensing, blinded pairwise decisions, cluster-coherence and reviewer records | At least three qualifying parents are required for M1-si realization. The selected Stage A roster ceiling is OWNER-SET. If the eligible frame is insufficient, report shortfall; do not relax lineage rules. |
| C2 | Stage 2 test-battery conformance | Prehashed fixtures, expected outcomes, positive/negative cases, coverage map, run logs and independent review | Every test must produce its predeclared expected result. An expected `UNRESOLVED` for an explicitly unsupported feature is a passing assertion; an unexpected result is a test failure. Profile rejected on any unexplained failure. |
| C3 | Candidate-search inventory | Frozen search frame and predicate; known-answer fixture corpus; separate implementation of the same declared syntactic predicate; match-set comparison and discrepancy log | No unexplained misses, extras, or duplicate matches on the validation corpus; all discrepancies resolved before enumeration. The second enumerator is a cross-check, not proof of universal completeness. |
| C4 | Construction/build reproducibility | Complete planned-variant register; source/build manifests; independent rebuild records; semantic-source and runnable-artifact digests | 100% of variants admitted as distinct valid contributions must meet the frozen reproducibility and digest rules. Failures remain accounted for and are not replaced. |
| C5 | M1-si realization | Full exact-cell audit across all planned and valid variants and parents | Apply v0.21 §3.4 unchanged. If fewer than three parents qualify in one common exact cell, report `M1-si NOT REALIZED / MATCHED-SUPPORT DESIGN FAILURE`; no repair. |
| C6 | Diagnostic completeness | Reconcile every planned variant to a valid diagnostic record or a predeclared invalid/inapplicable/non-executable disposition | Every planned variant accounted for. Missing or unclassified records stop the audit. Invalid variants need not produce diagnostic outcomes but must have documented reasons. |
| C7 | Correctness-oracle validity | Variant-independent expected-output method, frozen corpus/hash, provenance, generator/version record, independent validation subset and discrepancy log | Agreement threshold OWNER-SET before evaluation. Any unresolved oracle discrepancy stops correctness evaluation; no candidate-derived oracle. |
| C8 | Analysis-attempt reproducibility | Complete envelopes from two independently initiated complete attempts within frozen `A_max`; per-attempt environment/profile digests | Apply v0.21 §4.1.1b. Two complete byte-identical envelopes required. Mismatch is terminal nondeterminism; no majority vote or extra attempts. |
| C9 | Budget and stop ceilings | Human hours, CPU/memory/wall time, tool attempts, diagnostic/evaluation resources and monetary ceiling if applicable | All ceilings OWNER-SET before adoption/GO. Reaching a ceiling stops the affected gate; no retrospective extension. |

The numeric threshold OWNER-SET fields must be completed before adopting the protocol. A threshold cannot be revised after diagnostic or correctness results are observed. “Zero failures” means zero unexpected fixture assertions or unresolved discrepancies, not that every construct must be supported: unsupported constructs must produce the expected fail-closed status.

## 6. Stage gates and required owner authorizations

The stages below are ordered. Documentary readiness or review does not authorize an execution stage. Each GO is separate and names the exact artifacts and hashes.

### G0. Owner route decision, protocol adoption, and ceilings

Required before Stage A starts: written decision adopting or rejecting the exploratory route; approved Stage A scope and non-claims; selected parent/variant/operator/language ceilings; human, compute, time, monetary and calendar ceilings; named responsible operators and reviewers; approved data-handling and incident-response arrangements; and independent review/GPT adjudication of the completed protocol. Route remains OPEN until this decision is recorded.

### G1. Solver input contract and Stage A data-domain definitions

Complete and independently review the solver input contract in §3, including the reconciliation of all Stage A diagnostic and correctness inputs. Identify separate diagnostic and correctness datasets and their domains. No source or solver execution is authorized by this gate. Any future Stage B protected-set domain is reconciled under its own B1 amendment.

### G2. Candidate source frame and source acquisition

Freeze the permitted source frame and eligibility/licensing rules as a document. A separate `GO-1` is required to acquire candidate sources. It must name the repositories, allowed operations, immutable revision requirements, hashes to record, storage and permitted outputs. Preserve source URLs/identifiers, exact commits or immutable revisions, tree digests, license evidence, provenance and retrieval logs. Do not access the exposed 78-record development bank under this protocol.

### G3. Lineage feasibility and parent selection

First assess the feasibility of the per-language-family reference units, positive and hard-negative lineage examples, blinded reviewers, adjudication capacity, and pairwise workload. Keep similarity-threshold calibration/validation distinct from the mandatory blinded pairwise dispositions that determine parent clusters. Similarity thresholds remain triage tools; failure to validate a threshold does not nullify the mandatory pairwise review. An unresolved lineage component contributes zero to eligible parent support and cannot be selected as a parent.

A separate `GO-2` is required for parent selection under the frozen, outcome-blind procedure. Freeze the full selected roster, canonical lineage identifiers, pinned source revisions, tree digests, exclusions and unresolved reasons. If the eligible frame cannot meet the predeclared Stage A roster requirement, report the shortfall; do not lower the lineage standard or silently continue as though the planned cohort had been obtained.

### G4. Operator contract and realization design

For each selected parent and proposed `q`, define the invariant transformation semantics, canonical fingerprint, permitted variable fields, typed realization coordinates, ranges/levels, assignment schedule, and scientifically independent rationale. Freeze each per-`q` predicate/effect catalog before Stage 2 profile/domain selection and before candidate-site enumeration. Include at least one worked catalog example for each actual `q` at this Operator Contract Gate. The Stage 1 contract may include a generic worked example of the catalog schema, but cannot invent examples for operator classes not yet defined.

### G5. Stage 1 static-analysis contract and review

Resolve the Stage 1 requirements in v0.21 §4.1.1b, including canonical graph model/property, supported language/control-flow requirements, source/macro/generated-code normalization, input-contract dependency, catalog schema, abstract-domain adequacy criteria, status taxonomy, unsupported-feature dispositions, and permitted Stage 2 profile-selection rule. Obtain the required independent review before Stage 2 instantiation. A Stage 1 review does not validate any concrete toolchain.

### G6. Provisional Stage 2 profile and test-battery design

After parent/source and `q`/catalog freeze, provisionally instantiate the language/build-specific Stage 2 profile. Pin all relevant tools, versions, binary hashes or source-release hashes, dependencies, canonicalizer, parser/front end, abstract interpreter, serializer, instrumentation, external-call summaries, compiler/build settings, execution image, environment, serial scheduling, deterministic counters, work caps and `A_max`.

Before any candidate-site enumeration, define and hash the test battery, fixture corpus, expected outputs/statuses, positive/negative cases, coverage map, pass criteria, failure dispositions, run commands, independent reviewer and fault-injection plan. Cap calibration must use fixture-only data, never selected parent code or candidate-site yields. The test author should be independent of the profile implementer where practicable. The battery design and provisional profile require review before execution.

### G7. Stage 2 fixture-battery execution

A separate `GO-3` is required to execute tools on the prehashed synthetic/reference fixtures only. It does not authorize analysis of parent source code or candidate sites. The test report must separate (a) formal/design soundness arguments and tool assurance, (b) finite fixture coverage and observed results, and (c) residual unsupported constructs and limitations. A finite battery can reveal defects and measure detection against seeded faults; it does not prove soundness for all programs.

The profile is accepted only if every predeclared assertion passes and the required soundness/assurance argument is adequate for the declared supported scope. An expected `UNRESOLVED` result for a construct explicitly excluded from the supported scope is a passing assertion. An unexpected unresolved result for a construct claimed as supported, any mismatch from a predeclared expected result, or a detected analyser defect rejects the profile. A changed profile requires new review and a fresh battery; no candidate enumeration under the failed profile.

### G8. Candidate-site search frame and inventory

Freeze the syntactic search frame/predicate before running it. Validate the enumerator against a known-answer corpus and a separately implemented reference enumerator applying the same normative predicate over the same declared frame. Report missed/extra/duplicate matches and all disagreements. The second enumerator is an independent cross-check, not a proof of completeness outside the tested frame.

A separate `GO-4` is required for candidate-site enumeration over the selected parent sources. Enumerate every match, including rejected and unresolved candidates. Hash the complete inventory, profile, source frame, predicate, and results. Inventories under different profile digests remain separate and must not be joined or pooled as one candidate population. A changed profile requires complete re-enumeration of the entire declared frame.

### G9. Variant schedule, source diffs, and diagnostic-blind identity review

Freeze the complete variant roster and assignment schedule, including site/parameter coordinates and source diffs, before construction. Preserve v0.21's one-operator-invocation restriction unless a separate reviewed amendment changes it. Site relocation and parameter-only variation remain distinct design operations. Any site-relocation pair must have exact within-parent canonical context/value/effect equivalence under the same frozen profile and shared parameter settings. Two diagnostic-blind reviewers must independently review the `q` identity, catalog, profiles, candidate inventory, site signatures, proposed diffs and variant schedule before construction or diagnostics. Unresolved disagreement blocks the affected `q`/variant schedule.

### G10. Diagnostic instrument and probe freeze

Design the diagnostic probes and instrument without access to variant identity, realized `C_D`, failure/unresolved totals, exact-cell membership, correctness outcomes, or model results. Freeze probe-generation code, probe/input corpus, hashes, expected diagnostic categories, scoring/classification rules, output schema and capacity vector before diagnostics. Bind the actual eight-stratum roster and per-stratum capacities `c_j`; do not assume the Rev 1.4 8-by-8 candidate grid. The capacity binding is a design decision and must be reviewed before it becomes operative.

The data dictionary must represent analytical `C_D` as `NA` when `k_fail = 0`, with a separate `NO_OBSERVED_FAILURES` status. No diagnostic execution is authorized by this gate.

### G11. Isolation readiness

A separate `GO-5` is required for the isolation probe. Test the exact execution image, host boundary, filesystem mounts, network, process, resource, clipboard/shared-folder and data-access controls that will govern subsequent work. A local sandbox setting is not itself proof of adequate isolation. Any failure or unexpected access stops the gate and triggers incident review. No solver build, source mutation or solver run is authorized by the isolation-probe GO.

### G12. Mutation generation, build, and solver execution

After G9 freeze and successful G11 isolation verification, a separate `GO-6` is required for source transformation/mutation generation from the frozen roster and schedule. It names parent/source/q/schedule hashes, exact allowed writes, output locations, tools and stop rules. No post-freeze changes are allowed.

A further `GO-7` is required for builds and any solver execution needed for build validation. It must name source, build manifests, tool binaries, execution image, run inputs, resource ceilings and permitted outputs. Verify semantic-source and runnable-artifact digests and duplicate rules. Every build/run disposition is retained; non-reproducible or invalid variants remain accounted for and are not replaced. Only the isolated environment approved at G11 may be used.

### G13. Diagnostic execution

A separate `GO-8` is required for diagnostic execution. It must identify the frozen instrument, stratum/capacity vector, probe/input hashes, variant-roster hashes, environment hashes, output schema and authorized operators. After diagnostics, audit every planned variant under the frozen validity rules; derive exact `(q,Z,k_fail,k_unresolved)` cells and `C_D`; enumerate all within-parent cell sets, realization settings and distinct `C_D` values; and report B1 support, M1-si realization, LOPO support and diagnostic shortfall separately. No post-diagnostic pair selection, replacement, pooling or retuning is permitted.

### G14. Correctness oracle and evaluation-corpus validation

Before correctness evaluation, freeze the exact Stage A evaluation corpus, its source/hash/license/access authority, solver-input-domain conformance, scoring rules, environment, output schema and disclosure boundary. The expected-correctness oracle/reference method must not depend on any candidate variant. Freeze its provenance, generator/reference version, input hashes and outputs; independently validate a predeclared subset before any correctness-evaluation run. A separate `GO-9` is required for oracle/reference execution and validation. An unresolved oracle discrepancy stops correctness evaluation.

The exposed 78-record development bank is not accessed under this protocol. No protected confirmatory set is assumed to exist. Stage A does not claim protected-confirmatory status.

### G15. Correctness evaluation

A separate `GO-10` is required for correctness evaluation, identifying the validated corpus and oracle hashes, exact variant/build roster, scoring rules, execution environment, output schema, access boundary, authorized operators and stop conditions. Correctness labels and oracle traces must not be used for parent selection, q/operator design, site selection, mutation tuning, variant changes, or Stage A model selection. The output is a feasibility record and predeclared descriptive summary only; a formal B1 model fit/test requires a separate analysis plan, review and GO.

### G16. Closeout

Publish an auditable feasibility report containing the adopted protocol and all governing hashes; source, licensing and lineage audit; parent selection record; input-contract reconciliation; `q`/catalog/profile/test-battery reports; full candidate inventories and cross-profile separation; complete planned/realized variant accounting; source/build/run dispositions; isolation report; diagnostic and M1-si/LOPO support audit; correctness corpus/oracle provenance and disclosure-safe summaries; all deviations, unresolved cases, resource use and GO records; and explicit non-claims and Stage B separation.

## 7. Stop rules

Stop the affected gate immediately if a required owner GO, scope, source/input hash, license, tool/environment hash, or data boundary is absent or mismatched; a source or parent changes after freeze; lineage cannot be established under the frozen rules; an input falls outside the contract; the operator/catalog/profile/search frame/inventory/probe/corpus/oracle changes after freeze; the fixture battery or oracle fails its predeclared criteria; a required static-analysis feature is unresolved; a deterministic cap or attempt budget is exhausted; completed analysis envelopes differ; an execution is not reproducible; an isolation or data-access boundary is breached; an unauthorized access occurs; an unlogged run occurs; or any post-freeze selection, replacement, reassignment, retuning, pooling, or repair is attempted.

No stop rule may be waived retrospectively. A materially changed design requires a new reviewed protocol and new authorization. Data from a failed or superseded attempt remain separately identified and cannot be pooled with the later attempt as though one frozen design had been used.

## 8. Ceilings and owner-set values

The following remain **UNKNOWN** and must be supplied before protocol adoption or the relevant GO. They are not inferred from historical plans:

| Ceiling or input | Value | Required before |
|---|---|---|
| Stage A selected-parent count and maximum parent roster | **UNKNOWN** | G0 / parent-selection GO |
| Maximum planned variants | **UNKNOWN** | G0 / mutation-generation GO |
| Maximum operator classes `q` | **UNKNOWN** | G0 / operator-contract freeze |
| Language families/languages in scope | **UNKNOWN** | Source-frame approval |
| Lineage reference units and reviewer capacity/hours | **UNKNOWN** | Lineage-feasibility approval |
| Static-analysis work-counter caps and fixture-only calibration corpus | **UNKNOWN** | Stage 2 profile freeze |
| `A_max` and analysis attempt/resource limits | **UNKNOWN** | Stage 2 profile freeze |
| Build/run CPU, memory, wall-time and per-variant ceilings | **UNKNOWN** | Build/solver GO |
| Diagnostic probe count, input corpus and per-stratum capacities | **UNKNOWN** | G10 / diagnostic GO |
| Correctness-evaluation corpus size and record count | **UNKNOWN** | G14 / correctness GO |
| Total compute-hour ceiling | **UNKNOWN** | G0 |
| Total human-hour ceiling | **UNKNOWN** | G0 |
| Monetary ceiling, if applicable | **UNKNOWN** | G0 |
| Calendar stop date | **UNKNOWN** | G0 |

No numerical cohort size, variant count, probe capacity, cost, power, precision, expected pass rate, or admission rate is inferred. In particular, 30 parents × 5 variants is not adopted.

## 9. Stage B separation

Stage B is a separate possible future confirmatory study, not an automatic continuation of Stage A. It requires its own population/design freeze, B1 analysis-plan amendment, defensible observed-parent-conditional operating-count justification, protected evaluation set, independent custodian and access mechanism, joint-consent provenance, trigger-(i) ratification, validated computational plan, isolation approval, and separate execution GO.

Stage A outcomes are excluded from Stage B operating-count justification under v0.21 §2.5 and are not pooled with Stage B. Stage A may document operational feasibility, implementation failure modes and realized resource costs. Any proposed use of Stage A information beyond those permitted feasibility records must be addressed prospectively in a separately reviewed Stage B protocol and cannot override the exclusion of Stage A outcomes from the operating-count justification or the non-adaptive rules.

## 10. Current authorization state

At the time of this draft:

- exploratory versus confirmatory route: **OWNER DECISION OPEN**;
- this protocol: **DRAFT ONLY**;
- all numeric ceilings and cohort limits: **UNKNOWN**;
- solver input contract: **NOT FROZEN**;
- source acquisition and parent selection: **NOT AUTHORIZED**;
- mutation/operator allocation and generation: **NOT AUTHORIZED**;
- Stage 2 profile/tool execution and test-battery execution: **NOT AUTHORIZED**;
- candidate-site enumeration: **NOT AUTHORIZED**;
- isolation test, construction, builds and solver runs: **NOT AUTHORIZED**;
- diagnostic probe execution: **NOT AUTHORIZED**;
- correctness-oracle execution and correctness evaluation: **NOT AUTHORIZED**;
- numerical operating-characteristic evaluation, simulation, model fitting and analysis: **NOT AUTHORIZED**;
- protected-set access: **NOT AUTHORIZED**.

**End of consolidated document-only exploratory feasibility protocol draft 0.2.**
