# Claim-ledger correction: C-09 held-out bank row/output reconciliation

**Record date:** 2026-11-18  
**Repository:** `foued2/failure-concentration-study`  
**Scope:** One claim correction only. This is not the complete 17-claim LC518/Doctor ledger.  
**Status:** Preliminary claim-ledger correction based on an independent archive inspection reported by Claude.

## 1. Corrected claim and verdict

**Original C-09 proposition:** “The held-out bank has 80 inputs but only 78 oracle outputs, leaving an unresolved output gap.”

**Verdict: CONTRADICTED.**

The reported archive inspection found that the 80 held-out bank rows contain 80 unique row/input IDs but only 78 distinct canonical input IDs. The difference is accounted for by two pairs of rows that encode the same canonical input in a different coin order:

- H057 / H058
- H059 / H060

Both pairs are H6 cases with the same amount and the same coin multiset, ordered differently. They are therefore duplicate canonical inputs, not two missing oracle evaluations.

## 2. Reported archive counts

| Check | Reported result |
|---|---:|
| Rows in `heldout_bank.json` | 80 |
| Unique row/input IDs | 80 |
| Distinct canonical input IDs | 78 |
| Duplicate canonical-input pairs | 2 |
| Rows in `heldout_oracle_outputs.json` | 78 |
| Oracle answers per distinct bank canonical ID | Exactly 1 |
| Missing canonical-ID answers | 0 |
| Extra oracle-output IDs | 0 |
| Events in `heldout_bank.rejections.jsonl` | 26 |

The 26 rejection events were all reported as `H2_ORACLE_BELOW_TWO`, involving rejected candidate-generation attempts across H018–H024. They are not missing oracle-output records.

**Interpretation:** 78 oracle outputs cover all 78 distinct canonical inputs represented by the 80 held-out bank rows. There is no unresolved 80-versus-78 oracle-answer gap.

## 3. Artifact identity and verification provenance

| Field | Record |
|---|---|
| GitHub Actions artifact name | `lc518-bank-run-41591572358-1` |
| Artifact ID | `13210063805` |
| Registered SHA-256 | `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` |
| Archive size | 75,523 bytes |
| Verifier | Claude |
| Verification date | 2026-11-18 |
| Repository branch containing the C9 run | `gpt/lc518-github-recovery-2026-11-02` |
| C9 run commit | `a4ec1148698fe6612c5e873f1193069538a206e3` |
| Workflow run | `41591572358` |

Claude reported checking the archive SHA-256 and size against the artifact record. The verification message supplied in the conversation showed the digest in abbreviated form (`6e6d60c1…bb2`), not the full computed digest. The full value above is the registered artifact digest; the complete verifier output has not been deposited with this record.

**Archive member names reported as inspected:**

- `heldout_bank.json`
- `heldout_oracle_outputs.json`
- `heldout_bank.rejections.jsonl`

The conversation report supplied these member names but did not include any parent-directory prefixes from inside the ZIP. This record does not invent such prefixes.

**Verification independence and limits:** Claude reported inspecting the uploaded archive and checking row counts, canonical-ID coverage, duplicates, and rejection categories. This was an inspection of the underlying archive, not merely agreement with GPT's earlier report. GPT did not independently rerun the count during this repository update. No extraction script, machine-readable verification output, or full computed-digest transcript was included in the supplied Claude report. The result is therefore attributed to Claude's archive inspection; a later reviewer can strengthen reproducibility by preserving those materials.

## 4. Correction history

1. An earlier claim ledger marked the 80-versus-78 count as an open issue.
2. GPT reported that two duplicate H6 permutation pairs explained the difference.
3. Claude declined to mark the issue contradicted solely on GPT's report and retained **Unverified** pending archive inspection.
4. Claude subsequently reported direct inspection of the uploaded archive, identifying the two duplicate pairs and confirming one oracle output for every distinct canonical input, with no missing or extra output IDs.
5. This correction records the original proposition as **Contradicted**, while preserving the fact that it was previously unresolved and that GPT's earlier explanation was subsequently checked by Claude.

Do not delete the earlier uncertainty from the historical ledger. This record supersedes only the unresolved-gap interpretation of C-09.

## 5. Scientific interpretation boundary

This reconciliation resolves the data-count question only. It does **not** restore blinding or confirmatory validity.

The C9 held-out bank remains exposed development material. The count reconciliation does not establish that no one accessed the answers, does not reverse prior exposure, and does not make this bank suitable as a blinded confirmatory test set.

## 6. Repository placement and scope of change

The repository's current `master` root contains a `reviews/` directory with dated review records and no existing claim-ledger file. This correction is therefore placed in `reviews/` as a dated, standalone audit record.

The root `README.md` and `VERIFICATION_LOG.md` were not edited. In particular, the verification log is an earlier historical record and is left unchanged rather than silently rewritten to incorporate later C9 events.

This file records C-09 only. It does not alter protocols, mutation allocations, solver populations, authorization state, or any scientific result.
