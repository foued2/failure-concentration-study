# Final Runner Readiness Gate — 2026-10-21

## Decision

**HOLD — the full Python runner is not ready for the natural-solver feasibility pilot.** No model-written solver was generated or run. The CLI candidate and exact proposed one-shot prompt are recorded in `PILOT_SPEC.md`, but the required end-to-end calibration did not finish.

## What was checked

The prior 11 PowerShell Sandbox integration cases were not repeated. This check used the actual Python adapter, existing reference oracle and feature functions, the 30-probe diagnostic battery, and the existing 20-input evaluation bank. The four solvers were hand-built software controls that intentionally return wrong answers on selected diagnostic input identities. No evaluation outcomes or diagnostic rows from this failed run are used as scientific evidence.

The prepared banks passed the host-side checks: 30 unique diagnostic input identities, 20 unique evaluation identities, and no exact overlap. The planned Python path used separate Sandbox sessions for each controlled body’s diagnostic suite, each evaluation suite, and protocol controls. Only one `current-input.json` was mapped to the guest at a time; the complete banks, oracle and host-authoritative records remained unmapped.

## Failure and retained evidence

The first streaming strategy tried to atomically replace the mapped current-input file. Windows rejected the rename because the mapped file was in use. After changing to a single in-place overwrite, the guest consumed inputs and reported progress through 25 of 30 probes for `pattern_zero`, but the host did not observe input 30 before the 45-second per-input gate expired. The session ended without a finalized capture; the host therefore did not validate a complete 30-row transport, reconstruct the diagnostic labels or compute `k` and `C` for that body. The 20-input evaluation bank was not run.

The failed runs are preserved under `python-pipeline-integration/streamed-run-20261021T130430-02845bac/` and `streamed-run-20261021T130611-4923806a/`. The second run has empty host-authoritative and capture directories because no complete capture was finalized. Its console output records progress at 5, 10, 15, 20 and 25 of 30, followed by a timeout waiting for 30/30. The initial failed run records the `PermissionError` from atomic replacement. These artifacts are failures of the integration attempt, not solver or model observations.

| Measure | Result |
|---|---:|
| Model-written generation attempts | 0 |
| Model-written solver outcomes | 0 |
| Controlled Python diagnostic inputs observed in the second attempt | 25/30 for the first zero-failure fixture; batch incomplete |
| Complete controlled 30-probe fixture records | 0 |
| Evaluation-bank labels produced by this integrated path | 0 |
| Host-reconstructed feature vectors from completed streamed batches | 0 |

## Specification status

`PILOT_SPEC.md` now records the proposed new population as one-shot Codex CLI `0.160.1`, selector `gpt-6-luna`, dated 2026-10-21, with an exact SSSP prompt, output contract and available invocation settings. The earlier `Reply exactly OK...` call remains an interface smoke test only. Backend model version, immutable snapshot, and unexposed sampling settings are explicitly unavailable. This is a new, procedure-specific population, not a MIMO reproduction.

The specification is **not frozen for collection**: the exact Python diagnostic plus separate evaluation path has not passed. The previously authorized limits remain unchanged: at most 100 one-shot attempts, at most 100 unique evaluation inputs (the existing bank has 20), no replacement sampling, and no outcome-driven selection.

## Next decision

Do not begin model generation. The exact blocker is reliable completion and retention of all 30 per-input Python results within the current Sandbox streamed-input mechanism; until that works, the host cannot validate the expected family counts, `k`, `C`, or the separate 20-input correctness records through the integrated path. Resolve this specific completion/transport failure within the already authorized runner scope, or stop and reassess the execution design. No further infrastructure track, predictive analysis, or cap expansion is justified by this failed check.

This result does not change the scientific evidence: concentration has neither been shown useful nor shown unhelpful for natural solvers. The pilot remains at zero natural-solver attempts and zero natural-solver outcomes.
