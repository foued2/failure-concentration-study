# V8 runbook sequence review

Date: 2026-10-27. Review only; V8 remains frozen.

The frozen GATE.md says candidate generation must not begin until the execution-isolation check passes. The frozen RUNBOOK.md places Stage A (generation) before Stage B1 (the Sandbox isolation probe). Its introduction also says not to begin either generation or evaluation until the isolation check passes. These statements conflict.

No V8 generation was run, so the contradiction has not yet affected a candidate sample. A successor should use one explicit order. To preserve the stricter existing authorization rule:

1. Verify the freeze and local environment without model calls.
2. Run the isolation probe in a first Sandbox session.
3. Inspect and preserve the passing report.
4. Only then run the authorized generation segment.
5. Evaluate in a fresh Sandbox session using the repaired trust boundary.

Do not resolve this by silently treating the Runbook's order as an override of GATE.md. Any change to the authorization condition must be explicit in a new version.