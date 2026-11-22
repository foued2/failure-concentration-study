# B1 census intake — record validator and synthetic tests

**Version:** 0.1
**Status:** step-1 infrastructure only. No scientific result. No census performed.
**Date:** 2026-11-22

This folder provides a narrow semantic validator for **per-variant diagnostic records** whose only
purpose is to decide whether such records may be admitted to the Gate 1 design-only support census.

## 1. Authorization scope

The owner authorized step 1 only on 2026-11-22: make the B1 measurement instrument executable by
building the B1-specific semantic validator and synthetic tests, scoped to getting real diagnostic
records safely and reproducibly into the census.

**Provenance.** This authorization was an explicit owner selection among stated options in the
project session. It is a conversational act; this repository does not independently attest it.

**This folder does not authorize, perform, or enable by itself:**

- parent acquisition or selection;
- mutation allocation or solver construction/generation;
- diagnostic execution, bank generation, or bank access;
- outcome collection, correctness labelling, or construction of a `Y` matrix;
- the Gate 1 support census, model fitting, or predictive analysis;
- any change to B1 v1.7, Rev 11, or the frozen `C_D` definition.

The project pause remains in force outside this step-1 scope. An admitted record is an input that the
census *may* read once separately authorized; admission is not a support finding, a Gate 1 PASS, or
evidence about `P`.

## 2. Frozen definitions used

Taken from `LC518_A2_AUDIT_PROTOCOL_DRAFT_2026-11-06.md` Rev 11 as recorded in
`reviews/analytical-validity-2026-11-18/CD_MEASUREMENT_SPEC_2026-11-19.md` §1–§3:

- eight diagnostic strata `D1..D8`, which are input categories, not mechanisms;
- `f_j` counts **definite** diagnostic failures in stratum `j`;
- `k_fail = Σ_j f_j`; `C_D = max_j f_j / k_fail`, with `C_D = 0` and status
  `NO_OBSERVED_FAILURES` when `k_fail = 0`;
- `u_j` counts **unresolved** diagnostic outcomes. It is mandatory evidence, all eight entries
  supplied, and may never be converted into a failure or an implicit zero;
- `k_unresolved = Σ_j u_j` belongs to the exact cell, not to `C_D`;
- the frozen cell is `(m, z, k_fail, k_unresolved)`, aliased in the adopted contribution statement
  as `(q, Z, k, ℓ)`. Here `q = m` is mutation identity and `Z = z` is parent family.

**Exposure basis** is a required, explicit field. Two bases exist and are not interchangeable:

| Basis | `N` | Per-stratum capacity `R_j` |
|---|---:|---|
| `record` | 64 | `(8,8,8,8,8,8,8,8)` |
| `canonical` | 60 | `(8,8,8,8,8,4,8,8)` |

Canonical `C_D` must be recomputed from canonical failure counts; it is never obtained by averaging
or selecting record-level values. This validator checks basis-consistent capacity but does not
translate between bases.

## 3. Record contract

A manifest is a JSON array of records. Each record has these fields:

| Field | Type | Requirement |
|---|---|---|
| `variant_id` | string | non-empty; unique in the manifest |
| `parent_id` | string | non-empty |
| `parent_family` | string | non-empty; the `Z`/`z` cell coordinate |
| `mutation_id` | string | non-empty; the `q`/`m` cell coordinate |
| `exposure_basis` | string | exactly `record` or `canonical` |
| `f` | array of 8 integers | each `>= 0`; definite failures only |
| `u` | array of 8 integers | each `>= 0`; **mandatory** even when all zero |
| `strata_record_ids` | object | keys exactly `D1`–`D8`; each an array of distinct non-empty strings of length `R_j` for the declared basis; no identifier reused across strata |
| `source_digest` | string | 64-character lowercase hex SHA-256 of the upstream diagnostic manifest from which the record was derived |
| `notes` | string | optional |

Any other top-level field is rejected. In particular a correctness/outcome field (`correctness`,
`Y`, `outcome`, `pass`, `fail`, or a field whose name begins with `y_`) is rejected with
`OUTCOME_FIELD_PRESENT`: the census is outcome-free by construction.

Derived by the validator for each admitted record: `k_fail`, `k_unresolved`, `C_D` as an exact
integer ratio string (or `"0"` with `NO_OBSERVED_FAILURES`), and the cell tuple
`(mutation_id, parent_family, k_fail, k_unresolved)`.

## 4. Structural schema convention

`record_schema.json` is JSON Schema draft 2020-12 and is the **descriptive** structural contract.
`validate_records.py` implements the structural and semantic checks explicitly in the standard
library; it is **not** a JSON Schema evaluator and does not claim general draft 2020-12 coverage.
If tooling cross-checks the schema, it must use a conforming external implementation.

The schema `$id` is **per revision**: it carries the version identifier and must change with every
versioned revision. The mechanical check is `$id` endswith `/v{schema_version}.json`, where
`schema_version` is the schema's own field. A stale `$id` is a defect, not a cosmetic detail.

## 5. Use

```powershell
py census-intake/validate_records.py --manifest path/to/manifest.json --report path/to/report.json
```

Exit codes: `0` all records admitted; `2` at least one record rejected; `3` input/JSON error.
The report records the SHA-256 of the manifest bytes, counts, per-record decisions with reason
codes, and derived values for admitted records. It is deterministic for identical input bytes.

The report contains **no** census decision: no eligibility flag, no LOPO fold, no PASS/FAIL gate
verdict, and no outcome data.

## 6. Tests

`tests/test_b1_census_intake.py` contains synthetic software tests only. They use constructed
fixtures with invented identifiers; no bank, solver, or outcome data is read. They cover valid
record and canonical bases, mandatory unresolved vectors, capacity and length violations, duplicate
identifiers and variants, unknown strata, outcome-field rejection, the zero-failure convention,
report determinism, and input hashing. Passing them establishes validator behaviour, not the
existence of any LC518 diagnostic manifest.

## 7. Relation to the scientific record

The root `README.md` records Gate 1 preflight as BLOCKED / NOT ASSESSABLE because no LC518
per-variant eight-stratum diagnostic manifest exists. This folder does not change that status. It
provides the intake check that such a manifest would have to pass before the census could be run
under a separate authorization.

Rationale: register §16 and reviewer-ledger §34.
