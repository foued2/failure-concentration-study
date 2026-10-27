# INVALID_RUN: H3 footprint gate, 2026-10-27

**Status:** `INVALID_RUN`. The frozen gate executed, but its verdict is invalid and uninterpretable
because of a defect in the frozen candidate-extraction harness. This is an audit record, not a test of H3.

**Scope boundary:** this record does not amend the frozen gate, does not create a replacement tag, does not
generate more candidates, and does not assert any H3 conclusion. The frozen artifacts and tag
`h3-footprint-freeze-2026-10-26` are unchanged.

## What was executed

- Branch/worktree: `gate/h3-footprint-2026-10-26` (isolated; review branches untouched).
- Frozen budget: 72/72 batches, 8 requested bodies per batch, 3 generators, 3 prompt variants.
- Distinct stored bodies: 526.
- Frozen threshold evaluation: `results/footprint.json`, `results/REPORT.md`.

## Frozen verdict, marked invalid

The unmodified `run_gate.py` produced:

- Verdict: `FAIL (degeneracy)`
- All-or-none fraction: `0.994`
- Eligible bodies (`2 <= k <= 24`): 5
- Supported cells: 0

**This verdict is `INVALID_RUN`.** It is not evidence that H3 is untestable, and it is not a scientific
result about the instrument.

## Defect

`generate.py:extract()` splits each fenced code block at the first `def solve(...)` and discards the
preceding text. When a model emits a module-level import before `def solve`, that import is silently
dropped from the stored body. Example, `generated/raw/batch-043.txt`:

```python
import heapq          # dropped by extract()

def solve(n, edges, src, dst):
    ...
```

The stored body then references `heapq` without importing it, raises `NameError` on every probe, and is
recorded as `k=30` (all-fail). Per the frozen failure rule, a crash counts as a failed probe, so the gate
faithfully scores a corrupted candidate body.

Evidence:

- 174 of 544 raw code blocks with a `def solve` carried module imports in the prelude, and every non-empty
  prelude was an import prelude.
- Restoring the dropped imports changes `k` for 153 of 526 stored bodies.
- 153 of the 163 stored `k=30` bodies move below `k=30`; 147 of them become `k=0`.

Reproduce with `python audit/extractor_defect.py`; machine-readable output is in
`audit/extractor_defect.json`.

## Import-restoration diagnostic (not a replacement result)

After restoring imports, the 526 stored bodies break down as:

| class | bodies |
|---|---:|
| `k=0` | 497 |
| eligible `2<=k<=24` | 10 |
| `k=25` | 5 |
| `k=29` | 4 |
| `k=30` | 10 |
| **total** | **526** |

The corrected all-or-none fraction is `0.989`, with only 10 eligible bodies. This is diagnostic evidence
about the size of the harness effect. It is **not** a result from the frozen harness, is not a substitute
gate output, and does not establish that a corrected instrument would pass or fail. No H3 conclusion is
drawn from it.

## Denominator reconciliation

The `526` total is fully accounted for; there is no missing subset. The earlier apparent `526` vs `517`
discrepancy came from reading the eligible bucket (`10`) and the total (`526`) without the non-eligible
tail:

`526 = 497 (k=0) + 10 (2<=k<=24) + 5 (k=25) + 4 (k=29) + 10 (k=30)`.

The frozen run's own distribution also sums to 526:
`350(k=0) + 1(k=4) + 1(k=5) + 1(k=7) + 1(k=13) + 1(k=15) + 4(k=25) + 4(k=29) + 163(k=30)`.

## Artifacts preserved

- Frozen artifacts and `FREEZE.json` hashes: unchanged.
- `generated/attempts.jsonl`: per-batch generation records.
- `generated/bodies/`: 526 stored bodies actually scored.
- `generated/raw/`: raw model output used to demonstrate the dropped preludes.
- `results/footprint.json`, `results/REPORT.md`: unmodified frozen-harness output.
- `audit/extractor_defect.py`, `audit/extractor_defect.json`: defect evidence and diagnostic.

## Required next step

A corrected instrument version would need a separate authorization, a fixed extractor, and a new freeze
and tag created before any candidate is generated. None of that is performed here.
