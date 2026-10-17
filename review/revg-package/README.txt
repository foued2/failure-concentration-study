Revision G v3 review package (documentation only)
=================================================

Status: PUBLISHED candidate documentation. Content approved by Foued ("ALL APPROVED",
2026-10-17); publication instruction given ("PUBLISH", 2026-10-17). Stage 1
simulation-protocol freeze has NOT occurred. Phase 1 is NOT AUTHORIZED. Revision F is
not edited; the O2 package and existing numerical results are unchanged.

Contents:
- REVISION_G_v3_candidate.md
    The Revision G v3 candidate document.
- REVISION_G_v3_verification.md
    The verification report (CLAUDE), finalized by the implementation agent under the
    owner's direction; the publication blocker item is resolved.
- MANIFEST.sha256
    SHA-256 of every file in this folder except the manifest itself.
- .gitattributes
    Pins bytes (* -text).

Reference chain (as pinned in the candidate, section 0):
- A1 revision 3: branch review/a1-package, commit f69cc9ba9cf54562df2269f066465f7957c6ccde
- O2 review package rev 2: branch review/o2-package, commit 4d7517a1a30f47d3c41fb9f0ee6eed4397e8e05e
- M3 addendum Rev d: branch review/m3-addendum, commit c70a3870bc23fb973de4c8c7632f84ce0331bb33
- RevF design text blob c9ad2e1e19540e79d06a415e2eb5ab731c1a0daf, 100679 bytes

Caveat (also disclosed in the candidate and the verification report): the candidate
and verification documents were finalized by the implementation agent from the verbatim
reviewed text because CLAUDE's original local files were not accessible on the
implementation machine; byte-level equality with the pre-finalization local files is
not assumed. The published bytes are the reviewed content with only the specified M3
reference updates.

This package is document-only: no calculations, no regeneration, no complete-rule
probability, no solver generation. "INCONCLUSIVE: NOT FEASIBLE AT AN AFFORDABLE N"
remains an acceptable terminal outcome.
