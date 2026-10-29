# H3 V10 hosted-executor prototype

Status: engineering prototype only. This folder does not freeze a scientific protocol and does not authorize candidate generation or evaluation.

## What has actually passed

A run on GitHub-hosted VMs completed on 2026-10-29:

- Existing V9 host regression suite on Windows with Python 3.12 and 3.14: both jobs passed.
- Existing V9 manifest verification: passed.
- The actual execution gate: it refused evaluation with its expected fail-closed exit code.
- A separate Ubuntu/Docker smoke test: passed for one harmless probe with no checkout, no oracle, no expected answers, and no API key. The job verified a non-root UID, read-only root filesystem, denied network, hidden host canary, read-only inputs, writable output, dropped capabilities, no-new-privileges, PID cap, 512 MiB memory cap and one-CPU cap.

Workflow run: https://github.com/foued2/failure-concentration-study/actions/runs/40825944453

This proves hosted execution works for the checked host tests and the exact disposable smoke body. It does not establish the full H3 candidate boundary, process-tree adversarial behavior, generation availability, or scientific validity.

## What the prototype is for

The objective is to remove any requirement for a local AI agent, local runner, local paths, or Windows Sandbox on the researcher's PC.

A versioned protocol amendment is required before using this architecture for H3 data.

1. **Generation job:** makes calls to predeclared model families through explicit, recorded provider adapters. API keys are stored as GitHub Actions secrets. This job records prompts, model IDs, endpoint, parameters, request identifiers, raw responses and hashes. It does not execute generated code.
2. **Execution job:** runs on a fresh hosted VM. It receives only candidate bodies and public probe inputs, not reference answers, oracle, model-provider keys, write token, or the research repository. It executes each candidate in a constrained, networkless container and returns untrusted prediction records. It does not score candidates.
3. **Scoring job:** runs on a different fresh VM, receives only prediction records, checks their schemas and hashes, loads trusted probe answers, and scores the records. It never imports or executes candidate code.

This structure moves the trust boundary to hosted VM/job separation and the candidate container. It is not equivalent to the existing Windows Sandbox protocol and must be independently reviewed, threat-modelled, tested, and frozen before any candidate data are collected.

## Provider feasibility

The direct provider adapter and its unit tests are in this folder. A manual-only GitHub Actions workflow (.github/workflows/h3-v10-provider-smoke.yml) makes exactly one tiny, non-candidate request per route and stores only redacted metadata and a response hash, never the response text.

Routes proposed for that smoke:

- DeepSeek V4.1 Flash through NVIDIA NIM, with NVIDIA_NIM_API_KEY.
- GLM-5.3-Flash through NVIDIA NIM, with NVIDIA_NIM_API_KEY.
- MiMo-V2.6-Flash through Token Harbor's :free route, with TOKENHARBOR_API_KEY.

The NVIDIA developer program documents free prototype access to NIM endpoints; the NVIDIA endpoints are under trial terms. Token Harbor documents its free routes as a rolling seven-day, value-based allowance that is exhausted and then stops; it is not unlimited. Availability and quotas must be measured through smoke tests and the provider dashboard before budgeting any generation run.

Official provider documentation:
- NVIDIA NIM API access: https://docs.api.nvidia.com/nim/docs/product
- DeepSeek V4.1 Flash: https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash
- GLM-5.3-Flash: https://build.nvidia.com/z-ai/glm-5-3-flash
- Token Harbor free-model allowance: https://tokenharbor.ai/faq

For a provider smoke only, add the two key values through GitHub repository Settings -> Secrets and variables -> Actions. Use the exact names NVIDIA_NIM_API_KEY and TOKENHARBOR_API_KEY. Do not paste keys into chat, source files, commit messages, issues, or logs. Then manually launch H3 V10 provider access smoke in Actions. The workflow does not run automatically on pushes and never runs candidate generation.

The original OpenCode model aliases are routing aliases. Replacing the route or provider can change serving behavior even when the underlying model name is similar. This needs an explicit protocol amendment and a pre-data freeze; it must not be presented as an unchanged V3 run.

## Forbidden until separately authorized

- no generated solver candidates;
- no candidate evaluation or scoring;
- no held-out work;
- no changes to the frozen V3 branch;
- no secrets in artifacts or logs;
- no merging into the research branch.

This is a feasibility prototype, not an H3 scientific result.
