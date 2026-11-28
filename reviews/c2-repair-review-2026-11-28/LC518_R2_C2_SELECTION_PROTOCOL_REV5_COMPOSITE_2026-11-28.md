# LC518 Rev11 C2 Replacement Selection Protocol: Consolidated Composite Candidate

**Status: REVIEW COMPOSITE. DRAFT. NOT ADOPTED. NOT LOCKED. NO DRAW AUTHORIZED.**
**Date:** 2026-11-28
**Historical predecessor:** LC518_R2_C2_SELECTION_PROTOCOL_v0.7_2026-11-27.md, preserved unchanged.
**Purpose:** prospective protocol for selecting two distinct mechanism pairs as extra C2 repetitions under frozen Rev11.
**Composite scope:** v0.7 sections 1-6 are retained with the historical-status correction below. Sections 7-8 are replaced in full. Sections 9-11 add the adoption, lock-validity, Activity-ledger, retrieval-status, and evidence-preservation rules.
**Owner workflow:** technical review first. Only after scoped Claude PASS on the exact canonical composite may the owner create one immutable OAC for the pre-existing registered experiment ID. One valid lock under that OAC authorizes one production selection. No separate per-draw preregistration or second draw authorization is required. This draft is not adoption or a lock.
**Canonical byte form:** UTF-8 without BOM, LF line endings, exactly one final LF. The SHA-256 is in an external sidecar, not embedded in this file.

## 1. Scope and current disposition

This v0.7 successor preserves the selection method and evidentiary scope reviewed in v0.6, while correcting the review-transfer location and recording the independent reproduction's platform. It does not adopt R2, establish original R2 C2 compliance, amend Rev11, construct parent sources, execute solvers, or publish a candidate allocation. The v0.6 draft remains unchanged as the prior review artifact.

The original R2 repeat-pair choice (M01/M08 and M02/M04) remains **NOT ESTABLISHED under C2** because synthetic formulation-screen outputs informed that selection. The stopped round `34323983` remains permanently excluded. No production beacon round has been queried and no production rank or pair has been calculated.

### 1.1 Historical authority correction

No authenticated v0.3 selection-protocol source file or formal v0.3 lock event has been established in the reviewed local materials. A project filename search found no `v0.3` file. The v0.5 statements calling v0.3 “locked” are withdrawn as unsupported; this successor does not invent a historical freeze or claim byte identity for an unavailable source.

The two-stage algorithm below is **owner-confirmed as of 2026-11-27** and is restated prospectively here. That confirmation establishes the intended algorithm, not a historical v0.3 lock. The v0.4 single-seed `R mod 378` mapping is superseded and is not used.

### 1.2 v0.5 corrections and review status

- v0.5 §1 incorrectly described v0.3 as locked despite acknowledging that its source identity was unauthenticated. This successor corrects that claim.
- v0.5 §1 also said the selection vectors were unavailable and not reproduced. The later v0.5 verifier and `run-evidence.json` do contain the fixed synthetic selection-conformance vectors and report them passing. This successor makes those vectors an explicit part of the selection specification.
- The v0.5 author-side run used Windows x64 with Node v24.17.0. Claude's independent reproduction used Linux with Node v24.22.1; both environments are recorded here to distinguish the runs and avoid treating their platform/runtime details as identical.
- The independent reproduction was performed in a disposable copy of the v0.5 evidence bundle: clean `npm ci`, `npm ls`, `node --check`, and the verifier completed successfully. The verifier reported 53 checks passing and 0 failing. Regenerated `run-evidence.json` matched the recorded evidence on every field except timestamps and runtime. This reproduces the v0.5 verification package; it does not mean that Claude executed a production selection.
- The v0.5 review-transfer ZIP is preserved on branch `review/lc518-c2-v05-transfer-2026-11-27`, distinct from `foued2-patch-6`, which carries the v0.6 transfer ZIP. Comparison with `master` shows that the v0.5 branch is one commit ahead, zero behind, and has exactly one added file: the ZIP. Therefore, the v0.5 ZIP is not on `master`; it remains unmerged and is not an adoption artifact. Its SHA-256 is `dde7fea941bcacd510900fae53a2d0a2f2c148cbc939db5e29e6123331a83be1`.
- Historical status correction: the earlier statement that v0.7 awaited a final narrow review is superseded by this consolidated composite review. Claude's review of Revision 4 returned NOT ADOPTABLE. This composite is the new exact review target; it remains unadopted and unlocked. The earlier v0.6 PASS remains limited to v0.6 and does not transfer to this composite.

## 2. Frozen C2 requirement and limits

Rev11 §4 requires all 28 unordered mechanism pairs to appear at least once, exactly two distinct pairs to receive one additional appearance each, and 30 assignments total. The repeated pairs must be preselected before construction and not derived from outcomes. The owner's C2 disposition treats synthetic formulation-screen outputs as outcomes when used to select extra representation. Therefore this protocol uses a mechanical selection procedure rather than the earlier outcome-informed pair choice.

The selection result identifies only the two pairs to repeat in a future candidate allocation. It does not itself validate the allocation, pass any G0/G1/A2/C6 gate, adopt R2, or authorize parent-source construction or solver evaluation.

## 3. Pinned beacon verification

Use `drand-client@1.4.2` with two separate native API v1 client instances, one for each relay origin. These are independent relay-origin checks of the same signed drand beacon, not independent randomness or entropy sources. Do not use a v2 adapter or a development-branch client.

Pinned Quicknet identity:

| Field | Required value |
|---|---|
| Beacon ID | `quicknet` |
| Chain hash | `52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971` |
| Public key | `83cf0f2896adee7eb8b5f01fcad3912212c437e0073e911fb90022d3e760183c8c4b450b6a0a6c3ac6a5776a2d1064510d1fec758c921cc22b0e17e63aaf4bcb5ed66304de9cf809bd274ca73bab4af5a6e9c76a4bc09e76eae8991ef5ece45a` |
| Scheme | `bls-unchained-g1-rfc9380` |
| Genesis time | `1692803367` |
| Period | `3` seconds |

For bounded historical conformance only, the fixed test round is round `1` at both origins:

- Relay A: `https://api.drand.sh/52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971`
- Relay B: `https://drand.cloudflare.com/52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971`

Each origin must use a separate `HttpCachingChain` and `HttpChainClient`, with native beacon verification enabled. Compare the raw `/info` response against all six pinned identity fields above before requesting the historical beacon. The historical test must record raw request URLs, HTTP status, response body, all expected/actual metadata checks, native verification result, decoded signature bytes, and locally derived `SHA-256(signature bytes)`.

The historical test passes only if both clients validate round 1, return the same decoded signature bytes, and yield the same locally derived seed. If a response supplies `randomness`, it must match the locally derived seed. Round 1 is a test vector only and must never be treated as a production draw.

## 4. Ordered validation and required negative cases

Validation is sequential; record the first failing stage and do not let a later failure conceal it:

1. `HTTP_AND_JSON`: successful HTTP status and valid JSON.
2. `CHAIN_IDENTITY`: beacon ID, chain hash, public key, scheme, genesis time, and period exactly match §3.
3. `ROUND_IDENTITY`: response round equals the fixed historical round for conformance or the protocol-derived production target round in §7.
4. `SIGNATURE_HEX`: signature is nonempty, even-length valid hexadecimal.
5. `SIGNATURE_FORMAT`: decoded signature has the pinned scheme's valid compressed format and 48-byte length.
6. `BLS_VERIFICATION`: the pinned native client verifies the signature against the pinned chain and correct round message.
7. `RANDOMNESS_CONSISTENCY`: derive SHA-256 from decoded signature bytes; if wire `randomness` is present, require valid 64-character hexadecimal and exact equality.
8. `RELAY_AGREEMENT`: after both relay responses independently pass stages 1–7, require identical round, signature bytes, and derived seed.

The mandatory injected negative cases must each record fixture identity, expected stage, actual first-failure stage, and pass/fail:

| Fixture | Required rejection stage |
|---|---|
| Non-2xx HTTP response or malformed JSON | `HTTP_AND_JSON` |
| Wrong chain hash, public key, scheme, genesis time, period, or beacon ID | `CHAIN_IDENTITY` |
| Wrong response round | `ROUND_IDENTITY` |
| Malformed hexadecimal signature | `SIGNATURE_HEX` |
| Decodable signature of invalid format or length | `SIGNATURE_FORMAT` |
| Tampered but correctly encoded signature with recomputed SHA-256 randomness | `BLS_VERIFICATION` |
| Valid signature with incorrect supplied v1 randomness | `RANDOMNESS_CONSISTENCY` |
| Selection digest at or above the rejection boundary | `SELECTION_REJECTION`, then retry the same label at the next counter |

Two distinct disagreement tests are required:

- **D1, workflow fault injection:** one relay supplies the valid historical beacon; the other supplies a different correctly encoded signature for the same round, with its randomness recomputed. Verify each response independently; an invalid alternate signature must fail at `BLS_VERIFICATION` and the workflow must abort.
- **D2, comparator unit test:** inject two explicitly fault-injected validation-result objects with the same round but differing signature bytes and derived seeds. The comparator must reject at `RELAY_AGREEMENT`. Do not claim that both injected objects are cryptographically valid signatures.

## 5. Exact pair universe and two-stage selection algorithm

### 5.1 Canonical universe

The universe is every unordered pair from `M01` through `M08`, each once, sorted lexicographically by the two identifiers (numeric identifier order, then second identifier). Serialize as ASCII `Mxx/Myy` lines separated by LF, including one final LF. It must contain exactly 28 lines and 224 bytes and have SHA-256:

`d5e54cd8a071fde1fd06a897b611fb9d39bfa28f5aeecb06e46537a2f93149bd`

If the length or hash differs, abort before deriving any pair index.

### 5.2 Seed and digest framing

For a production draw, `seed` is the 32-byte SHA-256 digest of the decoded, cryptographically verified signature bytes for the single production target round in §7. The synthetic test seed below is never a production seed.

For each draw, use the fixed ASCII domain labels `repeat-1` and `repeat-2`, and unsigned 64-bit big-endian counter starting at zero. The exact digest input is:

`ASCII("LC518-REV11-C2-v1") || 0x00 || seed[32] || 0x00 || ASCII(label) || 0x00 || uint64_BE(counter)`

Compute SHA-256 and interpret the 32 digest bytes as an unsigned big-endian integer `x`.

### 5.3 Rejection sampling and mapping

For a universe of size `n`, define:

`L = floor(2^256 / n) × n`.

For both `n = 28` and `n = 27`, `L = 2^256 − 16`. If `x >= L`, reject that digest, increment the same label's counter by exactly one, and recompute. If `x < L`, the zero-based index is `x mod n`. If a rejected digest occurs at counter `2^64 − 1`, abort; do not wrap the counter.

1. Apply label `repeat-1` to the full 28-pair universe; select the indexed pair.
2. Remove that selected pair from the ordered universe, retaining the relative order of every remaining pair. The second universe has exactly 27 pairs.
3. Apply label `repeat-2` to that reduced universe; select the indexed pair.
4. The two selected pairs are distinct by construction. Do not reroll, replace, or manually substitute either pair.

The labels are fixed algorithm constants and are therefore used in both the synthetic conformance fixture and production. The fixture seed, fixture digests, fixture indices, and fixture pair values are test-only; they must never be copied into a production result. A production result may coincidentally contain either fixture pair through the prescribed random mapping; that coincidence does not permit changing the result.

### 5.4 Fixed synthetic conformance vectors

These vectors are deterministic test data, not a drand seed or production selection. They test byte framing, integer interpretation, index mapping, and the reduced-universe rule.

Synthetic seed:

`000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f`

| Label | Counter | Universe size | Expected digest (hex) | Expected index | Test role |
|---|---:|---:|---|---:|---|
| `repeat-1` | 0 | 28 | `996627683d5bd28b1445281d42762ae3c0fafaca315c33deb096582a9970f659` | 5 | Normal first draw; maps to `M01/M07` |
| `repeat-1` | 1 | 28 | `c59aff206cf93ecd342e7b6a70af095a0e40ff1d3cfffe38e13b74ec70fd0ddb` | 23 | Counter-increment path only |
| `repeat-2` | 0 | 27 | `bce13a787bba4cf2849ecc7f9291e17459543545a9162f34b0f37a7256474881` | 19 | Normal second draw after removal; maps to `M04/M07` |
| `repeat-2` | 1 | 27 | `8f096ae539624f40ea1ad9a5bf6272e0673c0e85d33f48971d7719edb55f3561` | 13 | Counter-increment path only |

For the normal fixture, counter 0 is accepted for both labels; the resulting fixture pairs are `M01/M07` and `M04/M07`. The counter-1 rows are not used in that normal result. Exercise counter advancement by injecting `ff...fff0` at counter 0 (the first rejected 256-bit value for each `n`), then verifying that the same label advances to counter 1 and yields index 23 or 13 respectively. Do not claim that the fixture reached rejection with a real SHA-256 digest.

The v0.5 run evidence reports the pair-universe hash, all four digest/index vectors, both injected rejection paths, and the fixture pair mapping as passing. Claude's independent reproduction also passed these checks; see §6. These are test-only fixture results.

Before relying on any selection digest, the verifier must also pass these SHA-256 primitive regression vectors:

| Input bytes | Expected SHA-256 |
|---|---|
| Empty byte string | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| UTF-8 `abc` | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |
| UTF-8 `hello` | `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824` |
| UTF-8 `The quick brown fox jumps over the lazy dog` | `d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592` |

## 6. Pinned implementation, evidence, and independent review

The retained v0.5 verification artifacts are the exact inputs/evidence for this successor unless a reviewer identifies a necessary correction. Their reported SHA-256 identities are:

| Artifact | SHA-256 |
|---|---|
| v0.5 protocol | `3fe16b05d31f1f45fa32afa7a5dc6f888055cc8f5e7bd4407dbf91d19a1d7d57` |
| verifier `verify_drand_c2_v05.mjs` | `2483027442339db0cc5cdd246f160c24a38bf86ab57842a88c4b598b6304068f` |
| `package.json` | `52776a256bc14ab214603d0956ffd1604aad724fdf120ea5bea801309006d147` |
| `package-lock.json` | `e32581489563ea4fcacf8779164e1c4bc53dc4e24a5bbb309ff9fb25a913d827` |
| bundled `drand-client-1.4.2.tgz` | `81de34afba38520b461152bf032cfb5139bb6ced205bf9f50bc8216fdc394eef` |
| `run-evidence.json` | `de4083b0d62c05f0db3b154183a9b7c19484fdbb06cf8b013db6fb45fe72dc2a` |
| `RUN_OUTPUT.txt` | `c01b493285b4de82fe5aa1a61bab54168c0caea8bd90ff5ed9c57a09af701bf6` |
| `npm-metadata.json` | `c39a7bc2b282e6e513a50f5ce9a8e41d7cdfc4f5276d28a35acd69565c8aa5af` |
| v0.5 evidence `README.md` | `84ecee40d76c483f1a67e0a875079b7c4112666725759367cd7916d95bc21d28` |
| v0.5 review-transfer ZIP (branch `review/lc518-c2-v05-transfer-2026-11-27`; not on `master`; unmerged) | `dde7fea941bcacd510900fae53a2d0a2f2c148cbc939db5e29e6123331a83be1` |
| v0.6 review-transfer ZIP (branch `foued2-patch-6`; not on `master`; unmerged) | `2ab9e0dcbac19d44c8d60af045132cfdcd56d072559fbae11a70158f7c1ee79f` |
| predecessor v0.6 protocol (inside the v0.6 ZIP on `foued2-patch-6`) | `fde02cef7bd0da7339f79772f138ed126cf648e524c389c4bb20f6594f083cc3` |

The v0.5 review-transfer ZIP is on branch `review/lc518-c2-v05-transfer-2026-11-27`. The branch comparison against `master` reports one commit ahead, zero behind, and exactly one added file, the ZIP. It is therefore not on `master` and remains unmerged. The v0.6 review-transfer ZIP is on the distinct branch `foued2-patch-6`; its comparison against `master` likewise reports one commit ahead, zero behind, and exactly one added file, the v0.6 ZIP. Neither transfer branch modifies `master`.

The original author-side run used Windows x64 with Node v24.17.0; its `npm ci`, `npm ls`, `node --check`, and verifier were reported successful. Claude's independent reproduction used Linux with Node v24.22.1 in a disposable copy of the v0.5 evidence bundle. Its clean `npm ci`, `npm ls`, `node --check`, and verifier completed successfully; the verifier reported 53 checks passing and 0 failing. The regenerated `run-evidence.json` matched the recorded evidence on every field except timestamps and runtime. The platform and runtime difference is intentional to preserve the provenance of each run, not to imply identical environments.

Claude's technical PASS applies to v0.6 only. Revision 4 received NOT ADOPTABLE on 2026-11-28. This consolidated composite replaces v0.7 as the current review target. Claude must issue a fresh scoped verdict on the exact canonical composite SHA-256 defined in section 8.1. Earlier statements that a narrow v0.7 review was pending are historical only and have no operative effect. This does not imply owner adoption.

The v0.3 source and formal lock record remain unavailable and must not be fabricated. Any recovered copy is historical evidence only; it cannot retroactively change this successor's prospective authority or lock status.

## 7. Prospective target, retrieval, and one-selection rule

### 7.1 Target derivation and authorization

This composite is not draw authorization. Only after Claude issues scoped technical PASS on the exact canonical composite bytes and cited evidence may the owner adopt those bytes through the immutable OAC procedure in sections 8-9. Under the owner's 2026-11-27 process decision, one valid OAC and lock authorize exactly one production selection. No additional per-draw preregistration or second draw authorization is required. The draft, reviewer PASS, and verifier outputs do not themselves authorize a selection.

For pinned Quicknet, round r is scheduled at T_r = genesisTime + period × (r − 1). Let t_lock be the exact whole-second UTC timestamp of the first qualifying B-to-A lock-push Activity event, parsed under section 9.6. Set B_lock = 300 seconds, the policy margin described in section 9.8. The target is the smallest integer r at least 1 satisfying T_r > t_lock + B_lock. The comparison is strictly greater. A round exactly at the cutoff is excluded. No person may select a round after observing a beacon. Do not use round 1, stopped round 34323983, a synthetic fixture, a previously observed round, /latest, another chain, or a later round as the production target.

One valid lock fixes one target round and one selection. Failure to retrieve it during one operator's run does not void the lock, change the target, or make the OAC available again.

### 7.2 Two-relay retrieval and operator-run retries

Retrieve exactly the derived target round from both pinned relay origins. Apply all v0.7 identity, encoding, BLS, randomness-consistency, and relay-agreement checks independently to both responses. Both pinned relays must return the exact target round and pass all required checks before computing the seed or pair. The two-relay rule is unchanged; the single-valid-relay proposal remains separate and unadopted.

The operator's retry policy governs that operator's execution run only. Every permitted retry requests the same pinned chain and exact same target round. Retry classes, schedule, timeout, and terminal horizon may govern when that operator stops retrying, but they do not govern the study-level result and cannot forfeit or invalidate the selection.

The retry policy governs the operator's execution run only. Exhausting it leaves the status NOT_YET_COMPUTED; it neither selects nor forfeits a pair and creates no right to a second draw. Any party may later retrieve the same round from both pinned relays. The first complete, validated two-relay retrieval defines the outcome, and all such retrievals must be identical.

A response from only one relay is incomplete. A timeout, HTTP 403/429, transport error, malformed response, wrong round, invalid signature, or relay disagreement during one run is a run-level incomplete attempt. It does not constitute a completed pair selection or permanent non-assessability. Any party may later repeat the same-round two-relay retrieval. The first complete two-relay retrieval that passes all checks establishes the deterministic outcome. Every later independently completed retrieval must match its round, signature bytes, and derived seed exactly. A conflict between independently validated results is an evidence-integrity conflict, not permission to choose one result or another round.

No post-lock discretion may extend the target, substitute a relay identity, use a later round, alter labels or the universe, reroll a pair, or manually replace a result.

### 7.3 Study-level result states

Before a complete, validated two-relay retrieval exists, the study-level state remains NOT_YET_RETRIEVED or NOT_YET_COMPUTED. An operator may separately record RETRIEVAL_INCOMPLETE or RETRY_WINDOW_EXHAUSTED for an individual run. Those labels do not change the study-level state.

Once the first complete two-relay retrieval passes all checks, preserve the exact target responses, validation results, derived seed, deterministic indices, and selected pairs. That outcome is fixed and must be reproduced by later independent retrievals.

Permanent NOT ASSESSABLE is reserved for an evidence-determined condition in which required evidence is objectively unavailable, incomplete, inconsistent, or independently unverifiable after relevant recovery and provenance checks. An operator's timeout, rate limit, retry exhaustion, failure to run code, or failure to preserve its own attempt is not enough. A run-level failure remains retryable by another party against the same target round. A permanent status must identify the exact missing or conflicting evidence and why it cannot be recovered or independently validated.

A successful pair selection authorizes no R2 adoption, allocation acceptance, parent-source construction, solver construction/evaluation, Rev11 amendment, publication, or scientific claim. Those decisions remain separate.

## 8. Exact composite review, adoption, and change control

### 8.1 Canonical composite identity

The exact review target is reviews/c2-repair-review-2026-11-28/LC518_R2_C2_SELECTION_PROTOCOL_REV5_COMPOSITE_2026-11-28.md.

Canonical bytes are UTF-8 without BOM, LF line endings, and exactly one final LF. Its SHA-256 is recorded in a separate .sha256 sidecar with the filename. The digest is not embedded in the composite, avoiding self-reference. Any byte change creates a new digest and requires fresh review. Git blob SHA-1 is not a substitute for SHA-256.

### 8.2 Review sequence

1. Preserve v0.5, v0.6, v0.7, Revisions 2-5, all evidence, and all staged/unstaged/untracked work. Do not overwrite, clean, or silently repair historical material.
2. Claude reviews the exact canonical composite SHA-256, its complete text, verifier evidence, and cited limitations. The verdict must identify the digest reviewed and issue explicit scoped PASS or NOT PASS. PASS does not imply owner adoption.
3. Any edit after PASS creates a new digest and requires another review. Earlier verdicts do not transfer to changed bytes.
4. The owner may adopt only the exact bytes receiving scoped PASS. Adoption is recorded through the immutable OAC in section 9, not through prose alone or a commit timestamp misrepresented as lock time.
5. No OAC may be created until the exact pre-existing registry entry and experiment ID are identified and cited. Do not invent an ID or create parallel IDs to choose between candidate protocols.
6. One valid lock under the adopted OAC authorizes one target round and one selection under section 7. It authorizes no downstream construction, allocation acceptance, solver evaluation, or scientific claim.

### 8.3 OAC is the adoption record and fixes the base

The immutable OAC is the owner's adoption record for one registered experiment. It pins the exact canonical composite SHA-256 and path, registry ID, actor, one-attempt rule, and canonical lock ref. The OAC must be committed to master through a direct Activity event of type push, not a pr_merge or merge-queue event.

The SHA in that qualifying master push event's after field is both the OAC commit and lock base B. Its tree must contain the exact canonical composite bytes, SHA-256 sidecar, immutable OAC JSON, and pinned verifier/source artifacts. No later master tip is substituted for B.

The OAC push does not itself create a lock. The canonical lock ref must be created at B, followed by the first qualifying B-to-A push under section 9. A Claude PASS or OAC commit alone does not establish a lock or trigger a beacon retrieval.

### 8.4 No silent replacement

The current v0.7 file and historical Revisions 2, 3, and 4 remain unchanged. This composite is proposed operative text for a future owner adoption; it does not claim v0.7 was adopted or locked. No old v0.7 header, review note, timestamp rule, or further-draw sentence overrides the exact composite once adopted.

A correction before a valid lock requires a revised exact candidate and fresh review before its OAC. After a valid lock, later changes cannot void it or create a successor draw under the same C2 study-purpose chain; see section 9.

## 9. Owner Adoption Charter, lock validity, and Activity ledger

### 9.1 Registry identity and OAC path

Before any lock-ref event, an immutable Owner Adoption Charter (OAC) must exist as a publicly recorded commit on master. Its single canonical path is adoptions/LC518-R2-C2/<experiment_id>/OWNER_ADOPTION.json.

The experiment_id must be the exact pre-existing study-registry value and match [A-Z0-9][A-Z0-9._-]{0,63}. The OAC cites the registry source path and immutable commit that pre-register the root ID. The canonical C2 registry entry has not yet been identified in the reviewed materials. No OAC or experiment ID may be created now. Do not invent or select an ID.

The OAC fixes the study-purpose key LC518-R2-C2, one registry-issued experiment ID, exact composite path and SHA-256, one lock-ref path, base-commit rule, one attempt, one allowed actor's numeric GitHub user ID/login/type, verifier/source hashes, and root/successor status including predecessor details if applicable. The OAC is immutable and is never edited in place.

### 9.2 One root and one non-branching successor chain

The entire subtree adoptions/LC518-R2-C2/ represents one C2 study purpose. It contains exactly one root OAC with null predecessor fields, followed only by zero or more successors that each name exactly one immediate predecessor. No second root, sibling successor, parallel branch, alternative charter, or competing protocol variant is permitted. The complete set of OACs must form one directed path.

A successor is permitted only if the predecessor is conclusively NO_VALID_LOCK. That requires complete relevant Activity and immutable Git evidence showing that the one attempt was consumed or closed without ever forming a valid lock. An invalid first attempt may qualify after that state is independently established and recorded.

A successor is forbidden after any valid lock, whether or not the beacon was retrieved, whether the result later becomes NOT ASSESSABLE, and whether the ref is later deleted, rewritten, force-pushed, or recreated. It is also forbidden if predecessor evidence is incomplete and valid-lock presence cannot be determined. Unknown is not NO_VALID_LOCK.

A valid lock permanently ends the C2 successor chain. A later protocol-deviation study must be a distinct prospective study under a different study-purpose key, separately reviewed, and explicitly disclose the prior valid lock/outcome and deviation rationale. It cannot be called a C2 successor or replacement draw.

All disqualifying conditions in sections 9.1-9.4 are evaluated on the Activity-ledger prefix ending at the first qualifying B-to-A lock push and on immutable commit objects reachable from the OAC, B, and A. Any event, file, ref, or OAC first appearing after that push is a post-lock audit flag only. It cannot void the lock, alter valid-lock status, or enable a successor. This cutoff prevents a later sibling OAC/file addition from retroactively manufacturing NO_VALID_LOCK.

### 9.3 OAC publication, direct push, actor, and base

The OAC must be added to master by a direct Activity event with activity_type = "push" and ref = "refs/heads/master". A pr_merge or merge-queue event does not qualify. The event's after SHA identifies commit B, the OAC commit and lock base. Its tree contains the exact canonical composite bytes and sidecar, OAC JSON, and pinned verifier/source artifacts. No later master tip is substituted for B.

The allowed actor is pinned by numeric GitHub user ID 116307732, login snapshot foued2, and actor type User. Each relevant Activity actor object must expose and match these fields. A bot or other actor does not qualify. The fields were observed in the connected Activity reader's first 100 records, but raw response preservation remains required before adoption.

The OAC event must be the qualifying first publication of that immutable charter file at its canonical path. Preserve commit B, tree, OAC JSON bytes, protocol bytes, and pinned blobs. This rule does not rely on an unevidenced assertion that master is protected.

### 9.4 Canonical lock ref and one attempt

The one canonical ref is fixed in the OAC and derived from the registered experiment ID, not a protocol hash: refs/heads/lc518-r2-c2-lock/<experiment_id>.

No alternate ref qualifies. The exact ref must have no event before the OAC push. The complete repository-wide Activity ledger is scanned for the ref's entire lifetime and all events under the reserved OAC/lock namespaces.

The only qualifying lifecycle is:
1. OAC publication: direct push on refs/heads/master; after = B, the commit containing the canonical composite and OAC.
2. Ref creation: first event on the canonical lock ref is branch_creation, with before = "0000000000000000000000000000000000000000" and after = B.
3. Lock push: first subsequent event on the same ref is push, with before = B and after = A, where commit A has exactly one parent, B.

All three events use the pinned actor. No extra event may occur on the canonical ref between creation and the first lock push. The lock manifest at A pins OAC commit, study-purpose key, experiment ID, composite SHA-256, exact ref, base SHA B, actor ID/login/type, verifier/source hashes, schema version, and selection algorithm. It does not contain t_lock or target round, which derive from the Activity lock-push event.

The first event that creates or mutates the canonical ref after the OAC consumes the one attempt, valid or invalid. Wrong actor, before/after, parent, manifest/hash, intervening event, or missing proof consumes the attempt and cannot be repaired by another ref or push under that OAC. A successor is possible only under section 9.2 after complete evidence proves NO_VALID_LOCK.

### 9.5 Post-lock cutoff and tampering

All validity checks in sections 9.1-9.4 use only the complete ordered Activity-ledger prefix ending with the qualifying B-to-A push and immutable objects reachable from OAC, B, and A. Any later deletion, force-push, rewrite, same-name recreation, extra OAC, sibling charter, or file edit is recorded as POST-LOCK AUDIT BREACH; it cannot void the lock, move the target, forfeit the pair, or enable a successor.

If a third party reconstructs the adopted composite, OAC, lock event, commit A, manifest, target, both relay responses, cryptographic validation, seed, and pair calculation, the result remains reportable with the audit-breach flag and full chronology. If required evidence is genuinely irretrievable or contradictory so the result cannot be independently reconstructed, apply section 10.3. An operator-requested halt cannot suppress a reconstructable outcome.

### 9.6 Event ordering and timestamp grammar

Fetch the complete Activity ledger in ascending order with explicit time_period, direction, and per_page; preserve server response order. Require all numeric event IDs to be strictly increasing in response order and timestamps non-decreasing in that same order. If response order, ID order, and timestamp order disagree, fail closed for that retrieval run. IDs are a consistency check, not a substitute for response order or a claim about undocumented API guarantees.

Accept only this timestamp grammar: YYYY-MM-DDTHH:MM:SSZ. All 944 Activity records Claude reports observing used this whole-second UTC form. Reject offsets, fractional seconds, missing timezone markers, invalid calendar dates, and leap seconds. Parse calendar fields explicitly and convert to integer Unix seconds without floating-point rounding or local timezone interpretation.

The lock time t_lock is the whole-second UTC timestamp on the qualifying lock-push event. Equal timestamps elsewhere do not authorize reordering via commit dates. Ledger response order and strictly increasing event IDs must agree; timestamps may be equal but cannot decrease.

### 9.7 Activity history and evidence requirements

Before adoption, preserve the exact unauthenticated request URL/query and headers, response URL/status, raw body bytes, and all headers for every page. Preserve Date, Age, Cache-Control, ETag, Vary, Link, Content-Type, Retry-After, rate-limit headers, and X-GitHub-Api-Version-Selected. Preserve every next-page link and follow its exact cursor under HTTPS on api.github.com. Do not infer cursors or use a commit SHA as a cursor.

The repository-wide feed must cover the repository's entire relevant lifetime and every canonical-ref and reserved-namespace event before the lock cutoff. The repository was created at 2026-10-14T09:37:17Z; the first Activity record observed was 2026-10-14T09:37:43Z, 26 seconds later. Claude reports 944 records across ten pages through 2026-11-28T10:34:48Z, with strictly ascending IDs, non-decreasing timestamps, and no repeated seconds. Those ten pages have not yet been preserved as complete raw bodies and headers.

The connected GitHub Activity reader independently returned a parsed first page of 100 records, event ID 46450944076 at 2026-10-14T09:37:43Z through event ID 47789198475 at 2026-10-26T06:31:00Z. Its normalized projection is preserved at evidence/ACTIVITY_PAGE1_NORMALIZED_EXTRACT_2026-11-28.json, SHA-256 14fa57a6a80515bce494178bc35a2955e5cea5f86a23074e63c86ebd94fec1e2. It is parsed data, not raw wire bytes; it contains no response headers or Link header and does not prove full-history completeness.

Claude reports a SHA-256 of 5e79ffa8661a43ebf9db80c4129be72ac8197b60b2640db5f9c6c2ce5bbfbf6e for raw page 1. The underlying bytes are not preserved here, so that reported digest is not independently authenticated. API retention is undocumented. If full history or raw records cannot be preserved and reconciled, absence of earlier events is not proved and no valid lock may be asserted.

### 9.8 Policy buffer and target boundary

Set B_lock = 300 seconds. This is a policy margin, not a measured visibility percentile, documented maximum event-clock lag, or contractual GitHub clock-accuracy bound. The 20-push visibility study is unnecessary and remains NOT AUTHORIZED; it measures observation latency, not event timestamp accuracy.

For Quicknet, T_r = genesisTime + period × (r − 1). The target is the smallest integer r at least 1 satisfying T_r > t_lock + 300 seconds. Equality is excluded. The target is mechanically determined from the adopted composite, qualifying lock event, and pinned chain constants.

## 10. Evidence recovery, retrieval failures, and permanent status

### 10.1 Activity evidence run failures

A 403/429, rate-limit response, timeout, missing page, incomplete pagination, inaccessible response, or failed raw-body capture is a run-level ACTIVITY_CAPTURE_INCOMPLETE. Record request parameters, error/status, and time, then retry read-only retrieval when possible. It is not an empty feed, does not prove event absence, and does not by itself establish permanent NOT ASSESSABLE.

Do not assert a valid lock until the required complete pre-lock Activity prefix and raw evidence have been preserved and independently checked. An interrupted retrieval means not yet established, not proof that an event did or did not occur.

### 10.2 Drand retrieval run failures

A local timeout, HTTP 403/429, transport error, retry-horizon exhaustion, malformed response, or failure to run code is a run-level RETRIEVAL_INCOMPLETE or RETRY_WINDOW_EXHAUSTED. The study-level status remains NOT_YET_RETRIEVED or NOT_YET_COMPUTED. Any party may later retrieve the same target from both pinned relays. A later complete validated retrieval fixes the same deterministic outcome. No local run can forfeit the pair or authorize a second draw.

### 10.3 Permanent NOT ASSESSABLE

Permanent NOT ASSESSABLE is allowed only after independent review establishes a study-level evidence defect that cannot be remedied through the prescribed recovery path, such as an irretrievably unavailable immutable source or qualifying event, a permanently incomplete required ledger, or independently validated irreconcilable evidence. The status record must enumerate exact missing/conflicting objects, attempted recovery, independent checks, and why recovery is impossible.

An operator's individual timeout, rate limit, retry deadline, or failure to preserve their own execution is never sufficient. If recovery or another party's same-round retrieval remains possible, status remains not yet retrieved/computed. Permanent NOT ASSESSABLE never restores an attempt, changes the target, permits a replacement lock, or enables a successor after a valid lock.

### 10.4 Evidence retention and optional TSA seal

Preserve raw Activity requests/responses and headers, pagination links, matching Git objects, OAC bytes, lock manifest, canonical composite bytes and sidecar, validation reports, drand requests/responses, cryptographic validation results, derived seed, digest/counter trace, indices, pairs, and SHA-256 digests.

An RFC 3161 TSA token (DigiCert may be used) is optional additional preservation evidence for the SHA-256 hash of the canonical evidence manifest. It is not the source of t_lock, not a validity condition, not a replacement for the Activity API, and not proof that timestamped bytes were returned by GitHub. Failure to obtain a TSA token does not void an otherwise valid lock or authorize a replacement. If used, preserve manifest bytes, exact TSA request/response/token, nonce, message imprint, signer certificate, chain, policy, and validation output. Do not require token arrival before the target.

GitHub Activity API retention and immutability are not assumed. A contemporaneous raw capture is preservation evidence; later public re-query is corroboration. A local archive alone does not authenticate a historical TLS response. If a raw record is unavailable and the preserved source cannot be independently trusted or reconciled, apply section 10.3.

## 11. Current disposition and remaining blockers

- This is a review composite only. It is not adopted, locked, or authorized for a draw.
- v0.5, v0.6, v0.7, and Revisions 2-4 remain historical and unchanged.
- The exact pre-existing C2 registry entry and experiment ID remain unidentified. No OAC may be created until identified.
- Claude reports observing 944 Activity records across ten pages through 2026-11-28T10:34:48Z. Those observations are not preserved as complete raw page bytes and headers.
- A normalized parsed projection of the first 100 records is preserved separately. It is not a raw wire capture and does not close full-ledger evidence requirements.
- The raw page 1 digest reported by Claude is not independently authenticated here because the original bytes are not preserved.
- The actual pinned drand retrieval client has not been exercised through a local mock-conformance harness.
- The deterministic verifier is GPT-authored and models the digest/selection loop; it is not the pinned production client.
- The two-relay v0.7 rule remains unchanged. The single-relay proposal remains separate and unadopted.
- The 20-push visibility study remains NOT AUTHORIZED and is not required.
- No production round, seed, or pair has been selected.
- R2 C2 remains NOT ESTABLISHED.
- No solver construction or execution is authorized.

