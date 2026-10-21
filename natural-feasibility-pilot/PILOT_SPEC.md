# Natural Solver Feasibility Pilot Specification

## Status

Readiness status: **`READY_FOR_BOUNDED_EXPLORATORY_PILOT`**, with explicitly weaker, non-adversarial input-isolation expectations. The historical MIMO procedure below remains preserved as historical evidence; the pilot population is the separately declared Codex CLI generation procedure. One generated smoke body completed the full diagnostic and evaluation banks through the Python Sandbox runner. This authorizes only the bounded feasibility collection described here, not predictive analysis or a confirmatory study.

Collection status (2026-10-21): **`HALTED_GENERATION_USAGE_LIMIT`**. The 100-request cap was reached, but only 39 requests returned model output; requests 40-100 failed before producing a body because the Codex CLI reported a usage limit. Fifteen distinct canonical bodies were generated and 10 completed both banks. This is an infrastructure halt, not a feasibility conclusion. See `natural-pilot-20261021T123319Z/PILOT_RESULTS.json`.

## Target and claim boundary

The historical target recorded in `specs/generator_spec.json` was `opencode/mimo-v2.6-flash-free`; its invocation mechanism is unavailable. It is not the target of the proposed pilot below and no claim is made that the new procedure reproduces it.

### Proposed generation procedure (not yet activated)

- **Population:** solver bodies returned by individual one-shot requests to the authenticated Codex CLI procedure below. This is a new, procedure-specific output population, not a representative sample of all naturally generated solvers and not a reproduction of MIMO.
- **Date declared:** 2026-10-21.
- **CLI:** Codex CLI `0.160.1`; model selector `gpt-6-luna`; invocation pattern `codex exec --ephemeral --sandbox read-only --model gpt-6-luna --json` with the following exact user prompt supplied as the task text. The preceding `Reply exactly OK...` request was a text-only interface smoke check and is not a generation attempt.
- **Exact one-shot prompt:**

  > Write one Python implementation of a function `solve(n, edges, s, t)` that computes the shortest path distance from node `s` to node `t` in a directed graph with non-negative integer edge weights. Nodes are integers `0` through `n-1`. `edges` is a list of `(u, v, w)` tuples; parallel edges and self-loops may occur. Return the minimum total weight of any directed path from `s` to `t` as an integer, or `-1` if `t` is unreachable. Make the function self-contained and use only the Python standard library. Do not read files, access the network, or print. Return only Python source code defining `solve`, with no Markdown fences, explanation, example usage, or tests. Write the first solution that comes to mind; do not self-review or revise it.

- **Output contract:** a single source response defining `solve(n: int, edges: list[tuple[int,int,int]], s: int, t: int) -> int`, returning `-1` for unreachable. Parse failures and any additional text are retained as invalid attempts; no retries or replacement sampling.
- **Available settings:** model selector is explicit; `--ephemeral`, `--sandbox read-only`, and JSON response mode are used. No temperature, top-p, seed, or backend snapshot setting was exposed in the recorded CLI interface; those values are unavailable/default and will not be guessed. Provider authentication is the existing logged-in Codex CLI session; no credential values are recorded.
- **Model identity limitation:** `gpt-6-luna` is the CLI model slug only. Backend model version and immutable snapshot are unavailable, so exact model reproducibility is not claimed.
- **Generation rule:** one CLI request per ordered attempt, at most 100 attempts, with no retry, prompt tuning, outcome-driven selection, or replacement sampling. The prompt and this procedure must be reviewed against the actual runner before the first request.

The generation interface has passed only one text-only smoke request. It has not yet returned a solver body through the pilot runner. Therefore the proposed population is specified but has zero observations and is not yet authorized for collection by this specification.

Correctness, if collection is later performed, means per-input agreement with `study.sssp.dijkstra_ref`; raw solver and oracle outputs must be retained. Evaluation inputs are separate from diagnostic probes. The pilot's target is a shared bank of new inputs for the generated bodies. It does not establish generalization to every input or to other solver-generation processes.

## Instrument and features

Use the existing `study.probes.make_probe_suite` 30-probe battery and its six fixed five-probe families, and `study.features.family_counts` / `concentration`. Preserve family counts, probe outcomes, `k`, and `C`. Per existing behavior, `k=0` yields `C=0`. Execution errors and timeouts are recorded with their status and count as diagnostic failures, consistent with `run_probes` treating exceptions and wrong answers as failures. An incomplete probe battery is ineligible for feature computation; it must not be silently imputed.

## Evaluation bank and overlap

Use `study.instances.make_hidden_suite(seed=20261020, m_count=20)` once: its documented 15 random graphs plus five edge templates, generated on the independent hidden-input code path. The cap is 100 distinct inputs; this existing generator supplies 20, and the distribution will not be extended or altered to fill the cap. Include each edge fixture once. Compute stable canonical input identities, reject duplicates, and check identities against all 30 diagnostic probes before evaluation. Any overlap or duplicate is a recorded integrity failure and blocks outcome collection. This one shared bank supports comparisons among bodies on the same inputs; body-by-input outcomes remain crossed, not independent.

## Attempt and record rules

The machine-readable field requirements and allowed statuses are in `record_schema.json`; `pilot_tool.validate_records` checks references, required fields, feature arithmetic, duplicate body/input evaluation rows, and input-bank membership. Keep generation attempts separate from canonical bodies. Each attempt receives an ordered ID (`attempt-0001`, etc.) and retains its raw output, provider metadata, prompt/configuration reference, parse/execution status, duplicate-body reference, and any failure/exclusion reason. Body identity is SHA-256 of source text after newline normalization only; do not discard duplicate attempts. For each executed body, retain one diagnostic row per probe and one evaluation row per input with input ID, raw solver output, oracle output, and correctness. Keep a manifest linking attempts, bodies, diagnostic rows, inputs, and evaluation rows. Do not use quality or correctness to select or replace attempts.

## Execution boundary

The direct `study.features.load_solver` importer is not used. The suite-level Windows Sandbox runner passed one generated smoke body over all 30 diagnostic probes and the separate 20-input evaluation bank. It launches a fresh Python worker for each input, with networking disabled, a 10-second worker timeout, a 128 MiB Job Object memory limit, and host-side oracle, label, and feature calculations. The whole current suite is guest-readable during that suite's session; source scanning is a best-effort screen and not a security boundary. The runner does not expose the oracle, reference outputs, host records, repository, or credentials as mapped folders. This weaker input-secrecy standard is accepted for exploratory feasibility only; results must not be described as securely blinded against a solver that can inspect its session's mounted suite. Earlier failed streaming attempts remain retained in `python-pipeline-integration/streamed-run-*` and are not treated as pilot evidence.

## Limits and decision rules

- Maximum generation attempts: 100; actual generation requests: 100 (39 model outputs; 61 usage-limit failures).
- Maximum distinct evaluation inputs: 100; planned bank: 20; executed for 10 complete bodies.
- Diagnostic probes per body: 30.
- No replacement sampling, expanded caps, model fitting, predictive-effect analysis, concentration-metric selection, or confirmatory inference.
- Feasibility is demonstrated only if some eligible fixed-`k` comparison has two different `C` values, each supported by at least two distinct canonical bodies, and independently scored correctness varies meaningfully across those bodies, with input separation and record-integrity checks passing.
- Otherwise feasibility is not demonstrated within these caps; identify the missing condition. This does not establish a null predictive effect.

## Reproduction status

The diagnostic seed and 20-input evaluation bank are specified above. The Codex CLI generated one trivial SSSP smoke body; it was not a pilot attempt. The host recovered 30/30 diagnostic rows and 20/20 evaluation rows, independently computed all labels, and reconstructed the feature vector. The smoke had `k=0`, `C=0`, and 20/20 evaluation cases correct; this checks the runner and says nothing about concentration prediction. See `generation-smoke-2026-10-21/SMOKE_REPORT.md`. One initial report-building KeyError occurred after both complete captures had been retained; the host-side finalizer reconstructed records from those captures without re-executing the solver. The runner is ready for the bounded feasibility pilot under the disclosed input-visibility limitation. Model backend/snapshot identity remains unavailable.
