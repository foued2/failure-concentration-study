# LC518 B1 v1.7 census-manifest intake checker

**SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED**

**Version:** 0.3.0, GPT-authored successor rewrite
**State:** merged into `work/b1-census-intake-validator-v02-2026-11-22` at `c1f76e4` via PR #11 (2026-11-23T10:44:42Z, work branch only, not `master`); Claude final verdict PASS for the six-line syntax repair and for v0.3 as a local structural intake check, recorded in PR #11
**Date:** 2026-11-23
**Gate 1 inputs machinery:** `gate1-inputs/` plus `ANNEX_INTAKE_FORM_SCHEMA.json`, `ANNEX_INTAKE_FORM_TEMPLATE.json`, `validate_annex.py`, and `build_preregistration_manifest.py` — the remaining-gap map, owner mutation-design annex intake, schema-pinned C1–C7 structural auditor (C4 requires adopted-family-map/hash binding; C6 checks note presence only), and a pre-registration builder that accepts a construction-supplied real inventory without inventing real IDs (see `gate1-inputs/README.md`)

This package checks a B1 v1.7 census-manifest JSON object against the exact reviewed revision 0.6 JSON Schema and applies bounded manifest-local semantic checks. Its owner-annex auditor uses a separate pinned schema and provides structural intake only: C4 requires verified adopted-family-map bytes and parent-source hashes; C6 checks nonblank witness-note presence, not witness adequacy or the full A2 verdict. It is not the Gate 1 census, not a full provenance validator, and not admission to census execution.

## 1. Controlling schema and measurement definition

The package includes the exact byte-for-byte copy of the reviewed schema:

- Source commit: f19e2a0ba09f2161f290558da5f61abc9d3ab52a
- Source path: reviews/analytical-validity-2026-11-18/b1-v17-census-review-2026-11-22/B1_V1_7_CENSUS_MANIFEST_SCHEMA_DRAFT_0_6.json
- Source Git blob SHA-1: 0f2865e606fa61400184c09abd01601497637a6b
- Schema ID: urn:lc518:b1-v1.7:census-manifest:0.6-draft

At startup, the validator recomputes the Git blob SHA-1 of the packaged schema and refuses to run if it differs from the reviewed source blob. It also checks the schema using a Draft 2020-12 validator before validating a manifest.

The schema does not define f, u or p as manifest fields. They do not appear among the 17 required root fields or the variant properties in $defs; both the root object and $defs.variant set additionalProperties to false. Adding those vectors to the manifest would therefore violate the reviewed schema. They are accepted only in the separate aggregate-assertion sidecar described below.

The statistic is implemented from the controlling measurement document, not inferred from the former code. The cited definition is C_D = max over j=1..8 of (f_j / k_fail), with k_fail = sum over j of f_j, from CD_MEASUREMENT_SPEC_2026-11-19.md §1 (which quotes Rev 11 lines 216–221); the reporting definition is also in §5. The source file is pinned by Git blob SHA-1 923655f20337b99f11e400f3428d1d18ac34c96d, at commit ccd95e4c125d081abca95153f9af9c9a28d65b9a.

u_j never enters the numerator or denominator of C_D. k_unresolved remains a separate component of the exact cell identity. For a complete VALID variant with k_fail = 0, the report uses the categorical label NO OBSERVED FAILURES, not a numeric predictor value. This is an implementation/reporting choice, not a claim that the convention is settled across instruments. The measurement specification §4 explicitly notes that the k_fail = 0 convention is inconsistent across instruments, even though its §1 transcription of Rev 11 states C_D = 0 with the NO OBSERVED FAILURES label.

## 2. What is checked

### Schema-local checks

The checker applies the packaged revision 0.6 schema, including all 17 required root fields, nested field types, constants, enums, references, conditional status rules, digest patterns, date-time formats, record cardinalities, and additionalProperties=false at every level where the schema specifies it. This rejects unknown root fields, outcome-bearing extra fields inside variants or diagnostic results, null required evidence objects, malformed digest values, malformed references, and malformed status decisions.

### Manifest-local semantic checks

- Parent IDs and variant IDs are unique in the manifest.
- Each variant's parent_id exists in parent_roster, and its Z_id agrees with that roster entry.
- Diagnostic record IDs are unique within each variant.
- All complete VALID variants have identical record-ID sets. Reuse of the same frozen-bank IDs across variants is permitted. This does not match those IDs to the actual bank.
- Identical semantic-source or runnable-artifact digests across different variants are flagged for explicit duplicate-variant adjudication; variants are never automatically collapsed.
- Non-VALID status decisions must use the status-appropriate decision basis, carry all seven schema-required fields, assert both terminal-value and derived-count consultation flags as false, and use record-presence/identity metadata only for INCOMPLETE.
- The locally checkable timing conditions for pre-diagnostic INVALID and EXCLUDED_BEFORE_DIAGNOSTICS, and for EXPECTED_NOT_RUN, are checked against the campaign first-start and ledger snapshot timestamps carried in the manifest. Per-variant ledger-row reconciliation still requires the referenced external ledger and is not performed here.

A local pass is labelled LOCAL_SCHEMA_AND_SEMANTIC_CHECKS_PASS_EXTERNAL_CHECKS_NOT_PERFORMED. It is not an admission to the census.

## 3. Measurement-output rules

For VALID variants, all 64 terminal records are required, exactly eight in each D1–D8 stratum. The checker derives f, u and p from DEFINITE_FAILURE, UNRESOLVED and DEFINITE_PASS records. It derives k_fail, k_unresolved, the exact B1 cell and C_D from the failure vector. The exact rational C_D is emitted as a reduced numerator/denominator string.

For INCOMPLETE, any received records produce only provisional per-stratum f/u/p counts labelled PROVISIONAL — INCOMPLETE INVENTORY. No k_fail, k_unresolved, full cell or C_D is emitted. An incomplete status with zero received records emits no vectors.

For INVALID, EXCLUDED_BEFORE_DIAGNOSTICS and EXPECTED_NOT_RUN, the package emits no diagnostic counts, no k_fail, no k_unresolved, no cell and no C_D. No records is not interpreted as zero diagnostic failures.

## 4. Aggregate-assertion sidecar

Optional aggregate assertions are stored outside the schema-exact manifest in aggregate_assertions.schema.json format. The sidecar has:

- manifest_sha256: SHA-256 of the exact raw manifest bytes supplied to the validator;
- sidecar_schema_blob_sha1: the Git blob SHA-1 of the committed sidecar schema, pinned in the validator and checked against the file at runtime;
- aggregate_assertions: one or more entries keyed by variant_id, each containing one or more optional f, u or p vectors.

The sidecar schema is committed at census-intake/aggregate_assertions.schema.json; its Git blob SHA-1 is 72fc746c3d6129534aeb2fdbcd866842865f98c7.

The sidecar is accepted only when its manifest SHA-256 matches the exact supplied manifest and its declared schema blob SHA-1 matches the actual committed sidecar schema. Each assertion must refer to a VALID variant in that manifest. Vectors are compared with values independently derived from individual terminal records. A mismatch yields AGGREGATE_MISMATCH; malformed vectors yield MALFORMED_AGGREGATE.

The sidecar can never change the manifest's validation decision. The combined report preserves manifest_report.manifest_decision separately from sidecar_report.sidecar_decision. A rejected or mismatched sidecar remains a sidecar rejection, not a revision of the manifest decision. A sidecar cannot be validated without the matching manifest bytes.

## 5. Explicitly unperformed checks

This package does not retrieve, read or verify the referenced external artifacts. In particular, it does not verify:

- diagnostic record IDs or stratum assignments against the frozen bank record manifest;
- bank hashes or record-manifest hashes against the bank artifact;
- exact one-to-one variant coverage against the frozen variant inventory;
- q_id membership against the q registry;
- Z_id membership against the external family map;
- per-variant run-ledger rows, execution states, start times or full status-to-ledger reconciliation;
- cross-file identity among the roster, q registry, family map, inventory, bank, build and diagnostic-run files;
- historical exposure evidence or the contents of a future bank-generation protocol;
- external evidence retrieval, source provenance or artifact integrity.

A digest or reference that is syntactically valid is not a verified artifact. The output repeats this boundary.

## 6. Installation and use

Python 3.9 or newer is required. The dependency is pinned in requirements.txt.

Install from the repository root:

    py -m pip install -r census-intake/requirements.txt

Manifest only:

    py census-intake/validate_records.py --manifest path/to/manifest.json --report path/to/report.json

Manifest plus optional aggregate sidecar:

    py census-intake/validate_records.py --manifest path/to/manifest.json --sidecar path/to/aggregate_assertions.json --report path/to/report.json

The JSON report has separate manifest_report and sidecar_report sections. A report without a sidecar has sidecar_report set to null.

Exit codes: 0 means local checks passed for the supplied manifest and, when supplied, its sidecar; 2 means a manifest or sidecar local rejection; 3 means an unreadable/malformed input or packaged-schema integrity/dependency error.

## 7. Tests and authoring history

tests/test_b1_census_intake.py contains synthetic adversarial fixtures. It tests the complete 17-field envelope; unknown fields at the root and nested levels; both prohibited status-decision consultation flags; null/malformed digests and evidence references; status-specific output including the false-zero correction; exact formula citation; cross-variant record-ID rules; sidecar hash binding and mismatch codes; and CLI outcomes. The tests use invented IDs, timestamps and digests only.

tests/test_gate1_inputs.py began as a GLM-authored 13-test suite and is extended in the GPT repair to 25 tests. The expanded suite covers C1–C7 intake boundaries, C4 effective-parent deduplication and adopted-family-map hash binding, C5 compliance-only reporting, C6 note-presence versus adequacy, schema blob pinning, real-inventory validation, q-registry crosswalks, and both synthetic-demo and non-demo pre-registration builds. All fixtures use invented IDs and hashes. The full census-intake suite passed **84/84 tests** on CPython 3.13.18 against the exact candidate repair blobs on 2026-11-23.

Historical code authorship is preserved accurately. The local agent HY4 authored the earlier prototype (0060e7b) and v0.2 successor (fd0b34b). Both commits remain unchanged in Git history. GPT inspected those implementations, found that they did not enforce the reviewed full manifest contract, and authored this v0.3 successor rewrite. The earlier implementations are not represented as GPT-authored. Claude agreed to the correction approach and conditions before implementation; that agreement is not a code PASS. Claude's independent review of this v0.3 successor concluded on 2026-11-23 with a PASS for the reviewed local structural intake checks and the syntax repair; the verdict, the withdrawn zero-convention objection and the limits are recorded in PR #11.

The v0.2 partial record_schema.json is removed from this successor branch to avoid presenting it as the controlling contract; its historical bytes remain available in the v0.2 commit. The prototype review packet and dated historical correction are also retained unchanged. See CORRECTION_RECORD_2026-11-23.md and REVIEW_PACKET_FOR_CLAUDE_V0_3_2026-11-23.md.

The C9 bank artifact exists from run 41591572358 (artifact ID 13210063805; SHA-256
`6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`). It contains generated
diagnostic and held-out input banks and oracle outputs; the held-out bank is publicly exposed,
not sealed. This repair does not retrieve, regenerate, or use those bank files. No parent solver
bodies or diagnostic outcome records were produced, and no mutation allocation was supplied or
reconstructed. Gate 1 remains BLOCKED / NOT ASSESSABLE; the scientific proposition remains unproven.
