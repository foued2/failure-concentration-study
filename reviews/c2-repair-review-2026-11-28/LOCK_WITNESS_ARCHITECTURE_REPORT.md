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

1. **Intent endpoint:** authorized operator submits a canonical request containing purpose key, registered ID, exact OAC SHA, ref, expected B, intended lock commit A/manifest digest, and idempotency key. Witness validates the request against pinned policy.
2. **Durable first-writer claim:** witness executes one serializable transaction. A unique constraint on study-purpose key allows exactly one intent. It appends an event to an append-only hash chain and commits before any GitHub request. A concurrent different request loses; exact duplicate retries return the same claim. No subsequent intent can replace it.
3. **Only then call GitHub:** witness worker (the sole holder of App credentials) creates the ref at B if absent, then advances it once from B to A. Ruleset restricts creations, updates, and deletions to that App; force pushes are disabled. The ref payload is immutable by policy after the one intended transition. Prefer a single Git receive operation with an atomic transaction if available; otherwise expose distinct states and never infer failure from a lost HTTP response.
4. **Crash/retry:** before durable intent, outage means no GitHub operation. After intent, outage leaves the attempt consumed and in `PENDING`; retry the same idempotency key only. After an ambiguous GitHub response, read the exact ref and compare against B/A before retrying. If ref is absent or still B, safely retry the same intended transition. If it is A, mark applied. Any other value/deletion is a breach; do not issue a replacement intent.
5. **Evidence:** witness signs each event/checkpoint with a key held separately from GitHub, exports checkpoints to at least two independently administered append-only/WORM stores, and obtains externally verifiable timestamped checkpoints. Store the exact signed request, accepted/rejected response, ordered sequence, prior-event digest, GitHub request ID/response, ref reads, App identity, and ruleset snapshot. Webhooks only prompt reconciliation and are never authoritative for order.

The witness transaction precedes GitHub mutation, but there is no distributed atomic transaction spanning witness storage and GitHub. The consumed intent is the safety mechanism: after a crash, recover that exact intent. This favors safety over liveness and can leave a permanently consumed but unapplied attempt.

## GitHub enforcement findings

- Branch/tag rulesets can restrict creations, updates, and deletions by ref pattern and define bypass actors. A ruleset can therefore deny direct human writes and admit one GitHub App. The Git refs REST API supports create and update calls; update includes a `force` option, which must be false.
- Rulesets do **not** remove the repository-admin trust boundary. GitHub documents that repository admins or users with `edit repository rules` can create/edit/delete repository rulesets. Bypass lists can include roles, users, teams, and Apps. An administrator who can alter policy can weaken it or add a bypass. On a personal repository there is no organization-level policy layer to separate those authorities.
- Organization-level rulesets provide a stronger boundary: org owners edit the org ruleset, and repo admins cannot loosen it (repository rules only aggregate restrictively); however repo admins can add stricter repo rules. Thus trust is shifted to organization owners, enterprise owners where applicable, and GitHub. This is not fully trustless.
- A GitHub App can receive installation tokens scoped to repositories and permissions, including `contents:write`; the token cannot exceed the App's granted permission. Configure only the target repo and minimum permissions, keep credentials exclusively in the witness worker, and do not grant the App ruleset administration. This makes it a practical exclusive writer for compliant users, not a cryptographic guarantee against policy administrators or GitHub.
- Webhook delivery is best effort: GitHub documents missing, delayed, duplicated/redelivered and out-of-order deliveries. Therefore webhook arrival order cannot establish firstness. Repository Activity is an observation feed, not an enforced append-only log; the supplied Revision 5 evidence is a parsed projection without raw headers and covers only the first 100 records. Organization Git audit events include `git.push`, but Enterprise Cloud git-event REST retention is documented as seven days; this is useful corroboration, not durable historical completeness.

## Property matrix

| Property | Witness + exclusive App + rulesets | GitHub Activity/webhook only |
|---|---|---|
| Firstness | Yes, as first intent serialized by witness, assuming all relevant writes are forced through it and witness ordering is linearizable | No; cannot establish absence of an earlier missed/unretained event |
| Single use | Yes for accepted intents via unique purpose-key claim; same request retry is idempotent | Detection only if complete records are available; no enforcement |
| Immutability | Ref create/update/delete restricted to App; later tampering blocked for ordinary actors and visible in ref/audit evidence. Admin can weaken rules | Detection/corroboration only; current ref can hide prior delete/recreate history |
| Completeness | Witness ledger completeness is conditional on durable append-only replicas/checkpoints; GitHub history remains separate | No guarantee; webhook misses and finite/undocumented retention prevent absence proof |
| Availability | Intentionally fail closed; outage before intent means no write, after intent means consumed/PENDING until recovery | Feed/webhook/API outage makes conclusion incomplete |
| Auditability | Signed hash-chain events + external checkpoints + exact GitHub request/response; WORM replicas | Public corroboration may exist, but evidence is delayed/duplicated/possibly missing; raw preservation is needed |

## Explicit trusted parties and services

1. Witness operator(s), database/storage administrators, and signing-key custodian(s); they must not collude to rewrite, suppress, reorder, fork, or roll back the log. Independent replicas/checkpoint witnesses reduce, but do not erase, this trust.
2. GitHub App owner and witness-worker operators, because they control the only credentials that can write the ref.
3. Organization owners/enterprise owners (or personal repository owner/admin if kept personal), because they can change enforcement/bypass policy; GitHub platform/service operators.
4. Independent checkpoint/TSA providers only if used; they attest to a digest/time, not to its truth or completeness.

## Adversarial prototype results

`lock-witness-poc/` is a local SQLite state-machine prototype. Its append-only event table has a per-scope unique claim, serializing transaction, SHA-256 hash chain, FULL synchronous commits, duplicate idempotency, and replacement rejection. It has no GitHub adapter and is not production-grade immutable storage. An external `(sequence, hash)` checkpoint is necessary to detect full database rollback; the prototype cannot provide that external custody.

| Test | Result | What it shows / does not show |
|---|---|---|
| Two competing requests in independent processes | PASS | Spawned processes with separate SQLite connections race; one intent wins. Does not test distributed databases or App/ruleset behavior |
| Duplicate and delayed same request | PASS | Idempotent retry returns original claim |
| Different replacement request | PASS | Unique scope prevents a second claim |
| Missing/out-of-order webhook notifications | PASS (model) | Witness ordering does not depend on webhook; does not emulate GitHub event service |
| Ref deletion/recreation and force update | PASS (model) | A second intent remains rejected; actual GitHub ref/ruleset enforcement untested |
| Ruleset modification/bypass | LIMITATION CONFIRMED | Witness cannot prevent an administrator changing GitHub policy |
| Crash after durable record, before GitHub request | PASS (simulation) | Crash boundary represented; restart continues same request and rejects replacement |
| GitHub applies ref, response lost, witness restarts | PASS (fake GitHub) | Reopened witness returns exact duplicate; mocked ref read sees A; same operation is idempotent. No real network/ref operation exercised |
| Ruleset change or admin bypass after intent | LIMITATION CONFIRMED (simulation) | Mocked policy change blocks App; modeled direct admin mutation diverges from expected ref. Witness DB alone does not prevent or detect it; an active reconciliation read detects divergence |
| Persistent storage corruption/rollback | PASS (simulation) | Event deletion detected; full database snapshot rollback remains internally valid but differs from independently retained checkpoint |
| Hash-chain payload mutation | PASS | Local verifier detects payload mutation; coordinated rewrite plus replacement of all external checkpoints remains inside trust boundary |

Command: `py -3 -m unittest discover -s . -p 'test*.py' -v` in `lock-witness-poc/`. Result after adversarial additions: **12 tests passed**. All GitHub behaviors remain mocks/models, not integration results.

## Exact remaining assumptions and blockers

- Historical first qualifying lock cannot currently be established from the preserved Revision 5 evidence. Raw Activity pages and headers, full ledger, retention/completeness guarantee, and creation-to-first-record gap remain unresolved.
- No safe cutover for the same C2 purpose is authorized by this prototype. Until the historical attempt is independently classified, witness activation must not be treated as a fresh first event or permit another same-purpose lock.
- No GitHub sandbox repository was created for end-to-end ruleset/App validation. No production settings were inspected or changed.
- For prospective enforcement, require a single-purpose App as the sole ruleset bypass/writer, no human bypass, no direct credentials, tightly protected App private key, and restricted admin policy authority. The GitHub App itself must be enabled to bypass the ruleset for its one intended action; no other actor may bypass.
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
