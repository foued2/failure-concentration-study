# LC518 C2 v0.7 provenance correction

Date: 2026-11-27

This record supersedes the provenance explanation in the local handoff package prepared with commit `ac092ab32023d4821f8bffdf1c188906a7f096e7`. It does not alter the v0.7 protocol bytes or its SHA-256.

## Correct predecessor identity

Claude located the earlier uploaded v0.7 draft in his uploads folder and verified its SHA-256:

`ed1beb59334ab8375cde5d3a1d1c57e825b583f62bcbf8cc548222348e534aa5`

The committed corrected v0.7 protocol is:

`05f432c1d6caa5eefcf4f8c0d76954aa769e04d1f10f72473daa832855485f3c`

After normalizing CRLF/LF line endings, Claude compared those two files and found 19 changed lines. He confirmed that all changes are documentary: the v0.5 transfer-branch and v0.6 supersession references, the evidence/location descriptions, and associated review/handoff wording. The algorithm, digest framing, rejection sampling, pair mapping, algorithm sections, and Section 7 target-round formula are unchanged.

Accordingly, the committed corrected v0.7 is a documentary revision of the earlier uploaded v0.7 artifact, not a reconstruction from v0.6 plus pasted text. The earlier draft is superseded for review by the committed corrected file. Both identities are preserved above.

## Correction to the prior handoff and commit description

The previous handoff note and the commit message for `ac092ab` described the corrected copy as reconstructed because the earlier raw v0.7 bytes were not available in the GPT working container at the time of preparation. That explanation is withdrawn in light of Claude's later confirmation that the original upload was available in his uploads folder and that the normalized comparison establishes documentary continuity.

The earlier commit itself is preserved unchanged. This addendum corrects the provenance record without rewriting Git history or changing the reviewed protocol.

## Review scope and disposition

Claude's scoped PASS applies to the committed corrected v0.7 protocol at SHA-256 `05f432c1d6caa5eefcf4f8c0d76954aa769e04d1f10f72473daa832855485f3c`, commit `ac092ab`, branch `review/lc518-c2-v07-corrected-2026-11-27`. The PASS covers the documentary corrections only. It is not owner adoption, a protocol lock, or authorization for a production draw.

No protocol algorithm change, production selection, draw, pair selection, solver construction, or solver execution is authorized by this provenance correction. Original R2 repeat-pair C2 remains `NOT ESTABLISHED`.
