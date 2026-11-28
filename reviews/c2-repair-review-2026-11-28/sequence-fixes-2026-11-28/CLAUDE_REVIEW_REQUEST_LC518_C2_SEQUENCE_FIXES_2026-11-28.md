# Claude Review Request: LC518 C2 Sequence Fixes

**Review date:** 2026-11-28  
**Repository inspected:** `foued2/failure-concentration-study`  
**Master at inspection:** `ccbd0bdefd2d02ec22f6e17f27e9d0074952605a`  
**Preservation branch:** `preserve/lc518-c2-repair-packet-2026-11-28`  
**Current preservation tip:** `6f4b6975dd956ea3303653aa3ac8f7a27be31646`  
**Review branch:** `review/lc518-c2-sequence-fixes-2026-11-28`  
**Request:** Review the exact draft files on the dedicated branch. This branch is a review submission only. Do not infer protocol adoption or production authorization.

## Files for review

1. `LC518_C2_V07_LOCK_VALIDITY_AMENDMENT_DRAFT_2026-11-28.md`
2. `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_REVISION_2026-11-28.md`
3. `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_REVISION_2026-11-28.md`
4. `LC518_C2_PRESERVATION_README_SECTION_DRAFT_2026-11-28.md`
5. `LC518_C2_PRESERVATION_HISTORY_DISCLOSURE_DRAFT_2026-11-28.md`

## Required verdicts

Issue a separate explicit `PASS` or `NOT PASS` for:

- the proposed replacement for v0.7 §7 and the current line-191 paragraph;
- the revised historical hash addendum;
- the revised timing-evidence clarification;
- the README force-push disclosure and preservation-history inventory.

For each `NOT PASS`, identify the exact sentence/rule, why it fails, and a replacement. A scoped PASS is technical review only. It does not authorize merging, adopting a new protocol hash, creating a lock ref, executing a draw, or running any lab pushes.

## Priority technical questions

1. **Target time:** Is the server-assigned Activity event-time field, parsed from the pinned raw live response, an acceptable primary time for `T_target = first T_r > t_event + 300 s`, while explicitly not claiming it is the exact HTTP receipt instant?
2. **Schema:** The prior review reports `timestamp`, `activity_type`, and `actor`, while GitHub's current documentation example shows `pushed_at`, `push_type`, and `pusher`. The raw wire response was not included in the packet. Is the proposed fail-closed raw-schema qualification sufficient, or must a raw response be captured before this design can be reviewed at all?
3. **Slot/retry semantics:** Is one canonical ref and one attempt per slot sufficiently resistant to re-roll? This draft intentionally does **not** permit automatic replacement after a pre-target invalid candidate. If you believe pre-target replacement should be allowed, specify an independently auditable pre-target invalidation record, deterministic attempt sequence, and rule proving the invalidation was public before the prior target. Do not simply assume the operator discovered the defect before the target.
4. **Post-lock tampering:** Are deletion, force-push, rewrite, recreation, extra push, loss of lifecycle history, or mismatch correctly treated as `FORFEIT / HALT` or `NOT ASSESSABLE / HALT`, never as a void that permits a new draw?
5. **TSA:** Is DigiCert RFC 3161 an adequate independent timestamp witness for the evidence-manifest hash? Check the actual policy, `accuracy`/uncertainty bound, nonce, message imprint, signer certificate, certificate chain, revocation, and long-term validation requirements. Confirm that the draft does not overclaim that the TSA authenticates the historical GitHub TLS response.
6. **Buffer:** Is `b = 300 seconds` defensible as a proposed fixed workflow margin, without calling it an experimentally measured visibility bound? If not, state a defensible alternative or require a separate measurement.
7. **No-second-lock proof:** Is the requirement to capture the complete repository-wide Activity feed, inspect all pages, and inspect commit manifests for the same `slot_id` enough to establish no competing lock? If not, specify what is missing. If the API cannot establish full coverage, the condition must fail closed.
8. **Retention:** Is `NOT ASSESSABLE / HALT` the correct disposition if GitHub no longer supplies the full lifecycle or if the captured bundle and live response differ? Do not describe Activity as immutable or permanently retained.
9. **20 trials:** Confirm whether the former 20-trial visibility study is unnecessary for the revised rule. It remains not authorized. Identify any smaller conformance tests that are essential and do not require unauthorized remote pushes.
10. **Scope discipline:** Confirm the draft leaves the pair-selection mathematics, Quicknet identity, two-relay requirement, and solver allocation unchanged. Any proposed cryptographic/relay change must be a separate amendment.

## Evidence boundary

The following are still open and must not be described as completed:

- raw Activity API request/response body and headers for the lock event;
- exact request URL/query and full unauthenticated read-back capture;
- pinned live response schema and pagination conformance;
- an actual DigiCert RFC 3161 request/token verification run;
- an independent offline Git object bundle for the superseded preservation commits and the 13,698-byte GitHub ZIP blob.

The local ZIP is a separate delivery artifact and is not committed to this review branch. The original local repair packet was 13,701 bytes with SHA-256 `4f2a16e624661417873d224982d015644916755cc9e90ae60d925502ad3b8c7f`. The GitHub ZIP blob in the initial preservation commit is a distinct 13,698-byte object with Git blob SHA-1 `b5998912ff9fcee8584ada76ebd370128ba8f6b2`. The two must not be conflated.

## Current governance state

- The six draft Markdown files are preserved individually on `review/lc518-c2-sequence-fixes-2026-11-28`, based on preservation tip `6f4b6975dd956ea3303653aa3ac8f7a27be31646`. The convenience ZIP is a separate local delivery artifact, not a GitHub binary.
- This review branch is not merged to `master`; the preservation branch itself is unchanged.
- No historical v0.7 file or lock record has been modified.
- No GitHub settings, issues, or pull requests have been changed.
- The original attempted lock remains VOID FOR PRODUCTION USE.
- No production round, seed, or pair has been selected.
- The 20-trial run remains NOT AUTHORIZED.
