# Step-1 authorization and executed result — 2026-11-22

## 1. Authorization

The owner authorized **step 1 only** on 2026-11-22, in an explicit selection among stated options:
make the B1 measurement instrument executable by building a B1-specific semantic validator and
synthetic tests, scoped narrowly to admitting real diagnostic records safely and reproducibly into
the Gate 1 census.

**Provenance.** This is an owner-authored conversational selection in the project session. The
repository does not independently attest it; no owner-authored file was added to manufacture such
attestation.

**Not authorized:** parent acquisition or selection, mutation allocation, solver construction or
generation, bank generation or bank access, diagnostic execution, outcome collection or labelling,
`Y`-matrix construction, the support census itself, fitting, or predictive analysis. The project
pause remains in force outside this step-1 scope.

## 2. Executed work

| File | Bytes | SHA-256 (working-tree bytes) |
|---|---:|---|
| `README.md` | 6,456 | `1b1bb802bcd87b55569b8095494ae27672c17abf1969c35240a3bbe1076824f1` |
| `record_schema.json` | 2,367 | `a00fc1edcc52ea062711f034bfc8adb146fd767aca927d8bfcc291a17858aa42` |
| `validate_records.py` | 9,066 | `12caf4b48908c79ea112fd45ca75e3a39988474bba72012679b8549c3880ebae` |
| `tests/test_b1_census_intake.py` | 7,577 | `a666127126d45a1856882dc245eed45d5284a9adb50d045cbb85049013f736d1` |

Command executed from the repository root:

```
py -m unittest discover -s census-intake/tests -v
```

**Result: 18 tests run, 18 passed, 0 failed.** An earlier run had two fixture defects (a duplicate
variant also reused record identifiers, and an intra-record identifier reuse was labelled with the
inter-record reason code); both were corrected in the test fixtures and the reason-code name before
the final run. The corrections changed no scientific definition.

The validator was exercised only on constructed synthetic records with invented identifiers.

## 3. What this result establishes

- A deterministic intake check exists for per-variant diagnostic records, with basis-consistent
  capacity (`record` 64 records, 8 per stratum; `canonical` 60, four in D6), mandatory per-stratum
  unresolved vectors, exact-ratio `C_D`, and the frozen `k_fail = 0` convention.
- Outcome-bearing fields are rejected, so the intake path cannot silently import held-out
  correctness into the design-only census.
- The report carries the manifest SHA-256 and per-record reason codes, and contains no census
  decision and no gate verdict.

It establishes software behaviour on synthetic fixtures only.

## 4. What it does not establish

- No LC518 diagnostic manifest exists or was read. Gate 1 preflight remains **BLOCKED / NOT
  ASSESSABLE** as recorded in the root `README.md`.
- No scientific output was produced: no parent roster, no variants, no bank, no diagnostic
  measurements, no census result, no held-out predictive result.
- `P` remains **unproven**; B1 v1.7 and Rev 11 are unchanged; no novelty claim is licensed.
- A passing synthetic suite is not evidence that a real manifest will be admissible, that the B1
  support conditions hold, or that the design has power.

## 5. Boundary for the next decision

The next activity — producing a real per-variant eight-stratum diagnostic manifest — is production
work and requires its own explicit authorization after the population, provenance, isolation and
generation-protocol prerequisites are settled. Running this validator on a real manifest would be a
separate, later act and would still not be the census.
