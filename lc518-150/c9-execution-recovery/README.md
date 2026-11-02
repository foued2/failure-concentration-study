# LC518 C9 execution-recovery package

This directory preserves the six files uploaded on 2026-11-02, copied byte-for-byte from the repository-root upload commit. The source upload remains unchanged on `master`.

## Contents

- `lc518_generator_state1.py`: configured generator, authorization remains `False`.
- `lc518_generator_state2.py`: predeclared activation candidate, authorization literal is `True`. **Do not execute this file.**
- `activation_diff.txt`: the single-line state1-to-state2 authorization diff.
- `execution_protocol_v1.md`: configuration protocol supplied with the upload.
- `SHA256SUMS`: hashes for the four files above.
- `VERIFICATION_LOG.md`: uploaded verification record.

The four entries in `SHA256SUMS` were independently recomputed after copying into this directory and matched.

## Current status: HOLD

No generator state in this directory is invoked by the recovery preflight. No diagnostic or held-out bank is authorized or generated. No solver code may be constructed or executed.

## GitHub execution compatibility issue

The supplied protocol pins `/usr/bin/python3.13`, a `Kangaroo` Linux platform fingerprint, and `/home/z/lc518_run`. Those are not yet verified as the actual GitHub Actions runner identity or a usable GitHub Actions run directory. The protocol must be reconfigured and rehashed for the chosen GitHub Actions runner before any execution.

The uploaded protocol also requires launcher constants and a launcher authorization change as part of a separate owner GO. The ZIP's original launcher remains the fail-closed review candidate; no GitHub-configured launcher is included here.

A GitHub Actions workflow for this package has not yet been installed or run.
