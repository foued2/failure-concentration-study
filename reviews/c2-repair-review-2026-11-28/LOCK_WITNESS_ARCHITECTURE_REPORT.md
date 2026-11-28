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

1. **Policy-bound intent endpoint:** the server pins one canonical purpose key, registered ID, and registry-entry digest. The caller cannot submit a scope; unknown request fields are rejected, and submitted experiment/registry identity must match server policy. A legitimate new scientific purpose requires a separate authorized policy change, outside this endpoint.
2. **External checkpoint append:** before acceptance is returned, the witness verifies the complete signed checkpoint chain and compares its local mirror. The separately modeled custodian atomically appends the purpose claim under a unique key. Exact duplicate retries return the old claim; changed request, alias ID, or metadata cannot create another claim. If local storage is behind because of a crash, the mirror is recovered from the custodian. If local state is ahead, signatures fail, or checkpoint state is missing/stale, the request fails closed.
3. **Only then call GitHub:** witness worker (the sole holder of App credentials) creates the ref at B if absent, then advances it once from B to A. Ruleset restricts creations, updates, and deletions to that App; force pushes are disabled. The ref payload is immutable by policy after the one intended transition. Prefer a single Git receive operation with an atomic transaction if available; otherwise expose distinct states and never infer failure from a lost HTTP response.
4. **Recovery states:** `UNCLAIMED → INTENT_RECORDED → GITHUB_APPLIED`; ambiguous or unavailable GitHub result goes `INTENT_RECORDED → PENDING_RECONCILIATION → GITHUB_APPLIED`. Unexpected ref lifecycle/state goes to terminal `BREACH`. From `GITHUB_APPLIED`, only later `BREACH` is allowed. No transition restores `UNCLAIMED`, and no replacement intent is allowed. The transition graph is implemented in the checkpoint model.
5. **Crash/retry:** the checkpoint append is the authoritative consumed intent. If the witness crashes after it but before local mirror update, it recovers the exact signed event. If GitHub applies A but the response is lost, the worker marks pending, reads the ref, and completes the same intent; a competing request remains rejected. If GitHub has not mutated the ref, retry only the recorded B-to-A operation. Unexpected deletion/recreation/force-update transitions to breach when the reconciler has complete lifecycle evidence.
6. **Evidence:** the model HMAC-signs checkpoint events and compares sequence/hash against a second local SQLite mirror. Production must replace this with a separately operated append-only service, asymmetric verification, and independently retained checkpoints. Store signed request, accepted/rejected response, ordered sequence, prior-event digest, GitHub request/response, ref reads, App identity, and ruleset snapshot. Webhooks only prompt reconciliation and are never authoritative for order.

There is no distributed atomic transaction spanning the checkpoint custodian and GitHub. The external append is authoritative before GitHub; local mirror failure is recoverable from the custodian. GitHub mutation is reconciled against that same intent. This favors safety over liveness and can leave a permanently consumed but unapplied attempt.

### State transition table

| Current state | Allowed next state(s) | Meaning |
|---|---|---|
| `UNCLAIMED` | `INTENT_RECORDED` | Canonical purpose consumed at external checkpoint |
| `INTENT_RECORDED` | `GITHUB_APPLIED`, `PENDING_RECONCILIATION`, `BREACH` | Exact operation applied, ambiguous/retryable, or contradictory evidence |
| `PENDING_RECONCILIATION` | `GITHUB_APPLIED`, `BREACH` | Reconcile exact intent; no replacement |
| `GITHUB_APPLIED` | `BREACH` | Later unauthorized ref lifecycle/tampering observed |
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
| Firstness | Prospective first accepted request under pinned purpose, if independent checkpoint is linearizable and every ref writer is controlled. Cannot establish historical firstness. | No; cannot establish absence of earlier/missed/unretained event |
| Single use | Implemented in model: server-owned purpose/registry binding plus unique external claim. New purpose policy requires separately trusted authorization. | No enforcement |
| Immutability | Ruleset/App can block ordinary actors; admin can weaken rules. Modeled reconciler detects deletion/recreation/force only with complete adapter lifecycle evidence. | Detection/corroboration only; webhook gaps and hidden same-SHA recreation may be invisible |
| Completeness | Model verifies signed chain and local mirror at every acceptance. Production completeness depends on independent custodian, append-only storage, key custody, and checkpoint retention. | No guarantee; webhook misses and finite/undocumented retention prevent absence proof |
| Availability | Fail closed for missing/stale/corrupt checkpoint. After intent, outage leaves consumed state pending recovery. | Feed/webhook/API outage makes conclusion incomplete |
| Auditability | Signed chain and mirror are implemented in the model; actual independent checkpointing, App exchange, and durable evidence export are not. | Public corroboration may exist, but evidence is delayed/duplicated/possibly missing; raw preservation is needed |

## Explicit trusted parties and services

1. Witness operator(s), database/storage administrators, and signing-key custodian(s); they must not collude to rewrite, suppress, reorder, fork, or roll back the log. Independent replicas/checkpoint witnesses reduce, but do not erase, this trust.
2. GitHub App owner and witness-worker operators, because they control the only credentials that can write the ref.
3. Organization owners/enterprise owners (or personal repository owner/admin if kept personal), because they can change enforcement/bypass policy; GitHub platform/service operators.
4. Independent checkpoint/TSA providers only if used; they attest to a digest/time, not to its truth or completeness.

## Adversarial prototype results

`lock-witness-poc/` separates `witness.py` (policy, acceptance, state transitions), its `CheckpointStore` class (signed append-only custodian model), and `github_adapter.py` (adapter boundary and fake). The caller never supplies the scope; the policy is read-only in the witness instance. Requests must match the pinned test registry ID/digest and exact schema. `CheckpointStore` is a separate SQLite file and verifies sequence, chain, HMAC signatures, and claims before every append. `Witness.intent()` verifies the custodian and mirror before accepting, and fails closed on corruption, a missing/stale anchor, or local rollback. This tests the acceptance logic, but it is not an independently operated service: the test process holds the HMAC key and can access both SQLite files. Production needs a remote custodian with separately controlled asymmetric signing keys and durable external checkpoint retention.

| Test | Result | What it shows / does not show |
|---|---|---|
| Caller scope/experiment alias/extra metadata | PASS (policy model) | No scope parameter exists; request must match pinned experiment/registry and exact schema; aliases rejected |
| Two independent processes submit competing intent payloads | PASS (SQLite model) | Separate spawned processes share external claim store; one accepted, one rejected. Not a distributed-service test |
| Corrupt external checkpoint signature | PASS (SQLite model) | Acceptance path verifies and fails before append |
| Missing/stale external checkpoint | PASS (SQLite model) | Empty anchor against nonempty local mirror fails closed |
| External checkpoint rollback | PASS (SQLite snapshot model) | Restore prior signed anchor while local mirror is ahead; acceptance fails closed |
| Recovery states | PASS | Transition graph enforces allowed moves; breach terminal and no return to unclaimed |
| Crash after intent, before GitHub call | PASS (fake adapter) | Restart recovers intent, then exact operation only; changed target rejected |
| GitHub applies ref, response lost | PASS (fake adapter) | Pending + ref reconciliation completes same intent after simulated lost response; no real GitHub request |
| Webhook duplicate, missing, reordered | PASS (delivery model) | Inbox deduplicates delivery IDs and preserves arrival order; missing create notification does not affect adapter-state reconciliation |
| Ref deletion / recreation / force update | PASS (fake adapter journal) | Reconciler sees complete modeled event journal and transitions to breach, including recreation at same SHA |
| Ruleset policy denial before write | PASS (fake adapter) | Intent remains pending and resumes only after same App request is allowed; policy administration itself not integrated |
| Real GitHub App/ruleset enforcement | NOT TESTED | No App, ruleset, repository API, or production setting touched |

Command: `py -3 -m unittest discover -s . -p 'test*.py' -v` in `lock-witness-poc/`. Result: **14 tests passed**. Custodian, GitHub refs, and webhook delivery remain local models, not integration results.

## Exact remaining assumptions and blockers

- Historical first qualifying lock cannot currently be established from the preserved Revision 5 evidence. Raw Activity pages and headers, full ledger, retention/completeness guarantee, and creation-to-first-record gap remain unresolved.
- No safe cutover for the same C2 purpose is authorized by this prototype. Until the historical attempt is independently classified, witness activation must not be treated as a fresh first event or permit another same-purpose lock.
- No GitHub sandbox repository was created for end-to-end ruleset/App validation. No production settings were inspected or changed.
- For prospective enforcement, require a single-purpose App as the sole ruleset bypass/writer, no human bypass, no direct credentials, tightly protected App private key, and restricted admin policy authority. The GitHub App itself must be enabled to bypass the ruleset for its one intended action; no other actor may bypass.
- The model uses HMAC and a second local SQLite file; it does not implement remote independent checkpoint custody, asymmetric signatures, signing-key protection/rotation, WORM replication, or external timestamp anchoring. These are required before calling it an enforceable independent witness.
- The request method has no user authentication or authorization layer. The pinned policy prevents request-supplied scope aliases, but a production endpoint must authenticate callers and enforce who may submit the one allowed intent.
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
