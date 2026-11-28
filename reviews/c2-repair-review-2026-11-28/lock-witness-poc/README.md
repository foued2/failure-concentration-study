# LC518 single-use lock witness proof of concept

Local proof of concept only. It does not contact GitHub, configure rulesets, create an OAC, query drand, or authorize a selection.

## Components

- `trust.py`: signed policy manifest, one-time initialization authorization, append-only external checkpoint file model, and role-specific receipt signatures.
- `witness.py`: fixed policy binding, exact request schema, SQLite checkpoint mirror, acceptance verification, and signed-evidence state transitions.
- `github_adapter.py`: adapter boundary, fake ref implementation, reconciliation logic, and webhook delivery simulator.
- `test_witness.py`: adversarial tests. GitHub and signer behavior is modeled locally.

The signed policy pins the canonical purpose key, experiment ID, registry digest, custodian identity, repository, ref, and App ID. The test ID is `TEST-ONLY-REGISTRY-ID`, not an LC518 registry value. The caller supplies no scope; aliases and unknown request fields are rejected. Replacing the witness policy after construction is rejected. A policy authority can issue changed manifests, so that authority remains a trusted boundary; the checkpoint genesis binds the custodian to one manifest digest.

Checkpoint genesis is created only through an explicit one-time initialization authorization. The policy-authority model records issuance/consumption in its own signed append-only log. A new/empty SQLite checkpoint database or external checkpoint file is not implicitly treated as a valid start. The append-only JSONL checkpoint model is outside both SQLite mirrors, is signed, pins custodian ID and manifest digest, and advances by compare-and-append. Acceptance verifies it against the SQLite checkpoint database and witness mirror. Tests reset both SQLite databases and roll back/corrupt the external checkpoint; all fail closed. The external files and HMAC keys are still local test fixtures, not independent production custody.

The generic caller transition method has been removed. `GITHUB_APPLIED` requires a role-authorized signed adapter receipt bound to the pinned purpose, request hash, repo, ref, App ID, and target SHA. `PENDING_RECONCILIATION` requires a worker receipt; `BREACH` requires reconciler evidence. HMAC role credentials model this boundary only. Production must authenticate callers and protect distinct signer keys.

States: `UNCLAIMED → INTENT_RECORDED → GITHUB_APPLIED`; ambiguous results move through `PENDING_RECONCILIATION`; unexpected ref history/state moves to terminal `BREACH`. There is no transition back to `UNCLAIMED` or replacement intent.

The fake adapter models ref creation/update, lost responses, deletion, recreation, force updates, and ruleset denial. Its event journal is assumed complete; no GitHub integration occurred. Webhook tests explicitly deliver duplicate, missing, and reordered notifications; webhooks are not the ordering authority.

Run from this directory: `py -3 -m unittest discover -s . -p 'test*.py' -v`.

The report describes the remaining trust assumptions and unresolved historical cutover. Witness activation cannot reset the existing C2 attempt.
