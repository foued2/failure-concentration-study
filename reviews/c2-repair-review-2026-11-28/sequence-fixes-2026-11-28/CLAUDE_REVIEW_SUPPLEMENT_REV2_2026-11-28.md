# Claude Review Supplement: Preservation Revision 2 and GPT Adjudication

**Date:** 2026-11-28  
**Review branch merge commit:** `29401db7c594795d53070057be561b29eb358bc6`  
**Preservation Revision 2 commit:** `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`

The review branch now contains both:
- the preservation branch's Revision 2 repair proposal and README; and
- GPT's separate sequence-fix drafts under `reviews/c2-repair-review-2026-11-28/sequence-fixes-2026-11-28/`.

GPT's preferred direction is now Revision 2's deterministic-ref / first-`B → A`-event design, not the earlier GPT TSA/300-second alternative. Read `GPT_ADJUDICATION_OF_CLAUDE_REV2_2026-11-28.md` first for the adjudication and specific unresolved challenges.

## Required separate verdicts

1. **Revision 2 lock design:** PASS / NOT PASS. Review deterministic ref derivation, branch creation `0 → B`, first push `B → A`, one-parent commit `A), event-time parsing, no later void/re-roll, and non-retrieval semantics.
2. **GPT adjudication:** Agree / disagree with its challenges, especially post-lock tampering not being allowed to suppress an otherwise reconstructable selection.
3. **Buffer:** State whether `B_lock` can be justified without the former 20-push visibility experiment. That experiment remains NOT AUTHORIZED; it does not measure timestamp clock accuracy.
4. **DigiCert RFC 3161:** State whether it is useful as an optional evidence-manifest timestamp only. Do not let it become a second validity gate or a substitute for GitHub response authentication.
5. **Historical hash addendum and timing clarification:** PASS / NOT PASS on the revised copies in the GPT sequence-fix directory.
6. **Force-push disclosure:** PASS / NOT PASS on the companion preservation-history draft and README section.
7. **Verifier source:** confirm whether the Revision 2 verifier source and raw 10-check output are present in the branch. The preserved Revision 2 tree lists the README and revised repair note, but does not list a separate `verify_lc518_c2_v07_vectors_REV2.py` file. The README says the verifier is in a session ZIP, not a GitHub blob. Do not issue a source-level PASS until the exact script is available.

Do not merge to `master`, adopt a protocol, create a lock ref, query a production round, select a seed/pair, or execute solvers as part of this review.
