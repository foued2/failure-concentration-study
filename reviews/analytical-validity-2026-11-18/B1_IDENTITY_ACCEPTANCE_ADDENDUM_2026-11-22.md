# B1 78-record identity acceptance addendum

**Date:** 2026-11-22  
**Status:** OWNER ACCEPTANCE RECORDED; IDENTITY SOURCE ACCEPTED; EXECUTION NOT AUTHORIZED  
**Applies to:** B1 v1.7 and the 78-record public development bank only

## 1. Owner decision

On 2026-11-22, the repository owner expressly accepted the documentary chain identifying the fixed 78-record B1 development bank and authorized this documentation-only addendum.

The accepted status is **source-recovered and owner-accepted**. This accepts the identity and documentary attribution of the 78-record population. It does not assert that B1 v1.7 itself enumerates the canonical IDs; the IDs are reconstructed from the preserved source artifact and recorded in the v3 derived manifest.

## 2. Accepted source identity

The source is the preserved GitHub Actions artifact:

- Workflow run: `41591572358`
- Artifact ID: `13210063805`
- Archive size: `75,523` bytes
- Archive SHA-256: `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`

The v3 identity audit records the archive-member hashes, the 80 raw presentations, the 78 unique canonical identities, and the one-to-one match between the 78 canonical identities and 78 oracle records. The v3 JSON and CSV manifests are derived reporting artifacts, not B1-issued enumerations.

Their exact derived-file identities are:

- CSV SHA-256: `af9c0d5adc2977cc8f3c0dc5053ab80c808bdb38bccf388416362fa6ac2bf95f`
- JSON SHA-256: `f3289fec5749b76ec4abc743e23f61b889d8831fc055590b034656f4d6bd1989`

These checksums are recorded in v3 audit §10 and are repeated here to make the accepted source-to-manifest chain directly traceable.

## 3. Accepted documentary chain

The owner accepts the following chain as sufficient documentary attribution for the fixed 78-record B1 development population:

1. B1/M1 Rev 1.1 §1.4 defines the population as 78 unique canonical records in the fixed, publicly exposed held-out bank.
2. Rev 1.4 §1 carries forward the 78-record bank definition and defines per-record correctness on canonical development records.
3. B1 v1.7 §1 and its acceptance record retain the fixed 78-record public-development-bank scope.
4. `B1_DECISION_RECONCILIATION_2026-11-11.md` §6.1 pins the source archive digest to Actions artifact `13210063805`, run `41591572358`; §§6.2–6.5 record publication lineage and exposure.
5. `B1_78_IDENTITY_AUDIT_2026-11-21_v3.md` documents direct reconstruction and byte-level checks against the preserved artifact.

This acceptance concerns documentary identity and attribution. It does not convert the public development bank into a sealed confirmatory set or extend the target to new records or new parent implementations.

## 4. Row-joining and reporting convention

- `canonical_id` is the authoritative key for joining any future record-level tables to the reconstructed 78 identities.
- `B1_identity_reporting_index` is a deterministic lexicographic reporting index from 1 to 78. It is **not** recovered historical B1 row numbering and must not be represented as historical \(r = 1,\ldots,78\).
- The v3 CSV and JSON manifests are derived views of the accepted source identities. They do not amend or replace B1 v1.7.

## 5. Explicitly unresolved decisions

This acceptance does not decide or imply any of the following:

1. **Historical row numbering:** the historical B1 (r)-to-identity ordering has not been recovered.
2. **H6 primary presentation and aggregation:** the two raw-order presentations in each H6 pair remain documented as original/permutation construction roles. No primary-order selection, both-orders rule, or aggregation rule is adopted.
3. **Unresolved-status handling:** the rule for unresolved solver statuses remains unspecified.
4. **Outcome coding:** no outcome coding rule is adopted here, and no solver-outcome matrix (Y_{v,r}) is created or accepted.

These items require separate, explicit measurement decisions before any outcome construction could be considered.

## 6. Execution boundary and project status

**This addendum is not an execution GO.** It does not authorize solver construction or execution, diagnostic collection, outcome labelling, creation of the (Y) matrix, sampling, fitting, predictive analysis, bank reuse, or changes to frozen B1 v1.7.

B1 execution remains **NOT AUTHORIZED**. Gate 0 remains **OPEN**; (P) remains unproven; no novelty or predictive claim is licensed. The project pause remains in force.

## 7. Related records

- `B1_78_IDENTITY_AUDIT_2026-11-21_v3.md`
- `B1_78_ROW_IDENTITY_RECOVERY_2026-11-21.md`
- `B1_78_CANONICAL_ID_MANIFEST_2026-11-21_v3.csv`
- `B1_78_CANONICAL_ID_MANIFEST_2026-11-21_v3.json`
- `B1_DECISION_RECONCILIATION_2026-11-11.md`
