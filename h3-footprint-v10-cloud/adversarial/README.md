# H3 V10 adversarial audit (claude/h3-v10-adversarial-fixtures)

Base: c3156cf6ec24fb25db9ec3fe55805c0184a7d1c1 (GPT's tested commit). Executor, scorer and fixture builder are NOT modified;
the workflow asserts byte-identity against that commit by git blob hash.

Scope: hand-written hostile bodies only. No model calls, no generated solvers, no held-out evaluation, no scientific definitions touched.
Verdicts are data: NO_FINDING / FINDING / INCONCLUSIVE / HARNESS_ERROR. A FINDING is preserved, not patched, here.

Files: bodies/*.py (hostile fixtures), run_adversarial.py (driver over run_container_candidate.run_candidate),
score_audit.py (mutates the control report and feeds it to score_smoke_report.score).
