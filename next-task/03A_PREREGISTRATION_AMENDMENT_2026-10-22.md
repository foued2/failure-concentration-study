# Preregistration Amendment: Expression Task

Status: **`PRE_AUTHORIZATION_AMENDMENT`**

This amendment is written before any expression-task generation. It does not change the frozen diagnostic or evaluation banks, the calibration panel, the calibration evidence, or the 30-attempt cap. It resolves review points that the original preregistration left implicit.

## Unary-minus scope

The declared grammar allows **one** unary minus before a primary, including a parenthesized primary. Stacked unary minus (`--3`, `-(-3)`) and empty or whitespace-only expressions are outside the declared grammar and are not scored.

Neither frozen bank contains stacked unary minus or an empty expression. A solver's behavior on those out-of-grammar inputs is not evidence for or against the six declared families. If a later task version adds stacked unary minus, it requires a new task version, new banks, and a new calibration.

## Distinctness rule

A canonical body is identified by the SHA-256 of its source after newline normalization only (`\r\n` and `\r` to `\n`). This is the existing `pilot_tool.body_id` rule.

- Exact duplicate normalized sources are retained as attempts but are not distinct bodies.
- No AST canonicalization is used.
- Source variants that differ in comments, variable names, or formatting count as distinct under this predeclared rule.
- The rule is frozen before generation; it must not be changed after outcomes are observed.

## Ceiling and no-contrast outcomes

The pilot may find that every eligible body has `k = 0`. In that case the state is:

**`CEILING_NO_FAILURE_VARIATION`**

This means the required fixed-`k`, different-`C` comparison was not demonstrated for this task and procedure within the cap. It does not mean the task is easy in general, that concentration is invalid, or that a predictive effect is absent.

Other missing conditions are reported with the same status discipline:

- `NO_INCORRECT_BODIES`
- `INCORRECT_BODIES_BUT_NO_REPEATED_K`
- `REPEATED_K_BUT_NO_C_SEPARATION`
- `C_SEPARATION_WITHOUT_EVALUATION_SEPARATION`
- `INCOMPLETE_OR_INELIGIBLE_SUITES`
- `GENERATION_HALTED`

If the pilot produces no useful contrast, the natural-solver route for this preregistered expression task ends. A harder task is **not** an automatic next attempt. Any harder task would require a separate structural task-selection decision, new banks, new calibration, and a separate preregistration and review. There is no post-result search across tasks until one produces a favorable contrast.

If a qualifying contrast is observed, the next step is review of the raw pilot evidence. It does not authorize predictive modeling, a confirmatory claim, or extrapolation beyond this generator and task.

## Source-screen and shortcut policy

The frozen source screen blocks `eval`, `exec`, `compile`, direct `open`, and the listed process/network/import capabilities. A source using one of those blocked constructs is retained as an attempt and is **not executed**.

The expression task's obvious shortcut is `eval`. It is blocked by the existing screen. `ast.literal_eval` is not a full arithmetic evaluator for this grammar and is not specially exempted or specially blocked; a solver may implement its own parser with the `ast` module. If a task-specific bypass is discovered that makes execution invalid, the disposition is **HOLD**, with the exact gap reported; the screen must not be silently broadened or patched after seeing model behavior.

A rejected source is an observed attempt, not a dropped sample and not a replacement opportunity.

## Oracle and expected-value separation

The expression runner must put only the current expression and its probe identity into the guest-readable suite payload. Expected outputs, family labels, host records, oracle code, and authoritative results remain host-side.

The known limitation remains: the guest can read the other expressions exposed in the current mapped suite. Source screening is a best-effort policy, not a security boundary. Expected values must not be present in the mount.

## No model calls

This amendment involves no provider request. It does not authorize generation. The 30-attempt fixed design and the separate review gate remain in force.
