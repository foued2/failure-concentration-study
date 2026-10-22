# Strict return-type calibration

Status: **PASS**

Run: `calibration-strict-20261022T112115Z-efe7bb1a`.
Model calls: 0; generation attempts: 0.
Output contract: `exact int; type(value) is int`.

| Variant | Target | Diagnostic failures | Target failures | Evaluation target failures | Gate |
| --- | --- | ---: | ---: | ---: | --- |
| reference_parser | reference | 0 | 0 | 0 | True |
| precedence_flat | F1 | 5 | 5 | 5 | True |
| minus_right_assoc | F2 | 5 | 5 | 5 | True |
| parens_dropped | F3 | 5 | 5 | 5 | True |
| unary_rejected | F4 | 5 | 5 | 5 | True |
| single_digit_tokenizer | F5 | 5 | 5 | 5 | True |
| whitespace_rejected | F6 | 5 | 5 | 5 | True |

Frozen banks were not modified. This is a calibration rerun through the strict adapter, not a pilot attempt.
