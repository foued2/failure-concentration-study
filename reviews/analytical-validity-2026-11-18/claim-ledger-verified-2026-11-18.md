# Claim ledger — verification pass

**Date:** 2026-11-18
**Scope:** the 17 claims in the LC518/Doctor ledger, checked against primary artifacts on this machine. Only rows where a primary artifact was opened are re-scored; the rest keep their earlier status and are marked `not re-verified here`.
**Status vocabulary:** Verified (primary artifact inspected in this pass) / Supported (independent record corroborates, primary not inspected) / Reported (unchanged) / Contradicted (primary artifact disagrees).

| ID | Proposition | Was | Now | Basis |
|---|---|---|---|---|
| C-01 | Artifact `lc518-bank-run-41591572358-1`, ID 13210063805, SHA-256 `6e6d60c1…b2bb2` | Reported | **Verified** (bytes); ID Reported | Three local copies each hash to `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`, 75,523 bytes, 15 members. The artifact *ID* remains GitHub-side metadata; it was not queried. |
| C-02 | The held-out bank was publicly readable in `foued2/failure-concentration-study` | Supported | **Verified** | GitHub API: `"private": false`, `"visibility": "public"`. Branch `foued2-patch-1` exists at `e22da84` and contains `lc518-publish-set-12-files-run-41591572358.zip` (73,831 bytes, blob `301e8e16`), publicly downloadable. The bank sits inside that publish set, not as a standalone bank ZIP on the branch. |
| C-03 | The held-out bank cannot serve as a blinded confirmatory set | Supported | Supported | Follows from C-02; no change. |
| C-04 | Zero LC518 solver evaluations completed | Reported | Reported | `lc518-150/` on `master` contains only `review-v1.2/`; no outcome artifacts found. Absence is consistent with the claim but does not prove no run happened elsewhere. |
| C-05 | GO `LC518-GO-2026-11-03-01` authorizes bank and oracle generation only | Reported | **Verified, with a wording correction** | GO text read at `wt-recovery/lc518-150/provenance/OWNER_GO_RECORD.md`. Scope line: "LC518-150 C9 bank-generation protocol only"; it "authorizes LC518 bank generation only" and "does not authorize solver execution, predictive fitting, private-annex access, power analysis, or merge to `master`". The GO does **not** separately name oracle generation; oracle outputs are part of the bank artifact, so "bank and oracle generation" is an interpretation, not the GO's wording. |
| C-06 | The November 6 mutation allocation is not established | Supported | Supported | Not re-inspected. |
| C-07 | Owner closed the old allocation as NOT CREATED on 2026-11-10 | Reported | Reported | Not re-inspected. |
| C-08 | A2 is BLOCKED / NOT ASSESSABLE, not a design failure | Reported | Reported | Not re-inspected. |
| C-09 | 80 held-out rows vs 78 oracle outputs is an open issue | Unverified | **Contradicted** | Recomputed from the artifact, not from any report. See §2. |
| C-10 | Zero evaluations means the hypothesis is unresolved | Inferred | Inferred | Unchanged. |
| C-11 | v0.2 had C = 5/k for all pairs, so concentration was not identifiable | Reported | Reported | Not re-inspected. |
| C-12 | Population design v0.5 published, not frozen | Reported | Reported | Not re-inspected. |
| C-13 | B1 plan v1.7 accepted as symbolic, execution not authorized | Reported | Reported | Not re-inspected. |
| C-14 | Old Doctor closed (76/14 via brute force); New Doctor terminated 2026-10-08; Pilot 0 never run | Reported | **Partly verified** | `new-doctor/README.md`: "Old Doctor is closed", "No 76/14 reproduction". `PILOT_0_RESULTS.md`: "STATUS: NOT RUN". `DECISIONS.md` final entries all dated 2026-10-08. The 76/14 *explanation* was not verified. |
| C-15 | H3 V10 hosted run 40833639560 completed | Reported | Reported | Not inspected. |
| C-16 | Stage A CONDITIONAL PASS | Reported | Reported | Not inspected. |
| C-17 | `environment_prevent_self_review = false` | Reported | Reported | Not inspected. |

## 2. C-09 recount — the check that changes a row

Performed directly on `lc518-bank-run-41591572358-1.zip` (digest above), no reliance on the Claude or GPT summaries:

| Check | Result |
|---|---:|
| `bank/heldout_bank.json` rows | 80 |
| unique `input_id` | 80 |
| distinct `canonical_id` | 78 |
| duplicated canonical IDs | 2 |
| duplicate pairs | H057/H058 (H6, amount 4758), H059/H060 (H6, amount 4949) |
| same coin multiset within each pair | yes, order differs |
| `heldout_oracle_outputs.json` rows | 78 |
| distinct oracle canonical IDs | 78 |
| bank canonical IDs with no oracle answer | 0 |
| oracle IDs not in the bank | 0 |
| rejection events | 26, all `H2_ORACLE_BELOW_TWO`, candidates H018–H024 |
| `bank/diagnostic_bank.json` rows | 64 |

The 26 rejection events are candidate-generation rejections, not missing outputs.

## 3. Two findings the ledger did not record

1. **Oracle answers are integers, not binary labels.** 78 integers spanning 0–284134 (36 zeros, 8 ones, 34 other). `Y` is a comparison between solver output and this integer, so "78 oracle outputs" must not be read as 78 pass/fail labels.
2. **The oracle file digest is embedded and consistent.** All 80 bank rows declare `oracle_output_file_sha256 = eaae81040424881cc9939e7415a8a5a0328fa870bd2a790d0b4409babd03e244`, and the actual member hashes to exactly that. This binds the two files the C-09 question turned on.

Supporting provenance from `logs/run_manifest.json` in the same archive: `overall_acceptance_status ACCEPTED`, exit 0, `protocol_sha256 9c54ffc2…`, generator `848984ca…` identical before and after the run, launcher `014e45c2…`, `c9_commit 511bc20…`, `c9_source_sha256 f291ae87…`, 63 rejection events in total, 57 tests passed.

## 4. Still unverified

C-06, C-07, C-08, C-11, C-12, C-13, C-15, C-16, C-17, and the 76/14 explanation in C-14. C-04 remains consistent with the records but is not proven by absence.

The v0.21 specification comparison for the manifest validator is a separate open item and is unaffected by this ledger pass.
