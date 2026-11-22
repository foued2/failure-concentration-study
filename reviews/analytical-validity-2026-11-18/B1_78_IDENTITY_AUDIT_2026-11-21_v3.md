# B1 78 canonical identity audit — v3

**Date:** 2026-11-21  
**Status:** IDENTITY RECONSTRUCTION VERIFIED; H6 PRIMARY OUTCOME RULE NOT DECIDED  
**Scope:** Read-only reconstruction of the 78 canonical held-out development-bank identities. No solver execution, outcome labelling, fitting, or repository changes.

## 1. Decision summary

The 78 canonical mathematical inputs are reconstructed directly from the preserved Actions archive, not inferred from matching counts. The original archive SHA-256 is `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` and its size is 75,523 bytes. Its held-out bank has 80 raw presentations and 78 unique canonical IDs. The corresponding 78 oracle records have exactly the same canonical key set.

**B1 attribution:** RECOVERED THROUGH A DOCUMENTARY CHAIN. B1 v1.7 does not enumerate the keys. It defines the outcome population as the fixed 78-record public development bank; the B1 reconciliation record pins that bank to the Actions artifact; this audit independently reconstructs the keys from the preserved artifact. This is a reconciled chain, not a claim that the B1 specification itself contains the ID list.

**H6 primary outcome rule:** NOT DECIDED. The generator's `original` / `permutation` roles describe construction history. They do not by themselves determine which raw order should represent the primary B1 correctness observation. This audit therefore makes no primary-row selection.

## 2. Byte-level source verification

| Object | Size (bytes) | SHA-256 |
|---|---:|---|
| Preserved archive `lc518-bank-run-41591572358-1-preserved-2026-11-21.zip` | 75,523 | `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` |
| `bank/heldout_bank.json` | 40,218 | `b273c053e874f212f060ff23791f9be445a48203cbbde0ca1b285192093d26d6` |
| `bank/heldout_oracle_outputs.json` | 15,262 | `eaae81040424881cc9939e7415a8a5a0328fa870bd2a790d0b4409babd03e244` |
| `lc518_generator.py` | 56,845 | `848984cac427547955a04b2e5c379762149ad94a37711a6483008fd55f2c161b` |

The archive digest matches the original Actions artifact digest for run `41591572358`, artifact ID `13210063805`. Every raw bank record’s `oracle_output_file_sha256` also matches the SHA-256 of the held-out oracle member (80/80).

## 3. Identity results

| Check | Verified result |
|---|---:|
| Raw held-out bank records | 80 |
| Distinct raw `input_id` values | 80 |
| Recomputed raw canonical IDs | 80/80 |
| Recomputed raw `record_sha256` | 80/80 |
| Raw records point to the exact held-out oracle-file SHA-256 | 80/80 |
| Unique canonical IDs | **78** |
| Oracle rows | 78 |
| Oracle key-set missing / extra / duplicate | **0 / 0 / 0** |
| Independently recomputed oracle counts | 78/78 |
| Oracle first-occurrence ordering | Matches canonical first-occurrence order |

Canonical grouping is 76 singleton identities and two groups of two raw presentations. The oracle values are integer combination counts, not binary correctness labels: 36 are zero, 8 are one, and 34 are other positive integers.

## 4. Canonical-ID payload convention (v2 defect corrected)

The generator's `canonical_id` function constructs exactly this object:

```json
{"amount": amount, "coins": sorted(coins)}
```

It serializes with sorted keys, compact separators `(',', ':')`, UTF-8, `ensure_ascii=False`, then hashes those bytes with SHA-256 and prefixes `C-`.

In v2, the displayed `canonical_payload` object used the key `coins_sorted`, while the canonical ID was calculated using `coins`. The hash values were correct, but the displayed payload was not itself the hash input. **V3 fixes that defect:** `canonical_payload` now has precisely the keys `amount` and `coins`. The convenience field `coins_sorted` remains separate. Every JSON and CSV row was read back and its displayed canonical payload was re-hashed successfully.

The sorted ID list remains 5,226 bytes under LF line endings and hashes to:

`01bb0e4c8edb2c4a0678d1b6c65c4295bdaf59c9baf2436d793f25c740c3cccd`

## 5. Position fields and reporting index

All source positions are explicitly 1-based:

- `bank_first_canonical_ordinal_1based`: position after collapsing repeated canonical identities in first-seen bank order.
- `bank_first_raw_array_position_1based`: actual raw JSON array position of the first presentation.
- `raw_bank_array_positions_1based`: actual positions of all raw presentations in that identity group.
- `oracle_array_position_1based`: position in the oracle output array.

`B1_identity_reporting_index` is a new, deterministic 1–78 index assigned by lexicographic sort of `canonical_id`. It is **not** a historical B1 `r` ordering. Outcome rows must be joined by `canonical_id`.

## 6. H6 pairs: what is verified and what remains undecided

The generator creates paired records with `ordering="original"` followed by `ordering="permutation"`. Its validator checks adjacency, matching pair ID, amount, sorted coin set and canonical ID, and requires the raw coin orders to differ.

| Pair | Original raw ID | Permutation raw ID | Canonical identity |
|---|---|---|---|
| H6-P01 | H057 | H058 | `C-22b6be364c68bfb475d20ac4e6111547c34188805fbee30ef94405471526fc9c` |
| H6-P02 | H059 | H060 | `C-188a2a3c0b6404b5f4b11943eb68e1a6355f45a8d35cbb987f4cca6f3af61a92` |

This is evidence about the bank's construction and serialization, **not a scientific decision about primary outcome presentation**. The v3 manifest contains both raw records, their roles and positions, and no selected primary input.

Possible future definitions differ scientifically: original-order primary; sorted-order primary; both-orders-must-pass robustness outcome; or two raw-order outcome rows with a revised outcome unit. None is selected here. In particular, do not infer an outcome aggregation rule from one oracle answer per canonical identity.

## 7. B1 documentary chain

1. B1/M1 Rev 1.1 §1.4 defines `n_h = 78` unique canonical records in the fixed, publicly exposed held-out bank.
2. Rev 1.4 §1 carries that bank definition forward and defines the primary outcome as per-record correctness `Y_{v,r}` on canonical development record `r ∈ {1,…,78}`.
3. B1 v1.7 §1 and its acceptance record retain the fixed 78-record, public-development-bank scope, not a sealed bank or new-record generalisation.
4. `B1_DECISION_RECONCILIATION_2026-11-11.md` §6.1 pins the original archive digest to Actions artifact `13210063805`, run `41591572358`; §§6.2–6.5 document publication lineage and exposure.
5. The original preserved archive was re-hashed in this audit and its bank/oracle member contents were read directly.

The exact IDs are supplied by the source artifact plus this reconstruction; neither B1 v1.7 nor the B1 decision record directly enumerates them. This is why the appropriate label is **documentary attribution reconciled**, not “B1 v1.7 directly lists the bank keys.”

## 8. Taxonomy and scope warning

The `H1`–`H8` labels in this manifest belong to the historical H80 held-out bank. They are not the v0.21 diagnostic `D1`–`D8` strata. Do not conflate these taxonomies or use H-bank strata to calculate diagnostic `C_D`.

## 9. What is not established

- No solver-output records or `Y_{v,r}` matrix were found or created by this identity audit.
- No H6 primary presentation or outcome aggregation rule has been selected.
- The manifest does not resolve whether a future execution uses the original raw order, sorted order, or a two-order robustness rule.
- The public development bank is not a sealed confirmatory bank.
- This identity work does not authorize bank reuse, execution, outcome construction, fitting, or any change to frozen B1 v1.7.

## 10. Output checksums

| File | SHA-256 |
|---|---|
| `B1_78_CANONICAL_ID_MANIFEST_2026-11-21_v3.json` | `f3289fec5749b76ec4abc743e23f61b889d8831fc055590b034656f4d6bd1989` |
| `B1_78_CANONICAL_ID_MANIFEST_2026-11-21_v3.csv` | `af9c0d5adc2977cc8f3c0dc5053ab80c808bdb38bccf388416362fa6ac2bf95f` |
| `B1_78_IDENTITY_AUDIT_2026-11-21_v3.md` | (see delivery checksum table; self-hash intentionally external) |
