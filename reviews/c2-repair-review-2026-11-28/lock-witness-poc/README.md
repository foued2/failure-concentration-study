# LC518 single-use lock witness proof of concept

Isolated simulation only. It does not contact GitHub, configure rulesets, create an OAC, query drand, or authorize a selection.

The witness serializes claims in SQLite under `BEGIN IMMEDIATE`. Its append-only event table has a unique study-purpose key and a hash chain; first accepted request claims the key durably before a GitHub adapter may run. Exact retries return the existing claim. Competing payloads are rejected. The adapter is deliberately a stub. Fake GitHub tests model applying B-to-A, lost responses, restart reconciliation, and admin divergence; they do not contact GitHub.

Run: `python -m unittest -v` from this directory.

This proves local state-machine behavior, not GitHub's operation ordering or administrator-proof enforcement. Tests include independent Python processes racing on one SQLite file, restart after an ambiguous GitHub success, and database rollback against a saved external checkpoint. A real witness needs independently administered durable storage, access controls that prohibit update/delete, backups, externally anchored checkpoints, and an operational reconciliation process. Witness activation must not be treated as a reset of the existing C2 attempt; historical status must be independently resolved before same-purpose use.
