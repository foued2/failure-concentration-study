# Output-Contract Amendment

Status: **`PREREGISTERED_AMENDMENT_BEFORE_PILOT_AUTHORIZATION`**

No model call was made before or during this amendment. No generated solver was requested or executed.

This amendment fixes the declared output contract before the strict adapter or its calibration run exists. It does not change the frozen banks, their hashes, or the completed `calibration-20261022T084750Z-288f2ac1` evidence. The pilot remains on `HOLD_NOT_AUTHORIZED`.

## Contract

`next-task/03_PILOT_PREREGISTRATION_2026-10-22.md` declares:

```text
solve(expr: str) -> int
```

The required return is an exact Python `int`:

- valid: `42`, `0`, `-6`;
- invalid and failed: `"42"`, `"0"`, `True`, `False`, `42.0`, `None`, and any non-`int` object.

A return value is accepted only when `type(value) is int`. `isinstance(value, int)` is not sufficient because `bool` is a subclass of `int`.

## Guest-boundary handling

The strict adapter records the actual return type inside the guest process, before the value is serialized. The value is not converted to text and then re-parsed as if its type were unknown.

The strict adapter writes one bounded JSON envelope to stdout:

```json
{"return_type": "int", "value": "42"}
```

For a non-`int` return, the envelope identifies the type and does not supply an integer value. The exact wrong-type representation is retained for audit, but the host must not accept it as an answer.

The host rejects an envelope unless:

- it is valid UTF-8/JSON with no duplicate or unexpected fields;
- `return_type` is exactly `"int"`;
- `value` is a bounded, strict ASCII decimal integer; and
- the parsed integer equals the host-side expected value.

This is a change from the calibration path, where the adapter stringified every return value. The existing adapter and its calibration evidence remain unchanged as historical evidence. The pilot uses a separate strict pipeline directory.

## Scoring rule

A wrong-type return is an answer failure, not an execution or transport error:

- diagnostic: it counts as a failed probe in the family of its input and therefore contributes to `k`;
- evaluation: it is not correct;
- it does not make the body ineligible;
- it is not excluded, replaced, or retried.

Malformed envelopes, malformed stdout, nonzero exits, crashes, and timeouts retain their existing handling. A timeout remains an ineligible transport result; a malformed or non-integer envelope is a failed answer.

## Calibration rerun

Before authorization, rerun the reference and all six prespecified mutants through the strict adapter in a new, separately identified calibration run:

- reference: 30/30 diagnostic passes and 30/30 evaluation correct;
- each mutant: 5/5 target-family diagnostic failures and 5/5 target-family evaluation failures;
- no non-target family failures;
- every row tree-terminated and not timed out.

The new run must record its own protocol, source hashes, prompt hash, bank hashes, and zero model calls. It must not modify or overwrite `calibration-20261022T084750Z-288f2ac1`.

## Tests required

- valid integer returns are accepted;
- numeric-string returns are rejected and counted as wrong-type failures;
- `True` and `False` are rejected;
- `42.0` and `None` are rejected;
- malformed envelopes are invalid;
- duplicate bodies remain retained without re-execution;
- the exact-int check uses `type(value) is int`, not `isinstance`.

## Authorization rule

The correction may be reported as `GO_FOR_FINAL_REVIEW` only after the focused tests and the strict calibration rerun pass. Generation remains `HOLD_NOT_AUTHORIZED` until a separate explicit authorization decision.
