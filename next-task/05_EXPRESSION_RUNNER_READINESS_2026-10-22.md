# Expression Runner Readiness Review

Status: **`GO_FOR_FINAL_REVIEW`**
Generation status: **`HOLD_NOT_AUTHORIZED`**

No model call was made in this phase. No natural-solver pilot run or provider generation was started.

This report supersedes the prior version of this report. The expression design/calibration evidence at `29c925a` remains unchanged.

## Evidence completed

| Item | Result |
| --- | --- |
| Expression design and calibration evidence | committed at `29c925a` |
| Original calibration run | `calibration-20261022T084750Z-288f2ac1`; **PASS** |
| Original calibration integrity | **PASS**, 2,317 checks, 14 captures |
| Strict return-type calibration run | `calibration-strict-20261022T112115Z-efe7bb1a`; **PASS** |
| Strict calibration captures | 14 captures, 420 rows; 390 complete exact-int envelopes, 30 target crashes, no timeouts |
| Strict calibration adapter hash | `d7a96e7d59f92f86858a29104c74a141bb9debeb9a85d9d98b58cd11cce55a67` |
| Frozen bank hashes | diagnostic `ca1ba993...47507847`; evaluation `e227c24d...e163946d` |
| Runner preflight, strict adapter | **PASS** |
| Runner prompt matches preregistration | **yes** |
| Runner prompt SHA-256 | `6796c14b29d0157fc618f51c4d4de90f8143857e620f94f2e332449aee143dff` |
| Offline runner/adapter tests | **24/24 PASS** |
| Strict calibration model calls | **0** |
| Model calls in this phase | **0** |

The runner is `next-task/run_expression_pilot.py`; tests are in `next-task/tests/`. The pilot path uses `next-task/pipeline_expression_strict/`.

## Output-contract correction

The declared `solve(expr: str) -> int` contract is now enforced at the guest boundary and host boundary:

- the strict guest adapter records the actual Python return type before serialization;
- only `type(value) is int` is accepted; `isinstance` is not used because `bool` subclasses `int`;
- numeric strings, booleans, floats, `None`, and non-int objects are rejected;
- a wrong-type return is a failed answer in the input's family, not an ineligible execution error;
- malformed envelopes and malformed stdout remain invalid answers;
- duplicates remain retained without re-execution.

This rule is frozen in `03B_OUTPUT_CONTRACT_AMENDMENT_2026-10-22.md` before the strict adapter and its calibration run. The old adapter and `calibration-20261022T084750Z-288f2ac1` were not modified; the strict calibration is separate evidence.

## Strict calibration result

The reference and all six prespecified mutants were rerun through the strict adapter in a new real Sandbox calibration run.

The authoritative strict run is `calibration-strict-20261022T112115Z-efe7bb1a`. It is the run that records `strict_adapter_sha256`, which `03C` requires the pilot to check at launch. The earlier strict run `calibration-strict-20261022T102511Z-381f62e1` produced the same pass result but did not record the adapter hash; it remains as historical evidence and is not the launch reference.

- reference: 30/30 diagnostic passes and 30/30 evaluation correct;
- all six mutants: 5/5 target-family diagnostic failures and 5/5 target-family evaluation failures;
- no non-target family failures;
- every row tree-terminated; no timeouts;
- 0 model calls and 0 generation attempts.

The 30 crash rows are target-family rows from `unary_rejected`, `single_digit_tokenizer`, and `whitespace_rejected`, whose defects raise on those inputs. They count as failed probes under the existing transport/eligibility rule. The exact-int enforcement itself is covered by the new wrong-type tests, not by those crashes.

The original calibration evidence still validates: `validate_expression_calibration.py` reports **PASS**, 2,317 checks, 14 captures.

## Test results

`python -m unittest discover -s next-task/tests -q` produced **24 tests, 0 failures, 0 errors**.

New coverage includes:

- valid integer returns accepted;
- numeric-string returns rejected as `wrong_type` and counted as failures (`k = 30`);
- `True` and `False` rejected;
- `42.0` and `None` rejected;
- malformed envelopes and malformed stdout invalid;
- duplicate bodies retained without re-execution;
- exact-type handling uses `type(value) is int`;
- guest payload still contains no expected values, family labels, or oracle data.

## Remaining limitations

1. **Generation is not authorized.** The declared route is Gemini `gemini-3.5-flash-lite`; it must be confirmed and explicitly approved. Codex is not a current route.
2. **Backend snapshot is unavailable.** Exact model reproducibility cannot be claimed.
3. **The calibration panel is hand-built.** It covers six specified defects, not the full space of natural solver errors, and it is not evidence for the concentration hypothesis.
4. **Source screening is best-effort.** `eval`, `exec`, `compile`, and direct `open` are blocked, but the screen is not a security boundary. `ast.literal_eval` remains unblocked and is not a complete arithmetic evaluator for this grammar.
5. **Input visibility remains partial.** The guest can read its current suite's expressions, but not expected values, family labels, oracle code, or host records during the diagnostic session.
6. **A null pilot result is possible.** Given the earlier ceiling pattern, all-`k=0` remains a real possibility; `CEILING_NO_FAILURE_VARIATION` covers it. The authorization decision should accept 30 requests as the cost of this task-level feasibility check, not as a test of the concentration hypothesis.

## Recommendation

**GO** for the explicit final review of the corrected runner and output contract.

**HOLD** on generation until that review confirms the provider route and authorizes the 30 requests. No generation should start from this report alone.

The runner, strict adapter, strict calibration run, tests, `03B`, and this report remain uncommitted in the working tree; the original design/calibration evidence is committed at `29c925a`. Commit the corrected set scoped before any `--execute` run; do not stage unrelated files.
