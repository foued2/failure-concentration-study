# Gemini solver smoke test

Status: **PASS**

- Run: `gemini-smoke-20261021T171848Z`
- Provider: Google Gemini API
- Model: `gemini-3.5-flash-lite`
- Request count: 1
- Generation config: `temperature=1.0`, `maxOutputTokens=4096`
- Invoked: `2026-10-21T17:18:49.103661+00:00`
- HTTP status: 200
- Finish reason: `STOP`
- Source screen: accepted
- Generated body ID: `9644ca012b24cab65bfc816983486d06d27a813a33bf5d97edfd942d52f800e6`
- Diagnostic: 30/30 rows complete and passing
- Evaluation: 20/20 rows complete and correct
- Diagnostic suite wall time: 38.63 s
- Evaluation suite wall time: 29.62 s
- Pilot started by smoke run: no
- Pilot collection count: 0

This smoke used the existing generation prompt, output contract, source screen,
diagnostic bank, evaluation bank, and Sandbox execution path unchanged. The
generated source was executed through the existing suite-level Sandbox runner.
The smoke request is separate from the pilot cap.
