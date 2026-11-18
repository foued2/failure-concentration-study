# GPT adjudication — GLM population-manifest validator v0.1

**Date:** 2026-11-17  
**Adjudicator:** GPT  
**Subject:** GLM engineering proposal and reported 19/19 test result for a deterministic population-manifest validator  
**Decision:** **HOLD FOR TECHNICAL REVISION**  
**Scope:** Working-branch engineering component only. Does not amend `master`, the population specification, or authorize construction, execution, fitting, or publication.

**Provenance note:** This adjudication was issued from GLM’s pasted proposal and test report. The Python source, JSON Schema, fixtures, expected-results file, and test runner were **not** available in the repository at adjudication time. The reported 19/19 result remains GLM-reported, not independently verified. Any GLM header date of **2026-11-18** for a “GPT engineering-first direction” is **not established** by this conversation’s chronology (today is 2026-11-17) and must be corrected or labelled unverified.

---

## Verdict

**ACCEPT** the engineering direction; **HOLD** GLM’s v0.1 as a normative validator.

The move toward executable infrastructure is meaningful. The proposed separation between manifest validation, realized-support auditing, and execution authorization is sound.

Several issues could cause the validator to reject a valid population or incorrectly declare an invalid one valid. Resolve them before adopting the schema or treating the reported 19/19 tests as evidence of correctness.

---

## 1. Blocking methodological corrections

### A. `E_DUP_SITE` conflicts with the adopted M1-si design

GLM proposes rejecting a duplicate `(parent_ref, q_ref, site_digest)`.

v0.21 §3.4 explicitly permits within-class variation at a fixed source site. Different literal, threshold, or extent settings at the same site can provide the required realization-setting variation.

| Parent | Site | Realization setting | Expected treatment |
| ------ | ---- | ------------------- | ------------------ |
| P1     | S17  | threshold = 5       | Admissible         |
| P1     | S17  | threshold = 10      | Admissible         |

These records must not fail merely because they use the same site.

**Adjudication: REJECT `E_DUP_SITE` as currently defined.** Replace it with a duplicate-operation-coordinate check that includes the realization settings and relevant operator identity. Reusing a site with different permitted settings must remain possible.

### B. Global digest uniqueness is too broad

The adopted M1-si rule requires semantic-source and runnable-artifact differences for a qualifying pair **within the same parent and exact cell**.

It does not establish that every digest must be globally unique across the entire population, regardless of parent or cell.

A digest collision across different parents should trigger a provenance and lineage review, not automatically invalidate M1-si. Within a parent-cell, an identical runnable artifact cannot count twice. Preserve the attempted record, link it to the canonical duplicate, and count the runnable implementation only once, as v0.21 requires.

**Adjudication: REVISE `E_DUP_SOURCE_DIGEST` and `E_DUP_ARTIFACT_DIGEST`.** Apply the distinctness rules at the correct scope. Do not silently discard duplicate records.

### C. `C_D` must be recalculated, not merely range-checked

The proposed `E_CD_RULE` description requires:

- `k_fail = 0` → `C_D = NA` and `NO_OBSERVED_FAILURES`.
- `k_fail > 0` → numeric `C_D >= 0`.

That is insufficient.

Given the eight stratum counts \(f_1,\ldots,f_8\), the validator must independently calculate:

\[
k_{\mathrm{fail}}=\sum_{j=1}^{8} f_j
\]

\[
C_D=\frac{\max_j f_j}{k_{\mathrm{fail}}}
\]

It must verify that the declared failure total agrees with the sum and that the declared concentration agrees exactly with the calculated fraction. Unresolved outcomes must remain outside that calculation.

Canonical rational representation (for example `"2/5"`) is preferred over floating-point JSON numbers.

**Adjudication: ACCEPT the intended rule, but EXPAND its implementation.** A plausible number between zero and one is not proof that the declared concentration is correct.

### D. Built does not mean diagnostically realized

GLM’s proposed strict/projected distinction uses `PLANNED` and `BUILT`. That is not enough.

A solver can be built while its diagnostic outcomes have not yet been collected. M1-si realized support requires actual, admissible diagnostic records and their realized \(C_D\) values, in addition to the required distinct source and runnable artifacts.

The lifecycle needs separate fields for:

- Construction status: `PLANNED`, `BUILT`, and relevant build failures.
- Diagnostic status: `NOT_RUN`, valid completed diagnostic disposition, invalid, unresolved, or other frozen terminal states.

A planned record can contribute to a planned-schedule inventory. A built record can contribute to a build-verified inventory. Neither establishes realized M1-si support until the diagnostic requirements are satisfied.

**Adjudication: REJECT the label `m1_si_projected` if it is presented as projected realized support.** Use something like `candidate_support_pairs` for the pre-diagnostic schedule. Reserve `m1_si_realized` for the post-diagnostic audit.

---

## 2. Additional corrections

### E. Ceiling checks must use an authoritative source

Checking counts against the manifest’s own ceilings is not a sufficient ceiling control. The same document being validated could simply declare a higher parent or variant limit.

Owner-set ceilings need a separately frozen, hash-identified G0 completeness record or limits manifest. The validator should verify that the population manifest echoes those values exactly and that its counts do not exceed them.

**Adjudication: BLOCK until ceilings are bound to an independently identified authority.**

### F. M1-si pair logic should follow the formal condition

For each qualifying parent-cell, v0.21 requires:

\[
|\mathcal{V}_{g,c}|\ge 2,\quad |\mathcal{A}_{g,c}|\ge 2,\quad |S_{g,c}|\ge 2
\]

The digest requirement additionally demands a qualifying pair whose two members differ in both semantic-source and runnable-artifact digests, alongside different settings and realized \(C_D\).

The validator should explicitly identify the qualifying pair and report its two variant IDs. It should not accidentally substitute a different rule such as global uniqueness or an unnecessarily stronger all-pairs test. It should also implement the v0.21 duplicate and build-reproducibility dispositions.

**Adjudication: ACCEPT the intended pair-level approach, subject to an explicit pair-witness report.**

### G. Placeholder scanning needs field-aware semantics

Rejecting every string containing `UNKNOWN`, `TODO`, or similar markers is too blunt. Such words can occur in descriptions, provenance notes, or legitimate category labels.

Reject placeholders in required machine-readable values and owner-set fields, while preserving legitimate explanatory text. Exact sentinel values and permitted enums should be distinguished from free-text fields.

**Adjudication: ACCEPT the fail-closed objective; REFINE the scan.**

### H. Embedded JSON Schema validator needs an independent compatibility check

A self-contained, zero-dependency validator is reasonable. Implementing only a subset of JSON Schema draft 2020-12 creates a risk that the embedded validator and standard implementations interpret the same schema differently.

The schema should explicitly prohibit unsupported keywords, and the fixture suite should be checked against an independent draft 2020-12 implementation.

**Adjudication: ACCEPT conditionally.** Keep the zero-dependency runtime if desired, but demonstrate agreement against an independent standards-compliant validator.

### I. “Processes no study data” needs qualification

Synthetic fixtures are good. A tool designed to validate an actual population manifest may process real parent, variant, digest, and diagnostic metadata when used.

The correct claim is that it does not independently acquire or access study data, and that the current test corpus is synthetic. Do not claim that the program itself can never process study data.

---

## 3. Accepted from GLM

| Proposal element                                          | GPT disposition                                        |
| --------------------------------------------------------- | ------------------------------------------------------ |
| One deterministic manifest-validation entry point         | Accept                                                 |
| Separate schema and semantic validation                   | Accept                                                 |
| Referential integrity and identifier checks               | Accept                                                 |
| Explicit parent eligibility and excluded-parent treatment | Accept                                                 |
| Exact-cell support, with no pooling                       | Accept                                                 |
| `k_fail=0` as `NA` plus `NO_OBSERVED_FAILURES`            | Accept                                                 |
| Shortfall reported rather than repaired                   | Accept                                                 |
| Planned and realized accounting kept separate             | Accept after lifecycle correction                      |
| Synthetic fixture suite and byte-determinism test         | Accept as a good test design, subject to source review |
| No automatic source discovery or solver execution         | Accept                                                 |
| Validator is non-normative and not an authorization       | Accept                                                 |

The 18 named fixtures plus one determinism check make 19 checks, so the reported test count is internally consistent. That does not independently demonstrate that the fixtures cover the rules correctly.

---

## 4. Exact M1-si contract to implement

1. Validate the input schema and authoritative G0 limits.
2. Validate parent, operator-class, variant, and cell references.
3. Recompute `k_fail` and exact \(C_D\) from the eight failure-stratum counts.
4. Retain every attempted record and its terminal disposition.
5. Within each exact cell, group admissible variants by parent.
6. Resolve duplicate runnable artifacts according to v0.21, without counting repeated artifacts as independent variants.
7. Identify qualifying within-parent pairs with distinct realization settings, realized \(C_D\), semantic-source digests, and runnable-artifact digests.
8. Count qualifying parents in each exact cell.
9. Report `M1-si REALIZED` only when one exact cell has at least three qualifying parents.

The result should include explicit pair witnesses, excluded records, duplicate aliases, shortfalls, and the exact hashes of the manifest, limits, schema, and validator.

Report the structural LOPO support implication separately. M1-si support does not guarantee optimizer convergence, successful model fitting, or an available B1 test.

---

## 5. Next action

**HOLD FOR TECHNICAL REVISION.**

Accepted: concept and most of the validation architecture.  
Not accepted as currently defined: site duplication, global digest uniqueness, realized/projected support, or ceiling authority.

Do **not** open another lengthy protocol review. Next work is confined to this validator:

1. **GLM delivers** the actual package on the working branch:
   - `validate_manifest.py`
   - `manifest_schema.json`
   - fixtures
   - expected-results file
   - test runner
2. **GPT checks** the exact implementation against v0.21 §3.4 and the corrections above.
3. Correct the source and add adversarial synthetic fixtures for the identified boundary cases.
4. Publish the accepted engineering component on the working branch only; leave `master` and the population specification untouched.

**Boundary:** this validator can establish whether a proposed population manifest satisfies the declared structural conditions. It cannot create the missing parent population or mutation allocation. It is a concrete tool for evaluating those artifacts when they exist — engineering progress toward the experiment, not a substitute for it.
