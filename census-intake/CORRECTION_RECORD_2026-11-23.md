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

Result: **59 tests run, 59 passed** against a locally reconstructed schema copy after temporarily changing the local validator's expected schema-blob constant to that reconstruction's Git blob SHA. The reconstruction was 7 bytes shorter than the reviewed source file; equivalence was not established. This run therefore verifies the validator logic and synthetic cases against that local reconstruction only. It is not a test against the exact source schema, not a byte-identity check, and not evidence that all 59 fixtures pass against the exact committed schema.

The committed successor packages the exact reviewed schema blob `0f2865e606fa61400184c09abd01601497637a6b`. The committed validator retains that exact expected constant, and the source-identity test now also asserts that literal expected hash. The exact-byte runtime guard and complete test suite must be run independently against the committed branch. Claude's independent review and test run remain required.

## 7. Scope and non-authorizations

No bank access, parent acquisition, mutation allocation, solver generation/build, diagnostic execution, real-manifest validation, census execution, outcome collection, modelling, fitting, prediction or power analysis occurred. No B1 protocol/schema freeze, evaluation-route decision, coverage-floor decision, or production GO is made by this correction.

Gate 1 preflight remains BLOCKED / NOT ASSESSABLE. The scientific proposition remains UNPROVEN. The earlier question about whether the conditional census authorization in instrument §10 item 7 remains operative is not addressed by this correction and remains unanswered.


## 8. Review response — zero-convention qualification and sidecar hash verification (2026-11-23)

Claude's v0.3 review identified that the original wording overstated the status of the zero-failure convention. The measurement specification §1 transcribes Rev 11 as stating C_D = 0 when k_fail = 0, labelled NO OBSERVED FAILURES; however, the same specification §4 explicitly records that the k_fail = 0 convention is inconsistent across instruments. The validator's categorical output is therefore documented as this implementation's reporting choice, not as a universally settled convention. The code and README wording have been corrected accordingly. The primary positive-failure formula remains sourced to the measurement specification §1 and its cited Rev 11 lines 216–221.

The sidecar schema pin was independently recomputed from the exact committed UTF-8 file bytes using the Git blob object preimage (the literal prefix `blob 1268\\0` followed by the file bytes). The computed Git blob SHA-1 is `72fc746c3d6129534aeb2fdbcd866842865f98c7`, matching both the file's reported GitHub blob SHA and the validator's expected constant. The exact reviewed B1 manifest schema was independently recomputed in the same manner: 24,279 bytes and blob SHA-1 `0f2865e606fa61400184c09abd01601497637a6b`, matching the reviewed source pin.

The 59-test suite has still not been executed against the exact committed branch bytes. The earlier local 59/59 result used a reconstructed schema and is not a substitute. Claude has not run the suite either. This remains the gating item for a code PASS; no PASS is claimed here.


---

## 9. Final review and work-branch integration — 2026-11-23

This entry supersedes the pending-review and "unmerged" status statements above. Those statements accurately record the state when the earlier entries were written; they are not rewritten.

### 9.1 Exact-commit execution

The syntax-repaired successor commit is `258c68df4a2ede77c0acd2e9ab0382080ae305b6`, parented directly by `a48cc9dfdc5af87661762f6be9b98e11030ce9b8`. The syntax repair itself changed only `census-intake/tests/test_b1_census_intake.py`, with six approved additions and six deletions. No validator, schema, requirements, or test assertion was changed in that repair commit.

Two independent clean-checkout runs against the exact committed bytes reported 59/59 passing:
- GPT: Python 3.13.18, `jsonschema` 4.26.0.
- GLM: Python 3.12.16, `jsonschema` 4.26.0.

Both runs recomputed and matched the manifest schema blob `0f2865e606fa61400184c09abd01601497637a6b` and sidecar schema blob `72fc746c3d6129534aeb2fdbcd866842865f98c7`. Claude accepted these as execution evidence, while noting that Claude did not personally run the suite.

### 9.2 Claude's final PASS

Claude's final verdict is **PASS for the six-line syntax repair and for the v0.3 validator as a local structural intake check**. Claude withdrew the zero-convention objection because the implementation and README already state that the `NO OBSERVED FAILURES` category is an implementation/reporting choice and not a universally settled convention.

The PASS does not establish bank membership, provenance, inventory/registry/run-ledger reconciliation, real-manifest validity, or any scientific claim. The checker remains labelled `SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED`.

### 9.3 Merge disposition

After Claude's PASS and completion of the separate §14.2 review condition, PR #11 was merged into its designated work branch only:
- Target branch: `work/b1-census-intake-validator-v02-2026-11-22`.
- Head commit: `258c68df4a2ede77c0acd2e9ab0382080ae305b6`.
- Merge commit: `c1f76e4b20c38f7b43e1ee2ef2ba27c9d61a09aa`.

The PR's aggregate diff against the HY4 v0.2 base contains the GPT-authored v0.3 successor plus the final syntax repair (5 commits, 10 files). The syntax-repair commit alone is limited to the one test file and six lines described above.

GitHub subsequently reports PR #10 as merged at its head `a48cc9dfdc5af87661762f6be9b98e11030ce9b8`, which is included in PR #11's merged history. No separate PR #10 merge operation was performed. PR #9 remains open/draft. The default branch `master` remains unchanged at `ccbd0bdefd2d02ec22f6e17f27e9d0074952605a`.

### 9.4 Scientific and operational boundary

No real manifest, bank use, protected set, parent acquisition, mutation allocation, solver construction or execution, diagnostic run, outcome collection, census, model fitting, or predictive analysis occurred. Gate 1 remains **BLOCKED / NOT ASSESSABLE**; the proposition remains **UNPROVEN**; the pause remains in force; the conditional census authorization remains dormant, neither revoked nor triggered; no production GO is active.
