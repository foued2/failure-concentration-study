# LC518 single-use lock witness proof of concept

Local proof of concept only. It does not contact GitHub, configure rulesets, create an OAC, query drand, or authorize a selection.

## Components

- `trust.py`: signed policy manifest, one-time initialization authorization, append-only external checkpoint file model, and role-specific receipt signatures.
- `witness.py`: fixed policy binding, exact request schema, SQLite checkpoint mirror, acceptance verification, and signed-evidence state transitions.
- `github_adapter.py`: adapter boundary, fake ref implementation, reconciliation logic, and webhook delivery simulator.
- `test_witness.py`: adversarial tests. GitHub and signer behavior is modeled locally.

The signed policy pins the canonical purpose key, experiment ID, registry digest, custodian identity, repository, ref, and App ID. Its persistent policy-authority log binds one manifest digest and custodian lineage to each scientific purpose; changing the experiment ID, registry digest, or custodian for that same purpose is rejected across authority reconstruction. The test ID is `TEST-ONLY-REGISTRY-ID`, not an LC518 registry value. The caller supplies no scope; aliases and unknown request fields are rejected. Replacing the witness or custodian policy after construction is rejected. This invariant is local to one authority log: a test demonstrates that two authority instances with the same root key but separate empty state files can issue divergent manifests for the same purpose. Production must pin one authority identity and registry head externally and route issuance through a singleton service with rollback-protected state. A compromised trusted root remains able to fork policy.

Checkpoint genesis is created only through an explicit one-time initialization authorization. The policy-authority model records issuance/consumption in its own signed append-only log. A new/empty SQLite checkpoint database or external checkpoint file is not implicitly treated as a valid start. The append-only JSONL checkpoint model is outside both SQLite mirrors, is signed, pins custodian ID and manifest digest, and advances by compare-and-append protected by a cross-process OS file lock covering read, compare, append, and fsync. A deterministic race test uses two independent SQLite DB copies synchronized at the same proposed head; one publication is accepted and the other rejected, with a valid resulting chain. This models processes sharing one local filesystem and is not a distributed checkpoint service. Acceptance verifies it against the SQLite checkpoint database and witness mirror. Tests reset both SQLite databases and roll back/corrupt the external checkpoint; all fail closed. The external files and HMAC keys are still local test fixtures, not independent production custody.

The generic caller transition method has been removed. `GITHUB_APPLIED` requires a role-authorized signed adapter receipt bound to the pinned purpose, request hash, repo, ref, App ID, and target SHA. Its receipt digest is persisted: an exact replay is idempotent after restart, while an altered signed receipt conflicts. `PENDING_RECONCILIATION` requires a worker receipt; `BREACH` requires reconciler evidence. HMAC role credentials model this boundary only. Production must authenticate callers and protect distinct signer keys.

States: `UNCLAIMED → INTENT_RECORDED → GITHUB_APPLIED`; ambiguous results move through `PENDING_RECONCILIATION`; unexpected ref history/state moves to terminal `BREACH`. There is no transition back to `UNCLAIMED` or replacement intent.

The fake adapter models ref creation/update, lost responses, deletion, recreation, force updates, and ruleset denial. Its event journal is assumed complete; no GitHub integration occurred. Webhook tests explicitly deliver duplicate, missing, and reordered notifications; webhooks are not the ordering authority.

Run from this directory: `py -3 -m unittest discover -s . -p 'test*.py' -v`.

The report describes the remaining trust assumptions and unresolved historical cutover. Witness activation cannot reset the existing C2 attempt.
