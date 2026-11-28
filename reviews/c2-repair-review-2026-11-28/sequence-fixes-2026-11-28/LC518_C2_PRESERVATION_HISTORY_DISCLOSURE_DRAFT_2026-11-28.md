# LC518 C2 Preservation-Branch History Disclosure Draft

**Date:** 2026-11-28  
**Target:** append to `reviews/c2-repair-review-2026-11-28/README.md` on the preservation branch, after scoped review.  
**Status:** Draft disclosure and archival inventory. This copy is preserved on the separate review branch `review/lc518-c2-sequence-fixes-2026-11-28`; it has not been applied to the preservation branch README. The historical commits are identified below; the full Git object archive has not yet been saved to an independent offline bundle.

## 1. Why this disclosure is required

At the time of GPT's read-only check, `master` pointed to `ccbd0bdefd2d02ec22f6e17f27e9d0074952605a`; its recursive tree did not contain `reviews/c2-repair-review-2026-11-28/`. The preservation artifacts documented here are therefore not merged to `master`.

The preservation branch `preserve/lc518-c2-repair-packet-2026-11-28` was force-pushed. The current branch tip does not descend from the three earlier preservation commits. A preservation README that describes only the final branch tip would omit material history and could incorrectly imply that the branch was append-only.

The Activity event times below are from Claude's read-only Activity API inspection, as reported in the 2026-11-28 review. GPT independently retrieved the four Git commit objects by full SHA and checked their parent links, commit/tree metadata, and tree contents through the GitHub connection. GPT did **not** independently retrieve or preserve the raw Activity API bodies/headers or the Activity event IDs for these branch events. The branch-creation and push times are therefore explicitly attributed to Claude's Activity inspection, not represented as GPT's independent raw-API verification.

## 2. Chronology

All times are UTC on 2026-11-28.

| Reported Activity event | Git commit time | Commit | Parent | Tree | What the Git object shows |
|---|---:|---|---|---|---|
| Branch creation: 06:56:54 | — | Branch created from base `24e973fc8517d5467807446f915841896b65f8a4` | — | — | Claude reports the preservation branch was created. No raw event ID/body is included in the packet. |
| Push: 06:59:56 | 06:59:55 | `a0f1ba90b92457bfaa43c3ec68c754578243cb0e` | `24e973fc8517d5467807446f915841896b65f8a4` | `b183c64520c60c293040bc53ca15a8103a2239a8` | Initial preservation commit. Its tree contained the four payload files (three Markdown review notes and the vector-check script), a README, and a ZIP blob. |
| Push: 07:02:04 | 07:02:03 | `0e6c47b26959019cafc6e11eb04e5f7e19a037dd` | `a0f1ba90b92457bfaa43c3ec68c754578243cb0e` | `170f8b1e436f75bc84ecef225f6a323176d048c4` | Removed the unverified ZIP blob. The five text/source artifacts otherwise retained their prior blob identities. |
| Push: 07:02:39 | 07:02:38 | `e0cddeacc7ea3ff17477708ec3470f71c8ee476b` | `0e6c47b26959019cafc6e11eb04e5f7e19a037dd` | `bf993fbaac482c2ef3c5e05ebe7fa86e1efc94cc` | Updated the four text notes, README, and vector script with final-newline/documentary corrections. README explained why the ZIP was not represented as a verified GitHub artifact. |
| **Force-push: 07:03:30** | 07:03:29 | `6f4b6975dd956ea3303653aa3ac8f7a27be31646` | `24e973fc8517d5467807446f915841896b65f8a4` | `ec3d41c6a5dace557c1053a20aa9bcccc1729506` | Replaced the branch tip by a new commit directly based on the original base commit, rather than on `e0cdde…`. Claude reports the Activity event as `force_push`, replacing `e0cdde…` with `6f4b697…`. The current branch tree contains the four source notes and vector script but not the ZIP. |

The exact force-push transition reported by Claude was:

- **Before:** `e0cddeacc7ea3ff17477708ec3470f71c8ee476b`
- **After:** `6f4b6975dd956ea3303653aa3ac8f7a27be31646`
- **Activity event time:** `2026-11-28T07:03:30Z` (reported by Claude)

The commit timestamps are one second earlier than their corresponding reported Activity event times. These are distinct fields and must not be conflated.

## 3. Superseded first-push contents and ZIP discrepancy

The initial preservation commit `a0f1ba90b92457bfaa43c3ec68c754578243cb0e` had the following tree entries under `reviews/c2-repair-review-2026-11-28/`:

| File | Git blob SHA-1 | Size (bytes) |
|---|---|---:|
| `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28.md` | `f85795cd2c6cbc6881ff7ff88cada14fadac62f8` | 17,982 |
| `LC518_C2_REPAIR_REVIEW_PACKET_2026-11-28.zip` | `b5998912ff9fcee8584ada76ebd370128ba8f6b2` | 13,698 |
| `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28.md` | `67e4d405f6060bac3a3c09ecdb0055bc5ca89bcc` | 3,801 |
| `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28.md` | `12bfc903c5502b790306f0ef9354762b17c8b00c` | 4,775 |
| `README.md` | `dd0a02e8b73c618a8ac59fd2ea552826ef288750` | 1,270 |
| `verify_lc518_c2_v07_vectors.py` | `ba3cb8c7882fb08a23f6629cb17a34e5d261ac16` | 3,242 |

The locally retained ZIP described in the original verification note is **13,701 bytes** with SHA-256:

`4f2a16e624661417873d224982d015644916755cc9e90ae60d925502ad3b8c7f`

The ZIP blob in the initial GitHub commit is 13,698 bytes and has Git blob SHA-1 `b5998912ff9fcee8584ada76ebd370128ba8f6b2`. Because the lengths differ, the GitHub blob cannot be byte-identical to the stated local ZIP. This supports the later decision to remove the unverified binary from the preservation branch. Do not represent the two as the same archive.

The GitHub file endpoint was successfully queried with base64 encoding, but the returned base64 payload has not yet been decoded into a locally stored ZIP file. Therefore, its ZIP CRC/integrity test and raw-byte SHA-256 have not been performed in this working archive. The full commit/tree/blob identities and size are recorded above, but this Markdown dossier is not a substitute for a Git object bundle containing the binary.

## 4. Contents of the intermediate commits

The intermediate commit `0e6c47b26959019cafc6e11eb04e5f7e19a037dd` retained the five text files from the first commit and removed only the ZIP:

| File | Git blob SHA-1 | Size (bytes) |
|---|---|---:|
| `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28.md` | `f85795cd2c6cbc6881ff7ff88cada14fadac62f8` | 17,982 |
| `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28.md` | `67e4d405f6060bac3a3c09ecdb0055bc5ca89bcc` | 3,801 |
| `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28.md` | `12bfc903c5502b790306f0ef9354762b17c8b00c` | 4,775 |
| `README.md` | `dd0a02e8b73c618a8ac59fd2ea552826ef288750` | 1,270 |
| `verify_lc518_c2_v07_vectors.py` | `ba3cb8c7882fb08a23f6629cb17a34e5d261ac16` | 3,242 |

The next commit, `e0cddeacc7ea3ff17477708ec3470f71c8ee476b`, updated all five of those text files. The tree inventory was:

| File | Git blob SHA-1 | Size (bytes) |
|---|---|---:|
| `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28.md` | `c6862a437c36791971f5848e03048f6eb226cb0a` | 17,983 |
| `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28.md` | `7639fd32181fcd7770683c51cb5b02d0363874a6` | 3,802 |
| `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28.md` | `4c2eff6afb01d0b91607266a62f71656f6ec5ab1` | 4,776 |
| `README.md` | `f3cf1b67408af7201cc491ae19cf0bbaafd01ba5` | 1,606 |
| `verify_lc518_c2_v07_vectors.py` | `f0bcacc088e698dd0e1c5600355bc110a52b7ff5` | 3,243 |

The changes recorded in that tree include final-newline repairs and a README clarification that the ZIP was removed because byte-for-byte identity of the binary transfer could not be established. The force-pushed tip then recreated the source set directly from the base commit, as detailed below.

## 5. What was preserved by the force-pushed tip

The final force-push commit `6f4b6975dd956ea3303653aa3ac8f7a27be31646` has parent `24e973fc8517d5467807446f915841896b65f8a4`. Its tree contains:

| File | Git blob SHA-1 | Size (bytes) |
|---|---|---:|
| `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28.md` | `c6862a437c36791971f5848e03048f6eb226cb0a` | 17,983 |
| `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28.md` | `7639fd32181fcd7770683c51cb5b02d0363874a6` | 3,802 |
| `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28.md` | `4c2eff6afb01d0b91607266a62f71656f6ec5ab1` | 4,776 |
| `README.md` | `2bb7b73340bba56e1b24a5dddb492bfc5de25522` | 1,669 |
| `verify_lc518_c2_v07_vectors.py` | `f0bcacc088e698dd0e1c5600355bc110a52b7ff5` | 3,243 |

This confirms the current branch tip preserves the four text source artifacts and vector script. It does not preserve the earlier ZIP blob. The earlier commits remain identifiable by their full SHA values, but their continued availability from GitHub is not guaranteed by any retention commitment established in this review.

## 6. Required independent Git-object archive

The four superseded commit objects and the initial ZIP blob should be saved to an independent offline Git bundle now, before assuming that SHA-addressed retrieval will remain available. This review has **not** completed that binary/Git-pack archival step.

On a machine with Git and network access, from the existing repository clone, retrieve and pin the objects by full SHA, then create and verify a bundle. Example PowerShell sequence (check every exit code and do not push anything):

```powershell
$repo = 'C:\Users\Foued\PycharmProjects\failure-concentration-study'
$shas = @(
  '24e973fc8517d5467807446f915841896b65f8a4',
  'a0f1ba90b92457bfaa43c3ec68c754578243cb0e',
  '0e6c47b26959019cafc6e11eb04e5f7e19a037dd',
  'e0cddeacc7ea3ff17477708ec3470f71c8ee476b',
  '6f4b6975dd956ea3303653aa3ac8f7a27be31646'
)

foreach ($sha in $shas) {
  git -C $repo fetch origin $sha
  if ($LASTEXITCODE -ne 0) { throw "Fetch failed for $sha" }
  git -C $repo update-ref "refs/archive/lc518-c2-preservation/$sha" $sha
  if ($LASTEXITCODE -ne 0) { throw "Could not pin $sha" }
}

$refs = $shas | ForEach-Object { "refs/archive/lc518-c2-preservation/$_" }
$bundle = Join-Path (Split-Path $repo -Parent) 'LC518_C2_PRESERVATION_HISTORY_2026-11-28.bundle'
git -C $repo bundle create $bundle $refs
if ($LASTEXITCODE -ne 0) { throw 'Bundle creation failed' }
git -C $repo bundle verify $bundle
if ($LASTEXITCODE -ne 0) { throw 'Bundle verification failed' }
Get-FileHash $bundle -Algorithm SHA256
```

Afterward, separately extract the ZIP blob from `a0f1ba…` and record its actual byte length and SHA-256. Do not overwrite the 13,701-byte local ZIP. Keep the extracted 13,698-byte GitHub version as a distinct superseded artifact. Store the verified bundle, extracted ZIP, and hash manifest outside the repository, preferably on two independent storage devices.

If Git refuses to fetch an unadvertised SHA, do not rewrite refs or force-push the preservation branch. Use a full clone/fetch or a GitHub object-download method that preserves the exact commit/tree/blob objects, then verify the resulting Git bundle and blob contents.

## 7. Evidence boundary and current disposition

- The current branch tip and all four commit objects were independently read by GPT through the GitHub connection. The parent links, commit metadata, tree SHAs, and tree file inventories are directly observed Git object data.
- The branch-creation/push/force-push event times are attributed to Claude's 2026-11-28 Activity API inspection. The raw Activity response bodies, response headers, exact request URL, and event IDs for these preservation-branch events were not supplied in the reviewed packet and were not independently retrieved by GPT.
- The initial ZIP discrepancy is directly established by the Git tree's blob size (13,698 bytes) versus the locally reported file size (13,701 bytes). Its raw GitHub bytes have not yet been archived locally.
- The force-push is not concealed or treated as a routine fast-forward update. It replaced the branch lineage; all superseded commit identities and tree contents are disclosed above.
- No project/master branch file was changed by this disclosure draft. No branch, commit, ref, or GitHub setting was created or modified during preparation of this file.

**Current status:** force-push disclosed in this review draft; commit identities inventoried; independent Git-bundle archival still outstanding; disclosure not yet applied to the preservation branch README; no merge to `master` or protocol adoption authorized.
