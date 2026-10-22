# Expression Task Pilot Preregistration

Status: **`PREREGISTERED_DRAFT_FOR_REVIEW`**

This document defines a new exploratory natural-solver pilot. It does not authorize generation, analysis, or a confirmatory claim. The expression banks and the calibration panel are separate from the earlier SSSP banks and findings.

## Purpose

Test whether independently generated first-attempt solvers on a bounded expression-evaluation task produce a fixed-`k`, different-`C` comparison with independently measured evaluation correctness variation.

The question is not whether one metric predicts correctness in general. The pilot is a feasibility check on this task and generation procedure.

## Target and claim boundary

- **Task:** `solve(expr: str) -> int` for a bounded integer arithmetic expression.
- **Population:** solver bodies returned by one-shot requests to the specified generation procedure below. This is a procedure-specific output population, not a representative sample of all natural solvers.
- **No claim** is made that the new task reproduces the earlier SSSP results or that any observed pattern generalizes beyond this procedure.
- **No generation is authorized by this document.** A separate review and authorization are required before the first request.

## Task contract

The expression grammar permits:

- non-negative integer literals;
- binary `+`, `-`, and `*`;
- parentheses;
- optional ASCII spaces;
- a unary minus before a primary.

Division and exponentiation are excluded. The returned value must be an exact integer. Parentheses may be nested; unary minus may appear before a parenthesized expression.

### Exact prompt

> Write one Python implementation of a function `solve(expr)` that evaluates a bounded integer arithmetic expression given as a string. The expression contains non-negative integer literals, binary operators `+`, `-`, `*`, parentheses, optional ASCII spaces, and a unary minus before a primary. There is no division or exponentiation. Return the exact integer result as an `int`. Make the function self-contained and use only the Python standard library. Do not read files, access the network, or print. Return only Python source code defining `solve`, with no Markdown fences, explanation, example usage, or tests. Write the first solution that comes to mind; do not self-review or revise it.

The prompt deliberately contains no test expressions from either bank.

## Generation procedure

- **Provider:** Google Gemini API.
- **Model identifier:** `gemini-3.5-flash-lite`.
- **Endpoint:** `/v1beta/models/gemini-3.5-flash-lite:generateContent`.
- **Generation settings:** `temperature = 1.0`, `maxOutputTokens = 4096`; no other sampled settings are asserted.
- **Authentication:** existing `GEMINI_API_KEY`; credential values are never recorded.
- **Attempts:** exactly 30 ordered one-shot requests, `attempt-0001` through `attempt-0030`.
- **No retries:** no retry, replacement, prompt tuning, outcome-driven selection, or second attempt for a failed response.
- **Raw retention:** every response, failure, parse result, and source screen result is retained.
- **Model identity limitation:** the backend snapshot is unavailable; exact reproducibility is not claimed. The model identifier is only the API model string.

The existing Gemini runner is SSSP-specific and must not be reused unchanged. A new expression prompt/outcome runner must be implemented and reviewed before generation. The calibration runner demonstrates the expression execution path but does not generate model output.

## Derived bodies

- Normalize newlines for body identity.
- Retain duplicate attempts; duplicates are not replacement samples.
- Distinct canonical bodies are those with distinct normalized source hashes after parsing.
- A failed parse is retained as an invalid attempt and does not produce an eligible body.
- Source-policy rejection is retained; rejected sources are not executed.

## Diagnostic bank

Use the frozen 30-probe expression diagnostic bank at `next-task/banks/diagnostic.json`: five probes for each of six families.

- `F1` operator precedence
- `F2` left associativity
- `F3` parentheses
- `F4` unary minus
- `F5` multi-digit tokenization
- `F6` whitespace

For each eligible body, record each probe outcome, each family failure count, and:

- `k` = total number of failed diagnostic probes;
- `C = max(family failure count) / k` when `k > 0`, otherwise `C = 0`.

This is the same concentration definition used in the earlier study.

## Evaluation bank

Use the frozen 30-input expression evaluation bank at `next-task/banks/evaluation.json`, five inputs per family. The exact expression strings are disjoint from the diagnostic bank.

For each eligible body:

- record every evaluation input, raw solver output, host-side expected value, and correctness;
- set `Y = 1` only if all 30 evaluation inputs are correct, otherwise `Y = 0`;
- retain the evaluation correct count for descriptive reporting.

The bank must not be edited after the calibration freeze. Any change creates a new task version and requires a new preregistration and calibration.

## Execution boundary

Use the existing suite-level Windows Sandbox path with the task-specific expression adapter:

- one suite per body per bank;
- a fresh Python worker for each expression;
- networking disabled;
- 10-second worker timeout;
- 128 MiB Job Object memory limit;
- host-side expected values, correctness, family counts, `k`, and `C`;
- every transport row must be tree-terminated.

The complete current suite is guest-readable during that suite's session. Source screening is a best-effort control, not a security boundary. Results must not be described as securely blinded against a solver that inspects its mounted suite.

## Eligibility and integrity gates

A body is eligible only if:

1. its source is accepted by the static screen;
2. it produced 30/30 diagnostic rows and 30/30 evaluation rows;
3. every row is tree-terminated and not timed out;
4. bank hashes, raw captures, and row identities validate against the freeze record.

Attempts with parse failures, source rejection, incomplete suites, or invalid captures remain in the manifest and are reported; they are not silently dropped or replaced.

## Feasibility decision rule

The pilot reports raw outcomes and checks for a **fixed-`k`, different-`C` comparison** with evaluation separation.

Define a fixed-`k` group as eligible distinct canonical bodies sharing the same `k > 0`. A qualifying comparison requires:

1. at least two distinct `C` values in that fixed-`k` group;
2. each reported `C` value is supported by at least two distinct canonical bodies;
3. evaluation correctness differs between those body sets, with at least one body at 30/30 and at least one body below 30/30.

If such a comparison exists, feasibility is **observed** for this pilot. This is an existence result, not an estimate of prevalence or a confirmatory effect.

If no such comparison exists, feasibility is **not demonstrated within this pilot**. The report must identify the missing condition, such as:

- no incorrect bodies;
- incorrect bodies but no repeated `k`;
- repeated `k` but no `C` separation;
- `C` separation without evaluation correctness separation;
- incomplete or ineligible suites.

Failure to observe the comparison does not establish that no predictive relationship exists, that the task is easy, or that concentration is invalid.

## Analysis boundary

- No model fitting, threshold selection, feature selection, or concentration-metric selection.
- No confidence interval, p-value, or causal claim.
- No dropping of ineligible bodies from the retained manifest.
- No post hoc bank edits or prompt changes.
- The pilot is exploratory and underpowered for prevalence estimation.

## Planning constants

| Item | Value |
| --- | --- |
| Generation attempts | 30 |
| Maximum retries | 0 |
| Diagnostic probes per body | 30 |
| Evaluation inputs per body | 30 |
| Diagnostic families | 6 |
| Probes per family | 5 |
| Planned generation route | Gemini `gemini-3.5-flash-lite` |
| Backend snapshot | unavailable |
| Generation now | **not authorized** |
| Confirmatory claim | **not authorized** |

## Frozen inputs

- `next-task/banks/diagnostic.json` — SHA-256 `ca1ba993ba3bcc6c3c2d011c49cd51e0f5eb32ff8f8cb0421768553c47507847`
- `next-task/banks/evaluation.json` — SHA-256 `e227c24d9bfea7f734b3a249015d33f15d3a2619e62ff5f3a4d8a557e163946d`
- `next-task/banks/FREEZE.json` — freeze record and post-freeze stop rule.

## Required review before generation

- confirm or replace the declared model and provider route;
- confirm the exact prompt and output contract;
- implement the expression generation runner and verify it does not reuse the SSSP adapter or prompt;
- verify that the generation runner writes only the intended prompt and does not expose either bank to the model;
- confirm generation budget and halt handling;
- explicitly authorize generation.
