# V9 security and measurement report

**Date:** 2026-10-28
**Branch:** `dev/h3-footprint-v9-implementation-2026-10-28`
**Base:** review branch, 0 commits behind `h3-footprint-v8-freeze-2026-10-27`
**Status:** implementation; not frozen; no generation or evaluation authorized.

This report maps each V8 defect to the implementing control and to the test
that exercises it. Where a test ran only on the development host, that is stated.
No Windows Sandbox isolation evidence exists yet.

## Threat model

The candidate is arbitrary untrusted Python with the same OS user as the
Sandbox supervisor. It may read and write any path it can reach, spawn
processes, replace interpreter state, and emit arbitrary output. The property
that must hold is not "the candidate cannot print" but:

> The candidate cannot learn a reference answer, and cannot cause a probe to be
> scored correct unless `solve` returns the correct value.

Application-level controls (an AST denylist) are explicitly not relied on.
V8's denylist permitted `io.open` and `sys.modules`; V9's fixtures use both.

## Findings and controls

| # | V8 finding | V9 control | Test |
|---|---|---|---|
| 1 | Candidate can replace the worker's response function (`sys.modules["__main__"]._emit`) | Candidate code never shares an interpreter with reference data or scoring. The child prints a raw value; the host compares it. Replacing the emitter in the child changes only the child's own untrusted output. | `test_boundary.test_compound_read_and_forge_attack_never_passes`, `test_stdout_hijack_cannot_improve_score` |
| 2 | Expected values readable in the Sandbox (mapped read-only) | No reference data enters the Sandbox image at all. `sandbox-runtime/` is exactly four files; `oracle.py` stays on the host. Only `{n, edges, s, t}` crosses. | `test_secrecy.test_runtime_contains_only_supervisor_and_child`, `test_secrecy.test_no_reference_data_anywhere_in_runtime`, `test_secrecy.test_active_job_is_one_body_and_one_input` |
| 3 | `subprocess.run(timeout=5)` leaves descendants alive | Every child is assigned to a Job Object with kill-on-close, memory and active-process limits. Timeout terminates the job and *verifies* `ActiveProcesses == 0` before the response is published. | `test_process_tree.test_timeout_kills_descendants` (asserts the grandchild pid is dead) |
| 4 | `--pure` is not a tool boundary | Versioned agent with every documented permission key denied, pinned `OPENCODE_CONFIG_CONTENT`, no `--auto`. Effective rules are resolved with last-match-wins and must all return `deny`. | `test_generation.*`; live check in `evidence/opencode-config.json` |
| 5 | Eight-body cap unenforced | `select_accepted` keeps the first 8 in response order; overflow is recorded with hashes and never counted. Any tool event, nonzero exit or empty response rejects the batch. | `test_generation.test_eight_body_cap_is_enforced`, `test_overproduction_is_recorded_not_counted`, `test_tool_event_rejects_the_whole_batch` |
| 6 | Gate/Runbook sequence conflict | `V9_RUNBOOK.md` puts the isolation probe and rendezvous test before any generation, and the generator is code-gated on `V9_AUTHORIZE_GENERATION=1`. | `V9_RUNBOOK.md`; gate in `generate_v9.main` |

## Additional V9 controls

**One-item active job.** The host publishes exactly one body and one probe
input, waits for the response, and refuses to publish the next job unless the
previous response exists and reported `tree_empty: true`
(`controller._require_previous_tree_dead`).

**Output boundary.** The staging and response directories are ACL-locked while
the child runs, and the child drops its token to low integrity before importing
the candidate. Read-only mapping is not used as a write boundary.

**ACL removal is tested, not assumed.** The V8 review established that the
owning user holds `WRITE_DAC`, so a deny ACE alone is removable. The `boundary_probe`
fixture runs `icacls /remove:d`, `/reset`, `/grant` and `takeown` against both
directories before attempting writes. Observed result on the host:

```
CMD_FAIL icacls ... /remove:d ...
CMD_FAIL icacls ... /reset ...
CMD_FAIL icacls ... /grant ...
CMD_FAIL takeown ...
BLOCKED ..\response\evil.json PermissionError
BLOCKED ..\staging\job.json PermissionError
BLOCKED ..\response\response-forged.json PermissionError
```

## Residual risks and limitations

1. **The child still controls its own stdout.** It can emit a `V9RESULT` line
   of its choosing, including after the runner's line. This is by design: the
   value is treated as data. It buys the candidate nothing beyond a guess — the
   `stdout_hijack` fixture guesses `0`, hits `Z4`'s true answer by coincidence,
   and still fails 29 of 30 probes.
2. **Process and memory caps are configured but not stress-tested.** The
   process-count cap is enforced by the Job Object; a dedicated exhaustion test
   is not yet written.
3. **Repository-level integrity.** V9 has no frozen manifest yet; hashes are
   produced by `make_manifest.py` at freeze time.
4. **Sandbox behaviour is unverified.** All tests above ran on Windows 11 on the
   development host. Job Objects, ACLs and low-integrity semantics are the same
   in Windows Sandbox, but that must be demonstrated, not assumed.
5. **No verdict layer.** `oracle.score` computes failures, `k`, `C`, `max_f`,
   eligibility and saturation. Base-algorithm classification, supported cells and
   the PASS/WEAK/FAIL verdict are not ported from V8 in this increment.

## Test evidence

32 tests, 0 failures:

```
python -m unittest discover -s tests -v
Ran 32 tests in 65.343s
OK
```

Full log: `tests/unit-test-log.txt`.

## Generation access, measured

`opencode-cli.exe` v2.2.0 was located at
`%LOCALAPPDATA%\Programs\@opencode-aidesktop\resources\opencode-cli.exe` and
probed without any model call. All three frozen model IDs are present in the
local catalog, and the `h3-generator` agent resolves with no permission leak
under last-match-wins resolution. This replaces the earlier undocumented claim
that the free models had been removed from the local installation.

It does **not** establish that inference succeeds under the required no-tools
profile: no model call was made, and the free-tier 403 caveat is untested.
