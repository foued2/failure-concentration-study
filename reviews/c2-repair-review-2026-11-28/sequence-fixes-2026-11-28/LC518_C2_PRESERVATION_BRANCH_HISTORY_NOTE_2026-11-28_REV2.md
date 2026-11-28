# LC518 C2 Preservation-Branch History Disclosure, Revision 2

**Date:** 2026-11-28  
**Preservation branch:** `preserve/lc518-c2-repair-packet-2026-11-28`  
**Current preservation tip:** `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`  
**Review branch carrying this disclosure:** `review/lc518-c2-sequence-fixes-2026-11-28`  
**Status:** Review disclosure only. This file does not modify the preservation branch README, master, or historical commits.

## 1. Correction to the earlier disclosure

The earlier draft incorrectly described “four superseded commit objects.” There are **three superseded preservation commits**:

1. `a0f1ba90b92457bfaa43c3ec68c754578243cb0e`
2. `0e6c47b26959019cafc6e11eb04e5f7e19a037dd`
3. `e0cddeacc7ea3ff17477708ec3470f71c8ee476b`

The base commit `24e973fc8517d5467807446f915841896b65f8a4` is not a superseded preservation commit. The force-pushed tip `6f4b6975dd956ea3303653aa3ac8f7a27be31646` is also not one of the three commits it replaced; it remains an ancestor of the current branch. The current tip is `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`.

## 2. Branch lineage verified from Git objects

GPT independently retrieved all relevant commit objects, including `0e6c47b`, and checked their parent links, commit/tree metadata, and recursive tree inventories.

| Event time reported by Claude | Commit timestamp (Git metadata) | Commit | Parent | Role |
|---|---:|---|---|---|
| Branch creation reportedly 06:56:54Z | — | — | `24e973f...` | Preservation branch reportedly created from the VOID-record base. |
| Push reportedly 06:59:56Z | 06:59:55Z | `a0f1ba90b92457bfaa43c3ec68c754578243cb0e` | `24e973f...` | First preservation commit; included three Markdown source notes, README, verifier, and ZIP blob. |
| Push reportedly 07:02:04Z | 07:02:03Z | `0e6c47b26959019cafc6e11eb04e5f7e19a037dd` | `a0f1ba9...` | Removed the unverified ZIP blob; retained the five text/source files. |
| Push reportedly 07:02:39Z | 07:02:38Z | `e0cddeacc7ea3ff17477708ec3470f71c8ee476b` | `0e6c47b...` | Updated five text/source files with documentary/final-newline corrections. |
| Force-push reportedly 07:03:30Z | 07:03:29Z | `6f4b6975dd956ea3303653aa3ac8f7a27be31646` | `24e973f...` | Replaced `e0cddea...` as branch tip. It did not descend from the three intermediate preservation commits. |
| Later normal Revision 2 commit | 07:54:01Z | `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21` | `6f4b697...` | Added `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md` and `README_REV2.md` by normal fast-forward commit. This is the current preservation tip. |

The three intermediate commit IDs and the force-push transition remain explicitly recorded:

- Force-push `before`: `e0cddeacc7ea3ff17477708ec3470f71c8ee476b`
- Force-push `after`: `6f4b6975dd956ea3303653aa3ac8f7a27be31646`
- Reported Activity event time: `2026-11-28T07:03:30Z`

The current preservation branch is therefore not the 07:03:29Z commit. Its current tip is the later Revision 2 commit `4ab5ce1...`.

## 3. Evidence boundary for Activity coverage

The branch-creation, push, and force-push event times above are attributed to Claude's read-only Activity API inspection. GPT independently verified Git commit object metadata and ancestry; Git author/committer timestamps must not be presented as Activity event timestamps.

Claude's latest read-only attempt to retrieve the preservation ref's Activity records returned HTTP 403 rate-limit responses on both attempts. No retry was made. Therefore:

- the Activity chronology is verified only through the reported 07:03:30Z force-push event;
- Activity coverage after 07:03:30Z is **OUTSTANDING**;
- the 07:54:01Z timestamp for `4ab5ce1...` is the Git commit metadata timestamp only, not a verified Activity push-event timestamp;
- no claim is made that the Activity ledger contains no later events.

When the rate limit permits, retrieve the exact raw unauthenticated Activity request/response, all pages, headers, and the selected API-version header. Record the exact request URL and any 403/429 responses. Do not treat an incomplete or rate-limited response as proof of absence.

## 4. Contents of the three superseded commits

### 4.1 Initial commit `a0f1ba9...`

Its tree contained:

| Path | Git blob SHA-1 | Size |
|---|---|---:|
| `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28.md` | `f85795cd2c6cbc6881ff7ff88cada14fadac62f8` | 17,982 |
| `LC518_C2_REPAIR_REVIEW_PACKET_2026-11-28.zip` | `b5998912ff9fcee8584ada76ebd370128ba8f6b2` | 13,698 |
| `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28.md` | `67e4d405f6060bac3a3c09ecdb0055bc5ca89bcc` | 3,801 |
| `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28.md` | `12bfc903c5502b790306f0ef9354762b17c8b00c` | 4,775 |
| `README.md` | `dd0a02e8b73c618a8ac59fd2ea552826ef288750` | 1,270 |
| `verify_lc518_c2_v07_vectors.py` | `ba3cb8c7882fb08a23f6629cb17a34e5d261ac16` | 3,242 |

The GitHub ZIP blob is 13,698 bytes. The separately reported local ZIP was 13,701 bytes with SHA-256 `4f2a16e624661417873d224982d015644916755cc9e90ae60d925502ad3b8c7f`. Those are different byte sequences and must not be represented as one verified archive.

### 4.2 Intermediate cleanup commit `0e6c47b...`

This commit removed only the ZIP blob from the directory. The five remaining text/source blobs were unchanged from the initial commit:

| Path | Git blob SHA-1 | Size |
|---|---|---:|
| `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28.md` | `f85795cd2c6cbc6881ff7ff88cada14fadac62f8` | 17,982 |
| `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28.md` | `67e4d405f6060bac3a3c09ecdb0055bc5ca89bcc` | 3,801 |
| `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28.md` | `12bfc903c5502b790306f0ef9354762b17c8b00c` | 4,775 |
| `README.md` | `dd0a02e8b73c618a8ac59fd2ea552826ef288750` | 1,270 |
| `verify_lc518_c2_v07_vectors.py` | `ba3cb8c7882fb08a23f6629cb17a34e5d261ac16` | 3,242 |

GPT independently verified the commit object `0e6c47b...`, its parent `a0f1ba9...`, its tree, and the deletion of the ZIP entry. This corrects the earlier statement that this commit had not been independently checked.

### 4.3 Intermediate documentation commit `e0cddea...`

This commit updated all five remaining files:

| Path | Git blob SHA-1 | Size |
|---|---|---:|
| `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28.md` | `c6862a437c36791971f5848e03048f6eb226cb0a` | 17,983 |
| `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28.md` | `7639fd32181fcd7770683c51cb5b02d0363874a6` | 3,802 |
| `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28.md` | `4c2eff6afb01d0b91607266a62f71656f6ec5ab1` | 4,776 |
| `README.md` | `f3cf1b67408af7201cc491ae19cf0bbaafd01ba5` | 1,606 |
| `verify_lc518_c2_v07_vectors.py` | `f0bcacc088e698dd0e1c5600355bc110a52b7ff5` | 3,243 |

The README explained why the unverified ZIP was removed from the GitHub branch. The force-push at 07:03:30Z replaced this commit as the tip.

## 5. Force-pushed tip and current Revision 2 tip

The force-pushed commit `6f4b697...` has parent `24e973f...` and contains the four review source files plus the vector script, without the ZIP. It is the point at which the preserved source packet was recreated directly from the base rather than appended to the initial preservation commit chain.

The later commit `4ab5ce1...` is a normal child of `6f4b697...`. Its recursive tree includes:
- `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md`;
- `README_REV2.md`;
- the prior source notes and vector script.

The Revision 2 README says the Revision 2 verifier and run output are in a session ZIP. The recursive Git tree at `4ab5ce1...` does not contain a separately named Revision 2 verifier source or its raw output. GPT has since prepared a separately identified verifier source and ten-check raw output on the sequence-fix review branch; those files are GPT's implementation, not a recovered copy of the missing session ZIP script.

## 6. Remaining offline preservation task

The superseded commit objects and the 13,698-byte ZIP blob should still be saved to independent offline storage. This review branch has recorded their full IDs and tree inventories, but **no independent Git bundle or extracted ZIP archive has yet been created and verified**.

Do not force-push, rewrite, or rebase the preservation branch to make the old history look linear. Fetch the three superseded commit objects by full SHA, the base, and the current tip; pin them under local archival refs; create and verify a Git bundle; separately extract the 13,698-byte ZIP blob and calculate its actual SHA-256. Keep that ZIP separate from the 13,701-byte local archive.

## 7. Current disposition

- Three superseded preservation commits: disclosed and identified.
- Base commit `24e973f...`: not counted as superseded.
- Force-pushed tip `6f4b697...`: retained as ancestor of current tip.
- Current preservation tip: `4ab5ce1...`.
- Activity coverage after the reported 07:03:30Z force-push: OUTSTANDING due HTTP 403 rate limit.
- Git object bundle and raw 13,698-byte ZIP extraction: NOT YET COMPLETED.
- The preservation branch README has not been modified by this review branch.
- No merge to `master`, protocol adoption, production lock, or experiment execution is implied.
