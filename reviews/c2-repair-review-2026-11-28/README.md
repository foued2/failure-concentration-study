# LC518 R2 C2 Review Packet

**Single entry point for this workstream.** Use this index. The current review materials, verifier, and quarantined input are grouped here; historical Revision 2 and Revision 3 records remain unchanged.

- Review branch: `review/lc518-c2-sequence-fixes-2026-11-28`
- Base before consolidation: `84ec3db0678904e92e63769be59c1547cee7fbc8`
- Master: `ccbd0bdefd2d02ec22f6e17f27e9d0074952605a` (unchanged)
- Preservation branch: `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21` (unchanged)
- Superseded-history archive branch: `archive/lc518-c2-superseded-history-2026-11-28`
- Status: Revision 4 review candidate only. NOT ADOPTED. NOT PRODUCTION AUTHORIZATION. No OAC, experiment ID, lock, draw, pair selection, or solver work is authorized.

## Read these first

1. [Revision 4 composite](LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV4.md): consolidated design and corrected rules.
2. [Complete v0.7 section 7 replacement](LC518_C2_V07_SECTION_7_REPLACEMENT_REV4_2026-11-28.md): full replacement text and explicit deletion of the further-draw sentence.
3. [Claude review request](CLAUDE_REVIEW_REQUEST_LC518_C2_REV4_2026-11-28.md): separate verdicts requested.
4. [GPT adjudication](GPT_ADJUDICATION_OF_CLAUDE_REVIEW_REV4_2026-11-28.md): accepted findings, changes, and blockers.
5. [Archive verification report](UPLOAD_ARCHIVE_VERIFICATION_REPORT_2026-11-28.md): uploaded bundle verification, Git branch retention, and corrupt-ZIP details.
6. [Revision 4 blob inventory](GIT_BLOB_INVENTORY_REV4.md): exact Git blob identities and artifact hashes.

## Evidence and verifier

- [Quarantined ZIP-labelled raw bytes](evidence/LC518_C2_REPAIR_REVIEW_PACKET_2026-11-28__GITHUB_BLOB_b5998912_CORRUPT.zip): exact 13,698-byte upload. It is corrupt and is not a usable ZIP.
- Preservation bundle: 475,220 bytes; SHA-256 `df16563f0244ba1e5231d0c40504a2dc2abefd397e455f99f01162819fc5665e`; Git blob `570dbd11f4ebb1591d855b8c27505e59118efc33`; six refs; verified locally. The original bundle container is not duplicated in the repository. Its Git object lineages are retained by the archive and preservation branches.
- Historical Revision 2 verifier and output remain under `sequence-fixes-2026-11-28/`, unchanged.
- Hardened Revision 3 verifier and raw output are in the same directory. Source SHA-256: `961aa2b3f4861cd827ea40efb726ab4bcd9b2ab175026f765e9cd69d37ec85f6`. Output SHA-256: `87d192c354b91b0a26fb92156b623e7265573afd29d291dd2e6a2d532bb3500e`. Fourteen deterministic checks pass.
- Both verifiers cover deterministic vectors/rejection sampling only. Neither queries drand, verifies BLS, tests the actual HTTP client, verifies GitHub Activity, or performs production selection.

## Historical record, preserved unchanged

- [Revision 3](LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV3.md)
- [Revision 2](LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md)
- [Revision 2 filename mapping](README_REV3.md)
- [Sequence-fix history and inventory](sequence-fixes-2026-11-28/README_REV3.md)

Older drafts, preservation notes, inventories, and verifier evidence remain under `sequence-fixes-2026-11-28/`. This root README is the single current index.

## Remaining hard blockers

1. The pre-existing C2 experiment-registry path/entry and canonical root `experiment_id` have not been found. Do not invent an ID.
2. Raw Activity response bodies and headers are not archived. The actor numeric-ID field and exact `before=0` representation remain unverified.
3. A complete repository-wide Activity ledger covering the canonical ref's entire lifetime, including pre-OAC events, has not been established. 403/429, missing pages, or partial history fail closed.
4. Revision 4's root/successor chain, equal-timestamp chronology, full-lifetime scan, and literal section 7 replacement require fresh Claude review.
5. The actual drand retrieval client has not been run through a local mock harness. Do not substitute a disconnected imitation.
6. Preservation Activity coverage after 07:03:30Z remains outstanding.

The 20-push visibility study remains NOT AUTHORIZED. The two-relay v0.7 rule remains unchanged. The current v0.7 file is not modified by this review packet. No master merge or protocol adoption is implied by this review-branch update.