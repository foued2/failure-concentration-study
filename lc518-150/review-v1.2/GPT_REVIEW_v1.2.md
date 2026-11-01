# GPT independent mathematical verification — LC518-150 v1.2

**Scope:** reference recurrence and per-input E1 bounds only. No bank generator, candidate solver body, or study pipeline was run.

## Reproducible test result

```text
ALL_CHECKS_PASSED
g22_distinct_correctness_and_state_bound_cases=19747
threshold_sweep_vs_bisect_cases=671832
single_contrast_status_pairs=9
interaction_status_quadruples=81
binary_interaction_patterns=16
```

Script SHA-256: 91c087b07fcda3fc1641353da5cdbd646630becbbbd81c8ce4a7e4ef883af041
Script bytes: 5533.

## Findings

1. G22's descending-amount threshold sweep agrees with the binary-search definition over duplicate and distinct positive denomination lists. The G22 recurrence agrees with the separate one-dimensional LC518 combinations oracle over the exhaustive distinct-coin test domain shown above. The memoized-state upper bound is checked on every such case.
2. The v1.2 single-contrast extrema formula agrees with complete enumeration of all nine status pairs.
3. The v1.2 interaction extrema formula agrees with complete enumeration of all 81 four-version status combinations. The binary-loss interaction extremes are unique: maximum +2 at (S0, SA, SB, SAB) = (1,0,0,1) and minimum -2 at (0,1,1,0).

## Remaining review points

- G22's termination-measure sentence in v1.2 says the measure strictly decreases "compaction included." Compaction is non-increasing and can be a no-op; each recursive skip/use edge strictly decreases the measure. The v1.2.1 wording corrects this distinction.
- C9 specifies a generator but no generator artifact or run is included in the published review package. Reproducibility is therefore specified, not empirically demonstrated. After v1.2 is accepted, the generator should be implemented, frozen, run twice under the exact interpreter pin, and its bank files compared byte-for-byte.
- D5 should name its auxiliary objective explicitly. "Greedy count != oracle optimal count" appears to compare a number-of-coins greedy procedure with a minimum-number-of-coins optimum, which is not the LC518 combinations-count output. The v1.2.1 draft distinguishes those objectives.
- The D6/H6 canonical-collision exemption should apply only to the two records sharing the same declared pair_id; collisions between different pairs or between a pair and a singleton should trigger a whole-instance/whole-record redraw. The v1.2.1 draft pins this.
- Status: no candidate solver construction or execution; no input-bank generation; the private mutation annex has not been supplied. E3 remains an owner decision.
