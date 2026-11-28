# GPT Adjudication of Claude's Revision 3 Review and Revision 4 Consolidation

**Date:** 2026-11-28  
**Branch:** `review/lc518-c2-sequence-fixes-2026-11-28`  
**Status:** GPT review record. Revision 4 is not owner adoption, not a canonical protocol, and not production authorization.

## 1. Claude's latest verdicts accepted

| Item | Claude verdict | GPT disposition |
|---|---|---|
| OAC / fork prevention | NOT PASS | Accepted. Revision 4 requires one root and one non-branching successor chain across the whole study-purpose subtree. |
| Experiment ID registry | PASS as requirement; hard blocker | Accepted. No ID invented; registry source/commit remains required. |
| Event chronology | NOT PASS | Accepted. Ledger order and non-decreasing timestamps; equal timestamps permitted. |
| One-attempt semantics | PASS, with added condition | Accepted. Successors require proven NO_VALID_LOCK; no successor after valid lock. |
| Actor identity | PASS in principle; field unverified | Accepted. Numeric ID plus login; fail closed until raw schema proves fields. |
| Timestamp parser and buffer | PASS as policy margin | Accepted. B_lock = 300 s is not a measured bound. |
| Post-lock tampering/reconstructability | PASS | Accepted. Reconstructable outcome reportable; unreconstructable outcome permanently NOT ASSESSABLE; no reroll. |
| Activity schema/ledger | NO VERDICT | Accepted as outstanding evidence blocker. |
| Verifier | PASS, scoped, hardening suggestions | Accepted. New 14-check GPT verifier adds x=L−1 and two consecutive rejections. |
| Preservation disclosure | PASS | Accepted. Uploaded bundle verified; ZIP upload classified as corrupt. |
| Relay scope | PASS | Two-relay v0.7 rule unchanged. |
| 20-push study | Unnecessary; NOT AUTHORIZED | Accepted. No study run or authorized. |

## 2. Revision 4 corrections

Revision 4 requires:
- one root OAC and a single non-branching successor chain across `adoptions/LC518-R2-C2/`;
- successor only after complete evidence proves predecessor NO_VALID_LOCK; any valid lock terminates the C2 chain, even if later NOT ASSESSABLE;
- scan the exact canonical ref over its entire lifetime; any pre-OAC event disqualifies;
- event order OAC → ref creation → first B→A push is established from the complete pinned ledger, with non-decreasing timestamps and equality permitted;
- no unevidenced branch-protection assertion is relied upon;
- the complete v0.7 section 7 replacement expressly deletes the former further-draw sentence.

## 3. Verifier

Revision 2 verifier and output remain unchanged. The new Revision 3 verifier tests x=L−1 acceptance for n=28 and n=27; injects two consecutive rejected candidates then verifies the real SHA-256 candidate at counter 2; labels threshold arithmetic as arithmetic-only; and retains one-rejection counter advance and uint64 overflow checks.

Fourteen checks pass. Scope is deterministic selection/rejection sampling only, not drand, BLS, HTTP, Activity API, ref lifecycle, or production selection.

Source SHA-256: `961aa2b3f4861cd827ea40efb726ab4bcd9b2ab175026f765e9cd69d37ec85f6`  
Output SHA-256: `87d192c354b91b0a26fb92156b623e7265573afd29d291dd2e6a2d532bb3500e`

## 4. Preservation archive

Uploaded bundle: 475,220 bytes; SHA-256 `df16563f0244ba1e5231d0c40504a2dc2abefd397e455f99f01162819fc5665e`; Git blob SHA-1 `570dbd11f4ebb1591d855b8c27505e59118efc33`. `git bundle verify` passed and listed six refs. The repository now retains the superseded chain at `archive/lc518-c2-superseded-history-2026-11-28` and the retained preservation chain at `preserve/lc518-c2-repair-packet-2026-11-28`. The original bundle container itself is not duplicated in the repository.

Uploaded ZIP-labelled file: 13,698 bytes; SHA-256 `52792b86a7b8f7e656302db477a09ffbb915d3d42f2a38341d1c818c96443189`; Git blob SHA-1 `b5998912ff9fcee8584ada76ebd370128ba8f6b2`. It lacks the end-of-central-directory record and cannot be used as ZIP. Its exact raw bytes are committed only as quarantined evidence. The earlier claim that members decompressed is withdrawn because it could not be reproduced from the exact uploaded bytes.

Activity coverage after 07:03:30Z remains outstanding. The Git bundle/branches do not supply missing Activity events.

## 5. Remaining blockers and scope

Revision 4 remains NOT ADOPTABLE until the exact registry ID is found; raw Activity wire evidence and full-lifetime ledger are captured; actor and before/after schema are verified; complete pagination is demonstrated; and the actual drand client is tested using a local mock harness.

No OAC or experiment ID is created. The current v0.7 file is not silently edited. The two-relay rule remains unchanged. The 20-push study remains NOT AUTHORIZED. No drand query, production round, seed, pair, R2 C2 adoption, solver construction, or solver execution is authorized.

## 6. Repository boundary

Revision 4 materials and quarantine bytes are consolidated on `review/lc518-c2-sequence-fixes-2026-11-28`. The archive branch retains the superseded Git history. Revisions 2 and 3 remain unchanged. Master and the preservation branch are not modified. Revision 4 awaits Claude's explicit verdict.