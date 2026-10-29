# H3 V10 hosted execution and provider amendment

**Status: DRAFT, NOT FROZEN. No candidate-generation or candidate-evaluation authorization.**

This document records the proposed differences between the frozen V3 footprint protocol and the hosted V10 engineering route. It is intentionally not a replacement for the V3 freeze and must not be used to label future V10 data as an unchanged V3 run.

## 1. Scientific footprint rules to preserve

The study remains a footprint-feasibility gate for the same directed shortest-path problem with non-negative integer edge weights. The instrument remains the frozen 30-probe suite: six families in the order R, Z, A, I, S, U, with five probes per family.

For each valid solver body, the diagnostic failure count is k, the total number of failed probes. For k greater than zero, C is the largest family failure count divided by k. The eligible range is 2 through 24 inclusive. The primary degeneracy statistic is the proportion of eligible bodies with a completely failed family, meaning maximum family count equal to five, with the frozen 0.80 cutoff. PASS still requires at least three supported cells, at least two distinct eligible k values, and at least 40 independent generation groups. The predeclared futility checks remain at batches 100, 200 and 300, with minimum 10, 20 and 30 eligible provenance groups respectively, and the hard cap remains 400 batches of eight requested bodies each.

The frozen V3 branch and tag are not to be edited. V10 records an engineering alternative on this separate branch.

## 2. Material generation amendment: direct provider routes

The frozen V3 generator uses the OpenCode routing aliases for DeepSeek V4.1 Flash, GLM-5.3-Flash and MiMo V2.6 Flash. V10 has proposed direct API routes instead:

- DeepSeek V4.1 Flash through Token Harbor, using its explicit deepseek-v4.1-flash:free model route.
- GLM-5.3-Flash through NVIDIA NIM, using z-ai/glm-5.3-flash.
- MiMo V2.6 Flash through Token Harbor, using its explicit mimo-v2.6-flash:free model route.

These routes have not been proven equivalent to the earlier OpenCode aliases. Model naming is not an immutable serving snapshot, and endpoint/provider changes can alter model builds, serving behavior, rate limits, response formatting and quota. The generator identity therefore changes and must be stated as such. A future result would be conditional on these exact direct routes and their recorded service behavior, rather than silently described as an unchanged V3 run.

The prompt variants and round-robin assignment can be carried over, but that alone does not make the generators equivalent.

**Current availability caveat (checked 2026-10-29):** Token Harbor's live [free-model catalogue](https://tokenharbor.ai/models?category=free) and [MiMo V2.6 Flash model page](https://tokenharbor.ai/models/mimo-v2.6-flash%3Afree) currently list `mimo-v2.6-flash:free` as a free-tier model. The static [FAQ](https://tokenharbor.ai/faq) still names MiMo V2.5 in its free-model summary, so those public pages are inconsistent or the FAQ is stale. The live catalogue establishes the advertised listing, not successful account access, request limits, or sufficient quota for this study. The manual provider smoke has not been run. Do not substitute MiMo V2.5 without an explicit generator amendment. Additional route references: [DeepSeek V4.1 Flash free-route page](https://tokenharbor.ai/models/deepseek-v4.1-flash%3Afree) and [NVIDIA GLM-5.3-Flash prototype endpoint](https://build.nvidia.com/z-ai/glm-5-3-flash/build). V3 requests eight independent implementations in one call. Splitting that into eight separate calls would change call-level provenance groups and the futility gate; it must not be done silently. If a provider cannot return eight complete bodies within its output constraints, the batch is recorded as underproducing. It is not repaired by extra calls or best-of selection.

The current provider adapter is a route-smoke client. A new pure planning module (generation_plan_draft.py) copies the frozen V3 round-robin assignment, prompt variants, and fenced-code extraction into testable functions. It makes no network calls and emits metadata only. The live generation call and raw-response artifact writer have not been enabled. Its default maximum output is 64 tokens and its configured API call uses temperature 0.0. V3 invoked its original route without an explicit temperature setting. Those smoke settings are not a valid generation configuration. Before generation, the exact prompt, temperature, maximum output tokens, timeout, endpoint/model identifier and extraction procedure must be frozen. The output-token cap and quota feasibility for eight bodies per call remain unverified.

## 3. Material execution amendment: hosted Ubuntu container

V10 replaces local Windows Sandbox execution with a GitHub-hosted Ubuntu job and a pinned Python Docker image. The candidate container has no network, a read-only root filesystem, bounded memory, CPU and process count, no-new-privileges, minimal supervisor capabilities, read-only candidate/input mounts, and a separate writable report path. The supervisor runs the candidate body in a fresh unprivileged child for the preflight and each probe. The executor is not given reference answers, a provider key, or the repository checkout.

The V3 static import/call policy and undefined-global check are applied before Docker is launched. Module-load failures are excluded before k is assigned. An exception or timeout while executing a particular probe becomes a failed probe, matching the frozen worker's core classification. A forged or malformed supervisor protocol response invalidates the candidate, with no k, rather than being treated as an ordinary probe failure.

This is a different operating-system and isolation boundary from Windows Sandbox. Passing the hosted smoke tests does not prove that all container escapes are impossible or that the two runtimes are equivalent. The hosted threat model and this exact execution path must be part of the V10 pre-candidate freeze.

## 4. Output-capture policy difference still requiring an amendment

V10 caps candidate-level captured stdout and stderr at 16 KiB each. If the cap is exceeded, V10 reports an output-overflow failure for that probe and never accepts the return value as a valid answer. This limit helps contain hostile output, but it is not identical to frozen V3, whose worker captures output without this bounded capture. A body that prints a large amount and otherwise returns a correct integer could therefore receive a different label under V10.

Recommendation for review: retain the bounded capture for safety and explicitly prespecify that overflow counts as a failed probe in the V10 amendment. Do not claim exact V3 classification equivalence, and do not collect candidate data until this rule is included in the V10 freeze.

## 5. Separate execution and scoring

The execution job produces only untrusted per-probe predictions. It binds each response to its phase, sequence, probe ID and empty-process-tree check. The execution report includes a hash of the actual canonical graph-input payload and the ordered probe IDs. A separate scoring job checks the actual body hash, the probe-payload hash, the order, and the expected-answer implementation before deriving a profile.

The scoring job also verifies that the relevant V3 instrument, expected values, gate code and gate specification still match the SHA-256 digests in the frozen V3 manifest. It never loads or executes the candidate body. The current end-to-end test uses only a hand-written, non-generated control: it returned correct answers on all 30 probes and has k = 0, C = 0. This is a plumbing control, not a sample from the generator and not a scientific result.

## 6. What has and has not been verified

The hosted workflow has passed controls for the pinned container settings, no-network behavior, read-only boundaries, the V3 static rejection policy, preflight exclusion of a module-load failure, exclusion of malformed per-probe protocol output, rejection of output floods, timeout cleanup of a spawned child process, exact probe-payload hash binding, and separate-job scoring of the 30-probe hand-written control.

The workflow has not generated a solver candidate, run the candidate footprint gate on generated bodies, made a provider request, or performed held-out work. The manual provider smoke has not been dispatched. Therefore, provider reachability, quota, rate limits, eight-body output capacity and cost-free completion of the frozen 400-batch schedule remain unknown.

## 7. Preconditions for any future candidate run

Before any candidate-generation call is permitted:

1. Run the manual provider access smoke only after the repository secrets are set by the owner and the tiny test requests are approved. It makes at most one short request per route whose key is present, and missing keys do not cause a request. It does not generate candidates.
2. Review the redacted evidence for provider/model IDs, reachability, response format, usage, rate-limit headers, output limits and quota. A successful short response does not establish that 400 eight-body batches are feasible.
3. Freeze the direct route and model identifier for each generator, the exact prompt variants, sampling/output settings, timeout and request-level provenance rules. Preserve the 400-batch schedule, the 8-body request size, the stop checkpoints and the no-best-of rule unless a separately reviewed amendment says otherwise.
4. Freeze the bounded output-overflow rule and the hosted execution boundary, with the tests and file hashes included in a new V10 pre-candidate manifest. The manifest must state zero candidate bodies and zero generation calls.
5. Require separate explicit authorization before the first candidate-generation call. If the provider allowance cannot support the predeclared schedule, the outcome is a feasibility failure, not permission to increase the budget or quietly change the design.

Until those conditions are satisfied, this branch remains execution infrastructure and protocol-review material only. No change to the frozen V3 branch, tag, instrument or existing terminal findings is authorized by this draft.
