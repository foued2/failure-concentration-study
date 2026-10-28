"""Stage the secret-free Sandbox runtime into a mapped inbox.

This module exists separately from ``controller`` so a diagnostic harness can
stage the runtime without importing the module that owns reference data. It
copies only files the guest is allowed to see; it holds no expectation, no probe
bank and no scoring code.
"""

from __future__ import annotations

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent

RUNTIME_FILES = (
    "supervisor.py",
    "child_runner.py",
    "protocol.py",
    "winjob.py",
    "sandbox_agent.py",
)


def stage_runtime(dest: Path | str, *, verify_only: bool = False) -> list[str]:
    """Copy the secret-free runtime into a staging or inbox directory.

    Staging is idempotent. Files that already match are left untouched, because
    a running Sandbox holds its mapped folders open and the host cannot overwrite
    them: attempting the copy produced ``WinError 32`` on a live mapping.
    ``verify_only`` turns a mismatch into a boundary error instead of a write.
    """
    # Imported lazily so this module stays importable without backend.
    from backend import FatalBoundaryError

    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for name in RUNTIME_FILES:
        source = HERE / name
        target = dest / name
        identical = target.is_file() and target.read_bytes() == source.read_bytes()
        if identical:
            continue
        if verify_only:
            raise FatalBoundaryError(
                f"{target} is missing or differs from {source}; restage the runtime "
                "before launching the Sandbox, because a live mapping cannot be "
                "overwritten from the host"
            )
        try:
            shutil.copy2(source, target)
        except PermissionError as exc:
            raise FatalBoundaryError(
                f"cannot restage {target}: a running Sandbox holds the mapped folder "
                f"open ({exc}); close the Sandbox, restage, then launch it again"
            ) from exc
    return list(RUNTIME_FILES)
