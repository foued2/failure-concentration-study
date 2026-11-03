# LC518 C9 GitHub execution configuration

> **2026-11-03 containment update.** Bank generation was later executed under owner GO
> `LC518-GO-2026-11-03-01` (GitHub Actions run `41591572358`, recorded final bank status
> `ACCEPTED`; run artifact `13210063805`). That GO is consumed and no further generation is
> authorized. In the containment commit, `lc518_generator_state2.py`,
> `lc518_launcher_state2.py`, `activation_generator.diff` and `activation_launcher.diff`
> were removed from this directory and `SHA256SUMS` was updated accordingly. See
> `LC518_GENERATION_HOLD.md` at the repository root. The text below is the historical record
> of the pre-generation configuration.

**Status: CONFIGURED_LOCKED_NOT_AUTHORIZED.**

- Runner: ubuntu-24.04, image ubuntu24 / 20261026.354.1
- Python executable: /opt/hostedtoolcache/Python/3.13.5/x64/bin/python3.13
- RUN_ROOT: /home/runner/work/failure-concentration-study/failure-concentration-study/lc518_run
- OUTPUT_DIR: /home/runner/work/failure-concentration-study/failure-concentration-study/lc518_run/bank
- Machine protocol SHA-256: 71ecf5e589baba5b25363f9fabd7aee9ab1702da0eb47611464cf162ba170403

The original c9-execution-recovery package remains unchanged. The configured state-1 launcher and generator remain locked. State-2 files are exact one-line activation candidates and were only compiled/hashed, never executed. The preflight executes the state-1 launcher only to confirm that it refuses before creating RUN_ROOT. No bank, solver output, fitting result, or power result exists. GitHub runners are ephemeral; a future authorized run must upload the entire run root as an artifact before teardown.
