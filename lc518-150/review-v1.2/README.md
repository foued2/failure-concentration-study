# LC518-150 v1.2 review material

**Purpose:** make the latest GLM correction record and its verification map available for independent review.

**Source archives:** Both ZIPs were retrieved from the repository root on `master`. They remain on `master`; they are not duplicated on this review branch.
- `message-70b0882f-9d72-402f-a641-36fa9f386b75.zip` — raw SHA-256 `bc7ca0cb20c5576a0c041b2133982c9d7a0bef42b36655b6e2213d3ffa604628`; Git blob `4c38d663b194d4cee7f824385d560548a2b96bd5`.
- `message-73aed204-bc5d-400e-8910-47557479f75e.zip` — raw SHA-256 `d2eee09368e6f70d0856048be25cad96cd8416f7d02844fbc929a1fd35e84257`; Git blob `58ecbc771004d9c26f902f348c2f3871eb50e492`.

## Current review files

| File | Source SHA-256 | Bytes |
|---|---|---:|
| `CORRECTIONS_RECORD_v1.1.md` | `663193006fa3c94a8601eee4b6ac2ed499b0443c342da71914fc572e68d9c78f` | 25,034 |
| `CORRECTIONS_RECORD_v1.2-draft.md` | `120b385c31906afb7ade11eeacc346b5e07f28cc2b15583e5af1417650ca1214` | 60,796 |
| `VERIFICATION_MAP_v1.2.md` | `df994570db441d6e65174501bf80d01ffa633050d6a17755254e65d7b7fb7e9a` | 13,922 |

The byte-identical superseded v1.2 draft from the entry-39 issue is retained under `archive/`:
- `archive/superseded-CORRECTIONS_RECORD_v1.2-draft.entry39-issue-sha256c97c95e0.md`
- SHA-256 `c97c95e0b80d154997b8ba2be1b0fddc5f1e6125593d4d92af8dcb26be32b08e`; 51,903 bytes.

## Scope and limitations

The two ZIPs contain five Markdown files in total (four distinct documents, with the superseded v1.2 version duplicated across the archives). They do **not** contain the two verification scripts, captured verification outputs, README/MANIFEST from GLM's earlier claimed 11-file package, the worklog, or the private mutation annex. Those items have not been reconstructed or invented here.

No solver bodies were added. No solver code was executed. No input bank was generated. The v1.0 source documents were not modified. This branch is a review-material handoff only; the correction record remains a draft and is not scientifically approved by this commit.


## GPT follow-up review branch

A later review-only branch, `gpt/lc518-150-review-followup-2026-11-01`, adds:
- `CORRECTIONS_RECORD_v1.2.1-draft.md` (new version; does not replace the archived v1.2 draft);
- `GPT_REVIEW_v1.2.md` (independent findings and remaining C9 conditions);
- `verification/verify_lc518_v1_2_math.py` (solver-free G22/E1 checks);
- `MANIFEST_GPT_FOLLOWUP.md` (sizes and SHA-256 receipts).

No bank generation or candidate-solver work is included or authorized by that review branch.
