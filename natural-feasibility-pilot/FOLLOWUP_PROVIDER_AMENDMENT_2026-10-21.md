# Follow-up provider-switch amendment: October 21, 2026

## Status

Append-only amendment to the frozen follow-up protocol in
`FOLLOWUP_PROTOCOL_2026-11-19.md` / `.json` (commit `74cd419`) and to the
interpretation branches in `FOLLOWUP_DECISION_MEMO_2026-10-21.md` (commit
`dd5be4a`). It does not alter the closed pilot evidence at commit `b0151ec`,
the frozen protocol, the decision memo, or the Codex follow-up run.

## Trigger

The authorized immediate Codex follow-up made one availability request in run
`natural-pilot-followup-20261021T164204Z`. The request was invoked at
`2026-10-21T16:42:04Z`, finished at `16:42:12Z`, returned exit code 1 with no
model output, and was classified as a provider usage-limit failure. The run is
`HALTED_GENERATION_USAGE_LIMIT` at 1/100 requests and is final. Evidence is at
commit `f4e1b91`.

The user authorized switching to an accessible provider immediately. The
Codex restriction does not require waiting until November 19, 2026 when a
different provider is used. Codex is not retried under this amendment.

## Provider selection

DeepSeek was checked first and is not available in the accessible environment:
no `DEEPSEEK_API_KEY`, no DeepSeek configuration, and no `openai`, `requests`,
`httpx`, or `google` client packages. Gemini is accessible through the
`GEMINI_API_KEY` environment variable; the key value is never written to the
repository or logs.

- Provider: Google Gemini API
- Model selector: `gemini-2.5-flash`
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent`
- Generation config: `{"temperature": 1.0, "maxOutputTokens": 4096}`
- Client: Python standard-library `urllib`

The models endpoint returned HTTP success and listed 50 models. A separate
minimal health request returned an HTTP-success envelope but no text: with
`maxOutputTokens: 8`, the candidate finished with `MAX_TOKENS` and
`thoughtsTokenCount: 4`. That health check is not a solver smoke result and is
not evidence of generation quality. It is recorded here only as provider
reachability evidence.

## New run and separateness

A new pilot run will use the prefix `natural-pilot-gemini-<UTC timestamp>` and
a fresh cap of at most 100 generation requests. It is a separately identified
provider population, not a continuation of the Codex follow-up and not a
third identical run under the frozen Codex protocol. No equivalence to the
Codex-generated population is claimed, and outcomes will not be pooled.

The preflight health request and the one-request solver smoke are outside the
pilot cap. The pilot cap starts when the new Gemini pilot run is created. Every
pilot generation invocation, including failures and duplicates, counts.

## Preserved design

The new run preserves the exact SSSP generation prompt, output contract,
source-policy screen, 30-probe diagnostic bank, 20-input evaluation bank,
Sandbox execution runner, input-integrity checks, and the frozen fixed-`k` /
different-`C` feasibility criterion. No prompt tuning, replacement sampling,
selective retries, outcome-based stopping, or predictive modeling is allowed.

Before pilot collection, one Gemini-generated solver must pass a real
known-task smoke test through the actual Sandbox path. The smoke criteria are:
source accepted by the frozen source screen; all 30 diagnostic rows complete
and pass; all 20 evaluation rows complete and correct. A mere HTTP-success
response is insufficient. If the smoke fails, the failure is retained and the
pilot does not start.

The pilot runner requires the PASS smoke-result file and records its SHA-256 in
the pilot protocol. The smoke result is separate evidence from the pilot.

## Limitations and disclosure

- The Gemini backend version or immutable snapshot is unavailable, so no exact
  reproducibility claim will be made.
- The generation prompt does not contain test inputs, but the source screen is
  best-effort and the full phase-specific input suite is guest-readable during
  its Sandbox session.
- The model population changed. Any later feasibility interpretation must say
  so explicitly.
- No outcome claim, concentration-effect claim, or predictive claim is
  authorized by this amendment.

## Scope controls

The closed runs, frozen protocol, decision memo, and `README.md` remain
unchanged. The four pre-existing untracked files are untouched. No push, merge,
tag, or publication is part of this amendment. The new runner and smoke runner
are committed separately from the pilot evidence.
