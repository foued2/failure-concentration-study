# LC518 D0.3 reconciliation result: H80 records, oracle keys and rejection attempts

**Record ID:** LC518-D0.3-RESULT-2026-11-21  
**Date:** 2026-11-21  
**Status:** H80-TO-ORACLE RECONCILIATION PASS; H80-TO-B1 IDENTITY COMPARISON OPEN (B1 IDENTITY SOURCE NOT ESTABLISHED)  
**Authorization:** Owner GO recorded in `docs/LC518_D0_3_OWNER_GO_AND_HASH_INVENTORY_2026-11-21.md`.  
**Artifact inspected:** GitHub Actions artifact `13210063805`, `lc518-bank-run-41591572358-1`, run `41591572358`.  
**Scope limit:** The historical H80 bank, its oracle attachment, its rejection sidecar, its publication report, and run-manifest fields were inspected. No diagnostic outcomes, solver outputs, protected E3 records, or other Actions artifacts were inspected.

---

## 1. Integrity and provenance

The downloaded archive is 75,523 bytes. Its SHA-256 is:

`6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`

This exactly matches the GitHub Actions artifact metadata digest. The ZIP member inventory and all 15 member SHA-256 hashes were recorded in the pre-inspection inventory document before parsing any JSON or sidecar.

Relevant internal file hashes:

| File | Bytes | SHA-256 |
|---|---:|---|
| `bank/heldout_bank.json` | 40,218 | `b273c053e874f212f060ff23791f9be445a48203cbbde0ca1b285192093d26d6` |
| `bank/heldout_oracle_outputs.json` | 15,262 | `eaae81040424881cc9939e7415a8a5a0328fa870bd2a790d0b4409babd03e244` |
| `bank/heldout_bank.rejections.jsonl` | 2,575 | `ef420f4e56bf15f15bc3f1d9c17838fbbee48c344dbab9e2068efe70260a7d92` |
| `bank/canonical_disjointness_report.json` | 1,085 | `839014e078580016c644667d41b9d83ab4bb8b3e888828c9cac67e952db5520c` |
| `logs/run_manifest.json` | 3,178 | `698f4e99731f707a0f2474fdb1d46b972cbc7ebbff76d9f247885b139d14201f` |

Run-manifest provenance reports C9 source SHA-256 `f291ae879ef6e046c6715bb0e6a84cd5a3f5e69f07ace09e213db9b84d8b87fe`, C9 source commit `511bc2099ecff74b4f850b169ceef7f853c334a0`, execution-protocol SHA-256 `9c54ffc2143eef807dad51ee5ba92e494e4588fa4655bd5772f613cec2f343a9`, and generator SHA-256 `848984cac427547955a04b2e5c379762149ad94a37711a6483008fd55f2c161b`. C9 rev 2.6 remains an unratified/unfrozen specification; the workflow's `ACCEPTED` label records the generation run's acceptance checks, not owner ratification of C9 or adoption by v0.21.

## 2. H80 raw rows and canonical identities

The inspected `heldout_bank.json` contains:

- 80 raw records;
- 80 unique `input_id` values;
- the declared H1–H8 stratum counts: 12, 12, 8, 8, 10, 10, 8, 12;
- 78 unique canonical keys;
- distinct coin denominations in every record; and
- stored `canonical_id` values that recompute correctly from `(amount, tuple(sorted(coins)))` for all 80 records.

There are exactly two within-bank duplicate canonical-identity groups:

| H6 pair | Input IDs | Canonical identity count | Ordering rule |
|---|---|---:|---|
| H6-P01 | H057, H058 | 1 | original, permutation |
| H6-P02 | H059, H060 | 1 | original, permutation |

Each pair has the same amount and sorted denomination tuple, but a different as-given coin order. The two records in each pair share their `canonical_id` and are recorded as the declared original/permutation orderings in `rule_params`.

No other duplicate canonical identity occurs in H80. Therefore the H80 cardinality is exactly:

`80 raw records - 2 duplicate reorder rows = 78 unique canonical identities`.

This is a verified property of the actual artifact, not merely an inference from BANK_DESIGN's planned H6 layout.

## 3. Oracle-output reconciliation

The inspected `heldout_oracle_outputs.json` contains exactly 78 objects and 78 unique canonical IDs.

The identity-key comparison establishes:

- every distinct H80 canonical key has exactly one oracle object;
- every raw H80 row resolves to exactly one oracle object by its canonical ID;
- each matched oracle object's amount and sorted coin list agree with the bank row's canonical identity;
- there are no H80 canonical keys missing from the oracle attachment;
- there are no extra oracle keys; and
- both records of each H6 pair resolve to the same oracle object.

Thus:

`|H80 raw rows| = 80`  
`|H80 canonical keys| = 78`  
`|H80 oracle objects| = 78`  
`H80 canonical-key set = H80 oracle-key set`.

**H80-to-oracle reconciliation: PASS.** The 80-to-78 difference is fully explained by the two H6 reorder pairs under the artifact's one-output-per-canonical-instance structure. There are no missing accepted-row oracle outputs.

## 4. Rejection-sidecar reconciliation

The inspected `heldout_bank.rejections.jsonl` contains **26 rejected candidate-attempt events**, not two events.

All 26 events have:
- `bank = heldout`;
- `stratum = H2`; and
- `reason = H2_ORACLE_BELOW_TWO`.

They concern seven planned H2 candidate slots:

| Candidate ID | Rejected attempts | Final accepted H2 record present? |
|---|---:|---|
| H018 | 6 | Yes |
| H019 | 3 | Yes |
| H020 | 1 | Yes |
| H021 | 1 | Yes |
| H022 | 10 | Yes |
| H023 | 2 | Yes |
| H024 | 3 | Yes |
| **Total** | **26** | **All seven present** |

These are retry-history events. Each affected candidate slot ultimately appears in the accepted 80-row bank. They are not two omitted H80 inputs, do not subtract accepted records, and do not cause the oracle attachment to contain fewer objects than unique canonical identities.

The run manifest's aggregate `rejection_event_count` is 63 across the generation run. Only the H80 sidecar was in this D0.3 inspection scope; the diagnostic sidecar was not parsed, so this report does not attempt to reconcile the remaining aggregate events.

**H80 rejection-sidecar interpretation: PASS.** The sidecar is a separate generation-history object and does not explain the 80-to-78 oracle cardinality. The canonical-identity collapse does.

## 5. Publication report

The inspected `canonical_disjointness_report.json` reports:
- schema `lc518-canonical-disjointness-v1`;
- status `PASS`;
- 64 diagnostic raw records and 60 unique diagnostic canonical identities;
- 80 held-out raw records and 78 unique held-out canonical identities; and
- zero cross-bank canonical collisions in all D1–D8 and H1–H8 strata.

Its SHA-256 matches the run manifest's `item8_report_sha256`. All six artifacts listed in the report match the hashes of their actual ZIP members.

The run manifest reports `item8_status = PASS`, `overall_acceptance_status = ACCEPTED`, process exit status 0, and 57 test-suite passes. These are evidence about this generation run's recorded checks only. They do not upgrade the C9 review text to owner-ratified authority or adopt it for v0.21.

## 6. H80-to-B1 comparison: source gap remains

The accepted B1 v1.7 analysis plan defines a fixed publicly exposed 78-record development set and uses canonical-record rows (r=1,ldots,78). Its acceptance record explicitly states that this set is development data, not sealed confirmatory data. However:

1. Neither B1 v1.7 nor its acceptance record supplies the 78 canonical identities or cites the H80 bank/oracle artifacts by path and hash.
2. The accepted B1 publication commit `ac06c6676982eed795db9cb04c6d91803b591ac7` has a 348-entry repository tree. The inspected tree contains the analysis and acceptance documents but no B1 78-row bank manifest, canonical-record file, or oracle-output attachment that independently enumerates the target identities.
3. The B1 record index (r=1,ldots,78) is a symbolic row index, not a recoverable list of input identities.
4. The H80 oracle file is a concrete 78-key set, but using it as the B1 source solely because its cardinality matches would assume the very lineage relationship this audit is meant to test.

Accordingly, the actual H80-to-B1 set comparison cannot be completed from the identified sources. This is not a finding of equality, partial overlap, or disjointness.

**Verified:** H80 has 78 unique canonical keys and 78 matching oracle keys.  
**Not established:** whether B1's 78 development rows are those same 78 keys.

To close this part, the owner must identify the independently attributable B1 78-row source manifest or artifact (with its immutable hash and provenance). If the intended B1 source is `heldout_oracle_outputs.json` from artifact 13210063805, that linkage must be supported by an authoritative B1 source record or contemporaneous provenance, not inferred from the matching count after the fact.

## 7. Confirmatory route, consent and artifact preservation

The owner selected the confirmatory route with consent. The accepted B1 v1.7 acceptance record still states that the joint-consent provenance gap remains open. No new consent artifact was identified by this D0.3 work. The route is selected, but confirmatory evaluation remains blocked until the historical consent record, independent custodian, trigger-(i) ratification, and separate B1 amendment are evidenced and reviewed.

Artifact `13210063805` remains preserved. It was downloaded for the authorized audit and not deleted, modified, replaced, or intentionally expired. Its archive digest and metadata are recorded in the owner-GO inventory.

## 8. Final D0.3 disposition

| Question | Result |
|---|---|
| Does H80 contain 80 valid raw rows? | **PASS** |
| Does H80 contain 78 unique canonical identities? | **PASS** |
| Are the only duplicates the two H6 reorder pairs? | **PASS** |
| Do 78 oracle objects match the 78 H80 canonical keys exactly? | **PASS** |
| Do rejected H80 attempts explain the 80-to-78 oracle count? | **NO**; 26 H2 retries, all later accepted, explain no missing outputs |
| Is H80 internally consistent under its published canonical-identity/oracle structure? | **PASS** |
| Are H80 and B1 v1.7's 78 records proven identical? | **OPEN**; the independently attributable B1 identity source is missing |
| Is B1 consent provenance closed? | **NO**; remains an explicit confirmatory gate |
| Is artifact 13210063805 preserved? | **YES** |

The strongest supported conclusion is: **the historical 80-row H80 artifact is an internally consistent 78-canonical-input bank with 78 corresponding oracle objects; its two-row reduction is due to the two H6 permutation pairs, not the H80 rejection sidecar. The identity relationship to B1's 78-row development target remains unproven because the B1 identity source is not established.**

No solver outcome, diagnostic result, protected E3 record, predictive fit, or confirmatory result was accessed or evaluated.
