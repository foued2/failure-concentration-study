# Reproduction Guide — GLM-Agent H3 Exploratory Footprint Screen (2026-10-29)

Prerequisites:
- Linux sandbox with user-namespace support: `unshare -r -m -n /bin/sh -c 'id'` must work.
- `z-ai` CLI available and keyless (existing platform access).
- Clone of `foued2/failure-concentration-study` (inspected at `f9cc893`, branch
  `gpt/h3-v10-integrity-fix-2026-10-29`). Frozen branches are never modified.
- Python 3.12+ on the host (trusted supervisor code). Candidate execution uses
  the system `/usr/bin/python3` inside the chroot view (3.13.5 here).

Paths used by the scripts (edit the constants at the top of each script if your
layout differs):
- `REPO_PILOT` = `<clone>/h3-footprint-v10-cloud/copilot_auto_pilot.py`
- `INSTRUMENT_PATH` = `<clone>/h3-footprint-v3/instrument.py`
- staging dir `/var/tmp/h3trusted/{trusted,candidate}` (world-writable location
  outside `/home/z`, which is covered by a tmpfs overlay inside the namespace)

Order of operations (each step gates the next):

1. Isolation check MUST pass before any candidate exists:
       python3 isolation_check.py
   Requires 6/6 controls PASS and unchanged host canaries; writes
   `isolation-report.json`. If this fails, do NOT execute generated code.

2. Generation — 12 requests, fixed schedule verbatim from the trusted module,
   no retries. Chunking flags exist ONLY to survive tool timeouts; a request
   that already has a recorded outcome is never re-attempted:
       python3 glm_generate.py --from 1 --to 4
       python3 glm_generate.py --from 5 --to 8
       python3 glm_generate.py --from 9 --to 12
   Produces `pilot-run/responses/`, `pilot-run/bodies/`,
   `pilot-run/candidate-index.json`, `pilot-run/generation-state.json`.

3. Isolated execution — preflight + 30 probes per candidate (fresh namespace
   per probe, 5.0 s deadline, rlimit stack):
       python3 local_supervisor.py
   Produces `pilot-run/execution-reports/<request_id>.json` and
   `pilot-run/execution-log.json`.

4. Independent oracle verification + trusted scoring (unchanged scorer):
       python3 score_driver.py
   Runs `validate_controls.py` on a hash-verified copy of `h3-footprint-v3`
   (freeze-chain check included), then invokes `copilot_auto_pilot.run_scoring`
   unchanged. Produces `pilot-run/score-report-RAW-trusted-scorer.json` and the
   identity-attributed `pilot-run/score-report-final.json`.

Interpretation rules (do not skip):
- This is an exploratory screen: no original-gate verdict, no held-out work,
  no confirmatory batches, no threshold changes, no prompt tuning.
- If no informative failures (no eligible k): STOP and diagnose the benchmark's
  failure diversity instead of generating more candidates.
- The generation cap of 12 is binding.

Patch application (optional, owner decision):
    git apply patch_0001_fix_gitattributes_BOM.diff
    sh test_gitattributes_no_bom.sh <repo_root>
