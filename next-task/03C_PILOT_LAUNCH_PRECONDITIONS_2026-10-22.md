# Pilot Launch Preconditions

Status: **`PREREGISTERED_BEFORE_PILOT_AUTHORIZATION`**

No model call was made before or during this amendment. It does not authorize generation.

## Scoped code state

The corrected expression runner, strict adapter, tests, `03B`, strict calibration evidence, and this report set must be committed before `--execute`:

- one scoped commit containing only the corrected expression-runner set;
- no unrelated files;
- a clean `next-task/` worktree at launch;
- no tracked modifications anywhere in the repository.

At run start, `PROTOCOL.json` records the repository commit, runner SHA-256, prompt SHA-256, strict-adapter SHA-256, and frozen bank hashes.

## Strict-path assertion

The pilot must fail before generation if `pipeline_expression_strict/python_adapter.py` does not match the adapter hash recorded by the strict calibration run. The old `pipeline_expression/` adapter must not be silently selected.

## Format-failure interpretation

A format failure is an attempt whose generated response cannot be used as a solver source: rejected source, missing `solve`, syntax/import failure before probes, or otherwise non-executable output.

If more than 10 of the 30 requests are format failures, report `PROMPT_CONTRACT_FORMAT_PROBLEM`. Treat it as a prompt/extraction-contract problem, not as a generator-quality or concentration result. Do not revise the prompt during the run and do not add retries or replacement samples. Any follow-up requires a separate preregistration and authorization.

Format failures below that threshold remain ordinary retained attempts and are not evidence about the hypothesis.

## Null-result decision

The likely outcome may be `CEILING_NO_FAILURE_VARIATION`, with few distinct bodies. If the pilot is null:

- the natural-route attempt ends there;
- do not automatically build a harder task or start a fourth attempt;
- a harder task requires a new preregistration, new frozen banks, new calibration, and separate authorization;
- the null result is about this task and declared generator procedure, not the concentration hypothesis in general.

## Authorization

Satisfying these preconditions makes the runner ready for final authorization review. It does not itself authorize the 30 Gemini requests. Generation remains `HOLD_NOT_AUTHORIZED` until the separate explicit authorization decision.
