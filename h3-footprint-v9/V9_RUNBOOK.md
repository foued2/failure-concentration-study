# V9 runbook

This runbook fixes the ordering conflict in V8, where the Gate said the
isolation check must pass before generation while the numbered stages put
generation first. Here the order is explicit and every step has a stop rule.

**Invariant: nothing that requires model output happens before the Sandbox
checks pass.** Steps 1 and 2 make no model calls and generate no candidates.

## Roles

- **Operator** runs the host controller, the Sandbox supervisor, and the
  non-generating CLI checks.
- **Reviewer** verifies hashes, the isolation report, and the effective
  permission evidence; does not run the job.

## Step 0: local integrity and configuration (host, no model calls)

```
python -m unittest discover -s tests -v
python make_manifest.py --check
python generation/generate_v9.py --verify-config --opencode <cli>
```

Stop unless: all tests pass, manifest matches, and the evidence shows
`agent_loaded: true`, `agent_fully_denied: true`, and all three frozen model IDs
present.

Stop rule: a permission leak (any probed action resolving to `allow` or `ask`)
is a hard stop. Do not weaken the profile to make a request succeed.

## Step 1: Sandbox isolation probe (Sandbox, networking disabled)

Stage into `C:\h3-staging` (read-only mapping) only:

- `h3-footprint-v9/sandbox-runtime/` (four files: supervisor, child, protocol, winjob)
- exactly one candidate body under `active/body.py`
- exactly one `active/job.json`

Never stage `oracle.py`, `constants.py`, `controller.py`, the full probe bank,
other candidates, or the Git repository. `C:\h3-out` is the only writable
mapping. `C:\h3-scratch` is Sandbox-local.

Run `supervisor.py` inside the Sandbox and confirm, from inside:

1. the host repository and credentials are not present;
2. network egress fails;
3. a child cannot write to `active/` or `response/`;
4. `icacls /remove:d`, `/reset`, `/grant` and `takeown` all fail from the child;
5. the grandchild-spawner fixture leaves no live descendant after timeout;
6. the child cannot read any reference answer (there is none to read).

Stop unless every check is recorded in `isolation-report.json`, stored outside
the writable mapping.

## Step 2: rendezvous test (Sandbox, no candidates)

Publish harmless token A, confirm the Sandbox sees it, kill the process tree,
confirm the tree is gone, then publish token B. Prove no surviving descendant
can observe B before it becomes active.

Stop rule: if the mapping does not reflect host updates with the required
ordering, or the ordering is ambiguous, stop. Do not map the full probe bank or
all bodies as a workaround.

## Step 3: generation (host, network allowed)

Only after steps 0-2 pass:

```
set V9_AUTHORIZE_GENERATION=1
python generation/generate_v9.py --batches 100
```

The generator is hard-gated on that variable and refuses otherwise. It uses one
workspace per batch, a deny-all agent, no `--auto`, and accepts at most eight
bodies in response order.

Stop rule: any tool event, permission event, nonzero exit, or partial response
rejects the batch. Do not retry with relaxed permissions or a substituted model.

## Step 4: evaluation (Sandbox)

The host controller owns the oracle and drives one job at a time:

```
python controller.py --bodies <staging> --work-root <runs/current>
```

The controller refuses to publish a new job unless the previous response exists
and reports `tree_empty: true`. Any `boundary_error`, `staging_mismatch` or
supervisor error aborts the run; it is never scored.

## Artifacts

Per run: `isolation-report.json`, rendezvous log, generation
`attempts.jsonl`, per-probe response records (job id, body hash, probe index,
exit status, timeout, tree-empty, bounded stdout hash), and the controller's
scored rows. The report must be recomputable from these records alone.

## Stop conditions

- Any gate in `STATUS.json` not PASS or explicitly waived: stop.
- Manifest or hash mismatch: stop.
- Permission leak: stop.
- Boundary or staging error: stop, do not score.
- Surviving descendant: stop.
