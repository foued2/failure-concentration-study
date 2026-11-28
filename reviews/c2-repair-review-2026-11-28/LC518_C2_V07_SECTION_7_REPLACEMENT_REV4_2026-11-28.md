# Complete proposed replacement for LC518 C2 v0.7 section 7

**Status:** Review text only. This document does not modify or adopt v0.7.

## 7.1 Prospective target and one-selection authorization

This draft is not draw authorization. Only after Claude gives a scoped technical PASS on the exact final protocol and its evidence may the owner adopt it and create the one OAC authorized by the pre-existing registry. Under the owner's previously stated process decision, that adopted OAC and its one valid lock authorize exactly one production selection. A reviewer PASS or this draft does not itself authorize a selection.

For pinned Quicknet, round r is scheduled at T_r = genesisTime + period × (r − 1). Let t_lock be the exact, losslessly parsed UTC Activity timestamp of the first qualifying B → A lock-push event. Let B_lock = 300 seconds, the policy margin in §5. The target is the smallest integer r ≥ 1 satisfying T_r > t_lock + B_lock. The comparison is strictly greater; a round exactly at the cutoff is excluded. No person selects a round after seeing a beacon. Do not use round 1, stopped round 34323983, a fixture, or a previously observed round as the production target.

One valid lock fixes one target round and one selection attempt. It does not authorize a second round, replacement lock, seed, or pair. Never substitute /latest, a later round, another chain, or a manually selected round.

## 7.2 Two-relay retrieval and same-round retries only

Query exactly the derived target round from both pinned relay origins. Apply the full v0.7 identity, encoding, BLS, randomness-consistency, and relay-agreement checks independently to both responses. Both pinned relays must return the exact round and pass all prescribed checks before computing the seed or pair. The two-relay rule is unchanged; the single-valid-relay proposal remains separate and unadopted.

Every permitted transport retry requests the same pinned chain and exact same target round. Retry classes, schedule, timeout, and terminal horizon must be frozen before OAC/lock and tested against the actual client in separate local mock-conformance work. No post-lock discretion may extend the target, substitute a relay, use a later round, alter labels or universe, reroll a pair, or replace a result.

One valid relay is insufficient. A transport failure, invalid response, signature failure, or disagreement yields no pair selection unless the fixed same-round retry policy obtains two valid agreeing responses. Exhausting that policy does not authorize another draw. The lock and target remain unchanged.

## 7.3 Terminal statuses and no replacement draw

Before target retrieval and validation, report NOT_YET_RETRIEVED or NOT_YET_COMPUTED. These are work states, not failed draws.

If all evidence permits independent reconstruction of OAC, valid lock, target, both relay responses, cryptographic validation, seed, and calculation, report the result. If required evidence is genuinely incomplete, unavailable, inconsistent, or cannot be independently validated, report permanently NOT ASSESSABLE. Failed or interrupted retrieval never permits a replacement target or second lock.

**The following sentence in the current v0.7 section 7 is deleted and must not remain in the operative protocol:**

> A failed or interrupted draw does not yield a pair selection; a further draw requires a new owner adoption/lock event under an appropriately reviewed protocol version.

The replacement rule is: one valid lock fixes one target and one selection only. Failure or non-assessability never restores the attempt or authorizes a replacement draw. A C2 successor is possible only where the predecessor never formed a valid lock under §2.2, and is not a reroll of an existing valid lock.

Retain lock event, target, both relay requests/responses, validation results, seed, digest/counter path, indices, selected pairs if any, statuses, and hashes.

A successful pair selection authorizes no R2 adoption, allocation acceptance, parent-source construction, solver construction/evaluation, Rev11 amendment, publication, or scientific claim. Those decisions remain separate.