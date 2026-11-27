# LC518 Rev11 C2 Replacement Selection Protocol v0.7 — Draft

**Status: DRAFT. NOT ADOPTED. NOT LOCKED. THIS DRAFT AUTHORIZES NO DRAW.**  
**Date:** 2026-11-27  
**Supersedes for review:** `LC518_R2_C2_SELECTION_PROTOCOL_v0.6_2026-11-27.md` (SHA-256: `fde02cef7bd0da7339f79772f138ed126cf648e524c389c4bb20f6594f083cc3`), contained at the repository root inside `LC518_C2_V06_REVIEW_TRANSFER_2026-11-27.zip` on branch `foued2-patch-6`.  
**Purpose:** prospective protocol for selecting two distinct mechanism pairs as the extra C2 repetitions under frozen Rev11.  
**Owner workflow disposition:** technical review first; owner adoption and a prospective lock only after a scoped Claude PASS. A separate per-draw preregistration and separate draw authorization are not required under the owner's 2026-11-27 decision. This draft is not that adoption or lock.

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
- Claude's scoped technical PASS applies to v0.6 as a review draft, not to this v0.7 successor. This v0.7 corrects the documentary conditions identified in that review and is submitted for a final narrow review; it remains unadopted and unlocked.

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

Claude's technical PASS applies to v0.6 as a review draft, not to v0.7. This v0.7 is submitted for a final narrow review of the corrected transfer-location statement, the two-platform record, and consistency with the previously reviewed evidence. The review should identify its scope and issue an explicit `PASS` or `NOT PASS`; it does not imply owner adoption.

The v0.3 source and formal lock record remain unavailable and must not be fabricated. Any recovered copy is historical evidence only; it cannot retroactively change this successor's prospective authority or lock status.

## 7. Prospective production target and draw authorization

This draft is not a draw authorization. The owner has directed that a separate per-draw preregistration and separate draw authorization are not required. To make the target non-discretionary without a separate preregistration, the adopted protocol will derive it mechanically from the exact UTC timestamp of its prospective lock:

- For the pinned Quicknet schedule, round `r` is scheduled at `genesisTime + period × (r − 1)` seconds.
- Let `t_lock` be the exact UTC Unix-second timestamp recorded in the owner adoption/lock event. The production target is the smallest integer `r ≥ 1` for which `genesisTime + period × (r − 1) > t_lock`.
- The lock event therefore precommits the first scheduled round strictly after the lock time. No person selects a round after seeing a beacon. Do not use round 1, stopped round `34323983`, any synthetic fixture, or a previously observed round as the production target.

Only after Claude gives a scoped technical PASS on this exact v0.7 text and its cited evidence may the owner adopt and lock the final exact text. The owner adoption/lock record must name the final protocol SHA-256 and record a whole-second UTC lock timestamp from a trusted clock. The lock event must be recorded before the derived target round's scheduled time. Under the owner's stated process decision, that adoption/lock itself authorizes **one** production selection using the target-round rule above; no additional per-draw preregistration or authorization is required. The current draft, any reviewer PASS, and any prior v0.5 evidence do not themselves authorize it.

For the authorized production selection, query exactly the derived target round from both pinned relay origins. Apply the full validation order in §4 and require relay agreement before deriving the seed. Any verification failure or relay disagreement aborts this draw; never substitute another round, change labels, alter the universe, reroll a selected pair, or manually replace a result. Retain the lock event, derived target round, full request/response evidence, validation results, seed, digest/counter path, indices, selected pairs, and hashes. A failed or interrupted draw does not yield a pair selection; a further draw requires a new owner adoption/lock event under an appropriately reviewed protocol version.

A successful pair selection authorizes no R2 adoption, allocation acceptance, parent-source construction, solver construction/evaluation, Rev11 amendment, publication, or scientific claim. Those decisions remain separate.

## 8. Required review sequence and decision record

1. Preserve v0.5, v0.6, and all existing staged, unstaged, and untracked work; do not overwrite or clean them.
2. Review this exact v0.7 draft and its cited evidence, focusing on the two documentary corrections and the consistency of the revised status statements. The independent v0.5 verifier reproduction is recorded in §6; do not rerun it absent a specific review-identified issue.
3. Claude issues an explicit scoped `PASS` or `NOT PASS` on this exact v0.7 text, transfer identity/location, consistency with the reviewed evidence, and remaining limitations. That technical verdict does not imply owner adoption.
4. After a scoped `PASS`, the owner decides whether to adopt. Adoption must be an explicit dated record naming the exact final protocol SHA-256, reviewer verdict, and whole-second UTC lock timestamp from a trusted clock. Until that separate owner action, v0.7 remains a draft and no production draw is authorized.
5. If adopted and locked, the lock itself authorizes only the one production selection defined in §7. It does not authorize any downstream construction or experiment.

**Current disposition:** v0.7 is a review draft; v0.3 historical lock is unverified; prospective algorithm is owner-confirmed but not adopted; Claude's independent v0.5 reproduction passed as reported above; final narrow review of v0.7 is pending; original R2 C2 remains NOT ESTABLISHED; no production draw, pair selection, candidate adoption, construction, or solver execution has occurred or is authorized by this draft.