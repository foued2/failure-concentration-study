# B1 78-record identity acceptance addendum

**Date:** 2026-11-22  
**Status:** OWNER ACCEPTANCE RECORDED; IDENTITY SOURCE ACCEPTED; EXECUTION NOT AUTHORIZED  
**Applies to:** B1 v1.7 and the 78-record public development bank only

## 1. Owner decision

On 2026-11-22, the repository owner expressly accepted the documentary chain identifying the fixed 78-record B1 development bank and authorized this documentation-only addendum.

**Decision provenance.** This decision records the owner's explicit written instruction in the project conversation on 2026-11-22: “ACCEPT AND PROCEED FOR THE REST. LET US END THIS.” The instruction is an owner-authored conversational authorization, not a repository artifact. A reviewer whose accessible transcript does not include that earlier owner message cannot independently authenticate the quotation from this repository alone. This addendum records the owner's decision; it does not present the quotation as independent corroboration or as a scientific finding.

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

## 8. 2026-11-22 byte-level revalidation of the source archive

A fresh copy of the original GitHub Actions artifact was downloaded directly by GPT on 2026-11-22 from artifact ID `13210063805` (workflow run `41591572358`). The archive was 75,523 bytes and its recomputed SHA-256 was:

`6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`

The following member hashes and sizes were recomputed from that ZIP:

| Member | Bytes | Recomputed SHA-256 |
|---|---:|---|
| `bank/heldout_bank.json` | 40,218 | `b273c053e874f212f060ff23791f9be445a48203cbbde0ca1b285192093d26d6` |
| `bank/heldout_oracle_outputs.json` | 15,262 | `eaae81040424881cc9939e7415a8a5a0328fa870bd2a790d0b4409babd03e244` |
| `lc518_generator.py` | 56,845 | `848984cac427547955a04b2e5c379762149ad94a37711a6483008fd55f2c161b` |

GPT independently recomputed the canonical ID from each raw record using the exact payload `{"amount": amount, "coins": sorted(coins)}`, sorted-key compact UTF-8 JSON, and SHA-256 with the `C-` prefix. All 80 raw records passed their record-hash check; the 80 raw rows yielded 78 unique canonical IDs; the 78 oracle objects had an exact one-to-one canonical-key-set match; and all 80 raw records referenced the correct oracle-member digest.

The recomputed sorted canonical-ID set digest was `01bb0e4c8edb2c4a0678d1b6c65c4295bdaf59c9baf2436d793f25c740c3cccd`, matching the 5,226-byte LF-terminated ID-list digest recorded in v3 identity audit §4. The two canonical duplicate groups are exactly H6-P01 (`H057`/`H058`) and H6-P02 (`H059`/`H060`). No aggregate canonical-payload set digest is asserted here.

**Scope of this revalidation.** This is a fresh GPT-side byte-level check of the source ZIP, its listed members, record hashes, canonical identities, and oracle key set. It is not a claim that Claude independently performed the same raw-byte reconstruction. Claude's supplied read-only review separately reports that the CSV and JSON manifest file checksums match the actual repository files; this revalidation did not independently recompute those two complete file checksums or repeat a CSV/JSON row-by-row comparison. No solver outcomes, (Y_{v,r}) labels, H6 primary rule, or unresolved-status rule were created or decided.

## 9. Correction to the earlier payload-set digest statement

An earlier version of this addendum stated that the aggregate canonical-payload set digest `8b67d1f0193d85838a98486ae4fbf7ef17d948b1cca4abdfc4c0180ae61e48fa` had been reproduced and matched the v3 identity audit. That statement is withdrawn. The v3 audit does not report this aggregate digest, and the serialization convention that would produce it has not been established reproducibly. The value must not be cited as a verified result.

This withdrawal does not affect the verified canonical-ID rule, the 80/80 raw-record checks, the 78 unique canonical identities, the exact 78/78 oracle-key-set match, the 5,226-byte sorted-ID digest, or the per-row canonical-payload checks used to recompute each canonical ID. The accepted identity set rests on those checks and the documentary chain, not on an aggregate payload-set digest.

