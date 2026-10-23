# Task selection

Status: selected once. No fallback task is permitted after seeing solver results.

## Selected task

`paren7_min_insertions`: return the minimum number of parenthesis insertions
needed to balance a length-7 string over `(` and `)`.

The declared domain is exhaustively enumerated. The primary oracle is the
prefix-balance identity; the independent oracle is a two-scan unmatched-count
method. They agree on all 128 inputs.

## Why this task

- The domain is finite, small, and fully enumerable.
- Both oracles are simple enough to verify independently.
- The answer is a native exact integer with no tolerance.
- Six structural families emerge from one unambiguous rule and cover the whole
  domain.
- The family partition supports a fixed-`k` comparison: at `k = 5`, both `C = 1`
  and `C = 0.2` are attainable.
- The task is unrelated to the retired pipeline hidden-structure claim.
- A solver can be evaluated one input per process under the strict Sandbox.

## Domain and bank construction

The domain has exactly 128 inputs. Each family supplies at least five
diagnostics. The diagnostic bank uses one palindrome in families 0–4 and none
in family 5, with the remaining slots assigned by ascending SHA-256. The
evaluation bank is the exact 98-input complement.

No random seed is needed for bank construction. The selection does not depend
on any candidate solver, model, generator, or earlier result.

## Fixed-`k` concentration range

At `k = 5`, the feasible vectors include:

- six maximum-concentration vectors, each with all five failures in one family;
- six low-concentration vectors with failures spread over five families.

The study targets all six maximum vectors (20 slots each) and one low vector
`[1,1,1,1,1,0]` (30 slots), for 150 slots. The low target omits `SEVEN_MIXED`;
this choice is fixed here and is not tuned after observing solvers.

## Alternatives rejected

- **Balanced-bracket validity:** the domain contains too few invalid cases for a
  stable six-family concentration design.
- **Exact edit distance on longer strings:** a larger domain weakens exhaustive
  enumeration and increases the chance of hidden difficulty outside the declared
  families.
- **Mixed arithmetic/string tasks:** destroys a single oracle and invites
  task-specific shortcuts.
- **Sampling from a large domain:** conflicts with the requirement for a
  complete finite domain and a disjoint exhaustive evaluation.

## Limitation

The six maximum-concentration vectors necessarily use six different carrier
families. The design therefore cannot, by itself, separate `C` from carrier
family. This limitation is recorded before generation and is a Gate 1 issue.
