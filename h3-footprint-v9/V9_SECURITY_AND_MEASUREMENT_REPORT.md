# V9 security and measurement report

**Date:** 2026-10-28 (revision 2)
**Branch:** `dev/h3-footprint-v9-implementation-2026-10-28`
**Status:** implementation; not frozen; **no candidate generation or evaluation authorized.**

Revision 2 repairs defects found in the first pushed revision. The most
important one was mine: revision 1 *described* a host/Sandbox boundary but its
controller executed the supervisor with the local Python interpreter. The
boundary now exists in the execution path, refuses to be bypassed, and the
weakness of the host path is measured rather than asserted away.

## What changed in revision 2

| Defect | Repair |
|---|---|
| Controller ran the supervisor locally while claiming Sandbox isolation | `Controller` requires an explicit transport. `evaluate_authorized` raises `BoundaryNotEstablished` unless the transport has a verified Sandbox attestation. |
| Forgery test only searched its own scratch directory | Two new fixtures: one given explicit absolute paths to the reference data, one that imports the host oracle and scores `k = 0`. Both now *assert the exposure*. |
| Generation accepted one valid body as a complete batch; ignored permission events and malformed lines | Batch requires at least the requested count; permission events and malformed event streams reject the batch. |
| Runbook documented a CLI that did not exist, and implied `V9_AUTHORIZE_GENERATION=1` enabled generation | The CLI exists and is tested; generation is not implemented and says so. |
| ACL fixture used `%USERNAME%`, which the child environment does not define, and ignored why commands failed | SID resolved via `whoami /user`, attempts use the SID, exit codes and output are recorded and asserted. |

## The measured host exposure

This is the reason the transport requirement exists. A low-integrity child on
the host, given the repository path, reads:

```
oracle           READ   """Host-only reference oracle.  SECURITY
expected_values  READ   {   "A1": 3,   "A2": 1, ...
controller       READ   """Host controller: the only component t
```

A second fixture imports that oracle and answers from the answer key without
solving anything. Observed on the host transport:

```
key_reader.py  ->  k = 0,  30/30 probes correct,  isolation_verified = False
```

That is the V8 defect reproduced end to end: key disclosure plus control of the
response channel yields fabricated correct answers. The difference is that it is
now a failing boundary condition that blocks evaluation, not a green test.

**Low integrity is not a read barrier.** Mandatory integrity control prevents
write-up; it does not prevent read-down. Only removing the data from the
candidate's filesystem view does that, which is what the Sandbox mapping does.

## Architecture

| Component | Runs where | Holds reference data | In Sandbox image |
|---|---|---|---|
| `oracle.py` | host | **yes** | no |
| `controller.py` | host | **yes** | no |
| `backend.py` | host | no | no |
| `supervisor.py` | Sandbox | no | yes |
| `child_runner.py` | Sandbox (untrusted child) | no | yes |
| `sandbox_agent.py` | Sandbox | no | yes |
| `winjob.py` | Sandbox | no | yes |
| `protocol.py` | Sandbox | no | yes |

The controller publishes one body and one probe input into a read-only mapped
folder. `sandbox_agent.py` executes it and returns one raw answer through a
writable mapped folder. The host compares that raw value against the oracle.

### The handshake

1. Host writes `session.json` containing a fresh nonce into the inbox.
2. Agent reads the nonce, reads **its own account from the token**
   (`GetUserNameW`, not the environment), and writes `hello.json` with the nonce
   echoed back.
3. Host accepts only if `nonce` matches, `inside_sandbox` is true, and the
   account is `WDAGUtilityAccount`.

The nonce stops a stale `hello.json` from a previous session being replayed. The
token read stops an environment variable from masquerading as the Sandbox
account. `tests/test_backend.py` exercises the rejection paths; the *acceptance*
path requires a real Sandbox and is `NOT_RUN`.

A candidate cannot forge the handshake because no candidate code exists until
after the handshake completes.

### Ordering

The host publishes job N+1 only after receiving response N, and the supervisor
publishes a response only after the candidate's Job Object reports
`ActiveProcesses == 0`. A descendant that survived job N therefore cannot
observe job N+1.

## Findings and controls

| # | Finding | Control | Test | Where it ran |
|---|---|---|---|---|
| 1 | Shared interpreter let a candidate replace the worker's emitter | Candidate never shares an interpreter with reference data or scoring; host compares a raw value | `test_stdout_hijack_cannot_improve_score` | host |
| 2 | Expected values readable from the candidate | No reference data in the Sandbox image; only `{n, edges, s, t}` crosses | `test_secrecy.*`, `test_boundary.HostBoundaryExposure` | host |
| 3 | `subprocess.run(timeout=5)` left descendants alive | Job Object kill-on-close; termination verified via `ActiveProcesses == 0` | `test_process_tree.test_timeout_kills_descendants` | host |
| 4 | `--pure` is not a tool boundary | Versioned deny-all agent, pinned config, no `--auto`, last-match-wins resolution | `test_generation.*`, `evidence/opencode-config.json` | host |
| 5 | Eight-body cap unenforced; incomplete batches accepted | Completeness check plus deterministic 8-body cap | `test_generation.CompletenessTests` | host |
| 6 | Gate/Runbook ordering conflict | Probe and rendezvous precede generation; generation hard-gated | `V9_RUNBOOK.md` | n/a |
| 7 | **Claimed Sandbox boundary was not in the execution path** | Explicit transport; `evaluate_authorized` refuses unverified transports | `test_backend.TransportTests`, `test_boundary.HostBoundaryExposure.test_authorized_evaluation_refuses_the_host_transport` | host |

## Output boundary

The staging and response directories are ACL-locked while the child runs, and the
child drops its token to low integrity before importing the candidate.

The owning user holds `WRITE_DAC`, so a deny ACE alone is removable. The fixture
resolves the account SID, uses it as the `icacls` principal, captures each
command's exit code and output, snapshots the resulting ACL, then attempts the
writes. Observed on the host:

```
sid  S-1-5-21-68253507-2885846877-556075993-1001
remove_deny:response   rc=5   ...\response: Acces refuse.
reset:response         rc=5   ...\response: Acces refuse.
grant_full:response    rc=5   ...\response: Acces refuse.
takeown:response       rc=1   ...ownership... "C:\...\response".
remove_deny:staging    rc=5   ...\staging: Acces refuse.
reset:staging          rc=5   ...\staging: Acces refuse.
grant_full:staging     rc=5   ...\staging: Acces refuse.
takeown:staging        rc=1   ...ownership... "C:\...\staging".
ACL after              DENY ACE still present for the user
```

`rc=5` is `ERROR_ACCESS_DENIED`, which is locale-independent. The test asserts
that value for the `icacls` attempts, asserts that no command reported a usage
error (`/?`), and asserts the deny ACE survived.

Two real bugs surfaced while making this evidence trustworthy:

1. `subprocess.run(..., text=True)` under the console code page returned
   **`rc=0` with an empty capture** for localized `icacls` output. Every ACL
   assertion would have been vacuous. Fixed by pinning `utf-8` with
   `errors="replace"`.
2. `takeown /f DIR /r /d y` is a **syntax error** on a non-English system
   (`/d` expects the localized answer). The command never attempted the takeover.
   Fixed by dropping `/r` and `/d`.

## Residual risks

1. **No Windows Sandbox run exists.** Every result above is host evidence. The
   Sandbox transport, agent, handshake acceptance and mapped-folder ordering are
   `NOT_RUN`.
2. **The Sandbox image ships no Python.** `--write-sandbox-config` therefore emits
   a `LogonCommand` pointing at `C:\h3-py\python.exe`; the operator must stage a
   portable interpreter into the read-only mapping. This is a preflight
   requirement, not something the code can arrange.
3. **Mapped-folder ACL behaviour is unverified.** Inside the Sandbox the
   supervisor skips ACL locking of the mapped folders (`lock_staging=False`,
   `lock_response=False`) because mappings reject ACL edits; it relies on the
   read-only mapping and on integrity levels. Preflight step 1 measures this.
4. **The host-local transport remains able to read the oracle**, by design and
   by measurement. It must never be used for study data. Rows it produces carry
   `authorized: false` and `isolation_verified: false`.
5. **Process and memory caps are configured but not stress-tested.**
6. **No verdict layer.** `oracle.score` computes `k`, `C`, `max_f`, eligibility
   and saturation. Base-algorithm classification, supported cells and the
   PASS/WEAK/FAIL verdict are not ported.

## Test evidence

```
python -m unittest discover -s tests -v
Ran 57 tests in 93.161s
OK
```

Full log: `tests/unit-test-log.txt`. Manifest: `MANIFEST.json`
(`python make_manifest.py --check` → `manifest OK`).

## Generation access, measured

`opencode-cli.exe` v2.2.0, probed without a model call: all three frozen model IDs
are present and `h3-generator` resolves with no permission leak under
last-match-wins resolution (`evidence/opencode-config.json`).

This does **not** establish that inference succeeds under the required no-tools
profile: no model call was made, and the free-tier 403 caveat is untested.
