# LC518 C2 Repair Packet: Revision 3 Review Index

**Date:** 2026-11-28  
**Review branch:** `review/lc518-c2-sequence-fixes-2026-11-28`  
**Status:** Review only. Not v0.11. Not adopted. No production lock or selection authorized.

## Revision 3 candidate

- `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV3.md` — updated lock-validity design with OAC, one registered experiment ID, one canonical lock ref, one consumed attempt, and reconstructability-based post-lock treatment.
- `sequence-fixes-2026-11-28/GPT_ADJUDICATION_OF_CLAUDE_REVIEW_2026-11-28_REV3.md` — GPT's adjudication of Claude's first review and the remaining blockers.
- `CLAUDE_FOLLOWUP_REVIEW_REQUEST_LC518_C2_REV3_2026-11-28.md` — exact requested verdicts for the Revision 3 files.

## Exact mapping for filenames cited by Revision 2 §10

The Revision 2 packet names files that do not literally exist under those names in the preserved tree. The review branch maps them as follows:

| Filename cited by Revision 2 §10 | Actual review-branch file |
|---|---|
| `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28_REV2.md` | `sequence-fixes-2026-11-28/LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_REVISION_2026-11-28.md` |
| `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28_REV2.md` | `sequence-fixes-2026-11-28/LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_REVISION_2026-11-28.md` |
| `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md` | `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md` |
| `verify_lc518_c2_v07_vectors_REV2.py` | `sequence-fixes-2026-11-28/verify_lc518_c2_v07_vectors_REV2.py` |
| `LC518_C2_PRESERVATION_BRANCH_HISTORY_NOTE_2026-11-28.md` | `sequence-fixes-2026-11-28/LC518_C2_PRESERVATION_BRANCH_HISTORY_NOTE_2026-11-28_REV2.md` |
| `CLAUDE_FOLLOWUP_REVIEW_REQUEST_LC518_C2_REV2_2026-11-28.md` | `CLAUDE_FOLLOWUP_REVIEW_REQUEST_LC518_C2_REV3_2026-11-28.md` |

The old documents are preserved. These are explicit path mappings, not assertions that the names in the earlier review packet are present literally.

## Revision 2 vector verifier and raw output

The review branch contains:
- `sequence-fixes-2026-11-28/verify_lc518_c2_v07_vectors_REV2.py`
- `sequence-fixes-2026-11-28/VERIFY_LC518_C2_V07_VECTORS_REV2_OUTPUT_2026-11-28.txt`

GPT independently authored this standard-library verifier using the frozen v0.7 deterministic vectors and Claude's specified rejection-loop requirements. The exact committed source was run locally and returned **10 checks passed**. It executes the same-label counter advance after an injected rejected integer and tests uint64 overflow. It does not query drand, validate BLS, exercise HTTP retry behavior, or perform a production selection. The injected integer is a test value, not claimed to be an actual SHA-256 digest. This source/output is GPT's own reproducible evidence, not the missing script from the Revision 2 session ZIP and not Claude's earlier reported run.

- Verifier SHA-256: `a83a8eb66e5d6bd9d8c16b146caba2c854400a3fc15e6b21d6794584467ade8d`
- Raw output SHA-256: `1000e3122792172a484697f5d3fb4e0a01baa32e9003fe5544e1d02d13d86d4b`

## Preservation branch status

- Current preservation tip observed: `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`, a normal child of `6f4b697...`.
- Three commits superseded by the prior force-push: `a0f1ba9...`, `0e6c47b...`, and `e0cddea...`. The base `24e973f...` and retained force-pushed tip `6f4b697...` are not counted as superseded.
- Claude's attempts to re-read preservation Activity after 07:03:30Z returned HTTP 403 rate-limit responses. Activity coverage after that event remains outstanding; the 07:54:01Z timestamp of the later `4ab5ce1...` commit is Git commit metadata, not a verified Activity timestamp.
- The independent Git bundle and extraction/hash of the 13,698-byte GitHub ZIP blob remain outstanding.

## Adoption and experiment boundary

GPT's master-tree and code-index checks found no pre-existing canonical C2 `experiment_id` or registry path. Revision 3 therefore requires the actual experiment ID to be taken from a prior study registry and treats its absence as an adoption blocker. No ID has been invented.

The OAC/Revision 3 design is not adoptable until the ID, raw Activity schema/actor fields, complete pagination, timestamp policy, and other listed freeze blockers are resolved and Claude gives fresh verdicts. The 20-push visibility experiment remains NOT AUTHORIZED. The two-relay v0.7 rule remains in force. The original v0.7 lock remains VOID FOR PRODUCTION USE. No production round, seed, pair, R2 C2 compliance, or solver execution is authorized.