# manifest-validator

Deterministic validator for a population manifest, implementing the M1-si structural
support contract in `../GPT_ADJUDICATION_MANIFEST_VALIDATOR_V0.1_2026-11-17.md` §4 with
corrections A–I. Standard library only; no study data.

## Run

```
py -3 run_tests.py
py -3 validate_manifest.py --manifest fixtures\valid_realized.json --limits fixtures\limits_standard.json --schema manifest_schema.json
```

Exit code `0` = valid, `1` = invalid, `2` = usage or IO error. The report is canonical
JSON (`sort_keys`, `indent=2`, `\n` terminator), so repeated runs are byte-identical.

## What the checks enforce

| Check | Behaviour |
|---|---|
| `CD_SUM_MISMATCH` | declared `k_fail` must equal the sum of the eight stratum counts |
| `CD_MISMATCH` / `CD_FORMAT` | `C_D` is recomputed as `max_j f_j / k_fail` from exact fractions and compared to the declared canonical rational (`"3/5"`, not `0.6`) |
| `CD_ZERO_CONVENTION` | `k_fail = 0` requires `C_D = null` and `concentration_label = "NO_OBSERVED_FAILURES"` |
| `DUP_OPERATION_COORDINATE` | duplicate (parent, operator class, site, settings) is retained, aliased and counted once; **same site with different settings is admissible** (correction A) |
| `DUP_ARTIFACT_DIGEST` / `DUP_SOURCE_DIGEST` | scoped to one parent and exact cell; duplicates become aliases, not independent variants (correction B) |
| `CROSS_PARENT_DIGEST` | warning only: provenance review required, no invalidation (correction B) |
| `LIMITS_ECHO_MISMATCH` / `LIMITS_ECHO_VALUE` / `CEILING_EXCEEDED` | ceilings come from the separate limits file whose SHA-256 is reported; the manifest echoes the id and every ceiling value, and any mismatch or excess is an error (correction E) |
| lifecycle | `PLANNED`, `BUILD_FAILED` and `NOT_RUN`/`INVALID`/`UNRESOLVED` records are retained but cannot contribute realized support (correction D) |
| M1-si | `REALIZED` only if one exact cell has ≥ `m1_si_min_qualifying_parents` (default 3) qualifying parents, each with an explicit **pair witness** differing in settings, `C_D`, source digest and artifact digest (correction F) |

Every report contains `pair_witness` entries, excluded records, duplicate aliases,
shortfalls, and the SHA-256 of the manifest, limits file, schema and validator.

## Boundary

This tool decides whether a proposed manifest satisfies the declared structural
conditions. It cannot create the missing parent population or mutation allocation, and
`M1-si REALIZED` does not imply optimizer convergence, a successful fit, or an available
B1 test.

## Files

- `validate_manifest.py` — validator (the normative implementation)
- `manifest_schema.json` — JSON Schema draft 2020-12, cross-checked against `jsonschema`
- `fixtures/build_fixtures.py` — deterministic synthetic fixture generator
- `fixtures/expected_results.json` — hand-declared expectations
- `run_tests.py` — 166 checks: expectations, determinism, schema agreement
