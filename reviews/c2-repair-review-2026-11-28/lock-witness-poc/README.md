# LC518 single-use lock witness proof of concept

Local proof of concept only. It does not contact GitHub, configure rulesets, create an OAC, query drand, or authorize a selection.

## Components

- `witness.py`: fixed policy binding, exact request schema, external checkpoint acceptance verification, local mirror recovery, and constrained state transitions.
- `github_adapter.py`: explicit adapter boundary, fake ref implementation, reconciliation logic, and webhook delivery simulator.
- `test_witness.py`: adversarial unit tests. All GitHub and custodian behavior is modeled locally.

The caller cannot supply a scope. The witness policy pins a canonical purpose key, experiment ID, and registry digest. The test uses `TEST-ONLY-REGISTRY-ID`; it is not an LC518 registry value. Unknown request fields and aliases are rejected. Authentication/authorization is not implemented; a production endpoint must enforce caller identity and separately authorized server-side policy changes.

`CheckpointStore` is a separate SQLite database model with a unique purpose claim, append-only event triggers, a hash chain, HMAC signatures, and claim/event consistency checks. `Witness.intent()` verifies that checkpoint and the local mirror before accepting. Corrupt, missing, stale, or rolled-back anchor state fails closed; a local mirror behind a valid anchor can recover from the anchored log. The HMAC key and both databases are accessible in the test process, so this is not independent operational custody or production-grade immutability.

States: `UNCLAIMED → INTENT_RECORDED → GITHUB_APPLIED`; an ambiguous result moves through `PENDING_RECONCILIATION`; unexpected ref history/state moves to terminal `BREACH`. No transition permits replacement or returns to `UNCLAIMED`.

The fake GitHub adapter models create-at-B, update B-to-A, lost responses, deletion, same-name recreation, force updates, and policy denial. Its event journal is assumed complete. This does not prove GitHub rulesets block admins or that production audit evidence is complete. The webhook simulator explicitly delivers duplicates, missing events, and out-of-order events; webhook order is not used by the reconciler.

Run from this directory: `py -3 -m unittest discover -s . -p 'test*.py' -v`.

The report describes the assumptions, test results, and the unresolved historical cutover. Witness activation cannot reset the existing C2 attempt.
