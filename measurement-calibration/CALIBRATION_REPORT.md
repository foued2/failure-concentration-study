# Diagnostic Measurement Calibration

## Scope

This calibration uses four trusted hand-written callable fixtures, including a correct reference wrapper and three controlled failure-injection wrappers. Each wrapper is run through the repository's actual `make_probe_suite` → `run_probes` → `family_counts` → `concentration` path. Failures are deliberately injected by exact diagnostic input identity. The wrappers are software fixtures, not naturally generated solvers and not realistic bug mechanisms.

The calibration checks whether the instrument and aggregation path can record equal `k=4` with concentrations `1.00`, `0.50`, and `0.25`, plus the zero-failure convention. It does not test correctness on a hidden/evaluation bank, fit a predictive model, or provide evidence about the natural-solver population.

## Pre-calibration test review

The 11 tests in `natural-feasibility-pilot/test_pilot_tool.py` test feature arithmetic on supplied boolean/status vectors, serialization/schema/link validation, input-bank integrity, and two bounded reference-oracle examples. They do **not** pass known solver callables through the 30-probe instrument. The gap justified this separate controlled calibration.

## Results

| Controlled fixture | F1 | F2 | F3 | F4 | F5 | F6 | `k` | `C` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Correct reference wrapper | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 |
| Four injected failures in F1 | 4 | 0 | 0 | 0 | 0 | 0 | 4 | 1.00 |
| Two injected failures each in F1 and F2 | 2 | 2 | 0 | 0 | 0 | 0 | 4 | 0.50 |
| One injected failure each in F1–F4 | 1 | 1 | 1 | 1 | 0 | 0 | 4 | 0.25 |

All cases ran all 30 probes in family-major order and matched the exact injected failure IDs and expected feature values. Row-level records are in `calibration_records.json`. Five calibration tests passed.

## Interpretation and remaining limits

This verifies the diagnostic probe execution and feature aggregation path can distinguish these three controlled patterns at fixed `k`. The failure patterns are injected by matching known probe inputs, so the test does not establish that real solver defects naturally produce such patterns. It also does not validate untrusted source loading, process isolation/timeouts, the evaluation oracle on these fixtures, or any predictive association. The natural-solver pilot remains `BLOCKED_GENERATION_UNAVAILABLE`; its records were not changed.
