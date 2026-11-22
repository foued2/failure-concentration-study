# B1 census intake v0.2 — correction record (2026-11-22)

## 1. Decision implemented

GPT accepted Claude's **NOT PASS** verdict on prototype commit `0060e7b` and the two-reviewer correction
scope. The prototype remains held and its commit is unchanged. This record covers the successor
implementation only. Claude's independent review of the successor has not yet been rendered.

## 2. Scope implemented

| Brief item | Implementation |
|---|---|
| Actual B1 record structure | `diagnostic_record_results` entries with `diagnostic_record_id`, `stratum_id`, `terminal_status`; individual terminal records are the source of truth |
| 64 results for `VALID`, eight per stratum, unique IDs, valid statuses | Enforced with `VALID_RESULT_COUNT`, `STRATUM_RESULT_COUNT`, `DUPLICATE_RECORD_ID`, `INVALID_TERMINAL_STATUS` |
| Primary basis `record_level_64` only | Enforced with `NON_STRING_EXPOSURE_BASIS` and `UNSUPPORTED_EXPOSURE_BASIS`; canonical-60 has no path |
| Derive f, u, p and k from terminal records; `C_D` from failures only | Enforced; exact rational output; unresolved excluded from numerator and denominator |
| `k_fail = 0` label | Exactly `NO OBSERVED FAILURES`, no numeric value |
| Aggregates as consistency checks | `AGGREGATE_MISMATCH`, `MALFORMED_AGGREGATE`; absent vectors derived |
| Cross-variant ID sets | Reuse accepted; within-variant duplicates and differing complete `VALID` sets rejected |
| Provenance claim boundary | Exact label `SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED` in output header and README |
| Empty manifest and basis types | `EMPTY_MANIFEST`; all five non-string basis types produce a controlled rejection |
| Status-specific rules | VALID / INCOMPLETE / INVALID / EXCLUDED_BEFORE_DIAGNOSTICS / EXPECTED_NOT_RUN implemented per the reviewed 0.6 conditional structure |

Aggregate `f`/`u`/`p` fields are an intake extension for the consistency check and are not fields of the
reviewed 0.6 schema. The validator does not claim full 0.6 conformance.

## 3. Artifacts

| File | Bytes | SHA-256 (working-tree bytes) |
|---|---:|---|
| `README.md` | 6,404 | `040029d4ca36da9b7befc7a987b54c09549391339184d569ea3c1e13869649f6` |
| `record_schema.json` | 3,894 | `455d0785057efaeed99036fb095280da0482e8a8adf37208eaea02ca5ffe84da` |
| `validate_records.py` | 16,660 | `ff1cfd5b23704aa7dc159573609740ff7dbe09056aa48d93cd667d6ea8bfd0ad` |
| `tests/test_b1_census_intake.py` | 13,044 | `0b883b8e30e8b2b9be04bf43e51896ad554093d164f0afc49acd91b07758a62f` |
| `REVIEW_PACKET_FOR_CLAUDE_2026-11-22.md` | 8,088 | `bbf4c96dbddd49d914fbe681f4ae8b9fe82844cc25948f7deefd43ac21443724` |

Command: `py -m unittest discover -s census-intake/tests -v`
**Result: 25 tests run, 25 passed.** One earlier fixture defect (a 65-result case that sliced a
64-element list) was corrected before the final run; no validator logic changed as a result.

## 4. Review-packet correction

The earlier review packet's 4(b) reproduction was incomplete. A dated correction was **appended** to
`REVIEW_PACKET_FOR_CLAUDE_2026-11-22.md` §6; the original review was not rewritten. It distinguishes
the minimal object (which never reached the basis check) from complete records: list and dictionary
bases raised the uncaught `TypeError`; number, Boolean and null were already controlled. The successor
uses an `isinstance` check before any dict lookup and tests all five types separately.

## 5. What this does not establish

No real manifest was validated. No bank membership, artifact provenance or source integrity was
checked. No parents were selected, no solvers built or run, no diagnostics collected, no census
computed, no model fitted. Gate 1 preflight remains BLOCKED / NOT ASSESSABLE. `P` remains unproven.

The 25 passing synthetic tests establish software behaviour only. They are not Claude's review, not a
PASS verdict, and not authorization for any downstream activity.
