# B1 v1.7 - recovery of the 78-row canonical identity source

**Record ID:** B1-78-IDENTITY-RECOVERY-2026-11-21
**Date:** 2026-11-21
**Status at issue (2026-11-21):** SOURCE RECOVERED BY DOCUMENTARY CHAIN; B1 ADJUDICATION PENDING AT THAT DATE.
**Current identity status (2026-11-22):** SOURCE-RECOVERED / OWNER-ACCEPTED. The earlier pending disposition is historical and superseded by the owner's decision in `B1_IDENTITY_ACCEPTANCE_ADDENDUM_2026-11-22.md`.
**Scope:** Read-only identity inspection of the pinned LC518 held-out bank artifact. No solver,
no fitting, no sampling, no outcome model, no protected E3 record. The bank remains development
data, publicly exposed, never sealed.

---

## 1. The owner's question, answered directly

**Question.** Does any file or data identify the actual 78 development-bank rows named by accepted
B1 v1.7?

**Answer.** B1 v1.7 itself does not enumerate them. The rows are nevertheless recoverable from the
pinned held-out bank artifact:

- `bank/heldout_bank.json` contains **80 raw records** (`H001`-`H080`) and **78 unique canonical
  identities**.
- `bank/heldout_oracle_outputs.json` contains **78 oracle objects**, and its canonical-key set is
  exactly equal to the 78-key set of the bank.
- The two-row difference is fully explained by the two declared H6 reorder pairs:
  `H057`/`H058` (`H6-P01`, original/permutation) and `H059`/`H060` (`H6-P02`,
  original/permutation). These are four raw records, two canonical identities.
- The 78 B1 rows are the **78 unique canonical records**, not the 80 raw rows. The raw rows are the
  exposure envelope; the canonical records are the analysis population.

The identification is **not** an inference from the coincidence `78 = 78`. It follows from B1's own
definition of its outcome population, quoted in section 3, plus the contemporaneous record that
identifies the publicly exposed held-out bank. The cardinality match is a consequence, not the
evidence.

**What remains open.** B1 v1.7 does not cite this artifact by repository path or immutable hash.
The plan was accepted as a symbolic document, and its v1.7 change table records that the
138/144/6 erratum counts were deliberately removed from the plan as out of scope. The chain below
therefore runs through the inherited Rev 1.1 §1.4 definition and the separate B1 decision record,
not through a B1-issued manifest. Whether that chain is sufficient to close the identity gate is
an owner/GPT adjudication, not an audit inference. This record does not amend B1 v1.7 and does not
declare the gate closed.

---

## 2. The artifact and its provenance

### 2.1 Original generation

The GitHub artifact record, as retrieved during the 2026-11-11 chain-of-custody verification,
gives:

| Field | Value |
|---|---|
| Repository | `foued2/failure-concentration-study` |
| Workflow run ID | `41591572358` |
| Run head branch | `gpt/lc518-github-recovery-2026-11-02` |
| Run head commit | `a4ec1148698fe6612c5e873f1193069538a206e3` |
| Artifact ID | `13210063805` |
| Artifact name | `lc518-bank-run-41591572358-1` |
| Artifact size | 75,523 bytes |
| Artifact SHA-256 | `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` |
| Created | `2026-11-03T06:43:57Z` |
| Expiry reported by GitHub | `2027-02-01T06:42:22Z` |

The generation run's `logs/run_manifest.json` records:

| Field | Value |
|---|---|
| C9 design commit | `511bc2099ecff74b4f850b169ceef7f853c334a0` |
| C9 source SHA-256 | `f291ae879ef6e046c6715bb0e6a84cd5a3f5e69f07ace09e213db9b84d8b87fe` |
| Generator SHA-256 | `848984cac427547955a04b2e5c379762149ad94a37711a6483008fd55f2c161b` |
| Seeds | diagnostic `11052026`; held-out `20261101` |
| Start / end (UTC) | `2026-11-03T06:43:55Z` / `2026-11-03T06:43:56Z` |
| `item8_status` | `PASS` |
| `overall_acceptance_status` | `ACCEPTED` |
| Process exit status | `0` |

These are the run's own acceptance labels. They do not make C9 rev 2.6 owner-ratified, and they do
not convert the bank into a sealed confirmatory target.

### 2.2 Repository copy

The same bytes are stored in Git as a convenience copy:

| Field | Value |
|---|---|
| Branch | `origin/foued2-patch-3` |
| Commit | `2d5f9c38f8b52bdf0204287a1a1cb74089a4a267` ("Add files via upload", 2026-11-18) |
| Path | `lc518-bank-run-41591572358-1 (2).zip` |
| Blob | `636d3b8a01f6256746c79611a51af3f7fe233e1c` |
| Size | 75,523 bytes |
| SHA-256 | `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` |

The Git upload postdates B1 v1.7. That does **not** make it a new bank. Its hash is the hash of the
2026-11-03 artifact, and the erratum's package-identity table pins that same hash to GitHub artifact
`13210063805`. The upload is a later copy of the pre-B1 artifact, not a post-B1 reconstruction.

### 2.3 Relevant members

| Member | Bytes | SHA-256 |
|---|---:|---|
| `bank/heldout_bank.json` | 40,218 | `b273c053e874f212f060ff23791f9be445a48203cbbde0ca1b285192093d26d6` |
| `bank/heldout_oracle_outputs.json` | 15,262 | `eaae81040424881cc9939e7415a8a5a0328fa870bd2a790d0b4409babd03e244` |
| `bank/canonical_disjointness_report.json` | 1,085 | `839014e078580016c644667d41b9d83ab4bb8b3e888828c9cac67e952db5520c` |
| `logs/run_manifest.json` | 3,178 | `698f4e99731f707a0f2474fdb1d46b972cbc7ebbff76d9f247885b139d14201f` |
| `bank/diagnostic_bank.json` | 35,665 | `13f2e435552b2aa1e0ba88104300b0a1dbc4bb5f8c5061d78a01fe90fc52bc92` |
| `bank/diagnostic_oracle_outputs.json` | 16,451 | `93eb393c0f56a7ed13a8ef4f1a29286c3aadcc6e5dc76fa59378bb0c1358214e` |

The full 15-member hash inventory is recorded in the D0.3 owner-GO record on
`gpt/gate0-scientific-foundation-blueprint-2026-11-20`
(`docs/LC518_D0_3_OWNER_GO_AND_HASH_INVENTORY_2026-11-21.md`).

---

## 3. The documentary chain

### 3.1 B1's own definition of its outcome population

Rev 1.1 §1.4 (the definition Rev 1.4 inherits):

> "Primary outcome unit (declared): version-level - \(h_v\) = number of correct answers among the
> \(n_h\) held-out development records (\(n_h\) = **78 unique canonical records of the fixed,
> publicly exposed held-out bank**). The held-out bank is development data; never sealed."

Rev 1.4 §1 retains that text: "§1.1-§1.4 of Rev 1.1 stand as written ... held-out bank = the fixed,
publicly exposed 78-record development set, **never sealed**." Rev 1.4 then fixes the per-record
unit: \(Y_{v,r}\in\{0,1\}\) for canonical development record \(r\in\{1,\dots,78\}\).

B1 v1.7 §1 item 1 operationalizes that definition: the primary likelihood unit is the
version × canonical-record row \(Y_{v,r}\) for \(r\in\{1,\dots,78\}\), on the same fixed 78-record
bank, described as development data, publicly exposed, never sealed.

### 3.2 The bank is the artifact

The B1 decision reconciliation (2026-11-11) §6.1 records the chain of custody directly:

> `~/Downloads/lc518-bank-run-41591572358-1.zip` (75,523 B), SHA-256
> `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`, equals GitHub's recorded
> digest for artifact `13210063805` (run `41591572358`, non-expired, expiry 2027-02-01).

Its §6.5 records the public exposure:

> "The 2026-11-03 exposure-verification note ... establishes from GitHub metadata that the
> repository is public and the non-expired Actions artifact containing `bank/heldout_bank.json`
> and its oracle answers was downloadable by anyone with repository read access."

The erratum (2026-11-11) §3 pins the package:

> embedded `zips/lc518-bank-run-41591572358-1.zip` — SHA-256
> `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`
> (== GitHub artifact digest `13210063805`).

The D0.3 reconciliation (2026-11-21) verifies the internal structure: 80 raw H80 rows, 78 unique
canonical identities, exactly two H6 duplicate groups, 78 oracle objects with an equal key set.

### 3.3 The chain in one line

> B1's 78 = the 78 unique canonical records of the fixed, publicly exposed held-out bank
> (Rev 1.1 §1.4, inherited by Rev 1.4 §1 and B1 v1.7 §1)
> = the 78 unique canonical identities of artifact `13210063805` / run `41591572358`
> (B1 decision reconciliation §6.5; erratum §3; D0.3 reconciliation).
> Therefore the 78 canonical keys are those in `bank/heldout_oracle_outputs.json`.

This is a definitional link. It is not the argument "H80 has 78 canonical keys, B1 has 78 rows,
therefore they are the same." The 80 raw rows are not the B1 population; the canonical records are.

### 3.4 The one link B1 v1.7 does not state

B1 v1.7's change table, item 7, says the 138/144/6 erratum counts and their dependency on the
local-only erratum were **removed** from §1; v1.7 cites only Rev 1.4's 78-record development-bank
definition, and the erratum was ruled out of scope. So the chain above is not written in v1.7
itself. It is inherited through Rev 1.1 §1.4 and corroborated by the separate B1 decision record.
A reviewer who requires a B1-issued path-and-hash citation will not find one in v1.7; that is the
remaining documentary gap, and it is why this record stops at "source recovered; adjudication
pending."

---

## 4. The 78 canonical records: verified structure

### 4.1 Counts

| Quantity | Value |
|---|---:|
| Raw held-out records | 80 |
| Unique `input_id` values | 80 |
| Unique canonical identities | 78 |
| Oracle objects | 78 |
| Oracle key set = bank canonical key set | yes |
| Duplicate canonical groups | 2, both in H6, both size 2 |
| Records with repeated denominations | 0 |

### 4.2 The two H6 pairs

| Pair | Input IDs | Stratum | Rule parameters | Canonical count |
|---|---|---|---|---:|
| `H6-P01` | `H057`, `H058` | H6 | `ordering: original`, `ordering: permutation` | 1 |
| `H6-P02` | `H059`, `H060` | H6 | `ordering: original`, `ordering: permutation` | 1 |

Each pair shares one amount and one sorted denomination tuple, and differs only in the as-given
coin order. Each pair resolves to one oracle object. No other canonical collision occurs in the
bank.

### 4.3 Canonical stratum counts

These are the **held-out outcome population** counts, not the diagnostic exposure basis:

| Stratum | H1 | H2 | H3 | H4 | H5 | H6 | H7 | H8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Raw records | 12 | 12 | 8 | 8 | 10 | 10 | 8 | 12 |
| Unique canonical records | 12 | 12 | 8 | 8 | 10 | 8 | 8 | 12 |

Do not confuse this with the **diagnostic** exposure basis used by `C_D`: 64 diagnostic records,
60 unique diagnostic canonicals, \(R=(8,8,8,8,8,4,8,8)\). The held-out 78 are the outcome rows;
the diagnostic 60 are the exposure rows. They are different objects.

### 4.4 Set hashes

Computed from the artifact by the recovery procedure in section 5:

| Object | SHA-256 |
|---|---|
| Sorted 78 canonical IDs, newline-terminated | `01bb0e4c8edb2c4a0678d1b6c65c4295bdaf59c9baf2436d793f25c740c3cccd` |
| Sorted canonical payloads `amount|sorted(coins)`, newline-terminated | `8b67d1f0193d85838a98486ae4fbf7ef17d948b1cca4abdfc4c0180ae61e48fa` |

The hashes pin the set. They are not a substitute for the artifact: the authoritative list is the
pinned JSON, not a newly manufactured manifest in this bundle.

---

## 5. Recovery procedure

From any clone that contains the Git copy:

```powershell
$blob = '636d3b8a01f6256746c79611a51af3f7fe233e1c'
$zip  = "$env:TEMP\opencode\lc518-bank-run-41591572358-1.zip"
git cat-file blob $blob > $zip
(Get-FileHash $zip -Algorithm SHA256).Hash
# expected: 6E6D60C1CB703ED80C1D4FC8191AD764A81B3C06517CAEFF9DB15BF52DB2BBE2
Expand-Archive $zip -DestinationPath "$env:TEMP\opencode\lc518-bank" -Force
```

Then:

```python
import json, hashlib, collections

base = r"<expanded>/bank"
bank = json.load(open(base + r"\heldout_bank.json", encoding="utf-8"))
oracle = json.load(open(base + r"\heldout_oracle_outputs.json", encoding="utf-8"))

keys = sorted({r["canonical_id"] for r in bank})
assert len(bank) == 80
assert len(keys) == 78
assert {r["canonical_id"] for r in oracle} == set(keys)

print(hashlib.sha256(("\n".join(keys) + "\n").encode()).hexdigest())
# expected: 01bb0e4c8edb2c4a0678d1b6c65c4295bdaf59c9baf2436d793f25c740c3cccd

payloads = sorted({(r["amount"], tuple(sorted(r["coins"]))) for r in bank})
assert len(payloads) == 78
print(hashlib.sha256(
    ("\n".join(f"{a}|{c}" for a, c in payloads) + "\n").encode()
).hexdigest())
# expected: 8b67d1f0193d85838a98486ae4fbf7ef17d948b1cca4abdfc4c0180ae61e48fa
```

The two assertions that do the work are `len(keys) == 78` and
`{oracle canonical IDs} == set(keys)`. The first is the 80-to-78 collapse; the second is the
oracle attachment. The two H6 pairs are the entire explanation of the collapse.

---

## 6. What this settles and what it does not

### Settled

1. **The 78-row identity set exists and is recoverable.** It is the 78 canonical IDs in
   `bank/heldout_oracle_outputs.json`, equivalently the 78 unique canonical IDs in
   `bank/heldout_bank.json`.
2. **The set is linked to B1 by definition, not merely by count.** Rev 1.1 §1.4 defines B1's
   outcome population as the 78 unique canonical records of the fixed, publicly exposed held-out
   bank; the B1 decision record identifies that bank as artifact `13210063805`; the erratum pins
   the hash; the artifact supplies the 78 keys.
3. **The H80-to-B1 comparison is no longer blocked by missing data.** A complete comparison can
   now be run: `|K_B1| = 78`, `|K_H80| = 78`, `|K_B1 ∩ K_H80| = 78` under the chain above,
   with the two H6 pairs carrying the raw-record multiplicity. The comparison is a documentary
   identity check, not an outcome analysis.
4. **The 80 raw rows are not the B1 set.** Any statement that "B1 has 80 records" or that "the
   held-out bank has 80 outcome rows" is wrong for B1's canonical-record unit. The 80 are the
   exposure envelope; the 78 are the outcome population.

### Not settled by this record

1. **B1's own citation.** B1 v1.7 does not name the artifact path or hash. The link is inherited
   and corroborated, not stated in the accepted plan. The owner/GPT must accept the chain or
   supply a contemporaneous B1 manifest.
2. **The historical enumeration order.** B1 does not fix an order for \(r=1,\dots,78\). The
   likelihood's record effect \(\omega_r\) is a free record effect, so a permutation of the record
   labels is a relabeling, not new identity. If a report needs an enumeration, it must declare a
   convention; it must not present a convention as B1's historical order.
3. **Confirmatory status.** The bank is development data, publicly exposed, never sealed. This
   recovery does not create a sealed target, cure the joint-consent provenance gap, appoint a
   custodian, or satisfy the separate B1 amendment required for a new protected set.
4. **Outcome coding for the two held-out pairs.** This record identifies the 78 canonical records; it
   does not fix how two raw execution statuses collapse to one `Y`. B1 v1.7 specifies no
   raw-pair-to-canonical aggregation rule; the artifact supplies one oracle answer per `canonical_id`,
   but identity is not outcome coding. The review record §27.3–§27.4 already treats the aggregation
   and unresolved-status handling as open Gate 1 measurement gaps.
5. **Scientific standing.** Nothing here demonstrates the concentration hypothesis, fits a model,
   evaluates a solver, or licenses a novelty claim.

### Disposition

**Identity source: RECOVERED.**
**B1 identity gate at issue on 2026-11-21: SOURCE-RECOVERED / ADJUDICATION PENDING.** This records the status before owner adjudication. The current identity status is **SOURCE-RECOVERED / OWNER-ACCEPTED**, as recorded in `B1_IDENTITY_ACCEPTANCE_ADDENDUM_2026-11-22.md`.
The prior status "source missing" is no longer accurate. The prior warning "do not substitute H80
by cardinality" remains correct: the substitution is rejected, and the definitional chain above is
the reason the 78 keys are B1's, not the coincidence of counts. The gate is not unilaterally closed
by this audit; closure is an owner/GPT act.

The two lawful paths remain:

- **(a) Accept the documentary chain.** The owner/GPT records the artifact path, hash, and the
  Rev 1.1 §1.4 → Rev 1.4 §1 → B1 v1.7 §1 chain in a dated B1 addendum, and the identity gate
  closes by adjudication.
- **(b) Require a B1-issued source.** If the chain is not accepted, the owner supplies a
  contemporaneous B1 78-row manifest with immutable provenance, or B1's design is reopened. No
  third path substitutes H80's keys by cardinality.

---

## 7. Scope and limits of this inspection

- Read-only. No solver construction, execution, fitting, sampling, calibration, or outcome model.
- Only the held-out bank, its oracle attachment, the canonical-disjointness report, and the run
  manifest were parsed for this record. The diagnostic bank and rejection sidecars were not used
  for any outcome analysis.
- No protected E3 record, credential store, private mutation annex, or external archive was
  accessed.
- The bank is public and never sealed. This record does not change its custody status.
- The Git copy is a later upload of the pre-B1 artifact; the hash, not the upload date, is the
  provenance link.


## 8. Subsequent owner adjudication (2026-11-22)

The disposition above records the status of this recovery audit on 2026-11-21. On 2026-11-22, the repository owner accepted the documentary chain in the dated addendum:

`B1_IDENTITY_ACCEPTANCE_ADDENDUM_2026-11-22.md`.

The current identity status is therefore **SOURCE-RECOVERED / OWNER-ACCEPTED**. This later act accepts the documentary identity and attribution of the 78 canonical records; it does not alter the source evidence or claim that B1 v1.7 itself enumerates the keys.

The historical B1 row ordering, H6 primary presentation and aggregation, unresolved-status handling, and outcome coding remain open. The addendum is not an execution GO: B1 execution remains unauthorized, Gate 0 remains open, and no predictive or novelty claim is licensed.

---

**End of record.**
