"""Tests for source-custody parent identity hashing.

All source files and hashes in this suite are synthetic fixtures. No real
LC518 parent body is created, imported, compiled or executed.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

CENSUS_INTAKE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CENSUS_INTAKE))

import build_parent_identity_manifest as identity_builder  # noqa: E402


def load_json(path: Path) -> dict:
    return json.loads(path.read_bytes().decode("utf-8"))


class TestParentIdentityManifestBuilder(unittest.TestCase):
    def setUp(self):
        self.roster = load_json(
            CENSUS_INTAKE / "gate1-inputs" / "PARENT_ROSTER_G01_G30.json"
        )
        self.family_map = load_json(
            CENSUS_INTAKE / "gate1-inputs" / "FAMILY_MAP.json"
        )
        self.roster["status"] = "ADOPTED"
        self.roster_raw = (
            json.dumps(
                self.roster, indent=2, sort_keys=True, ensure_ascii=False
            ) + "\n"
        ).encode("utf-8")
        self.roster_sha256 = hashlib.sha256(self.roster_raw).hexdigest()
        self.family_map["status"] = "ADOPTED"
        self.family_map_raw = (
            json.dumps(
                self.family_map, indent=2, sort_keys=True, ensure_ascii=False
            ) + "\n"
        ).encode("utf-8")
        self.family_map_sha256 = hashlib.sha256(self.family_map_raw).hexdigest()

        self.tmp = tempfile.TemporaryDirectory()
        self.source_root = Path(self.tmp.name)
        self.source_index = {
            "artifact_id": "SYNTHETIC-SOURCE-INDEX",
            "version": "0.0-synthetic",
            "parents": [],
        }
        for parent in self.roster["parents"]:
            parent_id = parent["parent_id"]
            relative_path = f"{parent_id}.py"
            payload = (
                f"# SYNTHETIC ONLY: source identity fixture for {parent_id}\n"
            ).encode("utf-8")
            (self.source_root / relative_path).write_bytes(payload)
            self.source_index["parents"].append({
                "parent_id": parent_id,
                "base_source_path": relative_path,
            })
        self.source_index_raw = (
            json.dumps(
                self.source_index, indent=2, sort_keys=True, ensure_ascii=False
            ) + "\n"
        ).encode("utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, **overrides):
        args = {
            "roster": self.roster,
            "family_map": self.family_map,
            "family_map_sha256": self.family_map_sha256,
            "roster_sha256": self.roster_sha256,
            "source_index": self.source_index,
            "source_index_sha256": hashlib.sha256(self.source_index_raw).hexdigest(),
            "source_root": self.source_root,
            "computed_by": "SYNTHETIC TEST FIXTURE ONLY",
            "computed_at_utc": "2026-11-23T00:00:00Z",
        }
        args.update(overrides)
        return identity_builder.build_parent_identity_manifest(**args)

    def test_builds_exactly_30_source_identities(self):
        manifest = self.build()
        self.assertEqual(len(manifest["parents"]), 30)
        self.assertEqual(
            [row["parent_id"] for row in manifest["parents"]],
            [f"G{i:02d}" for i in range(1, 31)],
        )
        self.assertEqual(
            manifest["source_hash_attestation"]["hash_subject"],
            "EXACT_BASE_SOURCE_FILE_BYTES",
        )
        self.assertEqual(
            manifest["parent_roster_adoption_ref"]["sha256"],
            self.roster_sha256,
        )
        self.assertEqual(
            manifest["parent_roster_adoption_ref"]["status"],
            "ADOPTED",
        )
        self.assertEqual(
            manifest["source_hash_attestation"]["method"],
            "READ_BYTES_AND_HASH_ONLY_NO_IMPORT_OR_EXECUTION",
        )

    def test_digest_is_over_exact_file_bytes(self):
        manifest = self.build()
        row = next(row for row in manifest["parents"] if row["parent_id"] == "G01")
        expected = hashlib.sha256((self.source_root / "G01.py").read_bytes()).hexdigest()
        self.assertEqual(row["base_source_sha256"], expected)

    def test_duplicate_source_bytes_are_retained_for_c4_deduplication(self):
        (self.source_root / "G02.py").write_bytes(
            (self.source_root / "G01.py").read_bytes()
        )
        manifest = self.build()
        g01 = next(row for row in manifest["parents"] if row["parent_id"] == "G01")
        g02 = next(row for row in manifest["parents"] if row["parent_id"] == "G02")
        self.assertEqual(g01["base_source_sha256"], g02["base_source_sha256"])
        self.assertNotEqual(g01["parent_id"], g02["parent_id"])

    def test_unadopted_parent_roster_is_rejected(self):
        roster = dict(self.roster)
        roster["status"] = "PENDING_ADOPTION"
        with self.assertRaisesRegex(
            identity_builder.IdentityInputError, "PARENT_ROSTER_NOT_ADOPTED"
        ):
            self.build(roster=roster)

    def test_unadopted_family_map_is_rejected(self):
        family_map = dict(self.family_map)
        family_map["status"] = "PENDING_ADOPTION"
        with self.assertRaisesRegex(
            identity_builder.IdentityInputError, "FAMILY_MAP_NOT_ADOPTED"
        ):
            self.build(family_map=family_map)

    def test_family_map_hash_must_match_exact_bytes(self):
        with self.assertRaisesRegex(
            identity_builder.IdentityInputError, "FAMILY_MAP_SHA256_INVALID"
        ):
            self.build(family_map_sha256="bad")

    def test_parent_index_must_cover_roster_once(self):
        source_index = dict(self.source_index)
        source_index["parents"] = source_index["parents"][:-1]
        with self.assertRaisesRegex(
            identity_builder.IdentityInputError, "SOURCE_INDEX_NOT_EXACTLY_30_PARENTS"
        ):
            self.build(source_index=source_index)

    def test_missing_source_file_is_rejected(self):
        (self.source_root / "G01.py").unlink()
        with self.assertRaises(FileNotFoundError):
            self.build()

    def test_path_traversal_is_rejected(self):
        source_index = json.loads(json.dumps(self.source_index))
        source_index["parents"][0]["base_source_path"] = "../outside.py"
        with self.assertRaisesRegex(
            identity_builder.IdentityInputError, "SOURCE_PATH_NOT_SAFE_RELATIVE_PATH"
        ):
            self.build(source_index=source_index)

    def test_symlink_is_rejected(self):
        outside = self.source_root.parent / "lc518-outside.py"
        outside.write_text("# synthetic only\n", encoding="utf-8")
        link = self.source_root / "G01-link.py"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation is unavailable in this runtime")
        source_index = json.loads(json.dumps(self.source_index))
        source_index["parents"][0]["base_source_path"] = link.name
        with self.assertRaisesRegex(
            identity_builder.IdentityInputError, "SOURCE_PATH_CONTAINS_SYMLINK"
        ):
            self.build(source_index=source_index)

    def test_source_text_is_never_executed(self):
        sentinel = self.source_root / "SHOULD_NOT_EXIST.txt"
        source_text = (
            "from pathlib import Path\n"
            f"Path({str(sentinel)!r}).write_text('executed')\n"
        )
        (self.source_root / "G01.py").write_text(source_text, encoding="utf-8")
        self.build()
        self.assertFalse(sentinel.exists())


if __name__ == "__main__":
    unittest.main()
