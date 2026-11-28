## Preservation-branch history and force-push disclosure (2026-11-28)

The branch `preserve/lc518-c2-repair-packet-2026-11-28` was force-pushed. The current tip does not descend from the preceding preservation commits. This chronology must be read as part of the packet's provenance, not as a fast-forward-only preservation history.

At the time of this read-only check, `master` pointed to `ccbd0bdefd2d02ec22f6e17f27e9d0074952605a`; its recursive tree did not contain `reviews/c2-repair-review-2026-11-28/`. The preservation artifacts described below are therefore not merged to `master`. The separate sequence-fix review branch `review/lc518-c2-sequence-fixes-2026-11-28` contains review drafts only and is also not merged to `master`.

The Activity event times below are those reported by Claude's read-only Activity API inspection. GPT independently retrieved the corresponding Git commit objects and checked their parent links, tree SHAs, and file inventories. GPT did not independently preserve the raw Activity API response bodies/headers or the Activity event IDs for these branch events. The Activity times are attributed to Claude; the commit timestamps and Git ancestry are independently observed object metadata.

All times are UTC on 2026-11-28.

| Activity event reported by Claude | Git commit timestamp | Commit | Parent | Disposition |
|---|---:|---|---|---|
| Branch creation 06:56:54 | — | — | `24e973fc8517d5467807446f915841896b65f8a4` | Branch reportedly created from the base commit. |
| Push 06:59:56 | 06:59:55 | `a0f1ba90b92457bfaa43c3ec68c754578243cb0e` | `24e973fc8517d5467807446f915841896b65f8a4` | Initial packet commit. Its tree included the four payload files (three Markdown review notes and the vector-check script), a README, and a ZIP blob. |
| Push 07:02:04 | 07:02:03 | `0e6c47b26959019cafc6e11eb04e5f7e19a037dd` | `a0f1ba90b92457bfaa43c3ec68c754578243cb0e` | Removed the unverified ZIP blob. |
| Push 07:02:39 | 07:02:38 | `e0cddeacc7ea3ff17477708ec3470f71c8ee476b` | `0e6c47b26959019cafc6e11eb04e5f7e19a037dd` | Updated source files and README with final-newline and documentation corrections. |
| **Force-push 07:03:30** | 07:03:29 | `6f4b6975dd956ea3303653aa3ac8f7a27be31646` | `24e973fc8517d5467807446f915841896b65f8a4` | Replaced `e0cddeacc7ea3ff17477708ec3470f71c8ee476b` as branch tip. The new tip was recreated directly on the original base, not appended to the prior preservation chain. It contains the four source notes and vector script, but not the ZIP. |

The force-push transition reported by Claude was:

- **Before:** `e0cddeacc7ea3ff17477708ec3470f71c8ee476b`
- **After:** `6f4b6975dd956ea3303653aa3ac8f7a27be31646`
- **Activity event time:** `2026-11-28T07:03:30Z`

The commit timestamps are one second earlier than the corresponding Activity event times. They are separate fields and must not be conflated.

### Superseded ZIP discrepancy

The initial commit `a0f1ba90b92457bfaa43c3ec68c754578243cb0e` contained `LC518_C2_REPAIR_REVIEW_PACKET_2026-11-28.zip` as Git blob SHA-1 `b5998912ff9fcee8584ada76ebd370128ba8f6b2`, size **13,698 bytes**. The locally retained ZIP reported elsewhere in this packet is **13,701 bytes**, SHA-256 `4f2a16e624661417873d224982d015644916755cc9e90ae60d925502ad3b8c7f`. These are not byte-identical archives. The GitHub ZIP blob was removed in the second push; the current branch does not contain it. Do not describe the GitHub blob and local ZIP as the same verified file.

### Preservation limitation

The superseded commit identities, parent links, tree SHAs, and blob inventories are recorded in the companion `LC518_C2_PRESERVATION_HISTORY_DISCLOSURE_DRAFT_2026-11-28.md`. The full Git object bundle and the 13,698-byte ZIP blob have **not yet been saved to independent offline storage**. They should be fetched by full SHA and placed in a verified Git bundle before assuming the unreferenced GitHub objects will remain available. No force-push or repository rewrite is authorized to repair this history.

**Current status:** force-push disclosed in this proposed section; superseded objects inventoried; independent Git-bundle archival still outstanding; the proposed section has not yet been applied to the preservation branch README; no merge or production authorization implied.