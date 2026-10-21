# Gemini solver smoke test

Status: **FAIL / HOLD**

- Run: `gemini-smoke-20261021T170725Z`
- Provider: Google Gemini API
- Model: `gemini-2.5-flash`
- Request count: 1
- Generation config: `temperature=1.0`, `maxOutputTokens=4096`
- Invoked: `2026-10-21T17:07:25.463070+00:00`
- HTTP status: 503
- Provider status: `UNAVAILABLE`
- Provider message: "This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later."
- Source returned: none
- Source screen: not run
- Sandbox execution: not run
- Pilot started: no
- Pilot collection count: 0

The smoke did not produce a solver body, so it did not test generation quality or
Sandbox execution. No retry was made and no model substitution was attempted.
The provider-switch amendment and pilot cap remain unchanged. A future smoke
must use a new run ID; this failed smoke is retained as evidence and must not be
resumed.

This run is separate from the pilot cap. The authorized Gemini pilot was not
started.
