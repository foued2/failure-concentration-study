"""Strict, first-observed provenance for V9 candidate bodies.

A generation response is the solver-side dependence group. This module refuses
synthetic per-body groups: every attempt record must carry a real batch ID and
an explicit list of accepted body hashes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import constants

_SHA256_RE = re.compile(r"[0-9a-f]{64}\\Z")


class ProvenanceError(ValueError):
    """Raised when a candidate cannot be assigned trustworthy batch provenance."""


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


def load_attempts_provenance(path: Path | str) -> dict[str, dict[str, Any]]:
    """Load body provenance from JSONL, retaining the first valid occurrence.

    Any malformed line, missing/null/invalid batch ID, or malformed accepted
    hash list aborts the whole load. In particular, an invalid first occurrence
    cannot be repaired by a later duplicate with a valid batch ID.
    """
    source = Path(path)
    if not source.is_file():
        raise ProvenanceError(f"attempts file does not exist: {source}")

    first_seen: dict[str, dict[str, Any]] = {}
    try:
        lines = source.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ProvenanceError(f"cannot read attempts file: {exc}") from exc

    for line_number, line in enumerate(lines, start=1):
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
