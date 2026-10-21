# Natural Solver Feasibility Pilot — Status Report

## Decision

**Terminal status: `BLOCKED_GENERATION_UNAVAILABLE`. Generation and solver evaluation were not executed. Natural-solver feasibility is not demonstrated.** This is a capability blocker, not evidence against concentration and not a completed 100-attempt feasibility check. No concentration-versus-correctness analysis was performed.

## Preparation and verification

- The target is the single historical procedure in `specs/generator_spec.json`: 20 one-shot MIMO SSSP generations in one session, under the recorded prompt and strategy directives. No other model, hand-built solver, or synthetic solver was substituted.
- A 30-probe diagnostic battery was prepared from the existing probe code with seed `20261020`.
- A 20-input evaluation bank was prepared from `study.instances.make_hidden_suite(seed=20261020, m_count=20)`, retaining its existing 15-random-graph plus five-edge-template distribution. The 100-input limit is a ceiling, not a requirement.
- Input integrity: 30 diagnostic inputs; 20 evaluation inputs; zero evaluation duplicates; zero exact diagnostic/evaluation overlaps. All five intended fixtures (`e0`–`e4`) appear exactly once, with no duplicate or unknown fixture IDs. The report, fixture check, and SHA-256 digests are in `input_manifest.json`; the full inputs are in `diagnostic_battery.json` and `evaluation_bank.json`.
- Eleven software tests passed. They cover the three four-failure concentration patterns, arithmetic and zero-failure convention, invalid/timeout status retention, duplicate attempt/body identity, duplicate and overlap detection, the seeded bank’s fixture constraints, bounded oracle cases, record schema and feature reconstruction, and trace validation. Synthetic fixtures validate software only; they are not solver observations.
- `record_schema.json` specifies the machine-readable record types and fields. `pilot_tool.validate_records` checks required fields/statuses, attempt/body references, complete diagnostic batteries, evaluation-bank membership, duplicate body/input outcome rows, and feature arithmetic.

## Collection counts

| Quantity | Count |
| --- | ---: |
| Generation attempts | 0 of 100 maximum |
| Executable generated bodies | 0 |
| Distinct canonical generated bodies | 0 |
| Diagnostic solver executions | 0 |
| Evaluation outcomes | 0 |
| Prepared unique evaluation inputs | 20 of 100 maximum |
| Fixed-`k`, different-`C` comparisons | Not observable; no solver records |

No generated outputs, solver-level diagnostic rows, solver outputs, oracle comparisons, or correctness labels exist. The input manifest covers only prepared inputs and integrity checks; it is not a solver-data manifest.

## Why execution stopped

The local generator record describes one MIMO session of 20 one-shot generations, but contains no executable invocation client. No `opencode` or `mimo` command was available, and no connected generation tool was exposed. The provider has no immutable model snapshot, so recovering invocation access would still not make the exact model version reproducible. The documented 100-attempt cap does not define whether or how to repeat or extend the recorded 20-attempt session. No alternative generator or undocumented invocation behavior was substituted.

The existing `study.features.load_solver` imports and executes solver modules in the current process, without a timeout or isolation; `scripts/run_pilot.py` uses that loader. It is not a safe execution boundary for generated code.

Host inspection found Windows 10 Pro with a hypervisor present, but no `WindowsSandbox.exe`, Docker or Podman command/runtime, or registered WSL distribution. WSL is installed but no isolated Linux environment is configured. Querying Windows optional-feature state required elevation and could not be completed. Thus no enforceable isolation mechanism was confirmed. No timeout, crash, invalid-output, duplicate-body execution, or workspace-escape fixtures were run: without a sandbox, those checks would not establish containment. No solver code was run.

## Feasibility finding

**`BLOCKED_GENERATION_UNAVAILABLE`** is the terminal state. The attempt cap was never exercised, so this is not “infeasible within 100 attempts.” Input preparation and software-level checks passed, but fixed-`k` variation and independent correctness outcomes cannot be assessed. This is neither a positive nor a negative result for the concentration hypothesis.

## Next prerequisites

Provide access to the original MIMO invocation mechanism and its recorded settings. Clarify whether the specified 20-attempt session may be extended up to the 100-attempt ceiling; do not infer this from the ceiling alone. Exact model reproducibility will remain unavailable without an immutable provider snapshot. Separately, enable or provide a disposable isolation runtime with enforceable filesystem containment, hard execution/resource limits, and cleanup. Test it using harmless timeout, crash, invalid-output, duplicate-body, and workspace-escape fixtures before executing generated solvers. Do not expand the caps or proceed automatically to a confirmatory study.
