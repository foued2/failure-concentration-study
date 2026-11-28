# Revision 5 Repository Blob Inventory

**Review branch:** review/lc518-c2-sequence-fixes-2026-11-28  
**Revision 5 composite SHA-256:** 8b5c670edc853acb15dab045f174153cc7253efa55d342b48e8184eab59815ea  
**Canonical bytes:** UTF-8, no BOM, LF line endings, exactly one final LF.  
**Note:** Git blob SHA-1 identifies a Git object. SHA-256 identifies the exact file bytes where explicitly listed.

| Path | Git blob SHA-1 | SHA-256 / purpose |
|---|---|---|
| `LC518_R2_C2_SELECTION_PROTOCOL_REV5_COMPOSITE_2026-11-28.md` | `e90b255501154a071d8693196e70b918261f6f87` | `8b5c670edc853acb15dab045f174153cc7253efa55d342b48e8184eab59815ea`; canonical review composite |
| `LC518_R2_C2_SELECTION_PROTOCOL_REV5_COMPOSITE_2026-11-28.sha256` | `3d6af5d7a4c6d1639c1e9258b5160d0c7cd90b23` | External checksum sidecar; hash is not self-embedded |
| `LC518_C2_REVIEW_RESPONSE_AND_REVISION_5_2026-11-28.md` | `e5de94c82ea94e08c581367d0083376b13fd2e71` | Claude Revision 4 response and v0.7 replacement map |
| `CLAUDE_REVIEW_REQUEST_LC518_C2_REV5_2026-11-28.md` | `47e191d097736db2f2a4eeff75767598904d9f67` | Fresh review request with 18 separate verdicts |
| `GPT_ADJUDICATION_OF_CLAUDE_REVIEW_REV5_2026-11-28.md` | `4f109f5d2a92852f4dfc769f6dd05b7393313ad4` | Accepted findings and unresolved evidence boundary |
| `README.md` | `eeb8b2e5fbec787b6764f17ffbbff7693daf7202` | Single entry point |
| `GIT_BLOB_INVENTORY_REV5.md` | To be inserted after its creation | This inventory |

## Parsed Activity page 1

| Path | Git blob SHA-1 | SHA-256 / purpose |
|---|---|---|
| `evidence/ACTIVITY_PAGE1_NORMALIZED_EXTRACT_2026-11-28.json` | `b4cfc031b894da9af1c29b2768f1fd0f55767ed2` | `14fa57a6a80515bce494178bc35a2955e5cea5f86a23074e63c86ebd94fec1e2`; 44,185-byte normalized projection of 100 parsed records, not raw HTTP data |
| `evidence/ACTIVITY_PAGE1_NORMALIZED_EXTRACT_2026-11-28.sha256` | `c3afe1f117e820d49e1f5e6028d7653e2b899d79` | External checksum sidecar |

## Historical files retained

- Revision 4 and its prior standalone section 7 replacement remain unchanged and historical; Revision 4 was NOT ADOPTABLE.
- Revision 3 and Revision 2 remain unchanged.
- Revision 2 and Revision 3 verifier source/output remain preserved.
- The Revision 3 verifier remains GPT-authored deterministic-model evidence only; not a pinned production-client test.
- The original v0.7 protocol file remains unchanged.

## Branch/ref boundary

- Master: `ccbd0bdefd2d02ec22f6e17f27e9d0074952605a` (not changed).
- Preservation branch: `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21` (not changed).
- Superseded-history archive branch: `archive/lc518-c2-superseded-history-2026-11-28` at `e0cddeacc7ea3ff17477708ec3470f71c8ee476b`.
- Review branch is the only branch receiving Revision 5 review materials.

## Evidence not yet preserved

Claude's reported 944-record ten-page Activity ledger and raw page 1 response bytes/headers are not committed as a complete wire-evidence package. The normalized 100-record projection is separately labelled as parsed data. Claude's reported raw page 1 SHA-256 is not independently authenticated here.