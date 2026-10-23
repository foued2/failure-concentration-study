# Task specification

Status: frozen before bank construction.

## Task

**Name:** `paren7_min_insertions`

Given a string of exactly seven characters, each `(` or `)`, return the minimum
number of parenthesis insertions needed to make the string balanced. A balanced
string has equal numbers of opening and closing parentheses and every prefix has
at least as many opening as closing parentheses.

The solver signature is exactly:

```python
def solve(text: str) -> int:
    ...
```

The declared input domain is every one of the 128 strings of length seven over
the two-character alphabet. No other input is part of the study.

## Output contract

The guest adapter accepts only an exact Python `int`. A `bool`, `float`, string,
`None`, exception, timeout, or malformed transport is a failed answer, not a
missing sample. The adapter returns:

```json
{"return_type":"int","value":"<decimal integer>"}
```

No other output is accepted.

## Oracle

The primary host oracle uses the prefix-balance identity:

```text
balance = openings - closings
minimum_prefix = min(0, all prefix balances)
answer = balance - 2 * minimum_prefix
```

The independent check uses two scans: count unmatched closing parentheses from
the left, then count unmatched opening parentheses from the right, and add the
two counts. The bank builder asserts equality on every one of the 128 inputs.

## Six families

For each input, compute `balance`, `minimum_prefix`, and
`answer = balance - 2 * minimum_prefix`. Families are exact-one and partition
the declared domain.

| Index | Name | Rule | Domain count |
| --- | --- | --- | --- |
| 0 | `ONE_CLOSE` | answer = 1 and balance = -1 | 14 |
| 1 | `ONE_OPEN` | answer = 1 and balance = 1 | 14 |
| 2 | `THREE_CLOSE` | answer = 3 and balance < 0 | 28 |
| 3 | `THREE_OPEN` | answer = 3 and balance > 0 | 28 |
| 4 | `FIVE_MIXED` | answer = 5 | 36 |
| 5 | `SEVEN_MIXED` | answer = 7 | 8 |

The family labels describe structural forms, not solver quality. A family
failure is a wrong answer on a diagnostic input in that family.

## Diagnostic and evaluation banks

- Diagnostic bank: exactly 30 inputs, five per family.
- Evaluation bank: the other 98 inputs in the declared domain.
- The two banks are exact-input-disjoint and together exhaust the domain.
- The evaluation score `S` is the fraction of the 98 evaluation inputs answered
  correctly. Every evaluation input is scored; no sampling or weighting is used.
- Diagnostic selection is fixed independently of candidate-solver outcomes:
  for families 0 through 4, include one palindrome and four non-palindromes
  chosen by ascending SHA-256 of the input string; for family 5 include five
  non-palindromes chosen the same way. This yields exactly five diagnostic
  probes per family and leaves at least one evaluation input in every family.

## Concentration

For a diagnostic outcome vector `(f_0, ..., f_5)`:

```text
k = sum(f_j)
C = max(f_j) / k              if k > 0
C undefined                   if k = 0
```

A solver with `k = 0` is retained as a correctness baseline and is excluded
from the primary fixed-`k` concentration comparison.

## Execution constraints

Each solver is evaluated on one input per process under the strict Windows
Sandbox path. The solver may use only the Python standard library, may not read
files other than its own source, may not access the network, and may not print
anything except through the adapter contract. Expected outputs, family labels,
and the full bank remain outside the guest.
