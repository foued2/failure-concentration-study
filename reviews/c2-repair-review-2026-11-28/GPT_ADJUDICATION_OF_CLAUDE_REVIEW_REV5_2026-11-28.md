# GPT Adjudication of Claude Revision 4 Review and Revision 5 Composite

**Date:** 2026-11-28  
**Branch:** review/lc518-c2-sequence-fixes-2026-11-28  
**Canonical composite SHA-256:** 8b5c670edc853acb15dab045f174153cc7253efa55d342b48e8184eab59815ea  
**Status:** GPT change record. Not owner adoption, not protocol lock, and not draw authorization.

## 1. Claude Revision 4 findings accepted

Claude found Revision 4 NOT ADOPTABLE because (a) post-lock sibling OACs could be used to disqualify a lock retroactively and make a successor eligible; (b) §7.2 could let operator retry exhaustion be treated as a failed draw, contradicting §6.3; and (c) the map omitted old v0.7 §8 and stale status statements. GPT accepts all three findings.

## 2. Corrections in the composite

1. **Post-lock cutoff:** all validity checks in §§9.1-9.4 are evaluated on the Activity-ledger prefix ending at the first qualifying B-to-A push and immutable Git objects reachable from OAC/B/A. Post-lock events are audit flags only and cannot void valid-lock status or enable a successor.
2. **OAC base:** B is the OAC commit itself, identified by the after field of a direct master push event. That commit tree contains the exact canonical composite bytes and sidecar.
3. **Direct push:** OAC publication requires Activity type push on refs/heads/master; pr_merge and merge-queue events do not qualify.
4. **Actor:** numeric ID 116307732, login foued2, type User; each relevant raw actor object must match.
5. **Event order:** preserve response order; require numeric event IDs strictly increasing in that order and timestamps non-decreasing. IDs are a consistency check, not an inferred API guarantee.
6. **Timestamp grammar:** accept only YYYY-MM-DDTHH:MM:SSZ; reject fractions, offsets, invalid dates, and leap seconds.
7. **Operator retries:** retry policy governs an execution run only. Exhaustion leaves NOT_YET_COMPUTED; any party may later retrieve the same target round. First complete validated two-relay retrieval defines the outcome; subsequent complete retrievals must be identical.
8. **Permanent status:** timeouts, rate limits, retry exhaustion, or failure to run code are not permanent NOT ASSESSABLE. That status requires an irrecoverable, independently reviewed evidence defect.
9. **Full replacement map:** the composite replaces v0.7 §§7-8 in full, including removal of the former §8 trusted-clock timestamp adoption rule. It updates header/workflow and stale §1.2/§6 review statements and replaces the old disposition.
10. **Canonical hash:** the exact composite digest is external in a sidecar to avoid self-reference.

## 3. Activity evidence

GPT independently retrieved one parsed page of 100 Activity records. It confirms the first observed master branch-creation event at 2026-10-14T09:37:43Z, zero-string before value, and actor id/login/type. The normalized projection is committed with SHA-256 14fa57a6a80515bce494178bc35a2955e5cea5f86a23074e63c86ebd94fec1e2.

This is not the raw response. It has no response headers, status line, Link header, or pagination cursor. Claude's report of 944 records across ten pages and the raw page 1 digest are recorded as reported observations, not as independently authenticated preserved raw bytes. The remaining pages and raw headers remain hard blockers.

## 4. Verifier and preservation

The hardened Revision 3 verifier remains GPT-authored, 14 checks, deterministic model only. It does not test the pinned production drand client, BLS, HTTP retrieval, Activity evidence, OAC, or production selection.

The preservation Git lineage remains reachable through the archive and preservation branches. The original bundle container is not duplicated in the repository. The ZIP-labelled file is quarantined as corrupt raw evidence.

## 5. Remaining blockers and authorization

- canonical C2 experiment ID and registry entry still unidentified;
- raw Activity pages/headers and full 944-record ledger not preserved;
- API retention undocumented;
- actual pinned drand client local mock-conformance test outstanding;
- fresh Claude verdict on the exact Revision 5 composite outstanding.

No OAC or lock is created. No drand query, production round, seed, pair, R2 adoption, solver construction, or solver execution is authorized. The 20-push study remains NOT AUTHORIZED. The two-relay requirement remains unchanged.
