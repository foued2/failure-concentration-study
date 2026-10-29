# H3 V10 hosted-executor prototype

Status: engineering prototype only. This folder does not freeze a scientific protocol and does not authorize candidate generation or evaluation.

## What this prototype proves

The objective is to remove any requirement for a local AI agent, local runner, local paths, or Windows Sandbox on the researcher's PC.

A GitHub-hosted workflow can run code and return artifacts in fresh standard VMs. The prototype workflow runs:
- host regression tests on a hosted Windows VM;
- a harmless, fixed-fixture isolation smoke test on a separate hosted Ubuntu VM.

The smoke test does not load the repository, its oracle, candidate answers, or model API credentials. It tests a disposable Python process inside a Docker container with no network, a read-only root filesystem, non-root UID, dropped capabilities, no-new-privileges, a PID cap, memory/CPU limits, read-only inputs, and a dedicated writable output directory. It records container observations and returns an artifact.

## Proposed production architecture

A versioned protocol amendment is required before using this architecture for H3 data.

1. **Generation job:** makes calls to the predeclared model families through explicit, recorded provider adapters. API keys are stored as GitHub Actions secrets. This job records prompts, model IDs, endpoint, parameters, request identifiers, raw responses and hashes. It does not execute generated code.
2. **Execution job:** runs on a fresh hosted VM. It receives only candidate bodies and public probe inputs, not the reference answers, oracle, model-provider keys, write token, or research repository. It executes each candidate in a constrained, networkless container and returns untrusted prediction records. It does not score candidates.
3. **Scoring job:** runs on a different fresh VM, receives only prediction records, checks their schemas and hashes, loads the trusted probe answers, and scores the records. It never imports or executes candidate code.

This structure moves the trust boundary to the hosted VM/job separation and the candidate container. It is not equivalent to the existing Windows Sandbox protocol and must be independently reviewed, threat-modelled, tested and frozen before any candidate data are collected.

## Provider constraint

The original OpenCode model routes are currently unavailable in the project environment. Direct API routes for the same model families may exist, but the exact serving revisions, sampling parameters, quotas, terms and retention must be checked and recorded before adoption. Provider replacement must never be silently described as an unchanged frozen run.

## Forbidden until separately authorized

- no generated solver candidates;
- no candidate evaluation or scoring;
- no held-out work;
- no changes to the frozen V3 branch;
- no secrets in artifacts or logs;
- no merging into the research branch.

This is a feasibility prototype, not an H3 scientific result.
