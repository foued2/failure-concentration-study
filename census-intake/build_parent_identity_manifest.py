"""Build a source-byte identity manifest for the LC518 parent roster.

SOURCE-CUSTODY TOOL ONLY — NOT AN A2 AUDIT OR CONSTRUCTION AUTHORIZATION.

The tool reads the exact bytes of explicitly indexed parent source files and
computes SHA-256 identities. It does not import, execute, parse, compile, or
modify those source files. The resulting identity manifest is intended for
later C4 intake. The A2 auditor consumes the manifest only and does not open
solver source, consistent with A2 Rev 11 §4.

Running this tool against real parent sources requires a separate owner
authorization for the parent-source identity-preparation stage. It must not
be run against synthetic fixtures as though they were real parents.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

TOOL_NAME = "lc518-parent-source-hasher"
TOOL_VERSION = "1.0.0"
LABEL = (
    "SOURCE-CUSTODY ONLY — READ BYTES AND HASH — NO IMPORT OR EXECUTION — "
    "NOT AN A2 AUDIT OR AUTHORIZATION"
)
EXPECTED_PARENT_COUNT = 30
ATTESTATION_METHOD = "READ_BYTES_AND_HASH_ONLY_NO_IMPORT_OR_EXECUTION"


class IdentityInputError(ValueError):
    """Raised when source identity inputs are missing, ambiguous or unsafe."""


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _safe_source_bytes(source_root: Path, relative_path: str) -> bytes:
    """Read one regular file under source_root, rejecting traversal and symlinks."""
    if not isinstance(relative_path, str) or not relative_path.strip():
        raise IdentityInputError("SOURCE_PATH_MISSING")
    if "\\" in relative_path:
        raise IdentityInputError("SOURCE_PATH_MUST_USE_POSIX_SEPARATORS")

    rel = PurePosixPath(relative_path)
    if rel.is_absolute() or not rel.parts or any(
        part in ("", ".", "..") for part in rel.parts
    ):
        raise IdentityInputError("SOURCE_PATH_NOT_SAFE_RELATIVE_PATH")

    root = source_root.resolve(strict=True)
    if not root.is_dir():
        raise IdentityInputError("SOURCE_ROOT_NOT_DIRECTORY")

    candidate = root
    for part in rel.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise IdentityInputError("SOURCE_PATH_CONTAINS_SYMLINK")

    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise IdentityInputError("SOURCE_PATH_ESCAPES_ROOT")
    if not resolved.is_file():
        raise IdentityInputError("SOURCE_PATH_NOT_FILE")
    return resolved.read_bytes()


def _validate_family_partition(roster: dict, family_map: dict) -> dict[str, str]:
    parents = roster.get("parents")
    if not isinstance(parents, list) or len(parents) != EXPECTED_PARENT_COUNT:
        raise IdentityInputError("ROSTER_NOT_EXACTLY_30_PARENTS")

    expected: dict[str, str] = {}
    for row in parents:
        if not isinstance(row, dict):
            raise IdentityInputError("ROSTER_PARENT_ROW_NOT_OBJECT")
        parent_id, z_id = row.get("parent_id"), row.get("Z_id")
        if not isinstance(parent_id, str) or not parent_id.strip():
            raise IdentityInputError("ROSTER_PARENT_ID_MISSING")
        if not isinstance(z_id, str) or not z_id.strip():
            raise IdentityInputError(f"ROSTER_FAMILY_MISSING:{parent_id}")
        if parent_id in expected:
            raise IdentityInputError(f"ROSTER_PARENT_ID_DUPLICATE:{parent_id}")
        expected[parent_id] = z_id

    if len(expected) != EXPECTED_PARENT_COUNT:
        raise IdentityInputError("ROSTER_PARENT_IDENTITY_NOT_UNIQUE")

    if family_map.get("status") != "ADOPTED":
        raise IdentityInputError("FAMILY_MAP_NOT_ADOPTED")

    family_rows = family_map.get("families")
    if not isinstance(family_rows, dict):
        raise IdentityInputError("FAMILY_MAP_FAMILIES_MISSING")

    mapped: dict[str, str] = {}
    for z_id, family in family_rows.items():
        members = family.get("parents") if isinstance(family, dict) else None
        if not isinstance(members, list):
            raise IdentityInputError(f"FAMILY_MAP_PARENT_LIST_INVALID:{z_id}")
        for parent_id in members:
            if not isinstance(parent_id, str) or parent_id in mapped:
                raise IdentityInputError("FAMILY_MAP_PARENT_COLLISION_OR_INVALID_ID")
            mapped[parent_id] = z_id

    if mapped != expected:
        raise IdentityInputError("FAMILY_MAP_ROSTER_PARTITION_MISMATCH")
    return expected


def build_parent_identity_manifest(
    *,
    roster: dict,
    family_map: dict,
    family_map_sha256: str,
    source_index: dict,
    source_index_sha256: str,
    source_root: Path,
    computed_by: str,
    computed_at_utc: str,
) -> dict:
    """Hash the explicitly indexed 30 parent files and return the C4 identity manifest."""
    if family_map.get("status") != "ADOPTED":
        raise IdentityInputError("FAMILY_MAP_NOT_ADOPTED")
    if not isinstance(family_map_sha256, str) or len(family_map_sha256) != 64:
        raise IdentityInputError("FAMILY_MAP_SHA256_INVALID")
    if not isinstance(source_index_sha256, str) or len(source_index_sha256) != 64:
        raise IdentityInputError("SOURCE_INDEX_SHA256_INVALID")
    if not isinstance(computed_by, str) or not computed_by.strip():
        raise IdentityInputError("COMPUTED_BY_MISSING")

    try:
        timestamp = datetime.fromisoformat(computed_at_utc.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise IdentityInputError("COMPUTED_AT_UTC_INVALID") from exc
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise IdentityInputError("COMPUTED_AT_UTC_MUST_INCLUDE_TIMEZONE")

    expected = _validate_family_partition(roster, family_map)
    index_rows = source_index.get("parents")
    if not isinstance(index_rows, list) or len(index_rows) != EXPECTED_PARENT_COUNT:
        raise IdentityInputError("SOURCE_INDEX_NOT_EXACTLY_30_PARENTS")

    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    parent_rows: list[dict] = []
    bundle_rows: list[dict] = []

    for row in index_rows:
        if not isinstance(row, dict):
            raise IdentityInputError("SOURCE_INDEX_ROW_NOT_OBJECT")
        parent_id = row.get("parent_id")
        source_path = row.get("base_source_path")
        if not isinstance(parent_id, str) or parent_id not in expected:
            raise IdentityInputError(f"SOURCE_INDEX_UNKNOWN_PARENT:{parent_id}")
        if parent_id in seen_ids:
            raise IdentityInputError(f"SOURCE_INDEX_PARENT_DUPLICATE:{parent_id}")
        if not isinstance(source_path, str) or not source_path.strip():
            raise IdentityInputError(f"SOURCE_INDEX_PATH_MISSING:{parent_id}")
        if source_path in seen_paths:
            raise IdentityInputError(f"SOURCE_INDEX_PATH_REUSED:{source_path}")

        raw = _safe_source_bytes(source_root, source_path)
        digest = sha256_bytes(raw)
        seen_ids.add(parent_id)
        seen_paths.add(source_path)

        parent_rows.append({
            "parent_id": parent_id,
            "Z_id": expected[parent_id],
            "base_source_path": source_path,
            "base_source_sha256": digest,
        })
        bundle_rows.append({
            "parent_id": parent_id,
            "base_source_path": source_path,
            "base_source_sha256": digest,
        })

    missing = sorted(set(expected) - seen_ids)
    if missing:
        raise IdentityInputError("SOURCE_INDEX_PARENT_COVERAGE_INCOMPLETE:" + ",".join(missing))

    parent_rows.sort(key=lambda row: row["parent_id"])
    bundle_rows.sort(key=lambda row: row["parent_id"])
    bundle_canonical = json.dumps(
        bundle_rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    bundle_sha256 = sha256_bytes(bundle_canonical)

    return {
        "artifact_id": "lc518-150-parent-source-identity-manifest",
        "version": "1.0",
        "label": LABEL,
        "source_hash_attestation": {
            "algorithm": "SHA-256",
            "hash_subject": "EXACT_BASE_SOURCE_FILE_BYTES",
            "method": ATTESTATION_METHOD,
            "computed_by": computed_by,
            "computed_at_utc": timestamp.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_index_sha256": source_index_sha256,
            "source_bundle_sha256": bundle_sha256,
            "tool": TOOL_NAME,
            "tool_version": TOOL_VERSION,
            "execution_boundary": (
                "File bytes were read and hashed. No source file was imported, "
                "executed, parsed, compiled or modified."
            ),
        },
        "family_map_adoption_ref": {
            "status": "ADOPTED",
            "artifact_id": family_map.get("artifact_id"),
            "sha256": family_map_sha256,
        },
        "parents": parent_rows,
        "boundary": (
            "This manifest attests to exact-byte SHA-256 values computed by the "
            "source-custody tool. The A2 auditor consumes this manifest only and "
            "does not open solver source. The manifest is not evidence that a parent "
            "is correct, nor authorization to construct or execute any solver."
        ),
    }


def _load_json(path: Path) -> tuple[dict, bytes]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise IdentityInputError(f"JSON_ROOT_NOT_OBJECT:{path}")
    return value, raw


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=LABEL)
    parser.add_argument("--roster", required=True)
    parser.add_argument("--family-map", required=True)
    parser.add_argument("--source-index", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--computed-by", required=True)
    parser.add_argument("--computed-at-utc")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        roster, _roster_raw = _load_json(Path(args.roster))
        family_map, family_map_raw = _load_json(Path(args.family_map))
        source_index, source_index_raw = _load_json(Path(args.source_index))
        computed_at = args.computed_at_utc or datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        manifest = build_parent_identity_manifest(
            roster=roster,
            family_map=family_map,
            family_map_sha256=sha256_bytes(family_map_raw),
            source_index=source_index,
            source_index_sha256=sha256_bytes(source_index_raw),
            source_root=Path(args.source_root),
            computed_by=args.computed_by,
            computed_at_utc=computed_at,
        )
        output = json.dumps(
            manifest, indent=2, sort_keys=True, ensure_ascii=False
        ) + "\n"
        Path(args.out).write_text(output, encoding="utf-8", newline="\n")
        sys.stdout.write(json.dumps({
            "tool": TOOL_NAME,
            "tool_version": TOOL_VERSION,
            "status": "IDENTITY_MANIFEST_BUILT",
            "parent_count": len(manifest["parents"]),
            "duplicate_source_hash_groups": _duplicate_hash_groups(manifest["parents"]),
            "output_path": str(Path(args.out)),
            "source_hash_attestation": manifest["source_hash_attestation"],
            "authorization_boundary": (
                "Tool invocation does not grant construction authorization. "
                "This run must be separately authorized."
            ),
        }, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        return 0
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, IdentityInputError) as exc:
        sys.stderr.write(f"PARENT_IDENTITY_BUILD_ERROR: {exc}\n")
        return 2


def _duplicate_hash_groups(rows: list[dict]) -> list[list[str]]:
    by_hash: dict[str, list[str]] = {}
    for row in rows:
        by_hash.setdefault(row["base_source_sha256"], []).append(row["parent_id"])
    return sorted(
        sorted(parent_ids)
        for parent_ids in by_hash.values()
        if len(parent_ids) > 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
