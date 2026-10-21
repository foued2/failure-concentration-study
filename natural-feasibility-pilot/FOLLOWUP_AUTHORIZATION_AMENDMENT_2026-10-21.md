# Authorization amendment: immediate follow-up start

**Date: 2026-10-21T16:40:57Z**

**Status: append-only amendment; supersedes only the start-time gate**

The owner, Foued, explicitly authorizes starting the prepared follow-up now. This
supersedes the `2026-11-19T18:55:00Z` not-before gate for this immediate start only.
It does not change the frozen follow-up protocol, its feasibility criterion, its
request cap, or any frozen input or runner logic.

## Preserved commitments

- The closed first run `natural-pilot-20261021T123319Z` remains closed at 100
  generation requests and is not reopened, extended, or relabeled.
- The follow-up protocol remains frozen at commit `74cd419`.
- The pre-collection decision memo remains frozen at commit `dd5be4a`.
- The exact prompt, source screen, diagnostic battery, evaluation bank, execution
  configuration, and feasibility criterion remain unchanged.
- The follow-up cap remains 100 generation requests.
- No replacement sampling, prompt tuning, outcome-based selection, predictive
  modeling, or automatic third run is authorized.
- The known input-visibility limitation remains disclosed: source screening is a
  best-effort policy, not a security guarantee, and a solver may be able to inspect
  other inputs in its mounted suite.
- The closed run, frozen studies, and `README.md` will not be modified. No push,
  merge, tag, or publication is authorized.

## Immediate-start procedure

The frozen runner's not-before guard is not edited. The start uses a documented
one-off availability-check driver that imports the frozen generation request function
and records the result under a new, separately identified follow-up run directory.

The driver performs exactly one generation invocation first. That invocation is the
availability check and counts toward the follow-up cap.

- If the provider returns a hard usage limit or equivalent block, record the request,
  set the run state to `HALTED_GENERATION_USAGE_LIMIT`, and stop immediately. Do not
  retry.
- If the request succeeds, preserve the generated body, record the actual invocation
  time and available model identity, and report the availability result before
  continuing with the pilot.

The CLI has no local usage-status command that reports the account allowance. The
single availability request is therefore the operational check. The backend version
and immutable snapshot remain unavailable; no exact reproducibility claim is made.

## Run identity

The new run directory will be `natural-pilot-followup-<UTC timestamp>` and is distinct
from the closed first run. Its `protocol.json` will record the actual start time, the
superseded gate, this amendment, and the available model identity.
