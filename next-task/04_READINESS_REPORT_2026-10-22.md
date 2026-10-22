# Expression Task Readiness Report

Status: **`CALIBRATION_PASSED_READY_FOR_REVIEW_NOT_AUTHORIZED_FOR_GENERATION`**

No model calls were made in this phase. No natural-solver pilot was started.

## What was completed

- Verified the earlier bug-detection counts against committed records; no transcription error.
- Wrote a static task-selection rubric before selecting the task.
- Selected bounded integer expression evaluation without searching over model outcomes.
- Built a 30-probe diagnostic bank and a separate 30-input evaluation bank, five per family, with disjoint exact expression strings.
- Checked every bank record against two independent host-side oracles: a recursive-descent evaluator and an AST evaluator.
- Froze the banks before calibration.
- Built a seven-implementation panel: one correct reference and one faulty implementation for each of the six defect families.
- Ran the panel through the existing suite-level Sandbox path with a task-specific expression adapter.
- Independently validated every raw capture.

## Calibration evidence

Run: `next-task/calibration-20261022T084750Z-288f2ac1/`

| Check | Result |
| --- | --- |
| Calibration status | **PASS** |
| Reference control | 30/30 diagnostic passes; 30/30 evaluation correct |
| Faulty variants | 6/6 executed and target-detected |
| Diagnostic target coverage | 5/5 probes for every family |
| Evaluation target coverage | 5/5 inputs for every family |
| Cross-family failures | none |
| Raw captures | 14 valid capture directories |
| Raw rows | 30 per capture |
| Integrity checks | 2317 PASS |
| Model calls | 0 |
| Generation attempts | 0 |

Per-family calibration:

| Faulty implementation | Target | Diagnostic target failures | Evaluation target failures |
| --- | --- | ---: | ---: |
| `precedence_flat` | F1 | 5/5 | 5/5 |
| `minus_right_assoc` | F2 | 5/5 | 5/5 |
| `parens_dropped` | F3 | 5/5 | 5/5 |
| `unary_rejected` | F4 | 5/5 | 5/5 |
| `single_digit_tokenizer` | F5 | 5/5 | 5/5 |
| `whitespace_rejected` | F6 | 5/5 | 5/5 |

`CALIBRATION_RESULT.json` records the full result, `CALIBRATION_REPORT.md` records the human-readable summary, and `INTEGRITY.json` records the independent validation of every capture, row, bank hash, source hash, and gate condition.

## Initial invalid attempt

An earlier attempt, `calibration-20261022T083345Z-38a56eb3`, reused the SSSP guest adapter and therefore crashed on every expression. It is **not** calibration evidence. It was moved outside the repository to:

`C:\Users\pakla\AppData\Local\Temp\opencode\expression-calibration-20261022T083345Z-38a56eb3-sssp-adapter-failure`

The frozen banks were not changed in response. The valid run used `next-task/pipeline_expression/` and passed.

## Frozen banks

- Diagnostic: `next-task/banks/diagnostic.json`
  - SHA-256 `ca1ba993ba3bcc6c3c2d011c49cd51e0f5eb32ff8f8cb0421768553c47507847`
- Evaluation: `next-task/banks/evaluation.json`
  - SHA-256 `e227c24d9bfea7f734b3a249015d33f15d3a2619e62ff5f3a4d8a557e163946d`
- Freeze record: `next-task/banks/FREEZE.json`
- Post-freeze rule: do not edit either bank or the freeze record. If a future calibration fails, report gaps and create a new task version rather than tuning observed banks.

## What the calibration supports

It supports the limited claim that these frozen banks distinguish the six prespecified hand-built expression defects, with independent coverage in both banks and a clean correct reference. It also validates the task-specific execution path, raw-capture handling, host-side scoring, and source screening used by the calibration.

It does **not** establish that natural solvers will make these defects, that the task is difficult enough to produce failure variation, that `C` predicts correctness, or that the earlier SSSP result was caused by test insensitivity.

## Remaining gaps before generation

1. **No expression generation runner exists.** The existing Gemini runner is SSSP-specific: its prompt, adapter call, and outcome function are for `solve(n, edges, s, t)`. Reusing it would repeat the invalid-adapter failure. A new runner must be implemented and reviewed before any request.
2. **Model route is not yet authorized.** The currently available route is Gemini `gemini-3.5-flash-lite`; Codex is blocked until `2026-11-19T18:55:00Z`, and DeepSeek is unavailable. The declared route must be confirmed or replaced during review.
3. **Backend snapshot is unavailable.** Exact model reproducibility cannot be claimed.
4. **Input visibility remains best-effort.** The guest can read its mounted current suite during execution; source screening is not a security boundary.
5. **The panel is hand-built.** The calibration proves coverage for these six defects, not for the full space of natural errors.

## Review decision requested

Review `03_PILOT_PREREGISTRATION_2026-10-22.md`, the exact prompt, the 30-attempt fixed design, the feasibility decision rule, and the provider route.

If approved, the next implementation step is a new expression generation runner with:

- the exact preregistered prompt;
- one-shot attempts with no retries;
- the expression guest adapter;
- the frozen diagnostic and evaluation banks;
- raw body and capture retention;
- the same source screen and Sandbox boundary;
- no outcome-based stopping or replacement sampling.

Generation remains **not authorized** until that runner is reviewed and the run is explicitly approved.
