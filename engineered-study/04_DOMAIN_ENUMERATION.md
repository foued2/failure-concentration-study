# Domain enumeration

Status: frozen before any solver generation.

## Exhaustive set

The domain is

```text
D = {"".join(chars) : chars in product("()", repeat=7)}
```

It contains exactly 128 distinct strings. No input is sampled, weighted, or
added later. Every input has an exact oracle answer in `0..7`.

## Family partition

For each text, let `balance` be openings minus closings and `minimum` be the
minimum prefix balance including the empty prefix. The answer is
`balance - 2*minimum`.

| Family | Rule | Count |
| --- | --- | --- |
| `ONE_CLOSE` | answer 1, balance -1 | 14 |
| `ONE_OPEN` | answer 1, balance 1 | 14 |
| `THREE_CLOSE` | answer 3, balance < 0 | 28 |
| `THREE_OPEN` | answer 3, balance > 0 | 28 |
| `FIVE_MIXED` | answer 5 | 36 |
| `SEVEN_MIXED` | answer 7 | 8 |
| **Total** | exact partition | **128** |

The partition is asserted during bank construction. Every family has at least
six inputs, so it can supply five diagnostics and retain at least one evaluation
input.

## Bank split

| Bank | Count | Purpose |
| --- | --- | --- |
| Diagnostic | 30 | Compute `k` and `C`; never contributes to `S` |
| Evaluation | 98 | Compute `S`; no input appears in the diagnostic bank |
| **Total** | **128** | exhaustive domain |

The evaluation counts by family are 9, 9, 23, 23, 31, and 3. The split is by
exact input string, not by text hash alone.

## Diagnostic selection rule

For families 0–4: one palindrome and four non-palindromes, each chosen by
ascending SHA-256 of the exact input text, with the text itself as a
deterministic tie-break. For family 5: five non-palindromes chosen the same way.
The palindrome in each of families 0–4 is the lexicographically first among
equal-hash candidates after sorting; because SHA-256 collisions are absent in
this set, ordering is by digest.

This gives one diagnostic failure in each of five families for the spread
palindrome control. The rule was fixed before controls were built.

## Recorded hashes

These are the hashes of the current files and match the frozen Gate 1 banks:

```text
domain.json       03a7fb21334909d5cb30fc7a2c5a3ea2a4db8fc425cadb04cad476e620a5559d
diagnostic.json   954be8607889896c2068f21851589060f1ff60ed6347daa24a67dacf0e7a0938
evaluation.json   98a370e0cb174ac4dfa67a4b484354f0050b2699186ea6c5ec05c0927655fc6c
MANIFEST.json     c5b7ef75b55605110fb4ce6b76b34f557e6a7ddef5c09503b138b04345da4f10
```

`MANIFEST.json` also records the hashes of `core/model.py`, `build_banks.py`,
and `03_TASK_SPEC.md`.
