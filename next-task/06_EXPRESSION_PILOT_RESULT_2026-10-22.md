# Expression Pilot Result

Status: **`COMPLETED_REPEATED_K_BUT_NO_C_SEPARATION`**

Run: `next-task/expression-pilot-gemini-20261022T163536Z/`

This run was explicitly authorized by Foued after the corrected runner, strict adapter,
output contract, and launch preconditions were committed at `1ee7eef`. The run started at
`2026-10-22T16:35:36Z`. No further run is authorized or started.

## Request reconciliation

| Item | Count |
| --- | ---: |
| Planned and consumed request slots | 30 |
| Model-written generation outputs | 27 |
| Generation failures | 3 |
| Source-policy rejections | 2 |
| Exact duplicate bodies retained without execution | 6 |
| Complete diagnostic/evaluation executions | 19 |
| Distinct canonical bodies | 21 |
| Eligible executed bodies | 19 |

The 30 slots reconcile as 19 executed + 2 rejected + 6 duplicate + 3 generation failure = 30.
No retry or replacement sample was made.

The three generation failures were one request timeout (`attempt-0019`) and two HTTP 503
provider errors (`attempt-0028`, `attempt-0029`). There was no authentication or usage-limit
hard block, so the run was not halted. Both source rejections (`attempt-0001`,
`attempt-0005`) were `syntax:invalid syntax`; they were retained and not executed. Two format
failures out of 30 is below the `03C` threshold of more than 10, so
`PROMPT_CONTRACT_FORMAT_PROBLEM` does not apply.

## Frozen inputs and execution boundary

| Item | Value |
| --- | --- |
| Repository commit at launch | `1ee7eef4f838af9ac3c2c71adedb2faabb5185fe` |
| Diagnostic bank SHA-256 | `ca1ba993ba3bcc6c3c2d011c49cd51e0f5eb32ff8f8cb0421768553c47507847` |
| Evaluation bank SHA-256 | `e227c24d9bfea7f734b3a249015d33f15d3a2619e62ff5f3a4d8a557e163946d` |
| Prompt SHA-256 | `6796c14b29d0157fc618f51c4d4de90f8143857e620f94f2e332449aee143dff` |
| Strict adapter SHA-256 | `d7a96e7d59f92f86858a29104c74a141bb9debeb9a85d9d98b58cd11cce55a67` |
| Provider / model | Google Gemini API / `gemini-3.5-flash-lite` |
| Output contract | exact `int`; `type(value) is int` |
| Predictive model fitted | no |

The guest could read the other expressions in its current suite. Expected values, family
labels, oracle code, and host records were not in the guest payload. Source screening is a
best-effort policy, not a security boundary. The backend snapshot is unavailable, so exact
model reproducibility is not claimed.

## Observed distribution

All 19 complete executions produced 30/30 diagnostic rows and 30/30 evaluation rows. Every row
was tree-terminated; no worker timed out. The `k` and `C` values below were recomputed from the
raw rows by the host-side implementation.

| `k` | `C` | Distinct bodies | Evaluation correct | Diagnostic family failures (F1..F6) |
| ---: | ---: | ---: | ---: | --- |
| 0 | 0.000000 | 6 | 30/30 each | `(0, 0, 0, 0, 0, 0)` |
| 2 | 1.000000 | 9 | 28/30 each | `(0, 0, 0, 0, 0, 2)` |
| 7 | 0.714286 | 1 | 23/30 | `(0, 0, 0, 5, 0, 2)` |
| 30 | 0.166667 | 3 | 0/30 each | `(5, 5, 5, 5, 5, 5)` |

Correctness varies across the pilot: 6 bodies are fully correct, 9 miss exactly two evaluation
inputs, one misses seven, and 3 fail every evaluation input.

## Fixed-`k` contrast

The frozen feasibility rule requires, within one `k > 0` group, at least two distinct `C`
values, each supported by at least two distinct canonical bodies, with evaluation correctness
differing between those body sets.

| `k` | `C` values present | Bodies per `C` | Evaluation contrast |
| ---: | --- | --- | --- |
| 2 | 1.000000 | 9 | none: one `C` value only |
| 30 | 0.166667 | 3 | none: one `C` value only |

The `k = 7` body is a singleton and therefore cannot support a contrast under the frozen
support rule. There is no fixed-`k` group with two adequately supported `C` values.

## Decision

The frozen criterion is applied exactly: feasibility is **not demonstrated** in this pilot.
The recorded missing condition is:

**`REPEATED_K_BUT_NO_C_SEPARATION`**

The pilot observed repeated `k` (`k = 2`, nine bodies; `k = 30`, three bodies) and observed
`C` variation only across different `k` values, not within a repeated-`k` group. It also
observed evaluation correctness variation, but not at a fixed `k` with supported `C`
separation.

This is not a falsification of the concentration hypothesis, evidence that the task is easy in
general, or a prevalence estimate. It is a task- and procedure-specific feasibility result.
Per `03A` and `03C`, the natural-solver route for this preregistered expression task ends here;
no harder task, follow-up run, or predictive analysis is authorized automatically.

## Integrity verification

An independent reconciliation script re-read every attempt directory, raw response, source hash,
source-screen record, host-authoritative diagnostic and evaluation result, bank record, and
protocol hash. It also recomputed every family count, `k`, `C`, evaluation correct count, and
the frozen feasibility state.

- Independent checks: **6,141 PASS**
- Errors: **0**
- `VALIDATION_ERRORS.json` present: **no**
- Frozen bank and strict-adapter hashes: **match**
- Protocol commit: **matches launch commit**
- Attempt slots: **30/30 reconciled**
