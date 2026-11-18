# Claim ledger — verification pass, revision 2

**Date:** 2026-11-18
**Supersedes:** `claim-ledger-verified-2026-11-18.md` (revision 1), which is retained unmodified.
**Change in this revision:** the contradicted original claim and the verified correction are now separate
records (C-09 vs C-18), the oracle-value semantics and digest consistency have their own IDs (C-19, C-20),
and the authorization text is separated from what the run actually produced (C-05 vs C-21).

**Status vocabulary:** Verified (primary artifact inspected in this pass) / Supported (independent record
corroborates, primary not inspected) / Reported (unchanged) / Contradicted (primary artifact disagrees).

Primary artifact for all new rows: `lc518-bank-run-41591572358-1.zip`, 75,523 bytes,
SHA-256 `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`, 15 members.

---

## Part A — original claims

| ID | Proposition | Was | Now | Basis |
|---|---|---|---|---|
| C-01 | Artifact `lc518-bank-run-41591572358-1`, ID 13210063805, SHA-256 `6e6d60c1…b2bb2` | Reported | **Part Verified** | The **bytes** are verified (see C-22). The **artifact ID** is unverified GitHub metadata; it was not queried. Split, not silently upgraded. |
| C-02 | The held-out bank was publicly readable in `foued2/failure-concentration-study` | Supported | **Verified** | GitHub API: `private=false`, `visibility=public`. Branch `foued2-patch-1` at `e22da84` serves `lc518-publish-set-12-files-run-41591572358.zip` (73,831 bytes, blob `301e8e16`). The bank is readable **inside that publish set**; there is no standalone bank ZIP on the branch. |
| C-03 | The held-out bank cannot serve as a blinded confirmatory set | Supported | Supported | Follows from C-02. No change. |
| C-04 | Zero LC518 solver evaluations completed | Reported | Reported (cautious) | `lc518-150/` on `master` holds only `review-v1.2/`; no outcome artifacts. Absence in examined locations cannot establish that no execution occurred elsewhere. |
| C-05 | GO `LC518-GO-2026-11-03-01` authorizes bank and oracle generation only | Reported | **Verified as to bank generation; wording corrected** | GO text, `wt-recovery/lc518-150/provenance/OWNER_GO_RECORD.md`: "LC518-150 C9 bank-generation protocol only"; excludes solver execution, predictive fitting, private-annex access, power analysis, merge to `master`. It does not name oracle generation. "Bank and oracle generation" is inference; see C-21 for what the run produced. |
| C-06 | November 6 mutation allocation not established | Supported | Supported | Not re-inspected. |
| C-07 | Old allocation closed NOT CREATED on 2026-11-10 | Reported | Reported | Not re-inspected. |
| C-08 | A2 BLOCKED / NOT ASSESSABLE, not a design failure | Reported | Reported | Not re-inspected. |
| C-09 | 80 held-out inputs but only 78 oracle outputs, an unresolved output gap | Unverified | **Contradicted** | Direct recount: there is no gap. The record is superseded by C-18, which is retained as a separate claim rather than folded into this one. |
| C-10 | Zero evaluations means the hypothesis is unresolved | Inferred | Inferred | Unchanged. |
| C-11 | v0.2 had C = 5/k for all pairs; concentration not identifiable | Reported | Reported | Not re-inspected. |
| C-12 | Population design v0.5 published, not frozen | Reported | Reported | Not re-inspected. |
| C-13 | B1 v1.7 accepted as symbolic; execution not authorized | Reported | Reported | Not re-inspected. |
| C-14 | Old Doctor closed (76/14 via brute force); New Doctor terminated 2026-10-08; Pilot 0 never run | Reported | **Part Verified** | `new-doctor/README.md` ("Old Doctor is closed", "No 76/14 reproduction"); `PILOT_0_RESULTS.md` ("STATUS: NOT RUN"); `DECISIONS.md` final entries dated 2026-10-08. The 76/14 **explanation** remains unverified. |
| C-15 | H3 V10 run 40833639560 completed | Reported | Reported | Not inspected. |
| C-16 | Stage A received CONDITIONAL PASS | Reported | Reported | Not inspected. |
| C-17 | `environment_prevent_self_review = false` | Reported | Reported | Not inspected. |

## Part B — new claims established by this pass

| ID | Proposition | Status | Evidence |
|---|---|---|---|
| C-18 | The held-out bank has 80 rows, 80 unique `input_id`, and 78 distinct `canonical_id`. The two duplicate canonical IDs are H057/H058 and H059/H060, both H6, same amount, same coin multiset in different order. The 78 held-out oracle rows cover exactly those 78 canonical IDs: 0 missing, 0 extra, 0 duplicate. | **Verified** | Recomputed from `bank/heldout_bank.json` and `bank/heldout_oracle_outputs.json`. 26 rejections, all `H2_ORACLE_BELOW_TWO`, candidates H018–H024, are generation rejections, not missing outputs. |
| C-19 | Held-out oracle answers are integers, not binary labels: 78 integers spanning 0–284134, of which 36 are 0, 8 are 1, and 34 take other values. | **Verified** | `bank/heldout_oracle_outputs.json`. Consequence: `Y` is a comparison between solver output and this integer. Describing the file as 78 pass/fail labels would misrepresent it. |
| C-20 | Every held-out bank row declares `oracle_output_file_sha256 = eaae81040424881cc9939e7415a8a5a0328fa870bd2a790d0b4409babd03e244`, equal to the SHA-256 of the oracle member. | **Verified** | 80/80 rows declare it; the member hashes to exactly that value. Establishes declaration-to-file consistency only, not the oracle's correctness or independent provenance. |
| C-21 | The C9 run produced bank artifacts including both oracle output files, with `overall_acceptance_status = ACCEPTED`, exit 0, `protocol_sha256 9c54ffc2…`, generator `848984ca…` identical before and after the run, launcher `014e45c2…`, `c9_commit 511bc20…`, 63 rejection events, 57 tests passed. | **Verified** | `logs/run_manifest.json` and the member set of the archive. This is what the workflow **generated**; it is not an expansion of what C-05 **authorized**. |
| C-22 | Three local copies of the bank artifact archive are byte-identical and match the registered artifact digest. | **Verified** | All three hash to `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` at 75,523 bytes. |

## Part C — corrections to earlier records

1. **C-09** was previously `Unverified`; it is now `Contradicted`, and its corrected content lives in C-18. Neither record replaces the other.
2. **C-05** previously read "bank and oracle generation". The GO names bank generation only. C-21 records the outputs; the two must not be merged.
3. **C-01** previously implied the artifact record as a whole; only the bytes are verified here.
4. The 2026-11-18 statement that three untracked files collide with incoming `master` paths was wrong; only `VERIFICATION_LOG.md` does. Recorded in `preservation-record-2026-11-18.md`.

## Part D — still unverified

C-04 (absence only), C-06, C-07, C-08, C-11, C-12, C-13, C-15, C-16, C-17, the 76/14 explanation within C-14, and the GitHub artifact ID within C-01.

Separate open item, unaffected by this ledger: conformance of the manifest validator to the v0.21 specification of record.
