"""Strict, first-observed provenance for V9 candidate bodies.

A generation response is the solver-side dependence group. Attempt data are
parsed from one byte snapshot; its SHA-256 is carried into every scored row.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import constants

_SHA256_RE = re.compile(r"[0-9a-f]{64}\\Z")


class ProvenanceError(ValueError):
    """Raised when a candidate cannot be assigned trustworthy batch provenance."""


@dataclass(frozen=True)
class ProvenanceIndex:
    """Body-hash provenance plus the digest of the exact attempts-file bytes."""

    by_hash: Mapping[str, Mapping[str, Any]]
    attempts_sha256: str

    def __post_init__(self) -> None:
        if not isinstance(self.attempts_sha256, str) or _SHA256_RE.fullmatch(self.attempts_sha256) is None:
            raise ProvenanceError("attempts_sha256 must be a lowercase 64-character SHA-256 digest")


def validate_batch_id(value: object) -> int:
    """Accept only exact integers in the predeclared batch range [0, 400)."""
    if type(value) is not int:
        raise ProvenanceError(
            f"batch_id must be an integer (bool/string/float are not accepted); got {type(value).__name__}"
        )
    if not 0 <= value < constants.MAX_BATCHES:
        raise ProvenanceError(
            f"batch_id must be in [0, {constants.MAX_BATCHES}); got {value}"
        )
    return value


def group_id_for_batch(batch_id: object) -> str:
    """Derive, never accept, the group identifier from a validated batch ID."""
    valid = validate_batch_id(batch_id)
    return f"batch-{valid:03d}"


def _validated_hashes(accepted_hashes: object) -> list[str]:
    if not isinstance(accepted_hashes, list):
        raise ProvenanceError("accepted_hashes must be a JSON array")
    checked: list[str] = []
    for index, body_hash in enumerate(accepted_hashes):
        if not isinstance(body_hash, str) or _SHA256_RE.fullmatch(body_hash) is None:
            raise ProvenanceError(
                f"accepted_hashes[{index}] must be a lowercase 64-character SHA-256 hex digest"
            )
        checked.append(body_hash)
    return checked


def make_attempt_record(batch_id: object, accepted_hashes: object) -> dict[str, Any]:
    """Build the canonical JSONL record emitted for one completed generation batch."""
    valid_batch = validate_batch_id(batch_id)
    hashes = _validated_hashes(accepted_hashes)
    return {"batch_id": valid_batch, "accepted_hashes": hashes}


def _parse_attempts_bytes(raw: bytes) -> dict[str, dict[str, Any]]:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ProvenanceError(f"attempts file is not valid UTF-8: {exc}") from exc

    first_seen: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ProvenanceError(
                f"attempts line {line_number} is not valid JSON: {exc.msg}"
            ) from exc
        if not isinstance(record, dict):
            raise ProvenanceError(f"attempts line {line_number} must be a JSON object")

        try:
            batch_id = validate_batch_id(record.get("batch_id"))
            hashes = _validated_hashes(record.get("accepted_hashes"))
        except ProvenanceError as exc:
            raise ProvenanceError(f"attempts line {line_number}: {exc}") from exc

        group_id = group_id_for_batch(batch_id)
        for body_hash in hashes:
            # The first observed body occurrence owns provenance. Later copies
            # remain duplicates and cannot move the body into another batch.
            first_seen.setdefault(
                body_hash,
                {"batch_id": batch_id, "group_id": group_id},
            )
    return first_seen


def load_attempts_index(path: Path | str) -> ProvenanceIndex:
    """Parse and hash the same immutable byte snapshot of the attempts file."""
    source = Path(path)
    if not source.is_file():
        raise ProvenanceError(f"attempts file does not exist: {source}")
    try:
        raw = source.read_bytes()
    except OSError as exc:
        raise ProvenanceError(f"cannot read attempts file: {exc}") from exc
    try:
        by_hash = _parse_attempts_bytes(raw)
    except ProvenanceError:
        raise
    return ProvenanceIndex(
        by_hash=by_hash,
        attempts_sha256=hashlib.sha256(raw).hexdigest(),
    )


def load_attempts_provenance(path: Path | str) -> dict[str, dict[str, Any]]:
    """Compatibility helper returning only the first-observed body mapping."""
    return dict(load_attempts_index(path).by_hash)
