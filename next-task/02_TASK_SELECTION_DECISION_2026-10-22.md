# Task selection decision

Date: 2026-10-22

Status: **selected before any new model generation**; no model calls were made.

## Selected task

**Bounded integer arithmetic expression evaluation.**

The solver implements:

```python
def solve(expr: str) -> int
```

`expr` is a well-formed expression over non-negative integer literals, binary
`+`, `-`, and `*`, parentheses, and optional ASCII spaces. Multiplication
binds more tightly than addition and subtraction; `+` and `-` are
left-associative; parentheses override precedence. A unary minus may prefix a
primary expression. There is no division or exponentiation. The return value
is the exact integer value.

## Rubric result

| Criterion | How the task meets it |
| --- | --- |
| Deterministic oracle | Recursive-descent evaluator plus an independent AST evaluator; both must agree on every bank input |
| Exact output | Integer only; no floating point or tolerance |
| Boundary conditions | Precedence, left associativity, parentheses, unary minus, multi-digit literals, whitespace, negative results |
| Error families | Six separable classes: precedence, associativity, parentheses, unary minus, multi-digit tokenization, whitespace |
| Diagnostic probes | Five structural probes per family; exact-one structural class check |
| Evaluation coverage | Five separate inputs per family, disjoint from diagnostic strings |
| Cost | 30 diagnostic and 30 evaluation short strings per body; standard-library Python only |
| Generation surface | One small function, exact source-only output contract |
| Claim separation | A new problem class; not an SSSP replication |

## Alternatives considered

These were assessed only on paper against the same rubric. No model calls and
no task trials were performed.

- **Longest increasing subsequence.** Deterministic and cheap, but the
  plausible defect classes are fewer and more concentrated around strictness
  and empty/duplicate handling; less independent family structure.
- **Balanced-bracket validation.** Exact and cheap, but the output is binary
  and the defect surface is narrow.
- **Interval scheduling.** Deterministic, but the implementation surface is
  more algorithmic and the boundary classes are less cleanly separable.
- **SSSP.** Excluded: the existing route is closed, and its frozen banks must
  not be reused or mutated.

The expression task is the single selected task. There is no fallback task
list. If its calibration gate fails, stop and report the gap; selecting another
task would require a new authorization.

## Claim boundary

The expression task is a different problem class from SSSP. A future result
would be conditional on this task, its banks, its generator, and its declared
procedure. It would not establish anything about SSSP, and it would not by
itself establish the general concentration hypothesis.
