# Bounded natural-solver feasibility pilot

State: **HALTED_GENERATION_USAGE_LIMIT**

## Accounting

| Measure | Result |
|---|---:|
| Generation requests attempted | 100 |
| Requests returning model output | 39 |
| Provider usage-limit failures | 61 |
| Distinct solver bodies generated | 15 |
| Bodies with complete diagnostic and evaluation records | 10 |
| Completed bodies with k=0, C=0, and 20/20 correct | 10 |
| Eligible fixed-k, different-C contrasts observed | 0 |

The 61 failures count as generation-request attempts, not solver bodies or solver outcomes. The current run remains closed at 100 requests.

## Interpretation

The preregistered feasibility criterion was **not met**: no eligible fixed-`k` contrast with two different `C` values was observed. Generator feasibility remains **inconclusive**, because the provider usage limit prevented 61 of 100 requests from producing outputs.

All ten complete bodies had `k=0`, `C=0`, and 20/20 evaluation correctness. That pattern is not evidence that concentration cannot predict correctness. This run is an infrastructure-interrupted result, not a scientific falsification claim.

Halt reason: Codex CLI usage limit reached at attempt 40; attempts 41-100 failed before any model output. The 100-request cap is exhausted, so this is an infrastructure halt, not a test of the generator through the planned cap. The provider message reports availability after 2026-11-19 18:55.

No predictive model was fitted and no concentration effect was tested.

The guest could read the full diagnostic suite during its diagnostic session and the full evaluation bank during its evaluation session. Source screening is a best-effort policy, not a security boundary.

This pilot can establish only whether this declared generator procedure supplies the required observed comparisons within its cap. It cannot establish that concentration predicts correctness.
