# Claude Review Handoff: LC518 Population and Experimental Design v0.8

**Date:** 2026-11-15  
**Status:** READ-ONLY INDEPENDENT REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** `gpt/b1-computational-plan-2026-11-14`

## 1. Exact review target

Please review the complete v0.8 specification, not only this handoff:

- **Path:** `lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.8.md`
- **Branch:** `gpt/b1-computational-plan-2026-11-14`
- **Git blob SHA-1:** `8e2ddd2cf4316c1cd68d60edd2dd6c167af29825`
- **Dimensions at preparation:** 969 lines; final newline present. (No UTF-8 byte count is asserted here.)

The immediate predecessor v0.7 remains unchanged:
- **Path:** `lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.7.md`
- **Blob:** `81f4a4dba051883916958713cfa9ee1acd69fc03`
- **Content-changing commit:** `32bebbff605c2204f24ad400ba6d8d48bab81235`

The accepted predecessor artifacts remain:
- **Rev 1.4 Amendment E:** commit `b8b8af042c16eeb9e02077c781ab05c582eeb65d`, blob `3728146356a74363a94fe75a87fd06c483954ee2`.
- **Rev 1.4 Amendment E acceptance record:** commit `ca15a29bd25c4c9c2293394f67cb19e1a18f34bd`, blob `074b40980eb96d164cd8411c8995bb1db4af0d46`.
- **B1 v1.7:** commit `c3abe107acd2a3f8be58bf933eafcd734823a129`, blob `8c666e501a31726c728447d155045c0b20adc178`.
- **B1 v1.7 acceptance record:** commit `ac06c6676982eed795db9cb04c6d91803b591ac7`, blob `ea51d72f4f85c5d832d72add561b4c93472c364a`.

Rev 1.4 Amendment E is accepted for the symbolic B1/M1 feasibility specification. B1 v1.7 is accepted and frozen as a symbolic analysis plan. Neither acceptance is an execution GO.

## 2. Review history and scope

Claude's provisional review of v0.7 identified:
1. the marked-position whole-function CFG equivalence rule could make site relocation exceptionally restrictive;
2. floating-point semantics were insufficiently specified;
3. unsummarized external calls lacked an explicit soundness fallback;
4. the operator-specific predicate/effect catalog needed a pre-enumeration freeze;
5. partial parameter-level availability between sites needed an explicit rule.

GPT's adjudication retained exact comparison but selected a target-centred, dependency-complete context slice as the equivalence object, rather than comparing the entire enclosing-function CFG. This deliberately defines equivalence between frozen operator-relevant context classes; it does not ignore semantically relevant control/data/state position. v0.8 also adds the floating-point, external-call, predicate-catalog and common-parameter rules.

Please independently challenge those decisions. Do not treat the prior GPT adjudication as authoritative where the technical argument does not hold.

## 3. New historical-audit implications to check

An independent GLM audit of the historical repository at `master` commit `33dca9b61d95b9fb750f750919c32c2e08b2ee90` reports that:

- in the v0.2 eligible confirmatory support, (C=5/k) in all 1,200 rows;
- the 120 files represented 40 base bodies copied three times, with no differing outcomes inside any of the 400 replica groups;
- the concentration feature was therefore aliased with failure count on that support;
- the reported near-zero model contrast/interval was materially sensitive to ridge regularization, with a separate basis-scaling/residualization diagnostic;
- the full audit also reports a frozen-versus-executed seed-rule deviation and separate generator/RLC-0 provenance defects.

These are historical findings, not results of the new population design. Do not transplant the historical seed, generator or RLC-0 corrections into this population specification.

Please test whether v0.8 sufficiently prevents the design from repeating the relevant failures:

1. **Independent parents:** do repository mirrors, forks, copies, byte-identical source trees and near-identical derivatives remain grouped under the lineage rules? Can renamed duplicates inflate (G_c)?
2. **Independent variants and support:** can repeated files, byte-identical variant copies, replicas or repeated evaluation rows ever count as distinct parent groups, distinct realization settings, distinct variants or distinct (C_D) support? Check §§2.1–2.3, 3.1–3.4 and 4.1.4.
3. **Actual identifying variation:** does the M1-si requirement guarantee at least two distinct realized (C_D) values within each contributing parent in the same exact ((q,Z,k,\ell)) cell, without post-diagnostic pair selection?
4. **Rank and regularization:** do the structural/rank checks in §3.6 and the sensitivity/rank requirements in §5.7 prevent regularization, repeated records, a narrow confidence interval or numerical fitting behaviour from being misrepresented as evidence that (C_D) is independently identifiable? State exactly what must be checked before any fit.

The historical audit report and its evidence index were supplied for this review, but the separate revised evidence ZIP/scripts/raw outputs are not part of this handoff. Do not claim to have executed those scripts or independently reproduced the audit unless you actually receive and run the corresponding artifacts.

## 4. Required technical review

Read the complete v0.8 text, including §§6.4–9. Classify each finding as **blocking**, **recommended**, or **accepted**, and cite the exact section and wording.

### A. Target-centred context slice

1. Is the five-step extraction procedure in §4.1.5(B) genuinely dependency-complete under a declared static-analysis model?
2. Does backward semantic dependency closure include every value, path, alias, memory, exceptional and control dependency that can affect target reachability or operands?
3. Does forward effect closure include all observable state/effect consequences through the first valid boundary, including callers, callbacks, external state and exception/cleanup paths where relevant?
4. Are omitted-region boundary nodes and summaries sufficient to stop context from being silently lost?
5. Does the canonical slice preserve relevant branch polarity, loop relations, exception/cleanup route, relative target position and dependency/effect structure while intentionally excluding unrelated whole-function CFG structure and absolute source addresses?
6. Is the extraction rule implementable and independently auditable without choosing its closure after seeing which candidate sites pass? Identify counterexamples where two materially different contexts could produce the same slice.
7. Does the fail-closed rule adequately handle incomplete call graphs, pointer/alias uncertainty, reflection, concurrency and language-specific control transfers?

### B. Canonicalization and source identity

8. Verify the canonical-labelling iff-isomorphism requirement for the declared typed, directed, edge-labelled multigraph and the exact canonical-byte comparison.
9. Review RFC 8785 JCS, numeric exact encodings, local alpha-renaming, observable identifiers, Unicode/source encoding, macro expansions, generated code, compiler-synthetic nodes and source-origin mapping.
10. Check that domain/profile/source digests and candidate inventory hashes cover every setting that can change the context representation.

### C. Abstract semantics

11. Review the per-operator predicate/effect catalog in §4.1.1c. Is the Operator Contract Gate correctly placed before Stage 2 profile selection and before candidate enumeration?
12. Does Stage 2 select a sound domain capable of resolving the frozen catalog, rather than tailoring the catalog or domain to candidates?
13. Review the floating-point requirements, including formats, rounding, signed zeros, subnormals, infinities, NaNs, conversions, exceptions/status flags, FMA, reassociation, excess precision and compiler/runtime settings. Is the fail-closed rule sufficient?
14. Review external/native/foreign/library/callback/dynamic call summaries and the conservative havoc/TOP fallback. Does it cover return values, aliased and escaped memory, globals/shared state, IO, exceptions, termination, callbacks, synchronization and control transfers?
15. Does the specification clearly restrict “equivalent” to equality under the frozen abstraction and context-slice representation, rather than claiming concrete or observational equivalence?

### D. Realization settings and candidate inventory

16. Does the shared-parameter intersection rule in §4.1.5 prevent a site-only contrast from being claimed at parameter levels that are not supported at both sites?
17. Is the site-by-parameter eligibility and assignment schedule fixed before construction, and protected from diagnostic/correctness-driven selection?
18. Is the complete syntactic search frame frozen before enumeration, with every matching, rejected and unresolved candidate inventoried and hashed before construction?
19. Is the call-graph check correctly limited to symbol/overload/dispatch resolution integrity, distinct from the target-centred context comparison?
20. Is one operator invocation per variant clearly a new design restriction, not an inherited requirement of B1 v1.7 or Rev 1.4? Are coordinated multi-hunk edits operationally distinguishable from independent invocations?

### E. B1/M1, support and governance

21. Check the proposed (q/\mathbf a) coding against accepted B1 v1.7 and Rev 1.4 Amendment E. Do not silently redefine the accepted (q) coordinate.
22. Check the same-parent/same-operator/same-exact-cell M1-si support conditions, distinct (C_D) requirements, LOPO implications and deterministic shortfall reporting.
23. Check that parent lineage and variant provenance prevent duplicated code or replicas from being counted as independent support.
24. Check the rank/identifiability language and ensure no regularization or numerical precision claim can substitute for actual within-cell concentration variation.
25. Review the Option B proxy-pathway limitation and N5 classification.
26. Review parent-count justification, protected-set custodian, trigger-(i) ratification, joint-consent provenance, isolation, data access and the separate execution GO.
27. Re-read §§6.4–9 and report any inconsistency with the preceding sections, accepted plans or explicit non-authorization.

## 5. Deliverable and boundary

Return a complete review table with finding ID, severity, exact section, technical reason, required correction (if any), and whether the issue blocks design freeze.

This is a read-only review. Do not edit the repository, generate sources/variants, allocate mutations, access banks or protected data, run diagnostics, fit models, simulate, or perform any execution.

v0.8 remains an **UNREVIEWED DESIGN-ONLY DRAFT**. GPT will adjudicate the review. Any substantive correction after this review must be published as a new version. No part of this handoff or v0.8 is an execution authorization.
