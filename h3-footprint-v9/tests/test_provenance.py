from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
V9 = HERE.parent
sys.path.insert(0, str(V9))
sys.path.insert(0, str(V9 / "generation"))

import backend  # noqa: E402
import controller  # noqa: E402
import generate_v9 as generation  # noqa: E402
import provenance  # noqa: E402

BODY_HASH = "a" * 64
SECOND_HASH = "b" * 64
FIXTURE = HERE / "fixtures" / "correct.py"


class BatchIdValidationTests(unittest.TestCase):
    def test_lowest_and_highest_batch_ids_are_valid(self):
        self.assertEqual(provenance.group_id_for_batch(0), "batch-000")
        self.assertEqual(provenance.group_id_for_batch(399), "batch-399")

    def test_rejects_missing_null_boolean_string_float_and_out_of_range_ids(self):
        for value in (None, True, False, "5", 5.0, -1, 400):
            with self.subTest(batch_id=value):
                with self.assertRaises(provenance.ProvenanceError):
                    provenance.validate_batch_id(value)

    def test_rejects_integer_subclasses(self):
        class IntSubclass(int):
            pass

        with self.assertRaises(provenance.ProvenanceError):
            provenance.validate_batch_id(IntSubclass(5))


class AttemptProvenanceTests(unittest.TestCase):
    def write_attempts(self, root: Path, records: list[dict]) -> Path:
        path = root / "attempts.jsonl"
        path.write_bytes(
            "".join(json.dumps(record) + "\n" for record in records).encode("utf-8")
        )
        return path

    def test_attempt_record_uses_the_canonical_schema(self):
        self.assertEqual(
            provenance.make_attempt_record(5, [BODY_HASH, SECOND_HASH]),
            {"batch_id": 5, "accepted_hashes": [BODY_HASH, SECOND_HASH]},
        )

    def test_attempt_record_rejects_non_integer_batch_id(self):
        with self.assertRaises(provenance.ProvenanceError):
            provenance.make_attempt_record(True, [BODY_HASH])

    def test_loader_maps_hash_to_the_batch_group(self):
        with tempfile.TemporaryDirectory() as td:
            path = self.write_attempts(
                Path(td), [provenance.make_attempt_record(5, [BODY_HASH])]
            )
            index = provenance.load_attempts_index(path)
        self.assertEqual(index.by_hash[BODY_HASH], {
            "batch_id": 5, "group_id": "batch-005"
        })

    def test_duplicate_body_keeps_first_valid_provenance(self):
        with tempfile.TemporaryDirectory() as td:
            path = self.write_attempts(
                Path(td),
                [
                    provenance.make_attempt_record(5, [BODY_HASH]),
                    provenance.make_attempt_record(12, [BODY_HASH]),
                ],
            )
            index = provenance.load_attempts_index(path)
        self.assertEqual(index.by_hash[BODY_HASH]["batch_id"], 5)
        self.assertEqual(index.by_hash[BODY_HASH]["group_id"], "batch-005")

    def test_missing_batch_id_on_first_occurrence_blocks_later_valid_duplicate(self):
        with tempfile.TemporaryDirectory() as td:
            path = self.write_attempts(
                Path(td),
                [
                    {"accepted_hashes": [BODY_HASH]},
                    provenance.make_attempt_record(5, [BODY_HASH]),
                ],
            )
            with self.assertRaisesRegex(provenance.ProvenanceError, "batch_id"):
                provenance.load_attempts_index(path)

    def test_null_batch_id_on_first_occurrence_blocks_later_valid_duplicate(self):
        with tempfile.TemporaryDirectory() as td:
            path = self.write_attempts(
                Path(td),
                [
                    {"batch_id": None, "accepted_hashes": [BODY_HASH]},
                    provenance.make_attempt_record(5, [BODY_HASH]),
                ],
            )
            with self.assertRaisesRegex(provenance.ProvenanceError, "batch_id"):
                provenance.load_attempts_index(path)

    def test_boolean_string_float_negative_and_400_ids_fail_closed(self):
        for batch_id in (True, False, "5", 5.0, -1, 400):
            with self.subTest(batch_id=batch_id), tempfile.TemporaryDirectory() as td:
                path = self.write_attempts(
                    Path(td),
                    [{"batch_id": batch_id, "accepted_hashes": [BODY_HASH]}],
                )
                with self.assertRaises(provenance.ProvenanceError):
                    provenance.load_attempts_index(path)

    def test_missing_or_malformed_hash_list_fails_closed(self):
        for record in (
            {"batch_id": 1},
            {"batch_id": 1, "accepted_hashes": None},
            {"batch_id": 1, "accepted_hashes": ["not-a-sha256"]},
            {"batch_id": 1, "accepted_hashes": ["A" * 64]},
            {"batch_id": 1, "accepted_hashes": [], "legacy_body_hashes": []},
        ):
            with self.subTest(record=record), tempfile.TemporaryDirectory() as td:
                path = self.write_attempts(Path(td), [record])
                with self.assertRaises(provenance.ProvenanceError):
                    provenance.load_attempts_index(path)

    def test_malformed_jsonl_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "attempts.jsonl"
            path.write_bytes(
                (json.dumps(provenance.make_attempt_record(1, [BODY_HASH]))
                 + "\nnot-json\n").encode("utf-8")
            )
            with self.assertRaisesRegex(provenance.ProvenanceError, "not valid JSON"):
                provenance.load_attempts_index(path)

    def test_non_utf8_attempts_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "attempts.jsonl"
            path.write_bytes(b"\xff\xfe")
            with self.assertRaisesRegex(provenance.ProvenanceError, "UTF-8"):
                provenance.load_attempts_index(path)

    def test_attempts_digest_identifies_exact_parsed_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            path = self.write_attempts(
                Path(td), [provenance.make_attempt_record(5, [BODY_HASH])]
            )
            raw = path.read_bytes()
            index = provenance.load_attempts_index(path)
        self.assertEqual(index.attempts_sha256, hashlib.sha256(raw).hexdigest())
        self.assertIn(BODY_HASH, index.by_hash)

    def test_index_mapping_is_immutable(self):
        with tempfile.TemporaryDirectory() as td:
            path = self.write_attempts(
                Path(td), [provenance.make_attempt_record(5, [BODY_HASH])]
            )
            index = provenance.load_attempts_index(path)
        with self.assertRaises(TypeError):
            index.by_hash[BODY_HASH] = {"batch_id": 2, "group_id": "batch-002"}

    def test_index_cannot_be_fabricated_without_loading_attempts_file(self):
        with self.assertRaisesRegex(provenance.ProvenanceError, "load_attempts_index"):
            provenance.ProvenanceIndex(by_hash={}, attempts_sha256="c" * 64)

    def test_missing_attempts_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(provenance.ProvenanceError):
                provenance.load_attempts_index(Path(td) / "missing.jsonl")


class GeneratorProvenanceTests(unittest.TestCase):
    def test_generator_attempt_record_uses_batch_outcome_hashes(self):
        outcome = {"accepted_hashes": [BODY_HASH], "rejected": None}
        self.assertEqual(
            generation.attempt_record(7, outcome),
            {"batch_id": 7, "accepted_hashes": [BODY_HASH]},
        )

    def test_generator_rejects_boolean_and_out_of_range_batches(self):
        for value in (True, -1, 400):
            with self.subTest(batch_id=value):
                with self.assertRaises(provenance.ProvenanceError):
                    generation.batch_dir(Path("work"), value)
                with self.assertRaises(provenance.ProvenanceError):
                    generation.build_command(value, Path("work"), "opencode")

    def test_candidate_digest_matches_exact_canonical_file_bytes(self):
        source = "def solve(*args):\n    return -1  \r\n"
        canonical = generation.body_bytes(source)
        self.assertEqual(generation.digest(source), hashlib.sha256(canonical).hexdigest())
        self.assertEqual(canonical, b"def solve(*args):\n    return -1\n")


class _TransportReached(Exception):
    """Sentinel proving a valid candidate reached the transport."""


class _NoExecuteTransport:
    name = "attested-no-execute"
    requires_sandbox = True
    isolation_verified = True

    def __init__(self) -> None:
        self.calls = 0

    def attestation(self) -> dict:
        return {"verified": True}

    def execute(self, *args, **kwargs):
        self.calls += 1
        raise _TransportReached("valid provenance reached transport")


class ControllerProvenanceTests(unittest.TestCase):
    def load_index(self, root: Path, body_hash: str) -> provenance.ProvenanceIndex:
        attempts = root / "attempts.jsonl"
        attempts.write_bytes(
            (json.dumps(provenance.make_attempt_record(5, [body_hash])) + "\n").encode("utf-8")
        )
        return provenance.load_attempts_index(attempts)

    def test_authorized_evaluation_rejects_missing_index_before_execution(self):
        with tempfile.TemporaryDirectory() as td:
            transport = _NoExecuteTransport()
            ctl = controller.Controller(Path(td) / "work", transport=transport)
            with patch.object(controller.gates, "require_authorized", return_value={"ok": True}):
                row = ctl.evaluate_authorized(FIXTURE, provenance_index=None)
        self.assertEqual(row["excluded"], "missing_provenance_index")
        self.assertIsNone(row["k"])
        self.assertIsNone(row["group_id"])
        self.assertEqual(transport.calls, 0)

    def test_authorized_evaluation_requires_body_hash_membership(self):
        with tempfile.TemporaryDirectory() as td:
            transport = _NoExecuteTransport()
            ctl = controller.Controller(Path(td) / "work", transport=transport)
            index = self.load_index(Path(td), SECOND_HASH)
            with patch.object(controller.gates, "require_authorized", return_value={"ok": True}):
                row = ctl.evaluate_authorized(FIXTURE, provenance_index=index)
        self.assertEqual(row["excluded"], "body_absent_from_attempts")
        self.assertEqual(row["attempts_sha256"], index.attempts_sha256)
        self.assertEqual(transport.calls, 0)

    def test_authorized_evaluation_with_valid_membership_reaches_transport(self):
        with tempfile.TemporaryDirectory() as td:
            transport = _NoExecuteTransport()
            ctl = controller.Controller(Path(td) / "work", transport=transport)
            body_hash = controller.protocol.sha256_bytes(FIXTURE.read_bytes())
            index = self.load_index(Path(td), body_hash)
            with patch.object(controller.gates, "require_authorized", return_value={"ok": True}):
                with self.assertRaises(_TransportReached):
                    ctl.evaluate_authorized(FIXTURE, provenance_index=index)
        self.assertEqual(transport.calls, 1)

    @unittest.skipUnless(sys.platform == "win32", "HostLocalTransport requires Windows APIs")
    def test_host_local_development_scoring_remains_non_study(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctl = controller.Controller(
                root / "work",
                transport=backend.HostLocalTransport(root / "runtime"),
            )
            row = ctl.evaluate(FIXTURE)
        self.assertFalse(row["authorized"])
        self.assertIsNone(row["group_id"])
        self.assertIsNone(row["attempts_sha256"])
        self.assertEqual(row["fails"], [False] * 30)


if __name__ == "__main__":
    unittest.main()
