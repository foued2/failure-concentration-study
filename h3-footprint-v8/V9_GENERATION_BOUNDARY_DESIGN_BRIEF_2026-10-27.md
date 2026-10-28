# V9 design brief: constrain the OpenCode generation mechanism

**Date:** 2026-10-27  
**Base:** V8 frozen at h3-footprint-v8-freeze-2026-10-27 (d5b002cf0802b54b5a18b81e6bb99a9566cdd5ff)  
**Status:** pre-generation design only. Do not alter V8 or generate candidates under this note.  
**Amended:** 2026-10-28, to incorporate the documented agent-permission interface and free-tier compatibility caveat.

## 1. Why a new version is needed before the first V8 batch

V8 has generated no candidates, so the generation method can be corrected before it affects the sample. The frozen script currently invokes:

    opencode run --pure --format json --model <frozen-model> --dir <shared-WORK> <prompt>

OpenCode documentation defines --pure as running without external plugins, not as disabling built-in tools. The default Build agent has built-in tools enabled, and common tool permissions are permissive unless configured otherwise. The prompt's sentence “Do not read files, access the network...” is an instruction to the model, not an enforced permission boundary. In addition, the default generator launches three calls concurrently and points all of them at the same generated/work directory.

The new generator must make the intended treatment real: model-generated code bodies from a fixed prompt/model call, with no file tools, shell tools, browsing tools, delegated agents, or access to neighbouring candidate or reference files during generation.

## 2. Constants to preserve

Keep these scientific/sampling constants unchanged:

- Exact model IDs: opencode/deepseek-v4.1-flash-free, opencode/glm-5.3-flash-free, opencode/mimo-v2.6-flash-free.
- Prompt variants: direct, menu, simple, with the frozen batch-number mapping.
- 400 batch IDs, 0 through 399; eight requested bodies per batch.
- Each batch is one provenance group because its outputs share the same generation request. Eight bodies from one request must not be counted as eight independent groups.
- No model substitution, outcome-guided prompt changes, manual cherry-picking, or budget widening.
- Generation remains separate from candidate execution. The generation stage can call OpenCode only after candidate execution is otherwise gated, but it must not import or run the returned Python.

## 3. Tool permissions and workspaces

For each batch:

1. Create a unique, otherwise empty work directory for that batch. Do not let concurrent model calls share writable files.
2. Use the documented OpenCode agent permission interface rather than relying on the prompt. The current CLI supports `opencode agent create --path ... --description ... --mode ... --permissions ...` (alias `--tools`); the permissions option is a comma-separated allowlist, and tools omitted from the list are denied. A checked-in agent Markdown file with explicit `permission` frontmatter is another auditable representation and may be necessary to specify all relevant keys. The `--permissions` CLI allowlist documents a subset of permission names; the broader permission schema also includes `list`, `external_directory`, `question`, and `doom_loop`, and wildcards can match custom/MCP tools. Use a dedicated primary generation agent with no file, shell, web, task/subagent, skill, LSP, question, or external-directory capability. Set every supported tool family to deny in the versioned agent config, including wildcard/custom-tool rules, then inspect the effective loaded config. Do not infer completeness from the flag's short allowlist alone. Include the actual agent/config file in the frozen hash manifest. See the [agent-create CLI docs](https://dev.opencode.ai/docs/cli/) and [permissions reference](https://dev.opencode.ai/docs/permissions/).
3. Never pass `--auto`. It auto-approves permission requests that are not explicitly denied. Do not allow user/project/global config to restore tools. Launch from a controlled environment with unintended `OPENCODE_PERMISSION`, `OPENCODE_CONFIG_CONTENT`, `OPENCODE_CONFIG`, and inherited config paths removed or explicitly pinned; record sanitized environment settings, effective loaded agent, CLI version, and config hashes.
4. Verify the installed CLI's effective configuration and event schema without launching an out-of-schedule model call. The profile must be inspected as actually loaded, not only read as a file. Preserve the exact invocation and event schema in the freeze record.
5. Preserve the complete JSON event stream. A batch with an executed tool operation, shell operation, write, external read, web operation, task/subagent call, or permission escalation must not yield accepted candidates. Treat attempted but denied tool use as a policy event too: record the batch, reject its body outputs, and do not re-prompt in the same batch.
6. Do not share session IDs or continue a previous agent conversation between batches. Every model call must be a new independent top-level request with its assigned model and prompt variant.

### OpenCode free-tier compatibility is an unresolved constraint

Do not assume that a fully denied toolset will be accepted by all three OpenCode free models. Upstream reports describe free-tier requests returning a 403 “free tier can only be used from within OpenCode” when `bash` or all tools are denied, while some configurations with permissions set to `ask` succeed. See [upstream issue #50627](https://github.com/anomalyco/opencode/issues/50627) and [upstream issue #49433](https://github.com/anomalyco/opencode/issues/49433). These issues are reports, not a guarantee about the installed version or every model.

This creates a real compatibility test, not permission to weaken isolation. First inspect configuration locally without model calls. Do not use `OPENCODE_PERMISSION={"*":"deny"}` as an assumed universal fix. If the fixed models reject the required no-tools profile, or require executable tools to remain allowed, record the frame as operationally incompatible and stop. Do not switch to `ask`/allow as an unrecorded workaround if that would expose tools to the model, and do not substitute another model or generation interface without a new protocol version.

OpenCode CLI documentation describes `--pure` as “without external plugins”; the flag does not establish a no-tools runtime by itself.

## 4. Response acceptance and hard caps

The current generator asks for eight blocks but stores every valid block in a response. A new version must enforce a deterministic response policy.

- A batch is acceptable only if the CLI exits successfully and the JSON event stream is structurally valid and complete under the pinned CLI protocol. If the CLI reports an error or exits nonzero, reject the entire response even if partial text contains code. Preserve the raw output and error for diagnosis.
- Extract valid complete Python modules in response order. They must parse and contain exactly one top-level synchronous solve function, with the full module retained.
- Accept at most the first eight valid modules in response order. If fewer than eight exist, accept those found and record the shortfall. If more than eight exist, record every overflow module's normalized hash and position, but do not store it in the candidate corpus or count it as a body.
- Never sort, score, re-prompt, or cherry-pick the first eight using code quality or later probe outcomes.
- Record total fenced blocks, syntactically valid blocks, valid solve modules, accepted count, overflow count/hashes, duplicates, command return code, timeout/error, tool events, prompt hash, model ID, prompt variant, batch ID, response hash, and raw-response path.

The body ceiling is 8 accepted modules per batch, therefore no more than 3,200 accepted modules across 400 batches before duplicate deduplication. Each body must retain the first successful batch ID as its provenance when an identical normalized hash appears again. Duplicate emissions are still logged in the attempt record but do not create another body or an independent group.

## 5. Failure and futility policy

A failed model request is not a new candidate group, but its fixed batch ID remains attempted and is not silently retried with a new prompt. Record whether that ID failed due to unavailable model, quota, authentication/provider error, timeout, invalid event stream, tool-policy violation, malformed response, or zero extracted functions. Do not count failed request bodies toward the 150 rejected-body target.

The generation gate must use the number of completed batch IDs consistently with the frozen futility logic. Before running a new version, verify with unit tests that:
- batch IDs remain 0–399 when the command is run in 100-batch segments;
- repeated segment commands do not rerun previously recorded batch IDs;
- a failed batch is recorded once, not counted as a successful generation group;
- an overproduced response cannot increase accepted bodies beyond eight;
- no failed response or forbidden tool event contributes candidate bodies;
- duplicates retain first-seen batch provenance;
- a short response is recorded without replacing its missing blocks with code from another model or prompt.

The futility rule remains the predeclared rule at checkpoints 100/200/300 requiring at least 10/20/30 eligible provenance groups. A generation-access failure or denied tool use can trigger the operational futility stop; it must not be interpreted as a scientific finding about concentration.

## 6. No-model-call local diagnostics

Before the first study batch, use the separate [OpenCode free-access diagnostic](OPENCODE_FREE_ACCESS_DIAGNOSTIC_2026-10-27.md) to confirm local catalog visibility and environment settings without generating text. Current public docs still list the original three free IDs, but this does not guarantee that they work for the user's account or installation.

If the frozen model frame is not usable, stop the generation run. Do not replace a failed model with another free model or call another service under the same data label. Any substitution changes the population sampled and requires a separately documented protocol version.

## 7. Acceptance criteria before freezing V9

The V9 generator is not ready to freeze until:

- deterministic unit tests cover event parsing, no-tools policy, complete and failed response handling, extraction, exact eight-body cap, overflow, duplicate handling, batch IDs, and work-directory isolation;
- the effective no-tools configuration can be inspected by a local metadata/config command without a model call, and compatibility with the frozen free-tier models is treated as a gate rather than an excuse to relax permissions;
- the CLI version and supported JSON event schema are recorded;
- FREEZE.json hashes all code/config artifacts affecting the sampling mechanism;
- the unchanged model/prompt schedule and budget are clearly stated;
- no model calls or candidate execution occur during design/testing.

Only then can a live generation request be counted as batch 0 of the actual frozen run. That first batch must use the no-tools configuration and all standard logs; it must not be spent on an unrecorded smoke test.

No study candidates or H3 conclusions are created by this brief.
