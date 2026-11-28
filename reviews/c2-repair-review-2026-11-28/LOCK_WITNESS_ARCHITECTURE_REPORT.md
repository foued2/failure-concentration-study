# LC518 C2 first-event and single-use lock investigation

**Starting point:** `review/lc518-c2-sequence-fixes-2026-11-28`, commit `2d42ff0c53f4bad1c006714e63c6e2020b626ee4`
**Scope:** infrastructure ordering and lock integrity only. The Revision 5 composite remains a candidate; nothing here adopts it or authorizes an OAC, lock, draw, seed, pair, or solver.

## Verdict

**FEASIBLE WITH EXPLICIT TRUST ASSUMPTIONS** for a *prospective* lock flow in which every authorized request must pass through an independent, linearizable witness before a dedicated GitHub App may create/update the canonical ref. This can establish the first request accepted by that witness and prevent a second authorized request from becoming a replacement.

It is **not feasible to prove historical firstness for the existing Revision 5 Activity-ledger method** from GitHub Activity/webhooks alone. Revision 5 itself says the raw pages and full ledger are not preserved, and the observed first record trails repository creation by 26 seconds. An absence claim cannot be recovered from the current partial normalized page. GitHub event timestamps and delivery order do not repair this.

No GitHub ruleset can make the design administrator-proof when people trusted to administer the repository can edit/disable rules or bypass them. With one personal-repository owner/admin in control, the witness provides meaningful protection only against actors who cannot alter the App, rulesets, or witness. For stronger separation, place the repository under an organization with an organization-level ruleset and distinct organization owners, while repository admins cannot modify that org-level policy; still trust org owners and GitHub itself.

### Historical cutover rule required before any use

Witness activation is not a reset, lock, or evidence that the prior C2 attempt was unused. It must not accept a production authorization for this same C2 purpose while historical lock status is unresolved. A prospective cutover would require an independently reviewed disposition of the legacy interval: complete evidence establishing `NO_VALID_LOCK`, or a recorded `VALID_LOCK` which consumes the attempt permanently. If the historical interval remains incomplete, status stays indeterminate and the same-purpose witness cannot authorize another attempt. A distinct future study-purpose key would require separate prospective authority and explicit disclosure; it cannot be used to relabel or bypass the existing C2 attempt. This is a proposed gate for review, not an adopted protocol amendment.

## Revision 5 point of departure

Revision 5 defines a sequence of master OAC push, canonical lock-ref creation at B, and first B-to-A push. It consumes the attempt on the first event that creates or mutates that ref, and makes later ref deletion/rewrite/recreation an audit breach rather than a successor route. This is a sound *interpretation rule after complete evidence is known*. It does not cause GitHub to enforce that only one actor can perform that first event, and it depends on a complete pre-lock Activity ledger to prove no earlier event. Its own §9.7/§11 identify missing raw Activity pages/headers and incomplete preservation.

## Proposed architecture

1. **Signed policy and pinned identity:** an authorized policy authority signs a manifest binding the canonical purpose key, registered ID/digest, custodian identity, repository, lock ref, and App ID. The caller cannot submit a scope; unknown request fields are rejected. A legitimate new scientific purpose requires a separately authorized manifest, and the current custodian will reject its different manifest digest.
2. **Explicit genesis and external checkpoint:** initialization requires a one-time signed authorization. The external checkpoint JSONL model writes a signed genesis record bound to the custodian identity and manifest digest; an empty/new store is never implicitly initialized. Before acceptance, the witness verifies the external log, the SQLite custodian mirror, and the witness-local mirror. Exact duplicate retries return the old claim; changed request, alias ID, or metadata cannot create another claim. A local witness mirror behind a valid checkpoint is rebuilt from the checkpoint DB; an empty/reset DB, external rollback, local-ahead mirror, signature error, missing genesis, or identity mismatch fails closed.
3. **Only then call GitHub:** witness worker (the sole holder of App credentials) creates the ref at B if absent, then advances it once from B to A. Ruleset restricts creations, updates, and deletions to that App; force pushes are disabled. The ref payload is immutable by policy after the one intended transition. Prefer a single Git receive operation with an atomic transaction if available; otherwise expose distinct states and never infer failure from a lost HTTP response.
4. **Recovery states:** `UNCLAIMED → INTENT_RECORDED → GITHUB_APPLIED`; ambiguous or unavailable GitHub result goes `INTENT_RECORDED → PENDING_RECONCILIATION → GITHUB_APPLIED`. Unexpected ref lifecycle/state goes to terminal `BREACH`. From `GITHUB_APPLIED`, only later `BREACH` is allowed. No transition restores `UNCLAIMED`, and no replacement intent is allowed. The transition graph is implemented in the checkpoint model.
5. **Crash/retry:** the checkpoint append is the authoritative consumed intent. If the witness crashes after it but before local mirror update, it recovers the exact signed event. If GitHub applies A but the response is lost, the worker marks pending, reads the ref, and completes the same intent; a competing request remains rejected. If GitHub has not mutated the ref, retry only the recorded B-to-A operation. Unexpected deletion/recreation/force-update transitions to breach when the reconciler has complete lifecycle evidence.
6. **Evidence and transition authority:** the model uses HMAC-signed checkpoint records and role-specific adapter/worker/reconciler receipts. `Witness` has no generic public `transition()` method. It validates receipt signature, role, request hash, canonical scope, repository, lock ref, App ID, and target SHA before recording `GITHUB_APPLIED`; worker-signed pending evidence and reconciler-signed breach evidence have separate roles. Production must use separately held asymmetric keys and an authenticated API. Store signed request, accepted/rejected response, ordered sequence, prior-event digest, GitHub request/response, ref reads, App identity, and ruleset snapshot. Webhooks only prompt reconciliation and are never authoritative for order.

There is no distributed atomic transaction spanning the checkpoint DB, external checkpoint file, witness mirror, and GitHub. If the external append succeeds but the SQLite commit does not, the stores disagree and fail closed; recovery needs an operator procedure for the exact recorded event. If GitHub applies A but its response is lost, a reconstructed worker reads the same adapter/ref state and signs evidence for the original intent. This favors safety over liveness and can leave a consumed but unapplied attempt.

### State transition table

| Current state | Allowed next state(s) | Required authority/evidence |
|---|---|---|
| `UNCLAIMED` | `INTENT_RECORDED` | Signed policy + explicit initialized custodian append |
| `INTENT_RECORDED` | `GITHUB_APPLIED` | Signed adapter receipt matching purpose, request hash, repo/ref, App ID, and target SHA |
| `INTENT_RECORDED` | `PENDING_RECONCILIATION` | Signed witness-worker receipt for ambiguous/incomplete operation |
| `INTENT_RECORDED` | `BREACH` | Signed independent-reconciler receipt |
| `PENDING_RECONCILIATION` | `GITHUB_APPLIED` | Matching signed adapter receipt after reading the ref |
| `PENDING_RECONCILIATION` | `BREACH` | Signed independent-reconciler receipt |
| `GITHUB_APPLIED` | `BREACH` | Signed independent-reconciler receipt for later ref lifecycle/tampering |
| `BREACH` | none | Terminal state |

No state transition unclaims a purpose or authorizes a second request.

## GitHub enforcement findings

- Branch/tag rulesets can restrict creations, updates, and deletions by ref pattern and define bypass actors. A ruleset can therefore deny direct human writes and admit one GitHub App. The Git refs REST API supports create and update calls; update includes a `force` option, which must be false.
- Rulesets do **not** remove the repository-admin trust boundary. GitHub documents that repository admins or users with `edit repository rules` can create/edit/delete repository rulesets. Bypass lists can include roles, users, teams, and Apps. An administrator who can alter policy can weaken it or add a bypass. On a personal repository there is no organization-level policy layer to separate those authorities.
- Organization-level rulesets provide a stronger boundary: org owners edit the org ruleset, and repo admins cannot loosen it (repository rules only aggregate restrictively); however repo admins can add stricter repo rules. Thus trust is shifted to organization owners, enterprise owners where applicable, and GitHub. This is not fully trustless.
- A GitHub App can receive installation tokens scoped to repositories and permissions, including `contents:write`; the token cannot exceed the App's granted permission. Configure only the target repo and minimum permissions, keep credentials exclusively in the witness worker, and do not grant the App ruleset administration. This makes it a practical exclusive writer for compliant users, not a cryptographic guarantee against policy administrators or GitHub.
- Webhook delivery is best effort: GitHub documents missing, delayed, duplicated/redelivered and out-of-order deliveries. Therefore webhook arrival order cannot establish firstness. Repository Activity is an observation feed, not an enforced append-only log; the supplied Revision 5 evidence is a parsed projection without raw headers and covers only the first 100 records. Organization Git audit events include `git.push`, but Enterprise Cloud git-event REST retention is documented as seven days; this is useful corroboration, not durable historical completeness.

## Property matrix

| Property | Witness + exclusive App + rulesets | GitHub Activity/webhook only |
|---|---|---|
| Firstness | Prospective first accepted request under signed pinned policy and checkpoint ordering, if the external custodian is independent and every ref writer is controlled. Cannot establish historical firstness. | No; cannot establish absence of earlier/missed/unretained event |
| Single use | Implemented in model: signed policy binding plus unique claim at pinned custodian identity. New-purpose manifest requires separate policy authority. | No enforcement |
| Immutability | Ruleset/App can block ordinary actors; admin can weaken rules. Modeled reconciler detects deletion/recreation/force only with complete adapter lifecycle evidence. | Detection/corroboration only; webhook gaps and hidden same-SHA recreation may be invisible |
| Completeness | Model verifies signed genesis, append-only external checkpoint, SQLite checkpoint DB, and local mirror at every acceptance. Production completeness depends on separately operated custody, append-only storage, key custody, and retention. | No guarantee; webhook misses and finite/undocumented retention prevent absence proof |
| Availability | Fail closed for missing/stale/corrupt checkpoint. After intent, outage leaves consumed state pending recovery. | Feed/webhook/API outage makes conclusion incomplete |
| Auditability | Signed manifest/genesis, checkpoint chain, and role receipts are modeled; actual independent custody, App exchange, and durable evidence export are not. | Public corroboration may exist, but evidence is delayed/duplicated/possibly missing; raw preservation is needed |

## Explicit trusted parties and services

1. Witness operator(s), database/storage administrators, and signing-key custodian(s); they must not collude to rewrite, suppress, reorder, fork, or roll back the log. Independent replicas/checkpoint witnesses reduce, but do not erase, this trust.
2. GitHub App owner and witness-worker operators, because they control the only credentials that can write the ref.
3. Organization owners/enterprise owners (or personal repository owner/admin if kept personal), because they can change enforcement/bypass policy; GitHub platform/service operators.
4. Independent checkpoint/TSA providers only if used; they attest to a digest/time, not to its truth or completeness.

## Adversarial prototype results

`lock-witness-poc/` separates `trust.py`, `witness.py`, and `github_adapter.py`. The signed test policy binds scientific purpose, canonical purpose key, experiment ID, registry digest, custodian ID, repo, ref, and App ID. Its `TEST-ONLY-REGISTRY-ID` is a fixture, not an LC518 registry value. `CheckpointStore` requires explicit signed genesis initialization and checks its SQLite state against a signed JSONL checkpoint outside both SQLite DBs. `Witness`, `CheckpointStore`, and `ExternalCheckpoint` reject policy/identity reassignment after construction. The external files, policy authority, HMAC keys, and receipt signers are all local test fixtures in the same trust environment; they are not independent operational custody. A reset external file/history also remains within the trusted-custodian boundary. Production needs separately administered services, protected asymmetric keys, and durable independently retained head checkpoints.

| Test | Result | What it shows / does not show |
|---|---|---|
| Caller scope/experiment alias/extra metadata | PASS (policy model) | No scope parameter exists; exact request schema rejects aliases and extra fields |
| Witness policy object replacement | PASS (object model) | Assignment to `policy`, `_policy`, or mapping entries fails after construction |
| Alternate purpose-key manifest / second Witness | PASS (policy model) | Trusted policy registry rejects same-purpose alias; existing custodian rejects a different manifest digest |
| Empty checkpoint / wrong custodian identity | PASS (genesis model) | New empty DB/file fails without explicit genesis; wrong custodian fails the signed manifest binding |
| Explicit genesis initialization | PASS (bootstrap model) | Requires signed one-time authorization and refuses duplicate initialization |
| Reset both SQLite databases | PASS (genesis model) | External checkpoint remains; reset checkpoint DB lacks authorized genesis metadata and fails closed |
| External checkpoint corruption | PASS (file model) | Invalid appended record fails before intent acceptance |
| External checkpoint rollback | PASS (file model) | Rollback to genesis while both SQLite DBs remain advanced fails closed |
| Two independent processes submit competing intent payloads | PASS (SQLite/file model) | Separate spawned processes share the checkpoint DB and external file; one accepted, one rejected |
| Duplicate and changed target | PASS | Exact retry is idempotent; changed target for the canonical scope is rejected |
| Authenticated state transitions | PASS (receipt model) | Generic Witness transition method absent; unsigned/wrong-role evidence rejected; fake signed App receipt required for applied |
| Crash after intent, before GitHub call | PASS (fake adapter) | Reconstructs witness/checkpoint components and resumes same intent; changed target rejected |
| GitHub applies ref, response lost | PASS (fake adapter) | Closes/reconstructs witness, checkpoint DB, external checkpoint reader, and reconciler; same target reconciles, different target rejected |
| Webhook duplicate, missing, reordered | PASS (delivery model) | Inbox receives duplicate and reversed notifications; omitted create notification does not control reconciliation |
| Ref deletion / recreation / force update | PASS (fake adapter journal) | Complete modeled lifecycle journal leads to BREACH, including recreation at the same SHA |
| Real GitHub App/ruleset enforcement | NOT TESTED | No App, ruleset, repository API, or production setting touched |

Command: `py -3 -m unittest discover -s . -p 'test*.py' -v` in `lock-witness-poc/`. Result: **16 tests passed**. Policy authority, checkpoint custodian, receipt signers, GitHub refs, and webhook delivery remain local models, not integration results.

## Exact remaining assumptions and blockers

- Historical first qualifying lock cannot currently be established from the preserved Revision 5 evidence. Raw Activity pages and headers, full ledger, retention/completeness guarantee, and creation-to-first-record gap remain unresolved.
- No safe cutover for the same C2 purpose is authorized by this prototype. Until the historical attempt is independently classified, witness activation must not be treated as a fresh first event or permit another same-purpose lock.
- No GitHub sandbox repository was created for end-to-end ruleset/App validation. No production settings were inspected or changed.
- For prospective enforcement, require a single-purpose App as the sole ruleset bypass/writer, no human bypass, no direct credentials, tightly protected App private key, and restricted admin policy authority. The GitHub App itself must be enabled to bypass the ruleset for its one intended action; no other actor may bypass.
- The model uses HMAC and a second local SQLite file; it does not implement remote independent checkpoint custody, asymmetric signatures, signing-key protection/rotation, WORM replication, or external timestamp anchoring. These are required before calling it an enforceable independent witness.
- The signed policy authority and custodian identity are modeled, but the policy signing key is not independently administered. Anyone who controls that root authority can authorize a new manifest/purpose; this must be a separately governed authorization boundary.
- The request method has no user authentication or authorization layer. The pinned policy prevents request-supplied scope aliases, but a production endpoint must authenticate callers and enforce who may submit the one allowed intent.
- Adapter receipts are HMAC-signed by a local fake adapter; they do not come from GitHub. Production must bind the receipt signer to a narrowly scoped worker credential and verify actual GitHub API responses/ref reads.
- Need independent witness deployment review: linearizable transactional storage; append-only/WORM storage and independent checkpointing; signing-key rotation/recovery; replicated backups; access controls; concurrency/load and crash fault injection; and tested GitHub reconciliation.
- A witness sequence proves order only within the witness's accepted request universe. To claim that the lock was the first qualifying operation, all paths capable of mutating/creating the ref must be blocked or included in the trusted ordering system. GitHub admins/platform remain capable of breaking this boundary.
- Revision 5's stated canonical registry ID remains unresolved and is outside this work. No protocol adoption, lock, or draw follows from this report.

## Primary sources

- [GitHub ruleset rules and administrator permissions](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Creating repository rulesets and bypass actors](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- [Organization rulesets and repository-admin limits](https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization)
- [GitHub webhook troubleshooting: missing, delayed and out of order](https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/troubleshooting-webhooks)
- [GitHub App installation access tokens](https://docs.github.com/en/rest/apps/apps)
- [GitHub REST Git refs](https://docs.github.com/en/rest/git/refs)
- [Organization audit log Git events and retention](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/audit-log-events-for-your-organization)
