# Expression task calibration

Status: **PASS**

No model calls were made. The correct reference and six prespecified faulty
implementations were run through the frozen 30-probe diagnostic bank and
30-input evaluation bank using the existing Sandbox path.

Reference control: **PASS** (diagnostic failures 0, evaluation correct 30/30).

| Variant | Target | Diag target failures | Eval target failures | Cross-family | Tree terminated | Gate |
| --- | --- | ---: | ---: | --- | --- | --- |
| `reference_parser` | none | n/a | n/a | n/a | yes | reference PASS |
| `precedence_flat` | F1 | 5/5 | 5/5 | no | yes | PASS |
| `minus_right_assoc` | F2 | 5/5 | 5/5 | no | yes | PASS |
| `parens_dropped` | F3 | 5/5 | 5/5 | no | yes | PASS |
| `unary_rejected` | F4 | 5/5 | 5/5 | no | yes | PASS |
| `single_digit_tokenizer` | F5 | 5/5 | 5/5 | no | yes | PASS |
| `whitespace_rejected` | F6 | 5/5 | 5/5 | no | yes | PASS |

The reference row is not a faulty-variant gate: it is qualified by the separate
reference-control check (30/30 diagnostic passes and 30/30 evaluation correct).
The `gate_pass` field in `CALIBRATION_RESULT.json` is defined only for the six
faulty variants; its `false` value on the reference row is not a failure.

## Gate gaps

- None.

## Scope

This is a hand-built test-coverage check. It does not establish that the task is easy,
that natural solvers concentrate failures, or that C predicts correctness. A pass only
qualifies these frozen banks for the next review step; it does not authorize generation.
