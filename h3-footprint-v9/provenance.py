"""Strict, first-observed provenance for V9 candidate bodies.

The attempts file is parsed from one byte snapshot. Its SHA-256 identifies the
exact bytes used, and each candidate is bound to that snapshot by its body hash.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

import constants

_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
_ATTEMPT_KEYS = frozenset({"batch_id", "accepted_hashes"})
_ENTRY_KEYS = frozenset({"batch_id", "group_id"})


class ProvenanceError(ValueError):
    """Raised when a candidate cannot be assigned trustworthy batch provenance."""


def validate_batch_id(value: object) -> int:
    """Accept only exact integers in the predeclared batch range [0, 400)."""
    if type(value) is not int:
        raise ProvenanceError(
            f"batch_id must be an integer (bool/string/float are not accepted); "
            f"got {type(value).__name__}"
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
                f"accepted_hashes[{index}] must be a lowercase 64-character SHA-256 digest"
            )
        checked.append(body_hash)
    return checked


def make_attempt_record(batch_id: object, accepted_hashes: object) -> dict[str, Any]:
    """Build the sole accepted JSONL record shape for one completed batch."""
    valid_batch = validate_batch_id(batch_id)
    hashes = _validated_hashes(accepted_hashes)
    return {"batch_id": valid_batch, "accepted_hashes": hashes}


_INDEX_FACTORY_TOKEN = object()


@dataclass(frozen=True, init=False)
class ProvenanceIndex:
    """Immutable first-observed body mapping plus the exact attempts-file digest.

    Instances are created only by load_attempts_index(), after parsing and
    hashing the exact attempts-file byte snapshot.
    """

    by_hash: Mapping[str, Mapping[str, Any]]
    attempts_sha256: str

    def __init__(
        self, *, by_hash: Mapping[str, Mapping[str, Any]],
        attempts_sha256: str, _token: object | None = None,
    ) -> None:
        if _token is not _INDEX_FACTORY_TOKEN:
            raise ProvenanceError("ProvenanceIndex must be created by load_attempts_index()")
        object.__setattr__(self, "by_hash", by_hash)
        object.__setattr__(self, "attempts_sha256", attempts_sha256)
        self.__post_init__()

    def __post_init__(self) -> None:
        if (not isinstance(self.attempts_sha256, str)
                or _SHA256_RE.fullmatch(self.attempts_sha256) is None):
            raise ProvenanceError(
                "attempts_sha256 must be a lowercase 64-character SHA-256 digest"
            )
        if not isinstance(self.by_hash, Mapping):
            raise ProvenanceError("by_hash must be a mapping")

        frozen: dict[str, Mapping[str, Any]] = {}
        for body_hash, raw_entry in self.by_hash.items():
            if not isinstance(body_hash, str) or _SHA256_RE.fullmatch(body_hash) is None:
                raise ProvenanceError("provenance index contains an invalid body hash")
            if not isinstance(raw_entry, Mapping) or set(raw_entry) != _ENTRY_KEYS:
                raise ProvenanceError(
                    f"provenance entry for {body_hash} must contain exactly batch_id and group_id"
                )
            batch_id = validate_batch_id(raw_entry.get("batch_id"))
            group_id = group_id_for_batch(batch_id)
            if raw_entry.get("group_id") != group_id:
                raise ProvenanceError(
                    f"provenance entry for {body_hash} has a mismatched group_id"
                )
            frozen[body_hash] = MappingProxyType(
                {"batch_id": batch_id, "group_id": group_id}
            )
        object.__setattr__(self, "by_hash", MappingProxyType(frozen))


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
            raise ProvenanceError(
                f"attempts line {line_number} must be a JSON object"
            )
        if set(record) != _ATTEMPT_KEYS:
            raise ProvenanceError(
                f"attempts line {line_number} must contain exactly batch_id and accepted_hashes"
            )

        try:
            batch_id = validate_batch_id(record.get("batch_id"))
            hashes = _validated_hashes(record.get("accepted_hashes"))
        except ProvenanceError as exc:
            raise ProvenanceError(f"attempts line {line_number}: {exc}") from exc

        group_id = group_id_for_batch(batch_id)
        for body_hash in hashes:
            # First observed occurrence owns provenance. A malformed record
            # aborts the entire load, so a later duplicate cannot repair it.
            first_seen.setdefault(
                body_hash,
                {"batch_id": batch_id, "group_id": group_id},
            )
    return first_seen


def load_attempts_index(path: Path | str) -> ProvenanceIndex:
    """Parse and hash the same byte snapshot, avoiding read/hash TOCTOU drift."""
    source = Path(path)
    if not source.is_file():
        raise ProvenanceError(f"attempts file does not exist: {source}")
    try:
        raw = source.read_bytes()
    except OSError as exc:
        raise ProvenanceError(f"cannot read attempts file: {exc}") from exc

    by_hash = _parse_attempts_bytes(raw)
    return ProvenanceIndex(
        by_hash=by_hash,
        attempts_sha256=hashlib.sha256(raw).hexdigest(),
        _token=_INDEX_FACTORY_TOKEN,
    )
