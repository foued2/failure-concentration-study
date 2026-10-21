# Recovery note

`attempt-0039` was interrupted after generation and after its diagnostic Sandbox suite had completed. The retained diagnostic capture was validated, and only the missing evaluation suite was executed. No solver source was regenerated or replaced.

The first resume pass then wrote an intermediate `attempts.json` that dropped the retained evaluation summaries for the first nine complete bodies and left the resume log's final summary at `eligible_bodies: 1`. That was a persistence defect in the recovery path, not a change to the underlying evidence. The evaluation summaries were restored from each attempt's retained `host-authoritative/evaluation.json`, and the final accounting was revalidated.

`runner-resume.stdout.log` is retained as an audit trail of the interrupted and repaired run. Its final pre-repair summary is superseded by `PILOT_RESULTS.json`, `FEASIBILITY_REPORT.md`, and `VALIDATION.json`. The 61 usage-limit failures still count against the current 100-request cap; the current run remains closed.
