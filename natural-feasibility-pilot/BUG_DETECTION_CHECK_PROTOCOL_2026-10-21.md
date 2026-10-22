# Bug-detection coverage check protocol

Status: **prespecified before the Sandbox execution**

## Purpose

Test whether the frozen 30-probe diagnostic battery and the frozen 20-input
evaluation bank can detect a small panel of known, hand-built shortest-path
defects. This is a test-coverage calibration, not a natural-solver generation
run and not a test of the concentration hypothesis.

No model-generation call is authorized by this protocol. No frozen input,
study record, or `README.md` may be modified.

## Inputs

- `diagnostic_battery.json`, 30 probes across families F1-F6
- `evaluation_bank.json`, 20 inputs
- `study.sssp.dijkstra_ref` as the host oracle
- The existing Python/Sandbox execution path in
  `python-pipeline-integration/`
- A correct hand-built Dijkstra reference as the negative control

Hashes of the banks, source policy, runner, and protocol will be recorded in
the check result.

## Prespecified panel

| Variant | Defect class |
| --- | --- |
| `reference_dijkstra` | No defect; correct reference control |
| `unreachable_wrong_sentinel` | Returns `0` instead of `-1` when the target is unreachable |
| `skip_zero_weight_edges` | Omits zero-weight edges from the graph |
| `last_parallel_edge` | Keeps only the last parallel edge for a node pair |
| `reject_self_loops` | Raises on any self-loop instead of processing the valid input |
| `bfs_unweighted` | Ignores edge weights and uses unweighted BFS hop count |
| `early_return_on_target_push` | Finalizes the target when first discovered, before a later shorter path |
| `directed_as_undirected` | Adds reverse edges to a directed graph |

These defect classes were selected before the Sandbox run. Every variant will
be retained and reported, including any variant that is not detected.

## Execution

For each variant, execute the same 30 diagnostic probes and 20 evaluation
inputs through the existing suite-level Sandbox path. The host, not the guest,
computes correctness against `dijkstra_ref`, family counts, `k`, and `C`.
Record the source screen result, raw captures, host-authoritative rows, failed
probe IDs, and per-family diagnostic failures.

The correct reference should record 30/30 diagnostic passes and 20/20
evaluation correctness. If it does not, the check is invalid and will be
reported as a runner failure rather than interpreted as coverage evidence.

## Interpretation rules

- A faulty variant is **caught by diagnostic** if `k > 0`.
- A faulty variant is **caught by evaluation** if fewer than 20 evaluation
  inputs are correct.
- A variant caught by only one bank is evidence of complementary coverage, not
  proof that either bank is adequate.
- A variant missed by both banks is a documented coverage limitation for that
  defect class.
- A caught defect supports only the claim that these specific banks detected
  that specific hand-built defect. It does not establish that the banks detect
  realistic model-generated faults, that the task is easy, or that
  concentration predicts correctness.

## Result handling

Preserve all raw evidence in a new `bug-detection-check-<timestamp>` directory.
Report the panel as descriptive rather than as a pass/fail validation of the
scientific hypothesis. Do not tune the banks, prompt, or variant panel after
seeing the results. No natural-solver run is authorized by this check.
