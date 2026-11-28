# LC518 R2 C2 Review Packet

**Single current entry point.** Review Revision 5 as the current candidate. Revisions 2-4 and v0.7 remain preserved historical records.

- Review branch: review/lc518-c2-sequence-fixes-2026-11-28
- Base before Revision 5 consolidation: 0b159127443dac275bf187943d5d558f5edcac56
- Master: ccbd0bdefd2d02ec22f6e17f27e9d0074952605a (unchanged)
- Preservation branch: 4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21 (unchanged)
- Superseded-history archive branch: archive/lc518-c2-superseded-history-2026-11-28
- Status: Revision 5 candidate only. NOT ADOPTED. NOT LOCKED. NO DRAW AUTHORIZED.

## Read first

1. LC518_R2_C2_SELECTION_PROTOCOL_REV5_COMPOSITE_2026-11-28.md: complete consolidated protocol candidate, retaining v0.7 §§1-6 and replacing §§7-8, then adding §§9-11.
2. LC518_R2_C2_SELECTION_PROTOCOL_REV5_COMPOSITE_2026-11-28.sha256: canonical SHA-256 sidecar. Digest: 8b5c670edc853acb15dab045f174153cc7253efa55d342b48e8184eab59815ea.
3. LC518_C2_REVIEW_RESPONSE_AND_REVISION_5_2026-11-28.md: Claude Revision 4 response and full replacement map.
4. CLAUDE_REVIEW_REQUEST_LC518_C2_REV5_2026-11-28.md: fresh review request.
5. GPT_ADJUDICATION_OF_CLAUDE_REVIEW_REV5_2026-11-28.md: accepted findings and remaining blockers.
6. GIT_BLOB_INVENTORY_REV5.md: exact blob identifiers and hashes.

## Activity evidence

- evidence/ACTIVITY_PAGE1_NORMALIZED_EXTRACT_2026-11-28.json: 100 parsed records from the connected GitHub Activity reader; normalized projection only, not raw HTTP bytes.
- evidence/ACTIVITY_PAGE1_NORMALIZED_EXTRACT_2026-11-28.sha256: SHA-256 14fa57a6a80515bce494178bc35a2955e5cea5f86a23074e63c86ebd94fec1e2.
- Claude reports a 944-record, ten-page ascending Activity feed through 2026-11-28T10:34:48Z, but raw bytes/headers for the ten pages are not yet preserved.
- Claude's reported raw page-1 SHA-256 is not independently authenticated because those raw bytes are not present.

## Verifier and preservation

- The hardened Revision 3 GPT verifier and 14-check output remain under sequence-fixes-2026-11-28/.
- They test deterministic vector/rejection-loop behavior only, not the pinned production client, drand, BLS, HTTP, Activity API, OAC, or production selection.
- The uploaded Git bundle was verified; its Git object lineages remain reachable via the preservation and archive branches. The original bundle container is not duplicated here.
- The ZIP-labelled 13,698-byte upload is preserved as corrupt evidence only, not as a usable archive.

## Historical records

- LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV4.md: previous Revision 4, NOT ADOPTABLE.
- LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV3.md
- LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md
- README_REV3.md and sequence-fixes-2026-11-28/README_REV3.md
- LC518_C2_V07_SECTION_7_REPLACEMENT_REV4_2026-11-28.md is historical and is superseded by the Revision 5 composite §§7-8.

## Hard blockers

1. The exact pre-existing C2 registry path/entry and root experiment ID remain unidentified. Do not invent an ID; no OAC may be created.
2. Raw Activity bodies/headers and the complete 944-record ledger are not yet preserved.
3. Activity API retention is undocumented; missing pages or rate limits fail closed for that retrieval run.
4. The actual drand retrieval client has not passed a local mock-conformance test.
5. Fresh Claude review of the exact Revision 5 composite SHA-256 is pending.

The two-relay v0.7 rule is unchanged. The 20-push visibility experiment remains NOT AUTHORIZED. No draw, R2 C2 adoption, solver construction, or solver execution is authorized.
