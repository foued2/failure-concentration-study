# Offline Power Simulation Report

Status: **`OFFLINE_POWER_SIMULATION_COMPLETE_NO_AUTHORIZATION`**

> **INVALIDATED FOR OPERATIONAL PLANNING — NOT APPROVED.** The simulation uses
> `C_high = 1.0` at `k = 6, 12, 24`. With five probes per family, the maximum
> attainable concentration is `C_max(k) = min(1, 5/k)`, so those high-C cells are
> impossible. The power and request figures below are invalid for the intended
> design and must not be used as operational estimates; this does not imply that
> every calculation in the script is erroneous. See
> `next-task/11_CLOSURE_RECORD_2026-10-22.md`.

Date: 2026-10-22

This report is preparation evidence only. It makes no model calls, selects no
task, changes no bank, and authorizes no generation. It uses no empirical
expression-pilot outcome data to fit, calibrate, or predict anything. The design
requirements it evaluates are in
`next-task/09_NEXT_STUDY_DESIGN_AMENDMENT_2026-10-22.md`.

## Bottom line

Under the conditional-independence null and the assumed score model, a cap of
**100 requests per condition** (8 cells, 12 bodies per cell, 96 requests) does not
support adequate power for a smallest effect of `beta = 0.06` unless score
overdispersion is near zero and duplicate/execution loss is absent.

- At `ICC rho = 0.05`, `beta = 0.06`: 80% power requires about **20 effective
  bodies per cell**, or **160 bodies per condition** with no loss. With 25%
  duplicate loss, the requirement is about **216 requests per condition**; with
  25% duplicate loss plus 20% execution-ineligible loss, about **272 requests per
  condition**.
- At the 100-request cap and `n = 12` per cell, `beta = 0.06`, `ICC = 0.05`:
  conditional power is **0.512** with 25% duplicate loss and **0.398** with 25%
  duplicate plus 20% execution-ineligible loss.
- At the same cap and loss assumptions, `beta = 0.10`, `ICC = 0.05`: power is
  **0.873** and **0.812**, respectively.
- If the smallest effect of interest is `beta = 0.06`, the defensible
  recommendation is to **stop the natural-solver route under the 100-request cap**,
  not to increase the cap quietly. If only `beta >= 0.10` is of interest, the cap
  is borderline and depends on loss; that narrower target would require an
  explicit decision before generation.
- At `beta = 0.03`, `ICC = 0.05`, 80% power is not reached even at 40 effective
  bodies per cell. No cap in the examined range supports that alternative.

The simulation is conditional on the generator producing populated `(k, C)` cells
and on the stated effect and loss model. It is not evidence that a natural
generator will produce those cells or effects.

## Inputs and design

The simulation is implemented in
`next-task/power_simulation/simulate_next_study_power.py` (SHA-256
`fb1a6855961009f0e04b487a1d9839c418c539a04aa95e80d32c108c6c180bca`). It ran
under Python 3.14.0 using only the standard library and made no network or model
calls.

Run command:

```text
.venv\Scripts\python.exe next-task/power_simulation/simulate_next_study_power.py --replicates 400 --null-replicates 1000 --permutations 99 --null-permutations 199 --yield-permutations 199
```

Outputs are written to `next-task/power_simulation/results/`.

Design used for the grid:

| Item | Value |
| --- | --- |
| Evaluation score | `S = correct / 200` |
| `k` levels | `2, 6, 12, 24` |
| `C` levels per `k` | `C_low = ceil(k/6)/k`, `C_high = 1.0` |
| Baseline score probability | `p_k = 0.90 - 0.0125*k` |
| Alternative | `p(k,C) = p_k + beta*(C - midpoint(C_low,C_high))` |
| Effect grid | `beta = 0.03, 0.06, 0.10, 0.15, 0.20` |
| Overdispersion grid | `rho = 0, 0.01, 0.05` |
| Score model | Binomial(200, p); `rho > 0` uses a beta-binomial body probability with ICC `rho` |
| Analysis | Within-`k` centered `C`-`S` slope, stratified permutation test |
| Alpha | 0.05, two-sided |
| Power replicates | 400 per grid point |
| Power permutations | 99 |
| Null calibration | 1,000 replicates, 199 permutations |
| Yield sensitivity | 400 replicates, 199 permutations |

`beta` is the score change per 1.0 unit of `C`. At the widest six-family contrast
(`C = 1` versus `C = 1/6`), the high-low score difference is `(5/6)*beta`:
`beta = 0.06` corresponds to 5.0 score points; `beta = 0.10` to 8.3 points.

The final evaluation sample is expected to be `N_eval = 200` with six families
sized `34, 33, 33, 33, 33, 34`. If the task uses a different `N_eval`, the power
calculation must be rerun at that value before authorization.

## Null calibration

Each cell is the false-positive rate at alpha 0.05, with a 95% Wilson interval
computed from 1,000 replicates. All intervals include 0.05.

| ICC `rho` | `n=2` | `n=5` | `n=10` | `n=20` | `n=40` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.00 | 0.049 | 0.043 | 0.046 | 0.050 | 0.044 |
| 0.01 | 0.043 | 0.049 | 0.049 | 0.049 | 0.049 |
| 0.05 | 0.055 | 0.046 | 0.043 | 0.046 | 0.052 |

Observed FPR range: **0.043 to 0.055**. The null calibration is consistent with
the nominal 0.05 level in this simulation. This checks the analysis pipeline, not
the natural generator.

## Required bodies for 80% power

`n` is effective bodies per `(k, C)` cell, from the coarse grid
`2, 3, 5, 8, 12, 20, 30, 40`. `total` is `8*n` effective bodies per condition.
The request columns divide by the effective yield `q = (1-duplicate_rate) *
(1-ineligible_rate)` and multiply by eight cells. They are planning approximations,
not guarantees.

| ICC `rho` | `beta` | `n/cell` | `total` | power | requests `q=1.0` | `q=0.75` | `q=0.60` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.00 | 0.03 | 8 | 64 | 0.853 | 64 | 88 | 112 |
| 0.00 | 0.06 | 3 | 24 | 0.930 | 24 | 32 | 40 |
| 0.00 | 0.10 | 2 | 16 | 0.985 | 16 | 24 | 32 |
| 0.01 | 0.03 | 30 | 240 | 0.920 | 240 | 320 | 400 |
| 0.01 | 0.06 | 8 | 64 | 0.927 | 64 | 88 | 112 |
| 0.01 | 0.10 | 3 | 24 | 0.902 | 24 | 32 | 40 |
| 0.05 | 0.03 | >40 | >320 | not reached | >320 | >432 | >536 |
| 0.05 | 0.06 | 20 | 160 | 0.805 | 160 | 216 | 272 |
| 0.05 | 0.10 | 8 | 64 | 0.843 | 64 | 88 | 112 |

`q=0.75` represents 25% duplicate loss. `q=0.60` represents 25% duplicate loss
plus 20% execution-ineligible loss. The `beta=0.06`, `ICC=0.05` row is borderline
at the 0.80 threshold: 0.805 with 400 replicates; 30 effective bodies per cell
gives 0.905 without loss. A plan that needs robust power should not rely on the
20-cell boundary.

## Conditional power at the 100-request cap

A condition with 8 cells and 12 requests per cell uses 96 of 100 requests.
Conditional power is shown for `n = 12`.

| ICC `rho` | `beta` | `q=1.0` | `q=0.75` | `q=0.60` | `q=0.30` | `q=0.25` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.01 | 0.06 | 0.988 | 0.945 | 0.890 | 0.598 | 0.480 |
| 0.01 | 0.10 | 1.000 | 1.000 | 1.000 | 0.938 | 0.865 |
| 0.05 | 0.06 | 0.560 | 0.512 | 0.398 | 0.223 | 0.190 |
| 0.05 | 0.10 | 0.953 | 0.873 | 0.812 | 0.468 | 0.427 |

`q=0.30` is 50% duplicate loss plus 40% execution-ineligible loss; `q=0.25` is
50% duplicate plus 50% ineligible. These are stress scenarios, not estimates from
the expression pilot.

At `beta=0.06` and `ICC=0.05`, no 100-request plan reaches 0.80 power. At
`beta=0.10` and `ICC=0.05`, 0.873 is reached with 25% duplicate loss, but the
power falls to 0.812 when 20% execution-ineligible loss is added, and to 0.468
under the severe-loss scenario.

## Yield sensitivity

The simulation treats duplicate and execution-ineligible bodies as binomial
thinning of the number of effective bodies. This is a planning approximation: it
reduces effective sample size but does not model clustered duplicates exactly.

At `beta=0.06`, `ICC=0.05`, with 20 requests per cell:

| duplicate rate | ineligible rate | effective yield | conditional power |
| ---: | ---: | ---: | ---: |
| 0.00 | 0.00 | 1.00 | 0.828 |
| 0.25 | 0.00 | 0.75 | 0.680 |
| 0.25 | 0.20 | 0.60 | 0.613 |
| 0.50 | 0.40 | 0.30 | 0.345 |
| 0.50 | 0.50 | 0.25 | 0.308 |

The estimability rate is approximately 1.0 except in the most severe yield
scenario, where some cells contain fewer than two bodies per `C` level. In those
cases conditional power is reported among estimable replicates; operational power
is lower. The full yield table is in `POWER_SIMULATION_YIELD.csv`.

## Interpretation

1. **Null behavior is acceptable.** The stratified permutation test is calibrated
   near 0.05 in the simulated null, including under the beta-binomial
   overdispersion scenarios.
2. **Overdispersion dominates.** At `ICC=0.05`, the required sample for
   `beta=0.06` is 20 effective bodies per cell; at `ICC=0.01` it is 8. The
   difference is larger than the effect of moderate duplicate loss.
3. **The 100-request cap is an effect-size-selective design.** It can detect a
   large effect (`beta=0.10`, about 8.3 score points across the widest contrast)
   under moderate loss, but not a 5-point effect (`beta=0.06`) under
   `ICC=0.05`. It also cannot detect `beta=0.03` under any examined cap.
4. **A fixed-k, different-C comparison is still not guaranteed.** Power is
   conditional on populated cells. The simulation does not establish that the
   natural generator will produce at least two behavioral profiles at the same
   `k` with different `C`, or that duplicate bodies will not erase the contrast.
5. **The expression pilot's duplicate pattern is not used as a rate estimate.**
   The audit's nine behaviorally identical `k=2` bodies make `q < 1` plausible,
   but the simulation does not estimate `q` from the pilot and makes no
   predictive claim about the next task.

## Recommendation

Do not authorize the next natural task under a 100-request-per-condition cap if
the smallest concentration effect of interest is `beta = 0.06` (about 5 score
points across the widest six-family contrast). At `ICC = 0.05`, the requirement is
about 216 requests per condition with 25% duplicate loss and 272 with 25%
duplicate plus 20% ineligible. That is outside the cap.

If the program is willing to restrict the target to `beta >= 0.10` and to accept
the loss-dependent power shown above, 100 requests per condition is borderline,
not robust. That narrower target must be stated before generation. Do not raise
the cap after seeing outcomes.

If `beta = 0.06` or smaller is scientifically required, the defensible
recommendation is to **stop the natural-solver route**, record the power
limitation, and preserve the option for a separately authorized methodological
study. This report does not increase the cap, select a task, or authorize either
route.

**Recommendation: do not authorize the next task under the current 100-request
design.** The analysis supports only a large-effect study (`beta` near 0.10)
under favorable loss assumptions, and the smallest effect that would be
scientifically meaningful has not been shown to be that large. Proceeding would
require a new explicit decision that accepts either a larger cap or a narrower,
loss-dependent target; neither is authorized here.

Decision requested:

- **A. Stop the natural-solver route** under the current cap and record the power
  limitation. This is the defensible default.
- **B. Authorize a new design decision** that either raises the cap to the
  required range or narrows the smallest effect of interest to `beta >= 0.10`
  and accepts the loss-dependent power. This requires a new power run at the
  frozen `N_eval` and is not authorized by this report.
- **C. Separately authorize a methodological study.** It cannot substitute for
  the natural-solver evidence.

## Limitations

- The simulation uses `N_eval = 200`; the final task must freeze the actual
  evaluation size and rerun the calculation if it differs materially.
- `beta` is a linear effect on score; the grid does not enumerate all plausible
  nonlinear or threshold alternatives.
- The baseline `p_k = 0.90 - 0.0125*k` is a planning assumption, not an estimate
  from the expression pilot. Power depends on it.
- The score model uses independent bodies with beta-binomial overdispersion. It
  does not model body clustering by provider, prompt, or generation batch beyond
  the ICC term.
- Duplicate and execution-ineligible bodies are modeled as thinning; clustered
  duplicates and input-specific execution failures are not modeled exactly.
- The test uses an unnormalized within-`k` slope. It is a valid stratified
  association test, but its power depends on the distribution of `C`; the
  simulation fixes that distribution by design.
- Power uses 400 replicates and 99 permutations; null calibration uses 1,000
  replicates and 199 permutations. Monte Carlo error is roughly plus or minus
  0.03 to 0.05 for power near 0.5 to 0.9 and roughly plus or minus 0.014 for the
  null FPR. Required `n` is grid-based and coarse; the 0.805 boundary should be
  treated as approximately 20 to 30 bodies per cell, not an exact threshold.
- The final study must use at least 999 permutations for any reported p-value and
  must not treat these planning p-values as study results.
- No empirical pilot outcomes were used to choose the effect sizes, ICC, loss
  rates, or baseline. They are sensitivity scenarios only.

## Preserved artifacts

This report and the simulation add files only. The frozen expression result,
banks, preregistration, audit, memo, raw run, `README.md`, and closed SSSP runs
are unchanged. No generation, bank edit, task selection, commit, push, merge, or
tag is authorized by this report.
