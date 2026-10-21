"""Host validator tests; all payloads are synthetic software fixtures."""
from __future__ import annotations

import base64
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from integration_runner import (
    CaptureRejected, EXPECTED_FILENAME, MAX_CAPTURE_BYTES, parse_transport,
    parse_worker_scalar, reconstruct_host_record, render_integration_report, validate_capture_directory,
    validate_integration_report,
)
from study.probes import make_probe_suite


PROBES = make_probe_suite(20261020)
NONCE = "test-nonce"


def envelope(case: str, fail_ids: set[str] | None = None) -> dict:
    fail_ids = fail_ids or set()
    rows = []
    for probe in PROBES:
        expected = -1 if __import__("study.sssp", fromlist=["dijkstra_ref"]).dijkstra_ref(
            probe["n"], probe["edges"], probe["s"], probe["t"]
        ) is None else __import__("study.sssp", fromlist=["dijkstra_ref"]).dijkstra_ref(
            probe["n"], probe["edges"], probe["s"], probe["t"]
        )
        value = expected + 1 if probe["probe_id"] in fail_ids and expected >= 0 else (0 if probe["probe_id"] in fail_ids else expected)
        rows.append({"probe_id": probe["probe_id"], "status": "complete", "exit_code": 0,
                     "timed_out": False, "tree_terminated": True,
                     "stdout_b64": base64.b64encode(f"{value}\n".encode()).decode(), "stderr_b64": ""})
    return {"schema": 1, "nonce": NONCE, "case_id": case, "probe_rows": rows}


class IntegrationRunnerTests(unittest.TestCase):
    def test_worker_scalar_accepts_windows_crlf(self):
        row = {"status": "complete", "stdout_b64": base64.b64encode(b"-1\r\n").decode()}
        self.assertEqual(parse_worker_scalar(row), -1)
        row["stdout_b64"] = base64.b64encode(b"-1\r\n42\r\n").decode()
        with self.assertRaises(CaptureRejected):
            parse_worker_scalar(row)

    def test_four_patterns_reconstructed_from_raw_outputs(self):
        cases = [
            ("zero", set(), [0, 0, 0, 0, 0, 0], 0, 0.0),
            ("one_family", {"F1_0", "F1_1", "F1_2", "F1_3"}, [4, 0, 0, 0, 0, 0], 4, 1.0),
            ("two_families", {"F1_0", "F1_1", "F2_0", "F2_1"}, [2, 2, 0, 0, 0, 0], 4, 0.5),
            ("four_families", {"F1_0", "F2_0", "F3_0", "F4_0"}, [1, 1, 1, 1, 0, 0], 4, 0.25),
        ]
        for name, failed, counts, k, c in cases:
            with self.subTest(name=name):
                record = reconstruct_host_record(parse_transport(json.dumps(envelope(name, failed)).encode(), NONCE, name), PROBES)
                self.assertEqual(list(record["family_counts"].values()), counts)
                self.assertEqual((record["k"], record["C"]), (k, c))
                self.assertFalse(record["worker_claims_used"])

    def test_transport_rejects_bad_json_size_identity_and_duplicate_keys(self):
        with self.assertRaises(CaptureRejected):
            parse_transport(b"{bad", NONCE, "zero")
        with self.assertRaises(CaptureRejected):
            parse_transport(b"x" * (MAX_CAPTURE_BYTES + 1), NONCE, "zero")
        with self.assertRaises(CaptureRejected):
            parse_transport(b'{"schema":1,"schema":1}', NONCE, "zero")
        doc = envelope("wrong")
        with self.assertRaises(CaptureRejected):
            parse_transport(json.dumps(doc).encode(), NONCE, "zero")

    def test_transport_accepts_separate_evaluation_and_control_batches(self):
        def one_row(probe_id: str) -> dict:
            return {"probe_id": probe_id, "status": "complete", "exit_code": 0,
                    "timed_out": False, "tree_terminated": True,
                    "stdout_b64": base64.b64encode(b"0\n").decode(), "stderr_b64": ""}
        for case, count in (("evaluation_pattern_zero", 20), ("controls_python", 6)):
            with self.subTest(case=case):
                payload = {"schema": 1, "nonce": NONCE, "case_id": case,
                           "probe_rows": [one_row(f"row-{i}") for i in range(count)]}
                self.assertEqual(len(parse_transport(json.dumps(payload).encode(), NONCE, case)["probe_rows"]), count)

    def test_claims_and_malformed_solver_stdout_never_become_host_metrics(self):
        doc = envelope("claims")
        # Worker tries to provide an object with fabricated correctness and features.
        doc["probe_rows"][0]["stdout_b64"] = base64.b64encode(b'{"answer":0,"correct":true,"k":0,"C":0}').decode()
        with self.assertRaises(CaptureRejected):
            reconstruct_host_record(parse_transport(json.dumps(doc).encode(), NONCE, "claims"), PROBES)
        doc["probe_rows"][0]["stdout_b64"] = base64.b64encode(b"\xff\xfe").decode()
        with self.assertRaises(CaptureRejected):
            reconstruct_host_record(parse_transport(json.dumps(doc).encode(), NONCE, "claims"), PROBES)
        doc["probe_rows"][0]["stdout_b64"] = base64.b64encode(b"x" * (64 * 1024 + 1)).decode()
        with self.assertRaises(CaptureRejected):
            reconstruct_host_record(parse_transport(json.dumps(doc).encode(), NONCE, "claims"), PROBES)

    def test_capture_directory_rejects_unexpected_file_and_link(self):
        valid = json.dumps(envelope("zero")).encode()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / EXPECTED_FILENAME).write_bytes(valid)
            (root / "extra.json").write_text("{}")
            with self.assertRaises(CaptureRejected):
                validate_capture_directory(root, NONCE, "zero")
            (root / "extra.json").unlink()
            target = root / "target"
            target.mkdir()
            (target / "payload").write_bytes(valid)
            junction = root / EXPECTED_FILENAME
            junction.unlink()
            command = f"New-Item -ItemType Junction -Path '{junction}' -Target '{target}' | Out-Null"
            completed = subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], capture_output=True, text=True)
            if completed.returncode != 0:
                self.fail(f"real junction fixture creation failed: {completed.stdout} {completed.stderr}")
            try:
                with self.assertRaises(CaptureRejected):
                    validate_capture_directory(root, NONCE, "zero")
            finally:
                subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Remove-Item -LiteralPath '{junction}' -Force"], capture_output=True)

    def test_report_summary_is_recomputed_from_retained_case_records(self):
        records = []
        for name, failed in [("zero", set()), ("one", {"F1_0", "F1_1", "F1_2", "F1_3"}),
                             ("two", {"F1_0", "F1_1", "F2_0", "F2_1"}),
                             ("four", {"F1_0", "F2_0", "F3_0", "F4_0"})]:
            records.append(reconstruct_host_record(parse_transport(json.dumps(envelope(name, failed)).encode(), NONCE, name), PROBES))
        summary = {"cases": len(records), "patterns": {r["case_id"]: {"family_counts": list(r["family_counts"].values()),
                   "k": r["k"], "C": r["C"]} for r in records}}
        self.assertEqual(summary["cases"], 4)
        self.assertEqual(summary["patterns"]["four"]["C"], 0.25)
        report_data = {"pass_count": 4, "case_count": summary["cases"],
                       "cases": [{"case_id": name, "result": "PASS", "reason": "host oracle and features",
                                  "family_counts": item["family_counts"], "k": item["k"], "C": item["C"]}
                                 for name, item in ((r["case_id"], r) for r in records)]}
        rendered = render_integration_report(report_data)
        validate_integration_report(report_data, rendered)
        with self.assertRaises(AssertionError):
            validate_integration_report(report_data, rendered.replace("Cases passed: 4/4", "Cases passed: 5/4"))
        self.assertIn("Cases passed: 4/4", rendered)
        for name, item in summary["patterns"].items():
            self.assertIn(f"| {name} | PASS |", rendered)
            self.assertIn(f"k={item['k']}; C={item['C']}", rendered)


if __name__ == "__main__":
    unittest.main()
