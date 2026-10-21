# End-to-end Python/Sandbox calibration

Status: **FAIL_OR_INCOMPLETE**

Controlled hand-built fixtures only. No model-generated code ran.

| Python fixture | Diagnostic counts | k | C | Evaluation correct | Result |
|---|---:|---:|---:|---:|---|
| pattern_zero | [0, 0, 0, 0, 0, 0] | 0 | 0.0 | 0/20 | FAIL |
| pattern_one_family | [0, 0, 0, 0, 0, 0] | 0 | 0.0 | 0/20 | FAIL |
| pattern_two_families | [0, 0, 0, 0, 0, 0] | 0 | 0.0 | 0/20 | FAIL |
| pattern_four_families | [0, 0, 0, 0, 0, 0] | 0 | 0.0 | 0/20 | FAIL |

Sandbox calls: 1. Each guest received one current input only; the complete diagnostic battery, evaluation bank, oracle, and host records were never mapped.

Protocol controls:


Host-side oracle outputs, correctness labels, six family counts, k, and C were computed outside the guest. These controls do not establish a natural-solver effect or resistance to a Sandbox escape.
