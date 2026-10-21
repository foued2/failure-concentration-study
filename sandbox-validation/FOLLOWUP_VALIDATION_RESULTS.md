# Follow-up execution and model-interface checks

Date: 2026-10-21

## Bounded execution fixtures

Ran `restrictive-bounded-runner-validation.wsb` in Windows Sandbox. It retained the prior restrictions: networking, clipboard redirection, vGPU, audio, video, and printer sharing disabled; Protected Client enabled; no mapped folders; VM memory configured at 2048 MB. The harness contained only controlled PowerShell fixtures.

| Check | Result | Observed evidence |
|---|---|---|
| Timeout terminates a process tree | PASS | A root PowerShell process waited for a start gate, was assigned to a 256 MiB Job Object with kill-on-close, then spawned a 90-second child. The 1.5-second supervisor timeout terminated both; parent and child were confirmed exited. |
| Bounded per-job memory limit | PASS | A separate worker was assigned to a 128 MiB Job Object. It attempted at most eight 32 MiB allocations (256 MiB total); allocation stopped at `LIMIT:2` and the worker completed. The allocation remained inside the 2048 MB Sandbox VM. No host memory stress was run. |

The guest displayed **2 PASS, 0 FAIL**. The result capture is `sandbox-bounded-runner-window.png`.

These results verify the tested Windows Job Object pattern inside this Sandbox configuration. They do **not** verify an integrated pilot runner: the pilot tools still only record/validate rows, while `study.features.load_solver` imports and executes source in the current process (`study/features.py:15-27`), and the historical `scripts/run_pilot.py:32` calls that loader. No generated solver was run.

## Model-generation interface inspection

No credential values were printed or stored in this report.

- The installed Codex CLI reports version `0.160.1`; its login-status command returned logged in. A read-only, ephemeral text-only `codex exec --json` request returned `OK` with exit code 0. The CLI output did not expose the effective default model ID. An explicit request for `gpt-6.1-sol` returned exit code 1; the failure detail was not retained, so that model is not considered verified.
- Claude Code `2.1.187` is installed, but its `auth status` returned exit code 1. No Claude credentials file was present in the checked user location; no usable Claude generation path was established.
- The `GEMINI_API_KEY` environment variable was non-empty (its value was never displayed). Authenticated read-only `models.list` and `models.get` requests succeeded. The catalog returned `models/gemini-3.8-flash` (display name `Gemini 3.8 Flash`, API version field `3.0`) and advertised `generateContent` support.
- Two text-only `generateContent` interface checks for that Gemini model, each asking only for `OK` with temperature 0 and a 4-token output cap, timed out (`TaskCanceledException`) at 20 seconds and 60 seconds. No solver code was requested or returned. Catalog access therefore succeeded, but Gemini inference access was not verified.

The Codex CLI is a callable text-generation route, but its effective model identifier is unavailable from the captured CLI metadata. The Gemini model has a known ID but its generation endpoint timed out. No model was adopted as the pilot generator in this follow-up, and no solver-generation attempt occurred.

## Current blockers and disposition

1. **Production execution path:** implement and validate a pilot runner that executes diagnostic and evaluation calls inside the tested isolation boundary, enforces process-tree timeout/resource limits, and retains the raw evidence chain. Do not use the current host-import loader for generated code.
2. **Generator declaration:** either expose the Codex CLI's effective model identity (or explicitly freeze the documented CLI-default procedure with that metadata marked unavailable), or establish a working generation endpoint for a named model. The Gemini `generateContent` endpoint did not complete within the bounded checks.
3. **Evidence transfer/retention:** the fixtures used no mapped folders. The pilot needs a reviewed way to provide only the declared inputs and retain row-level outputs without exposing unrelated host files; that path is not implemented or validated here.

The natural-solver pilot remains at **0 solver-generation attempts and 0 solver outcomes**. The previous Sandbox result remains accurately qualified: its 2048 MB ceiling was observed, not stress-tested. This work adds bounded Job Object checks; it does not test concentration or correctness prediction.
