# GPT Adjudication of Claude's 2026-11-28 Review and Revision 3

**Date:** 2026-11-28  
**Review branch:** `review/lc518-c2-sequence-fixes-2026-11-28`  
**Preservation tip verified:** `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`  
**Master verified:** `ccbd0bdefd2d02ec22f6e17f27e9d0074952605a`  
**Status:** GPT adjudication and review draft. Not owner adoption, not a canonical protocol, and not production authorization.

## 1. Adjudication of Claude's verdicts

I accept Claude's verdicts:

| Artifact | Claude verdict | GPT adjudication |
|---|---|---|
| Revised historical hash addendum | PASS | Accept; retain the exact quotation and current repository-status qualification. |
| Revised timing clarification | PASS | Accept; retain event time as a separate Activity field, not exact HTTP receipt or first visibility. |
| Force-push disclosure/README section | PASS with three text fixes | Accept the fixes and issue the Revision 2 history note. |
| Revision 2 lock design | PASS on direction; NOT PASS as adoptable text | Accept. Revision 3 addresses the three blockers. |
| Earlier GPT TSA/300-second amendment | NOT PASS, superseded | Accept; keep as an audit alternative only. |
| Revision 2 verifier source | No verdict; absent | Corrected by committing GPT's separately authored verifier and its own raw output. |

Claude's read-only report also corrects an important preservation-history detail: the current preservation branch tip is `4ab5ce1...`, a normal commit after `6f4b697...`, and the three commits superseded by the earlier force-push are `a0f1ba9...`, `0e6c47b...`, and `e0cddea...`. GPT independently retrieved and checked the `0e6c47b...` commit object, parent, tree, and tree inventory.

## 2. Revision 3 architecture

Revision 3 now adopts the following candidate structure.

### 2.1 One prior charter prevents protocol-hash forks

A protocol hash cannot be the only lock identity. The earlier design allowed an operator to produce multiple protocol variants, each with a different hash-derived ref.

The replacement requires one **Owner Adoption Charter (OAC)** to be committed on protected `master` before the lock attempt. The OAC fixes:
- one pre-registered `experiment_id`;
- one exact protocol SHA-256;
- one canonical lock-ref path;
- one exact base rule;
- one attempt;
- one authorized actor's stable numeric GitHub ID and login snapshot;
- the verifier/source hashes and selection identifier.

The canonical ref is derived from the pre-existing experiment ID, not from the protocol hash. The OAC's exact commit and its master Activity push event must precede the lock-ref creation event. Later or alternative protocol hashes under the same ID cannot replace the first OAC.

**Critical discovery:** GPT searched the current master tree and code index. No `experiment_id` occurrence, experiment-registry path, or canonical C2 experiment ID was found. The actual ID therefore remains unresolved. The draft correctly does not make one up. It is a hard adoption blocker until the prior study registry identifies it.

The owner repository identity currently resolves to numeric GitHub user ID `116307732`, login `foued2`. This is a grounded candidate for the OAC actor pin; the Activity response must still expose a stable actor ID and match it. The login is frozen as a snapshot and checked alongside the stable ID.

### 2.2 One attempt; no quiet replacement

The first event that creates or mutates the one canonical lock ref consumes the OAC's attempt, whether it forms a valid lock or not. A pre-existing ref, wrong actor, wrong `before/after`, extra event, wrong parent, wrong manifest, or schema ambiguity cannot be repaired by choosing another ref.

A new attempt is a new, separately registered successor experiment with a new pre-registered sequential ID, a public predecessor-disposition record, and a new OAC. It is not a replacement result or a correction under the same authorization. An earlier reconstructable result remains reportable.

This is the missing written rule from the Revision 2 text, now included in Revision 3.

### 2.3 Post-lock tampering cannot censor the result

The first qualifying `B → A` push remains the binding lock. Later deletion, force-push, rewrite, recreation, or additional pushes are audit violations, not voids.

- If the original lock, target round, and public beacon can be reconstructed, report the deterministic selection with a separate post-lock audit-breach flag.
- If required evidence is genuinely unavailable or inconsistent, mark the result permanently `NOT ASSESSABLE`.
- In neither case is a new lock or replacement draw allowed.
- Non-retrieval remains `NOT_YET_RETRIEVED` or `NOT_YET_COMPUTED`; it is not a failed draw.
- An operator or reviewer cannot request a halt after learning the result to suppress it.

This replaces the earlier draft's unsuitable `FORFEIT / HALT` wording.

## 3. Event order, actor, and target parser

The exact event order in Revision 3 is:

1. OAC push to protected `master`, with its `after` identifying the charter commit.
2. Branch creation on the one canonical ref, `before = 0`, `after = B`.
3. First push on that ref, `before = B`, `after = A`, with `A` having exactly one parent `B`.

The Activity timestamps must satisfy strictly `t_OAC < t_create < t_lock`. The actual live response must establish the wire representation of `before = 0`, actor ID/login, and event type. If the API does not expose those fields unambiguously, this lifecycle cannot be adopted without a revised design.

Revision 3 defines an RFC 3339 parser with timezone required, full fractional precision preserved, exact UTC normalization, no floating point, rejection of malformed timestamps, and a strict target rule. If the scheduled round equals the cutoff, it is not eligible; the target is the first round strictly later.

I accept Claude's recommendation to freeze `B_lock = 300 seconds` as a **policy margin**, not a measured or guaranteed maximum clock error. The 20-push visibility experiment does not measure Activity timestamp accuracy or maximum server-clock lag. Revision 3 states the trust assumption and limitation. If the study requires a formally bounded server-clock error, the API is not yet adequate as the sole time source.

## 4. TSA and relay decisions

DigiCert RFC 3161 remains an optional seal of the evidence-manifest hash only. It is not the lock clock, not a validity gate, and not evidence authenticating a historical GitHub TLS response. A missing token cannot void a qualifying lock. GPT does not require a TSA token to arrive before the target.

The two-relay v0.7 rule remains unchanged. The proposed single-valid-relay design remains separate and unadopted; it requires independent cryptographic review.

## 5. Verifier source and raw output

Claude could not review the Revision 2 verifier because its source was absent from the Git tree. GPT has committed a separately authored standard-library verifier at:

- `sequence-fixes-2026-11-28/verify_lc518_c2_v07_vectors_REV2.py`
- `sequence-fixes-2026-11-28/VERIFY_LC518_C2_V07_VECTORS_REV2_OUTPUT_2026-11-28.txt`

It runs ten checks:
1. pair-universe count, byte length, and SHA-256;
2–5. the four published deterministic vectors;
6. normal two-stage mapping to `M01/M07` and `M04/M07`;
7. rejection boundary for both (n=28) and (n=27);
8–9. actual rejection and same-label counter advancement for both labels, where the injected rejected integer at counter 0 is followed by the real SHA-256 digest at counter 1;
10. uint64 counter overflow.

The rejected integer is explicitly a test harness value, not claimed to be a real SHA-256 digest. The verifier does not query drand, validate BLS, test the HTTP client, create refs, or perform a production selection. Its ten-check output was captured from the locally run implementation and committed. It is GPT's source/output and is not claimed to be the missing script from the earlier session ZIP or Claude's reported earlier run.

## 6. Preservation-history corrections

Claude's three documentary fixes are implemented in the Revision 2 history note:

1. Current preservation tip is `4ab5ce1...`, not `6f4b697...`.
2. Exactly three commits were superseded by the force-push: `a0f1ba9...`, `0e6c47b...`, and `e0cddea...`. The base `24e973f...` and the retained force-pushed tip `6f4b697...` are not counted as superseded.
3. Activity coverage after the 07:03:30Z force-push is outstanding because Claude's later read attempts received HTTP 403. The 07:54:01Z timestamp for the normal Revision 2 commit is Git metadata, not an Activity event timestamp.

GPT independently verified the `0e6c47b...` Git object and tree, correcting Claude's statement that it was not checked. The independent Git bundle and extraction/hash of the 13,698-byte GitHub ZIP blob are still outstanding.

The Revision 2 packet's §10 artifact names are now mapped to the actual review-branch file paths in `README_REV3.md`.

## 7. Remaining freeze blockers

Revision 3 is not adoptable yet. The following evidence or owner-defined values remain outstanding:

- the exact pre-existing canonical `experiment_id`;
- an immutable OAC on protected `master` fixing that ID and one protocol hash;
- raw unauthenticated Activity body/headers and exact selected-version behavior;
- actor numeric ID, branch-creation `before=0` representation, and full lifecycle event order;
- complete repository-wide pagination without rate limiting or missing pages;
- timestamp semantics and acceptance of the five-minute policy margin;
- exact parser conformance and strict equality boundary tests;
- local mock-harness results for the same-round two-relay retry/halt behavior;
- later read-only Activity coverage of the preservation branch after 07:03:30Z;
- independent offline Git bundle and actual extraction/hash of the 13,698-byte GitHub ZIP blob.

The former 20-push visibility study remains **NOT AUTHORIZED** and is not required by this design. The buffer is not justified by that experiment.

## 8. GPT decision

I accept Claude's first-review corrections and prefer Revision 3's OAC + one experiment ID + one canonical ref + one consumed attempt + reconstructability design.

I do **not** declare it PASS or adoptable. The actual experiment ID and raw Activity evidence remain missing. Claude must review the exact Revision 3 text and committed verifier source/output. No merge to `master`, owner adoption charter, lock ref, production round, seed, pair, solver construction, or solver execution is authorized by this adjudication.
