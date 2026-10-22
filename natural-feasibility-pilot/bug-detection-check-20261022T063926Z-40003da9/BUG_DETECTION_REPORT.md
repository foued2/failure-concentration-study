# Bug-detection coverage check

Status: **COMPLETE**

No model calls were made. Seven prespecified faulty SSSP variants and one correct
reference were run through the frozen 30-probe diagnostic battery and 20-input
evaluation bank using the existing Sandbox path.

Reference control: **PASS** (diagnostic failures 0, evaluation correct 20/20).

| Variant | Defect | Diag failures | k | C | Eval correct | Diag caught | Eval caught |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `reference_dijkstra` | none; correct reference control | 0/30 | 0 | 0.00 | 20/20 | no | no |
| `unreachable_wrong_sentinel` | returns 0 instead of -1 for an unreachable target | 5/30 | 5 | 1.00 | 15/20 | yes | yes |
| `skip_zero_weight_edges` | omits zero-weight edges from the graph | 5/30 | 5 | 1.00 | 16/20 | yes | yes |
| `last_parallel_edge` | keeps only the last parallel edge for each node pair | 5/30 | 5 | 1.00 | 19/20 | yes | yes |
| `reject_self_loops` | raises on a valid graph containing a self-loop | 5/30 | 5 | 1.00 | 20/20 | yes | no |
| `bfs_unweighted` | ignores edge weights and returns unweighted hop count | 25/30 | 25 | 0.20 | 5/20 | yes | yes |
| `early_return_on_target_push` | returns when the target is first discovered, before later relaxation | 0/30 | 0 | 0.00 | 15/20 | no | yes |
| `directed_as_undirected` | adds reverse edges to a directed graph | 0/30 | 0 | 0.00 | 11/20 | no | yes |

## Coverage summary

- Caught by diagnostic: `unreachable_wrong_sentinel`, `skip_zero_weight_edges`, `last_parallel_edge`, `reject_self_loops`, `bfs_unweighted`
- Caught by evaluation: `unreachable_wrong_sentinel`, `skip_zero_weight_edges`, `last_parallel_edge`, `bfs_unweighted`, `early_return_on_target_push`, `directed_as_undirected`
- Caught by both: `unreachable_wrong_sentinel`, `skip_zero_weight_edges`, `last_parallel_edge`, `bfs_unweighted`
- Diagnostic only: `reject_self_loops`
- Evaluation only: `early_return_on_target_push`, `directed_as_undirected`
- Missed by both: none

## Scope

This is a hand-built test-coverage check. It does not establish that the task is easy,
that the diagnostic battery is generally sufficient, or that concentration predicts
correctness. A defect missed by both banks would be a documented coverage limitation;
a defect caught by only one bank is evidence of complementary coverage for that defect.
