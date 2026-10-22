# Bug-detection coverage check: interpretation

Run: `bug-detection-check-20261022T063926Z-40003da9`

Status: **COMPLETE**; reference control **PASS**; **0 model calls**;
`INTEGRITY.json` status **PASS**.

## Result

The correct Dijkstra reference passed 30/30 diagnostic probes and 20/20
evaluation inputs. All seven prespecified faulty variants were detected by at
least one bank.

| Coverage | Variants |
| --- | --- |
| Diagnostic only | `reject_self_loops` |
| Evaluation only | `early_return_on_target_push`, `directed_as_undirected` |
| Both banks | `unreachable_wrong_sentinel`, `skip_zero_weight_edges`, `last_parallel_edge`, `bfs_unweighted` |
| Neither bank | none |

The diagnostic battery detected 5/7 faulty variants; the evaluation bank
detected 6/7. The two evaluation-only defects each passed all 30 diagnostic
probes but failed the evaluation bank: `early_return_on_target_push` was
correct on 15/20 inputs and `directed_as_undirected` on 11/20. The
`reject_self_loops` variant crashed on all five F4 self-loop probes but passed
20/20 evaluation inputs; the frozen evaluation bank contains no self-loop
input.

## What this supports

- The diagnostic battery is not uniformly insensitive: it detects five common
  defect classes, including unreachable-target and zero-weight-edge errors.
- The evaluation bank is not merely a duplicate of the six diagnostic family
  predicates: it detects two defects that pass all 30 diagnostic probes.
- The universal `k=0` observed in the two generated-solver procedures cannot be
  explained by the blanket claim that "the tests cannot detect any wrong
  solver." These banks did detect several known wrong solvers.
- The execution path and host-side labeling behaved correctly for a known
  correct reference and a panel of known wrong references.

## What this does not support

- It does not establish that the task is easy, that the generated bodies were
  correct beyond these tests, or that natural solvers concentrate failures.
- It does not establish that the banks catch arbitrary model-generated faults.
  The panel contains seven hand-built defects; it is not a sample from a model's
  error distribution.
- The diagnostic battery's six family predicates are not exhaustive. Two
  plausible defects passed every diagnostic probe and were caught only by the
  evaluation bank.
- The evaluation bank alone has a self-loop coverage gap: it could not
  distinguish a solver that rejects valid self-loop inputs. The diagnostic
  battery covers that case through F4.
- It provides no fixed-`k` or non-zero-`C` contrast, so it cannot support a
  concentration or predictive-correctness claim.

## Implication for the closed natural-solver runs

The prior 35 completed bodies passed both banks, but that does not prove they
are correct outside the frozen inputs. Conversely, this check shows the banks
are capable of catching multiple realistic defects. The most defensible
reading is narrower than either extreme: these particular tests are not
globally insensitive, but the cause of the uniform `k=0` remains unidentified.

A "weak tests" explanation is therefore not ruled out as a partial explanation,
but it is not supported as a blanket explanation. The task-ease explanation
also remains a hypothesis. Neither explanation is established.

## Decision boundary

This check does not authorize a third identical natural-solver run. It also
does not establish that an engineered-solvers study is preferable. If the next
route is engineered, this panel can serve as positive controls and the
self-loop evaluation gap should be repaired or explicitly bounded. If the next
route is a harder natural task, that task and its generation procedure must be
prespecified before observing outcomes. The choice should not be presented as
a result of the concentration hypothesis.
