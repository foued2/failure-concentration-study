# Follow-up model-switch amendment: October 21, 2026

## Status

Append-only amendment to `FOLLOWUP_PROVIDER_AMENDMENT_2026-10-21.md` (commit
`8848384`) and the frozen follow-up protocol at commit `74cd419`. It preserves
all prior evidence, including the failed `gemini-2.5-flash` smoke run at commit
`121ea3c`. It does not alter the closed pilot, the frozen protocol, the decision
memo, or `README.md`.

## Reason for the switch

The first Gemini smoke attempt, run `gemini-smoke-20261021T170725Z`, made one
generation request to `gemini-2.5-flash` at
`2026-10-21T17:07:25.463070+00:00` and received HTTP `503 UNAVAILABLE`. The
provider response said: "This model is currently experiencing high demand.
Spikes in demand are usually temporary. Please try again later."

This is a server-capacity response, not evidence that the API key has exhausted
its quota. The Codex retry date of November 19, 2026 is unrelated and does not
apply to this Gemini route. Per the user's instruction, make one bounded model
switch rather than waiting for the Codex date.

## New model

- Provider: Google Gemini API (unchanged)
- Previous model: `gemini-2.5-flash`
- New exact model ID: `gemini-3.5-flash-lite`
- Display name reported by the models endpoint: `Gemini 3.5 Flash Lite`
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent`
- Generation config: `{"temperature": 1.0, "maxOutputTokens": 4096}`
- Client: Python standard-library `urllib`
- API key: existing `GEMINI_API_KEY`; the value is never written to the
  repository or logs

The models endpoint was checked at `2026-10-21T17:17:41Z` and listed
`models/gemini-3.5-flash-lite` with `generateContent` support. The model was not
used in this project before this amendment.

## Scope and sequencing

This is one new, separately recorded smoke test, not a continuation of the
failed `gemini-2.5-flash` smoke. Use the existing generation prompt and output
contract unchanged. Make one generation request to `gemini-3.5-flash-lite`.

If the model returns valid source, run that source through the existing Sandbox
smoke pipeline. Require all 30 diagnostic rows and all 20 evaluation rows to be
captured, independently validated, and complete, with 30/30 diagnostic passes
and 20/20 evaluation correctness. The source-policy screen must also accept the
source.

If this request or its Sandbox execution fails, record the exact failure and
stop. Do not cycle through additional models automatically. Do not retry the
failed request. Do not tune the prompt or replace the generated solver body
with a different body.

If the new smoke passes, record its result and launch a distinct bounded pilot
with a new run ID and a cap of at most 100 generation requests. The pilot runner
must require the PASS smoke result and record its SHA-256.

## Preserved measurement rules

The new pilot keeps the exact generation prompt, output contract, source
screen, 30-probe diagnostic bank, 20-input evaluation bank, Sandbox execution
runner, input-integrity checks, and fixed-`k` / different-`C` feasibility
criterion. No prompt tuning, replacement sampling, selective retries,
outcome-based stopping, or predictive modeling is allowed.

The generator population changes again. No equivalence to the
`gemini-2.5-flash` attempt or the Codex population is claimed, and outcomes are
not pooled across them. The pilot cap remains separate from the preflight
health check and smoke request.

## Scope controls

The prior pilot remains closed. The failed `gemini-2.5-flash` smoke remains
retained as evidence and is not resumed. Do not modify frozen studies or
`README.md`, and do not push, merge, tag, or publish. No predictive or
concentration-effect claim is authorized by this amendment.
