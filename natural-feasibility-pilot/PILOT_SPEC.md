# Natural Solver Feasibility Pilot Specification

## Status

Terminal status: **`BLOCKED_GENERATION_UNAVAILABLE`**. Implementation, input preparation, and synthetic software checks only. **Generation and solver evaluation were not executed.** The recorded generator was an MIMO session, not an executable local generator. No equivalent provider tool is available in this environment. No outputs have been fabricated or substituted.

## Target and claim boundary

The target is the output population of the single generation procedure recorded in `specs/generator_spec.json`: 20 one-shot implementations in one MIMO session using `opencode/mimo-v2.6-flash-free`, its recorded SSSP prompt and strategy directives, provider-default temperature/top-p, the stated Python function contract, and retention in generation order without revision or best-of selection. The authorized 100-attempt cap is an absolute ceiling, not a reason to repeat or extend this recorded 20-attempt procedure without an explicit generation rule. The provider exposes no immutable model snapshot. Recovering invocation access would not make the original model version exactly reproducible. This narrowly defined procedure is not asserted to represent all naturally generated solvers. The original invocation mechanism is unavailable, so this pilot made zero generation calls.

Correctness, if collection is later performed, means per-input agreement with `study.sssp.dijkstra_ref`; raw solver and oracle outputs must be retained. Evaluation inputs are separate from diagnostic probes. The pilot's target is a shared bank of new inputs for the generated bodies. It does not establish generalization to every input or to other solver-generation processes.

## Instrument and features

Use the existing `study.probes.make_probe_suite` 30-probe battery and its six fixed five-probe families, and `study.features.family_counts` / `concentration`. Preserve family counts, probe outcomes, `k`, and `C`. Per existing behavior, `k=0` yields `C=0`. Execution errors and timeouts are recorded with their status and count as diagnostic failures, consistent with `run_probes` treating exceptions and wrong answers as failures. An incomplete probe battery is ineligible for feature computation; it must not be silently imputed.

## Evaluation bank and overlap

Use `study.instances.make_hidden_suite(seed=20261020, m_count=20)` once: its documented 15 random graphs plus five edge templates, generated on the independent hidden-input code path. The cap is 100 distinct inputs; this existing generator supplies 20, and the distribution will not be extended or altered to fill the cap. Include each edge fixture once. Compute stable canonical input identities, reject duplicates, and check identities against all 30 diagnostic probes before evaluation. Any overlap or duplicate is a recorded integrity failure and blocks outcome collection. This one shared bank supports comparisons among bodies on the same inputs; body-by-input outcomes remain crossed, not independent.

## Attempt and record rules

The machine-readable field requirements and allowed statuses are in `record_schema.json`; `pilot_tool.validate_records` checks references, required fields, feature arithmetic, duplicate body/input evaluation rows, and input-bank membership. Keep generation attempts separate from canonical bodies. Each attempt receives an ordered ID (`attempt-0001`, etc.) and retains its raw output, provider metadata, prompt/configuration reference, parse/execution status, duplicate-body reference, and any failure/exclusion reason. Body identity is SHA-256 of source text after newline normalization only; do not discard duplicate attempts. For each executed body, retain one diagnostic row per probe and one evaluation row per input with input ID, raw solver output, oracle output, and correctness. Keep a manifest linking attempts, bodies, diagnostic rows, inputs, and evaluation rows. Do not use quality or correctness to select or replace attempts.

## Execution boundary

The existing `study.features.load_solver` imports generated Python directly into the audit process and provides no timeout or isolation. It is not suitable for untrusted generated code. Host inspection found Windows 10 Pro with a hypervisor present, but no `WindowsSandbox.exe`, Docker or Podman command/runtime, or registered WSL distribution. WSL itself is installed, but no isolated Linux environment is configured. Querying Windows optional-feature state requires elevation and was not possible; no isolation capability was therefore confirmed. No solver fixtures, including timeout, crash, invalid-output, or workspace-escape attempts, were run. Before collection, an enforceable disposable sandbox/container with filesystem/network containment, hard execution/resource limits, and cleanup must be made available and its boundary tested. A Python subprocess timeout alone is not considered a security sandbox.

## Limits and decision rules

- Maximum generation attempts: 100; actual attempts: 0.
- Maximum distinct evaluation inputs: 100; planned bank: 20, not executed.
- Diagnostic probes per body: 30.
- No replacement sampling, expanded caps, model fitting, predictive-effect analysis, concentration-metric selection, or confirmatory inference.
- Feasibility is demonstrated only if some eligible fixed-`k` comparison has two different `C` values, each supported by at least two distinct canonical bodies, and independently scored correctness varies meaningfully across those bodies, with input separation and record-integrity checks passing.
- Otherwise feasibility is not demonstrated within these caps; identify the missing condition. This does not establish a null predictive effect.

## Reproduction status

The generation specification and prompt are referenced from the frozen local generator spec; the seed, instrument, and evaluation bank are specified above. No original MIMO invocation mechanism was found in the available tools or local command environment. The pilot therefore records **GENERATION NOT EXECUTED**, **EVALUATION NOT EXECUTED**, and terminal status **`BLOCKED_GENERATION_UNAVAILABLE`**. Exact model reproducibility remains unavailable even if the invocation path is later recovered, because no immutable provider snapshot was recorded.
