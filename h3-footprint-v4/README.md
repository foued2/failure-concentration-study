# H3 Footprint Gate V4 proposal

This directory is a separate proposal cloned from the V3 feasibility harness. It does not replace or modify V3. V3 keeps its original three OpenCode model population and remains unrun.

V4 proposes a no-key hosted-model route using `gpt-oss-120b` at OVHcloud AI Endpoints and standard GitHub-hosted runners. A one-request operational smoke completed on 2026-10-28 with no API key. The endpoint is rate limited, and shared capacity may return 429 responses. The published anonymous rate is two requests per minute per IP/model; the generator design therefore serializes requests with a 35-second minimum start interval. See `GATE.md`.

V4 also proposes Docker-based isolation on an ephemeral Linux runner in place of Windows Sandbox. This is a different execution boundary and must be independently tested. The host scoring process must keep expected values; each candidate container receives only its own source and the current probe input. No solver body may run on the host.

**Status: not frozen, no batch generation, no candidate scoring.** The smoke completion is not a solver candidate and is not in the study dataset. Before V4 can run, the container isolation battery and all V4 tests must pass, the new model population and isolation method must be re-reviewed, and a new version-specific freeze plus explicit generation authorization must be committed.

This route uses the remote GitHub-hosted Actions environment, not PyCharm, your local file paths, an installed local coding agent or an API key. A future job will run remotely and preserve its logs/artifacts in GitHub.