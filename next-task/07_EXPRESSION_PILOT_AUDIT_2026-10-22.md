# Expression Pilot Post-Hoc Audit

Status: **`POST_HOC_AUDIT_COMPLETE_NO_INTEGRITY_DEFECT`**

Date: 2026-10-22

Scope: audit of the completed expression pilot at
`next-task/expression-pilot-gemini-20261022T163536Z/`, committed in `5b49629`.
No model calls, regeneration, replacement sampling, prompt changes, bank changes,
or edits to the frozen run were made. The audit reads retained records only.

## Evidence used

- `next-task/expression-pilot-gemini-20261022T163536Z/attempts.json`
- `next-task/expression-pilot-gemini-20261022T163536Z/PILOT_RESULTS.json`
- `next-task/expression-pilot-gemini-20261022T163536Z/PROTOCOL.json`
- each `attempts/<attempt-id>/generated-solver.py`
- each `attempts/<attempt-id>/generated-response.txt`
- each `attempts/<attempt-id>/gemini-response.json`
- each `attempts/<attempt-id>/generation-metadata.json`
- each `attempts/<attempt-id>/source-screen.json`
- each `attempts/<attempt-id>/host-authoritative/diagnostic.json`
- each `attempts/<attempt-id>/host-authoritative/evaluation.json`
- `next-task/banks/diagnostic.json`
- `next-task/banks/evaluation.json`
- `next-task/03_PILOT_PREREGISTRATION_2026-10-22.md`
- `next-task/03A_PREREGISTRATION_AMENDMENT_2026-10-22.md`
- `next-task/03B_OUTPUT_CONTRACT_AMENDMENT_2026-10-22.md`
- `next-task/03C_PILOT_LAUNCH_PRECONDITIONS_2026-10-22.md`

The earlier independent reconciliation covered 6,141 checks with 0 errors. This audit
adds source, error-signature, and behavioral-diversity checks. It found no record
corruption, bank mismatch, expected-value mismatch, or scoring inconsistency.

## Committed-record verification

The frozen run directory and the committed result have no diff from `HEAD`
(`5b49629`). Re-derived from the committed `attempts.json` and host-authoritative
records:

- 30 generation requests; 27 model-written outputs; 19 eligible bodies; 21 distinct
  canonical bodies across all generated outputs (including rejected bodies).
- Eligible groups: 6 at `k=0`, 9 at `k=2, C=1.0`, 1 at `k=7, C=5/7`, 3 at
  `k=30, C=1/6`.
- `k=2`: 252/270 diagnostic `pass` and 252/270 evaluation `correct`; every body has
  the same failed diagnostic probes `F6_0`, `F6_3` and evaluation probes `E6_0`,
  `E6_3`.
- `k=30`: 180/180 host-authoritative rows are `crash`, exit code 1, empty raw
  stdout, null return, tree-terminated, and not timed out.

These re-derived counts match the tables below.

## Audit A: the `k=2` bodies

### Count

There are **9** distinct eligible `k=2`, `C=1.0` bodies, not seven. All nine are
different canonical source hashes under the frozen newline-normalization rule.

| Attempt | Body SHA-256 | `k` | `C` | Diagnostic failures | Evaluation correct |
| --- | --- | ---: | ---: | --- | ---: |
| attempt-0004 | `433b735840241b108c5d851e42b63c3cf8f46dd175e5bbea243b3dd8b3cfa4b8` | 2 | 1.000000 | F6_0, F6_3 | 28/30 |
| attempt-0006 | `9ff39e024cf6390b68b6ca4d3df9e821eed9dadecc579a7c4783a8a502c26f66` | 2 | 1.000000 | F6_0, F6_3 | 28/30 |
| attempt-0007 | `0393483b6fad28f33cfb3b35bb0b6e3bea459c5587c55ce767934772c51c7a5e` | 2 | 1.000000 | F6_0, F6_3 | 28/30 |
| attempt-0011 | `5cecbd1e100dbcd37519fdd2537fed33f1741d16667a1da3ef928c0221cf1b5a` | 2 | 1.000000 | F6_0, F6_3 | 28/30 |
| attempt-0012 | `ba8bad3d20c33f0f90a4e736ae0c7c3df49aa82e9e73aa268c1477ec5a62551c` | 2 | 1.000000 | F6_0, F6_3 | 28/30 |
| attempt-0013 | `a974e67030948c350c0ad0301998235b7d3537104729b673e8d5b75a5ae37a9f` | 2 | 1.000000 | F6_0, F6_3 | 28/30 |
| attempt-0020 | `41753a30d479b2f70e10e1a3115551720dd56eca9179874460ef658f100d19a9` | 2 | 1.000000 | F6_0, F6_3 | 28/30 |
| attempt-0025 | `b0abb598e2724ce7b57a5e861e7429b3c6b3a9d05f9685aed6eab752f438ac12` | 2 | 1.000000 | F6_0, F6_3 | 28/30 |
| attempt-0026 | `1873a80b916cc0e55e4095ee6b15897341ae346d7a69bf4d30b8f2f812d5bc46` | 2 | 1.000000 | F6_0, F6_3 | 28/30 |

### Exact failure pattern

Every one of the nine bodies has the same six-family diagnostic vector:

```text
(F1, F2, F3, F4, F5, F6) = (0, 0, 0, 0, 0, 2)
```

The failed probes are exactly `F6_0` and `F6_3` in every body. The corresponding
evaluation failures are exactly `E6_0` and `E6_3` in every body.

Across the nine bodies:

- diagnostic: 252/270 `pass`, 18/270 `crash`;
- evaluation: 252/270 `correct`, 18/270 `crash`;
- every passing diagnostic row has exit code 0, `return_type = "int"`, and
  `solver_output` equal to the host expected value;
- every passing evaluation row has exit code 0 and `correct = true`;
- every failed row has exit code 1, empty raw stdout, `return_type = null`,
  `solver_output = null`, `error = "crash"`, `tree_terminated = true`, and
  `timed_out = false`;
- no failed row produced a valid integer that was then scored wrong;
- no row was malformed or lost in transport.

`F6` is the whitespace family. The five diagnostic inputs are:

| Probe | Expression | Expected | Status in all 9 bodies |
| --- | --- | ---: | --- |
| F6_0 | `" 2 + 3 "` | 5 | crash |
| F6_1 | `"4 + 5"` | 9 | pass |
| F6_2 | `"1+ 2"` | 3 | pass |
| F6_3 | `" 9 - 2 "` | 7 | crash |
| F6_4 | `"3 + 0"` | 3 | pass |

The evaluation counterparts are `E6_0 = " 3 + 4 "` and `E6_3 = " 8 - 1 "`, both
with leading spaces, and both crash in every body.

### Cause and classification

All 18 diagnostic crash rows and all 18 evaluation crash rows have the same terminal
error:

```text
IndentationError: unexpected indent
```

The traceback points to `ast.parse(expr, mode='eval')` in each generated source. The
leading space in `F6_0`, `F6_3`, `E6_0`, and `E6_3` is passed to `ast.parse` without
normalization. Every one of the nine bodies calls:

```python
ast.parse(expr, mode='eval')
```

and none calls `ast.parse(expr.strip(), ...)`.

The task prompt explicitly permits optional ASCII spaces, and `F6` is declared as the
whitespace family. The inputs are therefore valid under the task contract. The failure
is a genuine solver implementation bug: failure to strip leading whitespace before
`ast.parse`. It is not a harness error, not a serialization error, and not a scoring
error.

The source line number in the traceback differs across bodies (`solver.py` lines 32,
37, 40, or 42) because the source layouts differ. The exception type, failing input,
and behavior are the same.

### Source and behavioral diversity

All nine are distinct canonical bodies, but they are not nine independent behavioral
samples:

- 9/9 use `ast.NodeVisitor`;
- 8/9 implement per-node `visit_*` methods; 1/9 (`attempt-0012`) uses a single
  `visit` dispatcher;
- 9/9 use the same raw-string `ast.parse(expr)` path;
- pairwise source-text similarity is high for most pairs (26 of 36 pairwise
  `difflib` ratios are at least 0.90; the single-dispatch body is the main outlier);
- all 36 pairwise source ASTs are distinct, so the canonical-body rule correctly
  counts nine bodies;
- the diagnostic and evaluation outcome vectors are identical for all nine.

**Conclusion for Audit A:** the `k=2`, `C=1.0` cluster is one shared missing-strip
bug replicated across nine AST-based sources. The concentration value is real under
the frozen rule, but the cluster does not represent nine independent semantic failure
patterns. It should be reported as **9 canonical bodies, 1 behavioral class, 1 shared
failure mechanism**.

## Audit B: the `k=30` bodies

### Count and source-screen state

There are 3 eligible bodies with `k=30` and `C=0.16666666666666666`:

| Attempt | Body SHA-256 | Screen source bytes | Screen | Diagnostic | Evaluation |
| --- | --- | ---: | --- | --- | --- |
| attempt-0002 | `c80287fe075d3b717c612180f7a22273fd10293dbe494a68ca00b712736c8bdb` | 2541 | accepted | 30/30 crash | 30/30 crash |
| attempt-0009 | `b8024a66c5958c0369070957991b80a2f352c3398f22a16e5df0130497e72e53` | 1432 | accepted | 30/30 crash | 30/30 crash |
| attempt-0015 | `f1f6a1e7e29c859ff917a3d0d0b8d3e8a8df662a5cbd9c63518bafbe5a66ff03` | 1364 | accepted | 30/30 crash | 30/30 crash |

All three source screens report `accepted = true` with no reasons and a body hash that
matches the recorded canonical body. All three generation responses have HTTP 200,
`finish_reason = "STOP"`, and substantial source output; none was truncated or
extracted incorrectly.

### Execution evidence

Across the three bodies, all **180** host-authoritative rows (90 diagnostic, 90
evaluation) are:

- status `crash`;
- exit code 1;
- empty raw stdout;
- `return_type = null`;
- `solver_output = null`;
- `tree_terminated = true`;
- `timed_out = false`.

No valid integer envelope exists in this group. No row is a wrong answer with a
valid output; every row fails before producing an answer. The evaluation failure count
of 0/30 per body is therefore an execution failure count, not a semantic wrong-answer
count.

### Per-body cause

**attempt-0002 (tokenizer / shunting-yard):** all 60 rows fail with:

```text
TypeError: 'in <string>' requires string as left operand, not int
```

at `elif tok in '+-':`. The tokenizer appends integer tokens as Python `int` objects,
and the unary-minus preprocessing compares every token to the string `'+-'` before
checking its type. This is a genuine solver type/logic bug. It is not an interface
defect: the solver itself creates the integer tokens.

**attempt-0009 (AST `SafeEval`):** all 60 rows fail, with two error signatures:

- 56 rows: `AttributeError: module 'ast' has no attribute 'Num'` at
  `isinstance(node, ast.Num)`;
- 4 rows (2 diagnostic, 2 evaluation): `IndentationError: unexpected indent` at
  `ast.parse(expr)` for the two leading-space `F6`/`E6` inputs.

The source handles `ast.Constant` for integer constants but still evaluates
`isinstance(node, ast.Num)` for every `BinOp`. The execution runtime's `ast` module
has no `Num` attribute. The body also does not strip leading whitespace, so the
leading-space probes fail earlier at `ast.parse`.

**attempt-0015 (AST `Evaluator`):** all 60 rows fail with:

```text
AttributeError: module 'ast' has no attribute 'Num'
```

at `isinstance(node, ast.Num)`. This source does call `ast.parse(expr.strip(), ...)`,
so the leading-space probes reach the same `ast.Num` line and fail there. The failure
is not whitespace-specific; it is universal.

### Classification

| Body | Classification | Evidence |
| --- | --- | --- |
| attempt-0002 | Execution failure: genuine solver type/logic bug | 60/60 `TypeError` at `tok in '+-'` |
| attempt-0009 | Execution failure: solver/runtime API incompatibility plus missing whitespace normalization | 56/60 `ast.Num` `AttributeError`; 4/60 leading-space `IndentationError` |
| attempt-0015 | Execution failure: solver/runtime API incompatibility | 60/60 `ast.Num` `AttributeError` |

None of the three is a genuine **wrong answer** in the sense of a completed solver
returning an incorrect integer. None is a harness or serialization failure. The host
correctly recorded the worker exits, empty stdout, exception classes, and
tree-termination state.

The `C = 1/6` value is a structural consequence of every row crashing: five crashes in
each of six families. It is not evidence that failures are concentrated in a
meaningful semantic family.

### Runtime-version gap

The host-side interpreter used for this audit is CPython 3.14.0, and the sandbox
tracebacks confirm that the worker's `ast` module has no `Num` attribute. `ast.Num`
is a removed compatibility alias, not available in the execution runtime. The prompt
and `PROTOCOL.json` do not pin a Python version. That is a specification gap: a model
may reasonably write older-API code, but the run's declared execution environment
does not support it.

This gap explains two of the three `k=30` failures. It does not change the frozen
result, because the host correctly scored the code under the environment that was
actually used. It does limit any claim that these bodies demonstrate semantic
reasoning failures. The correct description is **runtime/API incompatibility**, not
"the solver gave wrong arithmetic answers."

### Context: the single `k=7` body

For completeness, `attempt-0022` is the only eligible `k=7` body
(`C=5/7=0.7142857142857143`, body
`f4f1ab638ff617c1c88b4cc2f0a11cc1c507c22eee56e521326d7ffe3a87eb42`). It scores
23/30 on both diagnostic and evaluation, with failures in `F4` (5) and `F6` (2) in
both suites. It is a singleton and cannot support a fixed-`k` comparison. The
audit's detailed behavioral checks focus on the `k=2` and `k=30` groups because
those are the only groups with more than one body.

## Integrity conclusion

No concrete integrity defect was found:

- bank hashes and expected values match;
- body hashes and source-screen records match;
- host-authoritative diagnostic and evaluation records match the manifest;
- valid exact-int envelopes were scored correct;
- crash rows were scored as failures, as required;
- no valid solver output was discarded or mis-serialized;
- no row is missing, duplicated in the manifest, or untree-terminated.

Because no integrity defect was found, no append-only audit note is required. The
frozen run remains unchanged; this report is an additive post-hoc audit.

## Interpretation limits

The pilot's frozen state remains **`REPEATED_K_BUT_NO_C_SEPARATION`**. The audit does
not reclassify it. It does, however, narrow what the state can mean:

1. The `k=2` group is not nine independent natural failure patterns. It is one shared
   whitespace-normalization defect replicated across nine AST-based sources.
2. The `k=30` group is not a semantic failure-concentration signal. It is universal
   execution failure, with two of three bodies affected by a removed Python API and
   one by a tokenizer type bug.
3. The pilot therefore supplies little evidence about the concentration question. It
   is better read as evidence that this generator/task/execution-contract combination
   produced redundant implementations, shared trivial defects, and catastrophic
   crashes, not as evidence for or against the hypothesis.

## Evidence paths

- Run root: `next-task/expression-pilot-gemini-20261022T163536Z/`
- k=2 examples: `attempts/attempt-0004/`, `attempts/attempt-0012/`,
  `attempts/attempt-0026/`
- k=30 examples: `attempts/attempt-0002/`, `attempts/attempt-0009/`,
  `attempts/attempt-0015/`
- Host results: each attempt's `host-authoritative/diagnostic.json` and
  `host-authoritative/evaluation.json`
- Screens: each attempt's `source-screen.json`
- Banks: `next-task/banks/diagnostic.json`, `next-task/banks/evaluation.json`
- Frozen result: `next-task/06_EXPRESSION_PILOT_RESULT_2026-10-22.md`
