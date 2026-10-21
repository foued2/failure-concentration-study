# Runner Readiness Check

Date: 2026-10-21

## Status

**`PRODUCTION_RUNNER_NOT_READY`**. No solver-generation request for solver code was made, no solver body was executed, and the feasibility pilot remains at zero generation attempts and zero solver outcomes. The existing `PILOT_SPEC.md` and pilot records were not changed.

## Generation interface

- Codex CLI version: `codex-cli 0.160.1`.
- Authentication: Codex reports logged-in ChatGPT authentication; no credential values were read or recorded.
- `codex debug models` listed the supported CLI model slug `gpt-6-luna`.
- One explicitly selected, text-only smoke request completed with exit code 0 using `codex exec --ephemeral --sandbox read-only --model gpt-6-luna --json` and prompt `Reply exactly OK. Do not use tools or run commands.` The final response was `OK`.
- The CLI did not return a backend model/version or immutable snapshot. `codex doctor` reported the selected model as `<default>` for its general environment and `server model present false` in the connectivity diagnostic. Thus `gpt-6-luna` is the exact requested CLI identifier, but the provider's backing snapshot is unavailable. No inference is made that this reproduces MIMO.
- The smoke request was not a solver-generation attempt. No generation prompts, solver bodies, or pilot observations were created.

## Sandbox transfer check

A one-off test used Windows Sandbox with networking and clipboard disabled, Protected Client enabled, a read-only input mapping, and a separate empty writable output mapping. There were no other mapped folders.

| Check | Result | Evidence |
|---|---|---|
| Guest reads declared input | PASS | Guest received the exact `input-v1` content. |
| Guest attempts to change read-only input | PASS | Write was denied; host input remained `input-v1`. |
| Guest writes result through output mapping | PASS | Host received a machine-readable result JSON. |
| Guest attempts a write to a host path outside mapped folders | PASS, limited | The guest-side attempt failed; a host marker outside the mappings remained `host-unchanged`. |

This establishes basic transfer and mount-scope behavior for the tested configuration. It does not validate a production runner or a hostile process attempting to falsify records. The guest code had write access to the mapped output folder by design. No separate guest identity, write-protected evidence channel, or other mechanism preventing solver code from tampering with that output was tested. A result channel writable by the code under test is not yet an auditable evidence channel.

## Remaining runner blockers

1. **Evidence integrity across the writable output mount.** The only demonstrated machine-readable return path is a writable host mapping. A future solver process could potentially alter or forge files in that mapped directory. This needs an enforceable separation between untrusted solver processes and the trusted result writer, followed by a targeted test showing the solver cannot modify the evidence channel while the runner can.
2. **Guest runtime and integrated launcher.** The available host Python runtime has not been launched from a read-only guest mapping. No guest supervisor has yet connected the actual 30-probe battery, per-case oracle, feature extraction, prepared evaluation bank, job-object limits, and row-level output schema end to end.
3. **Complete runner validation.** The existing Sandbox job-object fixtures establish process-tree termination and a bounded allocation case, but they are not integrated with the diagnostic/evaluation runner. No integrated trusted-fixture calibration has been executed inside Sandbox.

Until these items pass, generated solver code must remain disabled. The text-generation route is now explicitly selectable as `gpt-6-luna`, with provider snapshot identity unavailable; this does not remove the runner blocker.

## Follow-up: trusted result channel test (2026-10-21)

This is an appended follow-up to the readiness report. Earlier findings above are retained unchanged.

### Test arrangement

- Windows Sandbox retained networking, clipboard, audio/video/printer sharing, and vGPU disabled; Protected Client enabled; VM memory set to 2048 MB.
- Only two folders were mapped: the pilot-specific test input folder read-only and a dedicated, otherwise empty test output folder writable. No project root, credentials, or unrelated host folders were mapped.
- The trusted supervisor ran as `WDAGUtilityAccount`. The test created a separate standard local account, `fc_trust_worker`, with a random transient password held only in guest memory.
- The supervisor applied an ACL to the output channel granting access to itself and SYSTEM. The worker was given a distinct workspace. Only harmless PowerShell access and resource-limit fixtures ran; no solver code was generated or executed.

### Results

| Check | Result | Evidence |
|---|---|---|
| Distinct standard worker account launched | PASS | Worker identity was `D988DD58-CC1A-4\fc_trust_worker`; it could write in its designated workspace. |
| Worker cannot read supervisor output | **FAIL** | Worker read the supervisor-owned canary despite the applied ACL. |
| Worker cannot overwrite or forge output records | **FAIL** | Overwrite and new-file forgery succeeded. Delete of the separate delete-canary was denied. Supervisor later detected changed canaries. |
| Worker cannot modify mounted runner or input | PASS | Attempts to change the read-only mapped harness and input were denied; their host-side bytes remained unchanged. |
| Worker cannot write tested protected system path | PASS | Write to `C:\Windows\System32\fc-trust-escape-marker.txt` was denied. This checks that path only, not every guest filesystem location. |
| Job timeout terminates worker and descendant | PASS | A 1.5-second timeout terminated the separate-account worker and its 90-second child; both were confirmed exited. |
| Job memory cap applies to separate worker | PASS | A 128 MiB job cap stopped a fixture attempting up to 256 MiB; it reported `LIMIT:2` and exited. |

The first attempt stopped at ACL construction because `Set-Acl` could not translate an identity on the mapped share. A follow-up using `icacls` applied the ACL successfully, but the worker still read, overwrote, and forged channel files. This is direct evidence that the tested mapped-folder permissions do not separate the supervisor from a different standard guest account. The failure is not merely a missing ACL setup step.

### Disposition

**Reject the current writable mapped-folder result-channel architecture.** A guest process with the solver's unprivileged account can alter the channel used to recover results. The process-tree timeout and memory limits worked under that account, but they do not repair evidence integrity.

The smallest next infrastructure direction is a supervisor-controlled capture boundary where the authoritative records stay outside the guest and the guest cannot write those records. Windows Sandbox's mapped-folder return path, as tested here, does not provide that separation. Use a VM or execution service with a host-controlled RPC/pipe capture mechanism, or another boundary that has an independently enforceable one-way result channel. Do not add further ACL workarounds to this Sandbox setup.

No integrated diagnostic/evaluation runner was implemented, no pilot-spec change was made, and no solver-generation or solver-execution attempt occurred. Counts remain **0 generation attempts / 0 solver outcomes**. The Codex CLI candidate remains recorded as `--model gpt-6-luna`; the backend version and immutable snapshot remain unavailable. No further generation request was made.
