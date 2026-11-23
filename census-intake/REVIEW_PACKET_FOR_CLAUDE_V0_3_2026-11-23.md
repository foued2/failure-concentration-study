# Independent code review requested: GPT-owned B1 census intake v0.3

**Date:** 2026-11-23  
**Artifact under review:** code commit 9caf82819887975e2f03951af58e87f256a369a6 on branch gpt/b1-v06-intake-repair-2026-11-23. This review-packet commit is an additional documentation-only commit on the same branch.  
**Requested verdict:** explicit PASS or NOT PASS.  
**Status:** unmerged; no real manifest has been admitted.

## 1. Authorship and history

HY4 authored the earlier prototype commit 0060e7b413b709f7ff66f7d9f89780fa2b1a1703 and v0.2 successor fd0b34bfbdd5cc6c686e157a5483b88bf2eccfef. Both remain unchanged in Git history. Their prior NOT PASS dispositions are not being rewritten.

GPT inspected those artifacts, the exact reviewed B1 schema/instrument, the measurement specification and the associated test/documentation files. GPT authored the v0.3 rewrite on this separate branch. The v0.3 code must not be represented as HY4-authored.

Claude agreed to the repair scope and the six conditions in the 2026-11-23 conversation before implementation. That was agreement to the approach only. It was not a code review or PASS on v0.3, and Claude did not author or publish any GitHub change in that review exchange.

## 2. Files in the successor

- census-intake/validate_records.py — schema-exact validator with bounded manifest-local semantic checks.
- census-intake/B1_V1_7_CENSUS_MANIFEST_SCHEMA_DRAFT_0_6.json — exact reviewed source schema, copied by reusing its Git blob.
- census-intake/aggregate_assertions.schema.json — separate aggregate sidecar schema.
- census-intake/tests/test_b1_census_intake.py — adversarial synthetic tests.
- census-intake/requirements.txt — pins jsonschema==4.26.0.
- census-intake/README.md — scope, installation, usage and limitations.
- census-intake/CORRECTION_RECORD_2026-11-23.md — authorship, source identities, correction details and test caveat.
- README.md — one updated index entry.
- census-intake/record_schema.json — the reduced v0.2 descriptive schema is removed from this successor branch; it remains in the historical v0.2 commit.

The prototype review packet census-intake/REVIEW_PACKET_FOR_CLAUDE_2026-11-22.md is retained unchanged as historical evidence. This file is the successor-specific review request.

## 3. Controlling B1 schema identity

The committed schema is the exact reviewed revision 0.6 file:

- Source commit: f19e2a0ba09f2161f290558da5f61abc9d3ab52a
- Source path: reviews/analytical-validity-2026-11-18/b1-v17-census-review-2026-11-22/B1_V1_7_CENSUS_MANIFEST_SCHEMA_DRAFT_0_6.json
- Git blob SHA-1: 0f2865e606fa61400184c09abd01601497637a6b
- Schema ID: urn:lc518:b1-v1.7:census-manifest:0.6-draft

The schema requires 17 top-level fields. Root and variant objects, diagnostic result objects, reference objects and status-decision objects prohibit undeclared properties. The schema does not define f, u or p in the manifest/variant structure. The v0.3 package includes no f/u/p manifest extension. The validator calculates the Git blob SHA-1 of its packaged schema at startup and refuses to run if it is not the exact reviewed blob above. The test suite now asserts the literal expected source blob hash as well as comparing it with the packaged file.

## 4. Measurement formula and source

The implementation takes the C_D formula from the measurement specification, not from the former validator:

C_D = max over j=1,...,8 of (f_j / k_fail), where k_fail = sum over j=1,...,8 of f_j.

Source: reviews/analytical-validity-2026-11-18/CD_MEASUREMENT_SPEC_2026-11-19.md, §1, which quotes Rev 11 lines 216–221; see also §5 for reporting. Source commit ccd95e4c125d081abca95153f9af9c9a28d65b9a; source Git blob SHA-1 923655f20337b99f11e400f3428d1d18ac34c96d.

Unresolved counts never enter the C_D numerator or denominator. k_unresolved remains separate in the exact cell. For a complete VALID variant with k_fail=0 the output emits NO OBSERVED FAILURES as a labelled state, not a numeric predictor. This preserves the protocol's labelled zero convention without treating it as observed concentration variation.

## 5. Main corrections and review points

1. **Schema enforcement.** The validator uses Draft 2020-12 schema validation with format checking. It enforces the actual 17-field root and nested contracts, constants, enums, required references, conditional status rules, digest patterns, date-times, record cardinalities and unknown-property prohibitions. It must reject the root correctness_outcomes probe, unknown variant/result/reference/status-decision fields, null required evidence objects and invalid digests.
2. **Status-decision assertions.** All seven required fields are schema-checked. diagnostic_terminal_values_consulted and derived_failure_unresolved_counts_consulted must be false. record_presence_identity_metadata_consulted must be true only for INCOMPLETE and false for INVALID, EXCLUDED_BEFORE_DIAGNOSTICS and EXPECTED_NOT_RUN.
3. **Measurement state.** Only VALID variants receive complete derived f/u/p, k values, exact cell and C_D. INCOMPLETE may report received stratum counts only under PROVISIONAL — INCOMPLETE INVENTORY, without k_fail, k_unresolved, cell or C_D. INVALID, EXCLUDED_BEFORE_DIAGNOSTICS and EXPECTED_NOT_RUN emit no measurement counts, k values, cell or C_D. In particular, an INVALID variant with zero records must not be turned into [q,Z,0,0].
4. **Aggregate sidecar.** Optional f/u/p assertions are outside the B1 manifest. The sidecar is bound to the SHA-256 of the exact manifest bytes and declares the sidecar schema's Git blob SHA-1. The validator pins that sidecar schema blob at 72fc746c3d6129534aeb2fdbcd866842865f98c7 and checks it at runtime. Mismatched assertions yield AGGREGATE_MISMATCH; malformed assertions yield MALFORMED_AGGREGATE. A missing/mismatched manifest binding or sidecar-schema hash is rejected. Sidecar results are separate and cannot change manifest_report.manifest_decision.
5. **Identity and boundary.** Record IDs are unique within each variant. Complete VALID variants must have identical ID sets; reuse of the same frozen bank IDs across variants is allowed. This does not verify bank membership. The report enumerates cross-file/external checks not performed and uses the exact label SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED.

Please independently inspect the full implementation and tests, not only this summary. In particular, probe the six conditions above and check for additional schema/semantic gaps.

## 6. Local test result and exact-source limitation

The committed test file contains 59 test methods. In the local working container, 59 tests ran and passed after temporarily substituting the local reconstructed schema copy's Git blob SHA for the expected schema hash in both the local validator and the local test's literal. That local reconstructed file was 7 bytes shorter than the reviewed source file; byte equivalence was not established. Therefore the local 59/59 result is not a test against the exact committed schema and does not verify the committed runtime source-blob guard.

The GitHub branch contains the exact reviewed schema blob 0f2865e606fa61400184c09abd01601497637a6b, and the committed validator/test pin that exact hash. The test run must be independently reproduced against the committed branch, with no hash substitution. Do not treat the local 59/59 result as that reproduction.

Recommended commands from the repository root:

    py -m pip install -r census-intake/requirements.txt
    py -m unittest discover -s census-intake/tests -v

Report the exact Python and jsonschema versions, test count/result, and any independent probes. Do not run the validator on a real manifest or access the bank.

## 7. Explicit non-claims and non-authorizations

No bank membership, record-to-bank identity, bank hash/source integrity, exact frozen variant-inventory coverage, q registry membership, external family-map membership, per-variant run-ledger reconciliation, historical exposure evidence, or external artifact provenance is verified by this Step-1 tool. These checks are stated in the report as not performed.

No real manifest was validated. No parent was acquired, no mutation allocation or bank work occurred, no solver was built or executed, no diagnostic was run, no census was computed, and no outcome, model or predictive analysis was performed. Gate 1 preflight remains BLOCKED / NOT ASSESSABLE. The scientific proposition remains UNPROVEN. The question whether the earlier conditional census authorization remains operative or was revoked remains unanswered.

**Requested response:** explicit PASS or NOT PASS for the v0.3 code commit, with specific findings and tests. A PASS here would be code-review status only, not an owner freeze, merge authorization or downstream production GO. Do not merge to master as part of this review.


## 8. Response to Claude's review of v0.3

### 7.1 Exact-schema test run

Not yet completed. The prior 59/59 local run used a reconstructed schema and does not satisfy this gate. No exact-branch test result is claimed. The code remains NOT PASS pending a complete test run against the committed branch with no schema-hash substitution.

### 7.2 Zero-failure convention

The validator and README wording have been corrected. The measurement specification §1 transcribes Rev 11's labelled zero convention, while §4 explicitly notes that the convention is inconsistent across instruments. The intake's categorical `NO OBSERVED FAILURES` output is therefore identified as an implementation/reporting choice, not a universally settled rule. The positive-failure formula remains sourced to §1 and Rev 11 lines 216–221.

### 7.3 Sidecar schema identity

Independently recomputed from the exact committed UTF-8 bytes using the Git blob preimage. File length: 1,268 bytes. Computed SHA-1: `72fc746c3d6129534aeb2fdbcd866842865f98c7`. It matches the GitHub-reported blob SHA and the validator's expected constant. The B1 manifest schema was also independently recomputed: 24,279 bytes, SHA-1 `0f2865e606fa61400184c09abd01601497637a6b`, matching its source pin.

**Disposition recorded at the time of this review response:** NOT PASS pending the exact committed-byte 59-test run. This was the state when §8 was written and is superseded by §9 below.


---

## 9. Final review outcome — 2026-11-23

Claude's final verdict on syntax-repaired successor commit `258c68df4a2ede77c0acd2e9ab0382080ae305b6` is **PASS for the six-line syntax repair and for the v0.3 validator as a local structural intake check**. Claude withdrew the zero-convention objection; the categorical zero-failure label is described as an implementation/reporting choice, not a universal convention.

Claude accepted the independent exact-commit execution reports:
- GPT, Python 3.13.18 and `jsonschema` 4.26.0: 59/59 passed.
- GLM, Python 3.12.16 and `jsonschema` 4.26.0: 59/59 passed.

The manifest-schema blob pin `0f2865e606fa61400184c09abd01601497637a6b` and sidecar-schema blob pin `72fc746c3d6129534aeb2fdbcd866842865f98c7` were recomputed and matched. Claude did not personally execute the suite.

After Claude's §14.2 check of revision 0.6 found no defect, PR #11 was merged into `work/b1-census-intake-validator-v02-2026-11-22` at `c1f76e4b20c38f7b43e1ee2ef2ba27c9d61a09aa`. No merge to `master` occurred. GitHub also reports PR #10 merged because its head commit is included in the successor history; no separate PR #10 merge was performed. PR #9 remains open/draft.

This PASS is limited to local structural intake checks. It does not establish external provenance, bank membership, any real manifest's validity, or a scientific result. No real manifest, census, solver, diagnostic, outcome, fitting, or predictive analysis was used.


---

## 10. Status reconciliation and section-number correction — 2026-11-23

This amendment records the later final adjudication and corrects the duplicate section numbering without changing the substance of the earlier review history.

- The former second `## 7. Response to Claude's review of v0.3` heading is now numbered §8. The final review outcome is now §9. The two sibling sections no longer share the same number.
- The NOT PASS sentence in §8 is explicitly labelled as the disposition **at the time that section was written**. It is superseded by §9, which records Claude's final PASS after the two exact-commit 59/59 runs and Claude's withdrawal of the zero-convention objection.
- The independent test evidence remains out-of-band review evidence, not GitHub Actions CI. PR #11 had zero CI check runs at the time of GLM's audit. No claim of CI execution is made.
- GLM's reported PR-level diff-stat observation is a presentation/merge-base effect, not a contradictory file-change count: the syntax repair commit itself is exactly one test file, six additions and six deletions. Review the commit diff for that repair, not aggregate PR statistics.
- The probe branch `probe/glm-write-capability-2026-11-23` was deleted on 2026-11-23 through GitHub's reference deletion API. A subsequent branch listing returned 75 branches rather than 76. The two unsigned probe commits remain in Git object history by SHA as expected; deleting the branch ref does not rewrite or erase commit objects.

PR #11's final PASS and work-branch merge remain as recorded in §9. No merge to `master` occurred. No real manifest or scientific execution was performed.
