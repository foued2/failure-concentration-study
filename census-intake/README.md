# B1 v1.7 census intake validator — v0.2 successor

**SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED**

**Version:** 0.2 (successor to the held `0060e7b` prototype)
**Status:** implementation complete on a separate, unmerged successor branch; independent review pending.
**Date:** 2026-11-22

This folder validates the per-variant `diagnostic_record_results` structure of a B1 v1.7 outcome-blind
census manifest. The individual terminal records are the source of truth. It admits or rejects records
for a design-only census; it does not compute census support, LOPO coverage, or any scientific result.

## 1. Exact scope label

The label `SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED` appears in the validator's output header and
in this README. The validator checks syntax and structural consistency only. It does **not** verify:

- frozen diagnostic-bank membership of any record ID;
- diagnostic artifact provenance;
- source-artifact integrity or record-to-bank identity;
- any external evidence not available to this task.

A digest string is a syntactic field, not provenance verification.

## 2. Authorization and repository handling

The owner authorized step 1: a B1-specific semantic validator and synthetic tests. GPT accepted Claude's
NOT PASS verdict on `0060e7b` and the two-reviewer correction scope; that agreement authorizes this
correction within Step 1 only.

- Prototype commit `0060e7b` is preserved unchanged in history. This is a successor commit on a separate
  branch; no history was rewritten and nothing was merged into master.
- No bank access, parent acquisition, mutation allocation, solver construction, diagnostic execution,
  outcome collection, `Y`-matrix construction, census execution, fitting or predictive analysis occurred.
- The project pause remains in force outside the Step 1 scope. Whether an earlier conditional census
  authorization remains operative is **unanswered** and is deliberately not interpreted here.
- `P` remains unproven; B1 v1.7 and the reviewed instrument are unchanged.

## 3. Record structure enforced

The manifest is a JSON object using the B1 v1.7 field names:

| Field | Rule |
|---|---|
| `schema_version` | must be `0.6-draft` |
| `study_id` | must be `LC518` |
| `measurement_basis` | must be the string `record_level_64`; the canonical-60 basis has no path and is rejected |
| `diagnostic_bank` | `stratum_ids` = D1…D8, `records_per_stratum` = 8, `total_records` = 64 |
| `parent_roster` | non-empty; each `parent_id` / `Z_id` pair unique and consistent with variants |
| `variants` | non-empty list |
| `outcome_exclusion_assertion` | all three declared values must be `false` |

Each variant requires `variant_id`, `parent_id`, `Z_id`, `q_id`, `validity_status` and
`diagnostic_record_results`. Each result requires `diagnostic_record_id`, `stratum_id` in D1–D8, and
`terminal_status` in `DEFINITE_PASS`, `DEFINITE_FAILURE`, `UNRESOLVED`.

### Status-specific rules

| Status | Results | Additional requirements |
|---|---|---|
| `VALID` | exactly 64; exactly 8 per stratum; IDs unique within the variant | `diagnostic_evidence_ref`, `semantic_source_digest`, `runnable_artifact_digest` |
| `INCOMPLETE` | 0–63 | `status_reason`, `status_decision` with `POSTRUN_COMPLETENESS_AUDIT` and identity metadata consulted, `diagnostic_evidence_ref` |
| `INVALID` | 0 | `status_reason`, status decision with `PREDIAGNOSTIC_OBJECTIVE_INVALIDITY` |
| `EXCLUDED_BEFORE_DIAGNOSTICS` | 0 | `status_reason`, status decision with `PREDIAGNOSTIC_DESIGN_EXCLUSION` |
| `EXPECTED_NOT_RUN` | 0 | `status_reason`, status decision with `EXPECTED_NOT_RUN_INVENTORY_AUDIT`; no record receipt metadata consulted |

Partial and zero-result statuses are not forced to a 64-ID set.

### Derivation

Per stratum: `f_j` = count of `DEFINITE_FAILURE`, `u_j` = count of `UNRESOLVED`, `p_j` = count of
`DEFINITE_PASS`. With eight results per stratum, `f_j + u_j + p_j = 8` by construction. Then
`k_fail = Σ f_j`, `k_unresolved = Σ u_j`.

`C_D = max_j f_j / k_fail` when `k_fail > 0`, emitted as an exact rational string. Unresolved outcomes
never enter its numerator or denominator. When `k_fail = 0`, the emitted label is exactly
`NO OBSERVED FAILURES`, with no numeric value.

### Aggregates are non-authoritative

`f`, `u` and `p` fields are optional consistency checks. If absent, the vectors are derived. If present
and equal to the derived vectors, they are retained only as checks. If present and unequal, the variant
is rejected with `AGGREGATE_MISMATCH`; a structurally malformed vector gets `MALFORMED_AGGREGATE`.

These three fields are an intake extension for the consistency check and are not part of the reviewed
revision 0.6 schema. This validator does not claim full 0.6 structural conformance.

### Cross-variant record IDs

The frozen bank is expected to be reused. The same IDs across complete `VALID` variants are accepted;
IDs duplicated within one variant are rejected. All complete `VALID` variants must carry an identical
ID set, otherwise `CROSS_VARIANT_ID_SET_MISMATCH`. This is an ID-set check only — not a bank-membership
or source-artifact check.

## 4. Use

```powershell
py census-intake/validate_records.py --manifest path/to/manifest.json --report path/to/report.json
```

Exit codes: `0` all admitted with no manifest-level findings; `2` any rejection or `EMPTY_MANIFEST`;
`3` input/JSON error. The report is deterministic for identical bytes and carries the manifest SHA-256.
It contains no census verdict, no eligibility flag, no gate decision and no outcome data.

## 5. Tests

`tests/test_b1_census_intake.py` contains 25 synthetic tests with invented identifiers. They cover the
case table in the correction brief, every non-string basis type, status-specific rules, aggregate
handling, the exact zero-failure label, cross-variant ID sets, determinism, and CLI exit codes. Passing
them establishes validator behaviour on synthetic fixtures only; it does not establish that a real
manifest exists, is admissible, or supports a census.

## 6. Review status

Claude's independent review applies to this successor, not to the held prototype. The earlier review and
its dated 4(b) correction are in `REVIEW_PACKET_FOR_CLAUDE_2026-11-22.md`. See
`CORRECTION_RECORD_2026-11-22.md` for the implementation scope and non-authorizations.

Rationale in the scientific record: register §17 and reviewer-ledger §35.
