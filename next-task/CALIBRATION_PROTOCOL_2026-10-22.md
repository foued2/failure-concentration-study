# Expression Task Calibration Protocol

Status: prespecified before the expression calibration run. No model calls are part of this protocol.

## Task

The task is bounded integer arithmetic expression evaluation. The solver implements:

```python
def solve(expr: str) -> int
```

The grammar permits non-negative integer literals, binary `+`, `-`, and `*`, parentheses, optional ASCII spaces, and a unary minus before a primary. There is no division or exponentiation. The returned value must be an exact integer.

## Defect families

- `F1` operator precedence
- `F2` left associativity
- `F3` parentheses
- `F4` unary minus
- `F5` multi-digit tokenization
- `F6` whitespace

## Banks

The diagnostic and evaluation banks each contain 30 records, five per family. The two banks use disjoint exact expression strings. Expected values were checked with two independent host-side oracles: a recursive-descent evaluator and an AST evaluator. The banks were frozen before calibration in `banks/FREEZE.json`.

## Calibration panel

The panel contains one correct reference implementation and one prespecified faulty implementation for each defect family. Every implementation is static-checked by `source_policy.py` before execution. The correct reference must pass every diagnostic probe and every evaluation input.

## Calibration gate

The gate passes only if all conditions hold:

1. The reference implementation is clean: 30/30 diagnostic passes and 30/30 evaluation inputs correct.
2. All six faulty implementations are accepted by the source screen and execute.
3. For each faulty implementation, all five diagnostic probes for its target family fail.
4. For each faulty implementation, all five evaluation inputs for its target family fail.
5. No faulty implementation fails a non-target family.
6. Every transport row has `tree_terminated: true` and no timeout.

## Stop rule

If the gate fails, the run writes the result and a gap report, and stops. The frozen expression banks must not be edited in response. A revised task or bank is a new version and requires a new protocol and calibration run.

If the gate passes, the next deliverable is a readiness report and preregistration for review. It does not authorize model generation, predictive analysis, or a confirmatory claim.
