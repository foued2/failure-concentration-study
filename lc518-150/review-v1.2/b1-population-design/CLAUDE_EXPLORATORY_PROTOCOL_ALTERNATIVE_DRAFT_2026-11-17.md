# LC518 Exploratory Feasibility Protocol: Independent Alternative Draft

**Status:** Document-only draft prepared by Claude under the owner's one-time "DO ALL THREE" authorization. Not an owner decision, not a freeze, not an execution GO, not a source-access authorization, and not an analysis-plan amendment.
**Route:** Exploratory versus confirmatory is OPEN. This draft is conditional on an owner decision to adopt the exploratory route.
**Repository basis:** v0.21, blob `8af908f6b0ad4cd060194a0a63f4914939f07756`, working branch tip `1e894fe7e6c0b8f33a8e8534d4b717e260f4c000`, master `33dca9b61d95b9fb750f750919c32c2e08b2ee90`.
**Independence:** Written from v0.21 directly. GPT's draft 0.1 was not used as a source text. Comparison is in the accompanying review.

## 1. Scope

Stage A asks one structural question: can the intended pipeline (verified parent lineages, Stage 2 static analysis, frozen candidate inventory, construction, diagnostics, and correctness evaluation) be executed reproducibly, under v0.21's restrictions, with the adopted M1-si support condition realized or shortfalled and reported?

## 2. Non-claims

Stage A does not establish:
- confirmatory predictive evidence for the B1 claim;
- a direct, causal, or realization-setting-independent concentration effect (the primary Option B result is proxy-inclusive through a(v));
- generalization to naturally occurring solvers;
- any precision, power, or sample-size justification for Stage B;
- a validated operating parent count. The 30 x 5 and 150-variant figures are not adopted.

## 3. Measurable feasibility criteria

Each criterion has a fixed evidence artifact, a fixed measurement rule, and a predeclared disposition. Numeric thresholds that the owner has not supplied are marked **OWNER-SET** and must be filled before adoption. No value is inferred here.

| ID | Criterion | Measurement | Threshold | Disposition if not met |
|---|---|---|---|---|
| C1 | Independent parent lineages | Count of pairwise-coherent lineage clusters that pass frozen rules | Lower bound OWNER-SET; M1-si requires at least 3 | Report parent-frame shortfall; do not relax lineage rules |
| C2 | Stage 2 soundness battery | Pass rate on pre-registered fixtures for each construct the profile claims to support | Zero failures on supported constructs (proposed; owner to accept) | Profile rejected; no site enumeration under it |
| C3 | Search-inventory correctness | Known-answer corpus: missed and extra matches; second-enumerator disagreements | Zero unexplained disagreements (proposed; owner to accept) | Inventory unresolved; no enumeration |
| C4 | Construction reproducibility | Admitted variants whose source and runnable digests reproduce across independent builds | 100% of admitted variants | Non-reproducible variants excluded and counted, not replaced |
| C5 | M1-si realization | Qualifying parent count in a common exact cell after diagnostics | Frozen rule, §3.4 of v0.21 | Report M1-si NOT REALIZED; no repair |
| C6 | Diagnostic completeness | Planned variants with a classified diagnostic outcome | Every planned variant accounted for | Excluded variants reported with reasons |
| C7 | Oracle validity | Independent validation of expected correctness outputs on a fixed subset | Agreement threshold OWNER-SET | Correctness collection stopped |
| C8 | Attempt reproducibility | Admitted sites with two byte-identical complete result envelopes within A_max | 100% of admitted sites | Site unresolved |
| C9 | Budget | Realized compute, wall time, and human hours against ceilings | Ceilings OWNER-SET | Stop rule applies |

No criterion may be re-thresholded after any diagnostic or correctness result is observed.

## 4. Outcome firewall

This draft adopts v0.21 §§4.2, 5.6, and 6.5 without change:
- no parent, mechanism, identity, realization coordinate, parameter level, or site may be chosen or changed using realized C_D, failure totals, unresolved totals, cell membership, correctness, or model results;
- no variant may be added, removed, replaced, reassigned, or selectively paired after diagnostics;
- shortfalls are reported as shortfalls;
- Stage A outcomes are not inputs to any Stage B operating-count justification (v0.21 §2.5), and any external prior used for such a justification must be labelled as an assumption with a documented source.

## 5. Authorization gates

Each gate that touches sources, code, tools, solvers, data, or outcomes needs a separate owner GO. The GO must name the operation, the artifact hashes, the environment hash, the data boundary, the permitted outputs, and the stop conditions. A GO for one gate does not authorize another. Documentary review gates need no execution GO but still need route approval.

| Gate | Activity | Authorization |
|---|---|---|
| G0 | Route decision; scope; ceilings in §7 | Owner decision |
| G1 | Lineage frame and candidate sourcing within the approved frame | GO-1 (source acquisition) |
| G2 | Input contract (schemas, preconditions, ranges, environment, out-of-contract handling, assumption labels), reconciled with the v0.21 §5.1 protected-set domain; then Stage 1 contract review (v0.21 §4.1.1b) | Review route only; contract must be frozen before G4 |
| G3 | Parent selection and pinned source revisions | GO-2 (parent selection) |
| G4 | Operator specifications q, fingerprints, realization fields, predicate/effect catalogs | Review route; frozen before G5 |
| G5 | Stage 2 profile instantiation and **execution of the fixture test battery** (tools run on fixtures only, not on parent code) | GO-3 (tool execution on fixtures) |
| G6 | Frozen syntactic search and complete candidate inventory, only after G5 acceptance | GO-4 (enumeration) |
| G7 | Isolation probe of the execution environment | GO-5 (isolation test) |
| G8 | Construction of frozen variants | GO-6 (construction), after G7 |
| G9 | Diagnostic probe design (blind to variant identity and outcomes), then probe freeze | Review route; probe hashes frozen before G10 |
| G10 | Diagnostic execution | GO-7 (diagnostics) |
| G11 | Correctness oracle construction and independent validation | GO-8 (oracle) |
| G12 | Correctness evaluation | GO-9 (evaluation) |
| G13 | Closeout report | Owner acceptance |

**Oracle (G11).** Expected correctness outputs must be generated by a method that does not depend on any candidate variant. Its provenance, generator version, and input hashes are frozen and validated against an independent check before any solver runs. v0.21 §5.1 requires this for protected sets and Stage A is held to the same standard.

**Diagnostic probes (G9).** Probe construction must be blind to variant identity and to outcomes. Probe generation code and parameters are frozen and hashed before G10. The eight-stratum definition and capacity vector are bound at G9, not assumed from the Rev 1.4 8 x 8 grid.

**Test battery (G5).** The fixture battery is written and hashed before tools are run on it. Its author should not be the same person who builds the profile. The battery's pass criteria are frozen before execution. A passed battery shows conformance on its coverage; it does not prove semantic soundness (see the §4.1 review).

## 6. Stop rules

Stop the affected gate immediately if: a required GO or its scope or hashes are missing or mismatched; a parent or source changes after freezing; the profile, catalog, probe set, or inventory changes after its freeze; the battery or oracle fails its predeclared criteria; an unresolved construct is needed for admission; a budget ceiling is reached; isolation or data access is breached; an unauthorized access occurs; or any post-freeze selection or repair is attempted. No stop rule may be waived retrospectively. A changed design needs a new reviewed protocol and new authorization, and its data must not be pooled with the earlier attempt.

## 7. Ceilings (all OWNER-SET)

Parent-count ceiling and rationale; maximum variants; maximum operator classes; languages in scope; lineage reviewer hours; static-analysis work-counter caps and their calibration data (calibration must not use parent code or the candidate frame); build and run CPU, memory, wall time, and A_max; diagnostic probe count and per-stratum capacities; correctness corpus size; total compute, human-hour, and monetary ceilings; calendar stop date. No number is inferred here.

## 8. Review route

The formal review route for this protocol is the route the owner designates under the current v0.21 governance record. GPT adjudicates. This draft does not restate or reinstate any route.

## 9. Stage B separation

Stage B is a separate future confirmatory design. It needs its own population freeze, B1 amendment, operating-count justification, protected set with an independent custodian, consent provenance, trigger-(i) ratification, validated computation plan, isolation approval, and separate GO. Stage A outcomes are not pooled into Stage B and are not used to choose its parents, mechanisms, variants, or operating count.

## 10. Current authorization state

Route: OPEN. Protocol: DRAFT ONLY. Source acquisition, parent selection, operator freeze, Stage 2 tool execution, enumeration, construction, isolation testing, diagnostic probing, oracle construction, correctness evaluation, simulation, and protected-set access: all NOT AUTHORIZED.
