# GPT-owned B1 census-intake successor rewrite — correction record (2026-11-23)

## 1. Purpose and disposition

This record documents a successor rewrite of the B1 v1.7 census-manifest intake checker. It does not amend the B1 analysis plan, the reviewed revision 0.6 instrument/schema, the measurement specification, any upstream generation protocol, or any scientific claim.

The new implementation is on a separate unmerged branch based on HY4-authored v0.2 commit fd0b34bfbdd5cc6c686e157a5483b88bf2eccfef. Historical commits 0060e7b and fd0b34b are preserved unchanged. The v0.2 partial schema is removed only from the new branch's working tree; its original blob remains recoverable from the historical commit.

**Current status:** GPT-authored v0.3 successor implemented and synthetically tested; Claude's independent code review is pending. This is not a PASS and does not authorize downstream work.

## 2. Authorship and review attribution

- HY4 authored the original prototype in commit 0060e7b and the v0.2 successor in commit fd0b34b.
- GPT inspected the historical code, schema, fixtures, README, correction record, review packet, and controlling B1 schema/instrument. The v0.2 implementation did not enforce the reviewed 17-field manifest contract or the schema's nested additionalProperties=false rules. It admitted schema-invalid outcome-like fields, ignored required status-decision consultation flags, admitted null evidence/digest values, and generated zero-valued exact cells for statuses with no diagnostic measurement.
- GPT authored the v0.3 rewrite on a new branch. This is not a claim that GPT authored the earlier implementation.
- Claude agreed to the correction approach and six conditions in the 2026-11-23 conversation before implementation. That agreement is a design-scope agreement, not an independent code review or PASS on v0.3.
- This record and the new review packet do not attribute any GitHub action to Claude unless Claude actually posts that action through the connected GitHub identity.

## 3. Controlling schema identity

The packaged B1 manifest schema is copied byte-for-byte from:

- Source commit: f19e2a0ba09f2161f290558da5f61abc9d3ab52a
- Source path: reviews/analytical-validity-2026-11-18/b1-v17-census-review-2026-11-22/B1_V1_7_CENSUS_MANIFEST_SCHEMA_DRAFT_0_6.json
- Source Git blob SHA-1: 0f2865e606fa61400184c09abd01601497637a6b
- Schema $id: urn:lc518:b1-v1.7:census-manifest:0.6-draft

The schema requires 17 top-level fields and sets additionalProperties=false at the root. It also sets additionalProperties=false on $defs.variant and nested objects including diagnostic results and status decisions. Neither f, u nor p is a manifest or variant property. These aggregate vectors therefore cannot be embedded in the manifest without violating schema draft 0.6.

The validator pins the packaged schema's Git blob SHA-1 and refuses to run if the local schema bytes differ from the reviewed source blob. It validates JSON Schema draft 2020-12 constraints before running local semantic checks.

## 4. Measurement rule and source

The implementation's primary formula is taken from the C_D measurement specification, not inferred from prior code:

C_D = max over j=1,...,8 of (f_j / k_fail), where k_fail = sum over j=1,...,8 of f_j.

Source: reviews/analytical-validity-2026-11-18/CD_MEASUREMENT_SPEC_2026-11-19.md, §1 (which quotes Rev 11 lines 216–221), with the reporting definition in §5. Source commit: ccd95e4c125d081abca95153f9af9c9a28d65b9a. Source Git blob SHA-1: 923655f20337b99f11e400f3428d1d18ac34c96d.

Unresolved outcomes are never included in the numerator or denominator. k_unresolved remains separately recorded for the exact cell. For k_fail=0, the output label is NO OBSERVED FAILURES with no numeric predictor value. That is a categorical display state preserving the protocol's labelled zero convention; it does not convert a zero-failure state into measured concentration variation.

## 5. Corrections made

### 5.1 Full schema enforcement

The new checker uses the actual 0.6 schema, not the reduced v0.2 record_schema.json. It validates all 17 required root fields, fixed values, nested references, arrays, conditional status rules, date-time formats, digest patterns, status-specific result cardinalities, and unknown-field prohibitions. Outcome-like unknown fields at root, variant, diagnostic result, status-decision and reference levels are rejected.

### 5.2 Status decisions and evidence

All seven status-decision fields are enforced. Both diagnostic_terminal_values_consulted and derived_failure_unresolved_counts_consulted must be false. record_presence_identity_metadata_consulted must be true only for the INCOMPLETE post-run completeness audit, and false for prediagnostic and EXPECTED_NOT_RUN statuses. Rule and decision references must satisfy the exact schema shapes, timestamps must satisfy date-time, and required digests/evidence references cannot be null or malformed.

Local timing checks enforce that INVALID and EXCLUDED_BEFORE_DIAGNOSTICS decisions precede the campaign first-start timestamp, or do not exceed the ledger snapshot when the first-start field is null. EXPECTED_NOT_RUN decisions cannot postdate the ledger snapshot. Exact per-variant run-ledger row reconciliation remains unperformed because the external ledger is not retrieved.

### 5.3 Correct no-measurement handling

- INVALID, EXCLUDED_BEFORE_DIAGNOSTICS and EXPECTED_NOT_RUN have no diagnostic counts, no k_fail, no k_unresolved, no cell and no C_D.
- INCOMPLETE may report received per-stratum f/u/p vectors only, labelled PROVISIONAL — INCOMPLETE INVENTORY. It has no aggregate k values, no full cell and no C_D. A zero-record incomplete receipt has no vectors.
- Only VALID variants receive complete derived counts and a full B1 cell.

This corrects the v0.2 false-zero behaviour identified by Claude and GPT. No missing or unmeasured diagnostic record is converted into a definite pass, failure or zero-valued cell.

### 5.4 Aggregate sidecar

Optional f/u/p assertions are moved into aggregate_assertions.schema.json, outside the B1 manifest. The sidecar binds to the exact manifest bytes by SHA-256 and declares the sidecar schema's Git blob SHA-1. The validator pins that sidecar schema SHA-1 and checks it at runtime. Only VALID variants can receive aggregate assertions. Mismatches yield AGGREGATE_MISMATCH; malformed vectors yield MALFORMED_AGGREGATE.

Sidecar validation is reported separately and can never mutate or override manifest_report.manifest_decision. A mismatched or unbound sidecar is rejected before its aggregate values are evaluated.

### 5.5 External-validation boundary

The report is prominently labelled SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED. It enumerates external checks not performed, including bank membership, exact inventory coverage, q-registry membership, family-map identity, per-variant run-ledger reconciliation, historical exposure evidence, and external artifact/provenance verification. Local structural/semantic success is not described as full census admissibility.

## 6. Testing

The synthetic suite contains 59 test methods. It covers complete-envelope validation, all root and nested unknown-field cases, both prohibited status consultation flags, null/malformed digests and evidence references, date-time checks, prediagnostic timing, all five validity statuses, the no-false-zero rule, provisional incomplete counts, failure-only C_D, record-ID checks, artifact-digest collision flags, sidecar binding/schema identity/reason codes, and CLI outcomes.

Local execution in this working container:

    py -m unittest discover -s census-intake/tests -v

Result: 59 tests run, 59 passed. For this local run, the validator's expected packaged-schema SHA constant was temporarily set to the local reconstruction's Git blob SHA because the local working file was reconstructed for testing. The committed code was then restored to the reviewed source blob SHA 0f2865e606fa61400184c09abd01601497637a6b. Therefore the local 59/59 run verifies validator and test behaviour against a semantically equivalent reconstruction of schema 0.6; it is not a byte-identity test of the eventual committed schema. The exact source schema blob is added to the GPT successor branch; the branch's runtime source-blob guard must be tested independently against those exact bytes. Claude's independent review and test run remain required.

This qualification is intentional: the local run must not be described as byte-identity verification of the eventual committed schema.

## 7. Scope and non-authorizations

No bank access, parent acquisition, mutation allocation, solver generation/build, diagnostic execution, real-manifest validation, census execution, outcome collection, modelling, fitting, prediction or power analysis occurred. No B1 protocol/schema freeze, evaluation-route decision, coverage-floor decision, or production GO is made by this correction.

Gate 1 preflight remains BLOCKED / NOT ASSESSABLE. The scientific proposition remains UNPROVEN. The earlier question about whether the conditional census authorization in instrument §10 item 7 remains operative is not addressed by this correction and remains unanswered.
