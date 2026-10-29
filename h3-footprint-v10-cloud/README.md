# H3 V10 hosted-executor prototype

Status: engineering prototype only. This folder does not freeze a scientific protocol and does not authorize candidate generation, candidate evaluation, or scientific scoring.

## Verified hosted execution, 2026-10-29

The GitHub-hosted workflow run completed successfully:

https://github.com/foued2/failure-concentration-study/actions/runs/40833639560

Evidence from that run:

- The existing V9 host regression suite passed: 168 tests on Windows Python 3.12 and 168 tests on Windows Python 3.14.
- The 37 V10 provider, container-executor, fixture, probe-binding, preflight-phase, load-error, output-overflow, and protocol-exclusion tests passed on both Python versions.
- The frozen V9 manifest check passed.
- The actual V9 execution gate continued to refuse candidate evaluation with its expected fail-closed exit code.
- The independent keyless Ubuntu container smoke verified a non-root child, network denial, read-only root, blocked host-canary access, bounded memory/CPU/process count, read-only inputs, and a separately writable output channel.
- A hand-written, non-generated control solver ran across the full 30-probe V3 input set. Its prediction report was passed to a separate hosted scoring job. That job re-verified frozen V3 hashes and reference values, checked the actual body bytes and canonical probe payload, then verified 30/30 control predictions. The test-only failure profile was k = 0, C = 0.
- A hostile timeout control spawned a grandchild and looped. The isolated supervisor timed it out and verified that the container process tree and temporary work area were cleaned.
- The container protocol distinguishes module-load failure from an exception inside solve(), binds responses to the requested phase, excludes malformed or forged per-probe protocol records before assigning k, and rejects output-overflow records rather than allowing them to become valid answers.
- The execution and scoring jobs bind on both the ordered probe IDs and a SHA-256 digest of the exact canonical graph-input payload, not IDs alone.

The 30-probe fixture artifact contains only the input fields (probe ID, graph, source, target) and the hand-written control solver. It does not contain expected answers. The candidate execution job has no repository checkout, oracle, expected-answer file, or model-provider key. The scoring job runs separately after the execution report is produced.

**Scope limitation:** this is evidence for the exact hosted runner configuration and fixed control tests only. It does not prove every possible container escape is impossible, does not test model-generated solvers, does not establish that the V3 model-generation frame is available, and is not an H3 scientific result. The existing V9 execution gate remains closed.

## What this prototype is for

The objective is to remove any requirement for a local AI agent, local runner, local paths, or Windows Sandbox on the researcher's PC. Code is committed on this isolated GitHub branch; GitHub-hosted runners execute it and return logs and artifacts.

A versioned protocol amendment is required before using this architecture for H3 data.

1. **Generation job:** calls the predeclared model families through explicit, recorded provider adapters. Provider credentials stay in GitHub Actions secrets. The generation job records prompts, model IDs, provider endpoint, sampling parameters, request identifiers, usage and hashes. It never executes generated code.
2. **Execution job:** runs on a fresh hosted VM. It receives only candidate bodies and public probe inputs, not reference answers, oracle, provider keys, repository write token, or research repository. It executes each solver call in a constrained, networkless container and returns untrusted prediction records. It does not score.
3. **Scoring job:** runs on a separate fresh VM, receives prediction records, validates their schema and hashes, loads trusted reference outputs, and scores them. It never imports or executes candidate code.

This trust model is different from the existing Windows Sandbox protocol. It must be independently threat-modelled, tested, and frozen before any H3 candidate data are collected.

A known V10 protocol difference remains unresolved for scientific use: solver stdout/stderr capture is capped at 16 KiB each, and overflowing a capture becomes a failed probe. Frozen V3 captures this output without that cap. This engineering safeguard changes classification for a solver that prints excessively, so it requires an explicit V10 protocol amendment and freeze before any candidate data are collected.

## Provider feasibility

The direct provider adapter and its unit tests are in this folder. The manual-only workflow at .github/workflows/h3-v10-provider-smoke.yml sends at most one short, non-candidate request per configured model route. It stores redacted request metadata, rate-limit headers where returned, usage, response length and a response digest, never the raw response text.

Proposed routes:

- DeepSeek V4.1 Flash through Token Harbor's explicit deepseek-v4.1-flash:free route.
- MiMo V2.6 Flash through Token Harbor's explicit mimo-v2.6-flash:free route.
- GLM-5.3-Flash through NVIDIA NIM's prototype endpoint.

DeepSeek and MiMo use TOKENHARBOR_API_KEY. GLM uses NVIDIA_NIM_API_KEY. The provider workflow is manual-only. Missing keys produce a blocked report without sending a request for that route; no candidate generation occurs.

**MiMo route availability is unverified.** The current Token Harbor FAQ lists MiMo V2.5 among its free models but does not mention MiMo V2.6. Treat the proposed mimo-v2.6-flash:free route as a hypothesis for the manual smoke, not as confirmed available free capacity. Do not silently switch to MiMo V2.5; that would change the generator and requires an explicit protocol amendment. See the [protocol amendment draft](PROTOCOL_AMENDMENT_DRAFT.md).

These are free-tier access paths, not unlimited compute. Token Harbor says its free models use a value-based rolling seven-day allowance that stops when exhausted. NVIDIA NIM offers free prototype access under trial terms. The actual allowance, serving availability, and output capacity must be tested before committing to the original 400-batch schedule. Even if all routes answer a tiny smoke prompt, that does not establish enough quota for 3,200 candidate generations.

Official provider documentation:
- NVIDIA NIM access: https://docs.api.nvidia.com/nim/docs/product
- GLM-5.3-Flash: https://build.nvidia.com/z-ai/glm-5-3-flash
- DeepSeek V4.1 Flash: https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash
- Token Harbor free allowance: https://tokenharbor.ai/faq

To perform the provider smoke without touching the local PC, add the API keys as GitHub repository secrets under Settings → Secrets and variables → Actions, with the exact names above, then manually launch **H3 V10 provider access smoke** in Actions. Never paste keys into chat, source files, commit messages, issues, or logs. The provider smoke costs at most one tiny request for each route whose key is present. As of this checkpoint, the provider smoke has not been dispatched and no provider requests or candidate-generation calls have been made.

The original OpenCode aliases are routing aliases. Replacing the route or provider can change serving behavior even where model naming looks similar. Any provider substitution requires an explicit protocol amendment and pre-data freeze; it cannot be silently labelled an unchanged V3 run. The draft records the changes and outstanding blockers; it is not frozen.

## Forbidden until separately authorized

- no generated solver candidates;
- no H3 candidate evaluation or scientific scoring;
- no held-out work;
- no changes to the frozen V3 branch;
- no secrets in artifacts or logs;
- no merging into the research branch.

This is verified execution infrastructure, not an H3 scientific result.
