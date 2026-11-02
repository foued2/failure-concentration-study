# LC518 C9 execution-recovery package

This directory preserves the six files uploaded on 2026-11-02. They are copied into this isolated recovery branch and retained unchanged. The original uploaded files on `master` were not modified by this recovery work.

## Contents

- `lc518_generator_state1.py`: supplied configured generator, authorization remains `False`.
- `lc518_generator_state2.py`: supplied activation candidate, authorization literal is `True`. **Do not execute this file.**
- `activation_diff.txt`: supplied one-line state1-to-state2 authorization diff.
- `execution_protocol_v1.md`: supplied protocol, retained as uploaded.
- `SHA256SUMS`: supplied checksums for the four files above.
- `VERIFICATION_LOG.md`: supplied verification record.

The four supplied checksum entries were recomputed after copying into this directory and matched. The original ZIP and its nine internal file hashes were also independently verified by GitHub Actions.

## Current status: CONFIGURED AND LOCKED, NOT AUTHORIZED

GitHub Actions now runs the recovery and locked-package preflight on a GitHub-hosted `ubuntu-24.04` runner using CPython 3.13.5. The workflow is:

`.github/workflows/lc518-github-recovery.yml`

The GitHub-specific configuration is kept separately at:

`lc518-150/c9-github-execution/`

Machine protocol SHA-256:

`71ecf5e589baba5b25363f9fabd7aee9ab1702da0eb47611464cf162ba170403`

The runner identity, interpreter binary hash, run path, generator/launcher candidates, activation diffs, and 52-test suite are pinned in that package. The latest full preflight passed in GitHub Actions run [41521799815](https://github.com/foued2/failure-concentration-study/actions/runs/41521799815). It verified the source checksums, built the GitHub-specific locked configuration, compiled the candidates without executing them, passed 52 synthetic tests, and executed the configured state-1 launcher only to confirm that it refuses for lack of the separate owner GO before creating `RUN_ROOT`.

## Explicit holds

- No generator state 2 or launcher state 2 has been imported or executed.
- No diagnostic or held-out bank has been generated.
- No solver code has been constructed or executed.
- No predictive fitting, power analysis, or private-annex access has been performed.
- No merge to `master` is authorized by this recovery work.

The supplied protocol pins the Kangaroo sandbox. It remains preserved for provenance and must not be treated as the GitHub protocol. The GitHub-specific machine protocol above is a separate configuration with its own hash chain. A separate owner GO must name that exact protocol SHA-256 and both activation diff hashes before bank generation.

GitHub-hosted runners are ephemeral. Any future authorized generation workflow must upload the complete run directory, logs, and manifests as a retained Actions artifact before the job ends.
