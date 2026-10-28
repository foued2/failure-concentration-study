# H3 Footprint Gate V4: anonymous hosted-model proposal

**Status: PROPOSAL ONLY. NOT FROZEN. NO candidate-generation batch or candidate evaluation has been run.** V3 remains unchanged and retains its original three-model frame. V4 is a separate, explicitly different study population.

## Why V4 exists

The V3 generation frame names three OpenCode free backends that are no longer reliably available in the current workflow. Repeating setup attempts cannot restore those endpoints. A remote execution path is available through standard GitHub-hosted Actions, and a live smoke test on 2026-10-28 reached the anonymous OVHcloud AI Endpoints chat API without an API key. This prototype tests whether that path can support a new, separately frozen feasibility run.

V4 changes two material parts of the protocol:

1. **Generation population:** one model, `gpt-oss-120b`, served through the anonymous OVHcloud AI Endpoints lane, replaces V3's three OpenCode models. All claims from V4 must name this population. V4 cannot be described as a replication of the V3 three-model population and cannot support comparisons among generators.
2. **Execution boundary:** the Windows Sandbox-specific execution path is replaced by a constrained Docker-container boundary on an ephemeral GitHub-hosted Linux runner. This is not assumed equivalent to Windows Sandbox. It has to pass the fixed-fixture isolation battery, including host-file denial, network denial with a local control, read-only candidate source, writable scratch, process cleanup and resource-limit checks, before any generated solver is executed.

All other scientific choices are carried forward provisionally for the feasibility question: the SSSP task, the 30 fixed probes and six-family map, the (k) and (C) calculations, eligible range (2 \le k \le 24), the saturation statistic, the support thresholds, the 400-batch cap, eight requested candidates per batch and the futility checkpoints. Any final freeze must hash these choices along with the new provider and isolation design.

## Anonymous model access: observed fact and limitation

Endpoint: `https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/chat/completions`

Model id: `gpt-oss-120b`.

OVHcloud documents a rate limit for anonymous requests of two requests per minute per IP and model; shared-capacity throttling can still occur. See the [official troubleshooting documentation](https://docs.ovhcloud.com/en/guides/public-cloud/ai-machine-learning/ai-endpoints-troubleshooting). On 2026-10-28, a GitHub-hosted Ubuntu runner made one operational, non-study completion without an Authorization header. It returned HTTP 200, the expected health token, and 156 total tokens in 4.21 seconds. This smoke response is **not** candidate data, an availability guarantee, or evidence of scientific feasibility.

The proposed generator is serial and schedules request starts at least 35 seconds apart. It preserves exact raw text, the full JSON response, token usage, response id, prompt hash and provider errors. It stops and preserves progress when the anonymous endpoint remains throttled. There is no API key, account secret or local path in this proposed path.

## Research task and unchanged instrument

Task: directed single-source/single-target shortest path with non-negative integer edge weights. Candidate interface: `solve(n, edges, s, t)`, returning the minimum path distance as an integer, or `-1` if unreachable.

The 30 probes, six families R, Z, A, I, S and U, and five probes per family are carried forward provisionally from V3. The expected values remain in `instrument.py` and `expected_values.json`. Before the V4 freeze, the unchanged instrument must pass `validate_controls.py` and all controls must agree.

## Generator schedule and cap

- Generator: only `gpt-oss-120b` via the anonymous OVHcloud endpoint.
- Prompt variants: `direct`, `menu`, `simple`, assigned by `batch_id % 3) before any outputs are observed.
- Batch size: eight requested complete solver modules.
- Hard cap: 400 completed batch requests, 3,200 requested candidate bodies.
- Candidate bodies returned in the same response share the batch's provenance group. A unique normalized body hash is counted once, with first observed provenance retained.
- Preserve complete code modules, including leading imports and helper definitions. Do not trim source at the first `def solve`.
- No outcome-driven prompt, model, timeout, budget or threshold changes.

Anonymous endpoint limits mean 400 requests require at least 3 hours 53 minutes at a 35-second request-start interval, before retries. A failed or throttled attempt is not counted as a completed batch. Completed outputs and raw evidence must be committed before a resumable run continues. If service capacity is inadequate, record the operational failure rather than switch providers silently.

## Feasibility thresholds and futility rule

For eligible candidates ((2 \le k \le 24)), saturation is the fraction with (max_j f_j=5). The version-2 all-or-none fraction is secondary only.

- (m_{min}=4) candidates per supported cell.
- PASS: at least 3 supported cells across at least 2 distinct (k) values, with at least 40 distinct provenance groups.
- WEAK: 1 or 2 supported cells.
- FAIL: otherwise.
- Degeneracy cutoff: saturation rate greater than 0.80.
- At completed-batch checkpoints 100, 200 and 300, stop if distinct eligible provenance groups are below 10, 20 or 30 respectively.
- The target of 150 unique valid candidates with (k>0) is reported but does not justify changing the cap or thresholds.

The precise frozen implementation and interpretation must be re-reviewed before a V4 freeze because the new model population and execution boundary differ from V3.

## Isolation and execution authorization

Candidate bodies are untrusted. They must never be imported or run by the host-side oracle process. The candidate container is to receive only its own source module and one probe's input, never the probe bank, expected values, GitHub token, API access, repository tree or host directory. Each probe runs in a fresh container with networking disabled, a read-only root filesystem, a read-only source bind mount, no added Linux capabilities, no-new-privileges, bounded memory/CPU/PIDs and only a temporary scratch filesystem. The host computes the expected answer and scores the returned value outside the container.

Before candidate generation is permitted, all of the following must be true:
1. The V4 host test suite and instrument controls pass on the hosted runner.
2. The fixed-fixture Docker isolation battery passes with its raw outputs and resource configuration archived.
3. The container runner is reviewed for absence of oracle/probe data and API/GitHub credentials inside the candidate boundary.
4. A new V4 `FREEZE.json` pins the model, endpoint, prompt schedule, instrument, analysis thresholds, isolation design and code hashes.
5. A separate explicit generation authorization is committed.

The proposal currently satisfies none of those freeze/authorization requirements. No model output from the connectivity smoke is included in the study data.