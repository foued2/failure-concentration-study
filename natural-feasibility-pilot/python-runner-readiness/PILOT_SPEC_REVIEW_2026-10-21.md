# Pilot Specification Review — 2026-10-21

## Decision

**Python execution and input-isolation checks passed. The natural-solver pilot is not yet ready to start, and the pilot specification is not frozen for the currently available generator/runner combination.** No model-written solver was generated or executed; counts remain zero generation attempts and zero solver outcomes.

This review is limited to the target, generator, runner, and evidence boundaries. It does not authorize collection.

## What this check established

The Windows Sandbox ran a read-only mapped Python 3.14 runtime and harmless Python fixtures. Each fixture ran as a fresh child process and received one current test input over standard input. The guest did not receive the repository, diagnostic battery, evaluation bank, reference oracle, or host authoritative records. Six explicit file-open attempts against those protected locations failed with `FileNotFoundError`.

The supervisor captured bounded raw stdout/stderr, recorded a deliberate attempt to forge the exact capture filename, replaced it after worker termination with a nonce-bound capture, and retained its authoritative readiness record outside the guest-writable mapping. The 128 MiB Windows Job Object limit produced `MemoryError` when a harmless fixture requested 256 MiB. A timed-out Python parent and child were both confirmed terminated. Malformed bytes, oversized output, and a nonzero exit were retained as untrusted execution results.

The retained machine-readable evidence and concise run report are in the adjacent `run-20261021T123554-9462bafd/` directory. All ten checks in that run passed. Earlier failed harness attempts remain in their own run directories and were not removed.

## Why the pilot specification is not frozen

1. `PILOT_SPEC.md` still names the unavailable MIMO session as its target procedure. The available alternative is Codex CLI `--model gpt-6-luna`, whose prior successful request was a text-only smoke prompt, not an SSSP solver-generation request. The CLI slug is known, but the provider backend snapshot is unavailable. Substituting it changes the target population and requires an explicit new generation specification; it cannot be represented as resuming the MIMO procedure.
2. The previous 11-case diagnostic integration used a hand-built PowerShell solver fixture. This Python check used harmless protocol fixtures with a single known answer. The Python process was not yet run through all 30 existing diagnostic probes, and the Python path was not connected end to end to the existing host oracle, `integration_runner.py` reconstruction, family-count aggregation, `k`, and `C` calculations.
3. Therefore, no single retained test currently demonstrates the full path for a Python solver: one current diagnostic input → Python execution → trusted host oracle comparison → 30-probe family counts and features. The components have passed separate controlled checks, but their combination remains unverified.

## Required state before collection

- Keep the current MIMO specification and records unchanged as historical evidence.
- Create a separately identified specification for a new generator population only after the Python execution path is integrated with the existing probe and host-reconstruction machinery. It must state the exact SSSP prompt and per-attempt invocation, the actual CLI model slug, available settings, and the unavailable backend snapshot.
- Validate the resulting Python path with the existing controlled concentration fixtures and host-side feature reconstruction, while continuing to expose only one current input to each worker invocation.
- Re-review that new specification and its records before any model-written solver executes.

This is a bounded integration gap, not evidence that Sandbox isolation failed. The test supports the stated accidental-misbehavior and naive-forgery threat model for the tested configuration; it does not establish resistance to a Sandbox escape or a determined guest-kernel attacker.
