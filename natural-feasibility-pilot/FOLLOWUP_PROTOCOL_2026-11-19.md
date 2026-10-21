# Natural-solver follow-up protocol

**Status: FROZEN - NOT STARTED**

This document defines a separate follow-up allocation to the closed exploratory run
`natural-pilot-20261021T123319Z`. It does not reopen that run and does not authorize
any generation request before 2026-11-19 at 6:55 PM. The machine-readable freeze
manifest is `FOLLOWUP_PROTOCOL_2026-11-19.json`.

## Relationship to the closed run

- The closed run remains closed at 100 generation requests: 39 model-written outputs,
  61 usage-limit failures, 15 distinct canonical bodies, and 10 complete bodies.
- All 61 failures count against the closed run's cap. They are not excluded,
  reclassified, or transferred.
- The closed run's final state remains `HALTED_GENERATION_USAGE_LIMIT`.
- The follow-up has its own identifier and its own maximum of 100 generation requests.
  It is not an extension, relabeling, or retry of the closed run.
- No result from the closed run may be used to select, edit, or replace follow-up
  samples. The follow-up has no replacement sampling.

## Start condition

Do not start before **2026-11-19T18:55:00Z**. The provider stated 6:55 PM without a
timezone; this is a conservative reading. The runner enforces this floor for any label
beginning with `natural-pilot-followup` and records the actual start in
`protocol.json`.

The first generation invocation is itself the availability check. If it returns a
usage limit, quota, rate limit, or equivalent hard block, persist that attempt and halt
immediately. If it returns another hard failure, persist it and halt as
`HALTED_GENERATION_FAILURE`. Do not repeat the failed request.

There is no resume for a halted or capped follow-up run. A fresh allocation requires
new authorization.

## Frozen material

The follow-up retains the closed run's exact generation prompt, source screen,
diagnostic battery, evaluation bank, execution configuration, and feasibility rule.
The closed run's `run_bounded_pilot.py` remains untouched at its validated hash.
The follow-up uses a separate copy, `run_followup_pilot.py`, whose only changes are
operational: a distinct run label, the not-before guard, recording of failure kind,
and an immediate halt on the first failed generation request. Generation, screening,
execution, and evaluation logic are unchanged.

The authoritative SHA-256 hashes are in `FOLLOWUP_PROTOCOL_2026-11-19.json` under
`freeze_manifest`. Hashes are computed over UTF-8 text after universal-newline
normalization. Before starting, verify every hash matches. Do not edit a frozen file
to make a hash pass.

## Run command

From the repository root:

```powershell
py -3.14 natural-feasibility-pilot\run_followup_pilot.py --run-label natural-pilot-followup --not-before 2026-11-19T18:55:00Z
```

This creates a new directory named `natural-pilot-followup-<UTC timestamp>` and writes
the exact prompt, protocol metadata, attempts, results, report, and guest captures.

## Accounting and stopping

- Maximum: 100 generation requests. Every invocation counts, including failures.
- Stop immediately on the first non-generated response. Persist the attempt first.
- Do not retry, replace, or continue after a halt.
- Stop early only if the feasibility rule is demonstrated.
- If 100 requests are reached without demonstrating feasibility, stop and record
  `FEASIBILITY_NOT_DEMONSTRATED_WITHIN_CAP`.
- No predictive model is fitted. No concentration effect is tested. No claim may be
  made that concentration predicts correctness.
- Preserve all attempts, raw outputs, source-screen decisions, diagnostic records,
  evaluation labels, and guest captures.

## Feasibility rule

Feasibility is demonstrated only if some eligible fixed-`k` comparison has two
different `C` values, each supported by at least two distinct canonical bodies, and
independently scored correctness varies meaningfully across those bodies, with input
separation and record-integrity checks passing.

## Identity and reproducibility

Record the actual invocation time, run directory, model selector `gpt-6-luna`, and
Codex CLI version `0.160.1`. The backend snapshot/version is unavailable. No exact
reproducibility claim is made, and the selector name alone is not treated as proof of
backend identity.

## Scope limits

This follow-up is exploratory feasibility work only. It does not authorize a master
merge, push, tag, publication, Phase 1, G6b, predictive analysis, or changes to any
existing frozen study. The repository README remains `TERMINATED - INFEASIBLE` unless
the owner explicitly changes it.
