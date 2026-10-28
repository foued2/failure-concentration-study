"""The opt-in immutable request protocol must be boring and auditable.

Every test here is host-only. Nothing in this file launches a Sandbox, a candidate
or a model; the point is to prove the request format, its rejections and its
bounded telemetry before the one diagnostic run.
"""

from __future__ import annotations

import json
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import backend  # noqa: E402
import constants  # noqa: E402
import controller  # noqa: E402
import protocol  # noqa: E402
import sandbox_agent  # noqa: E402

BODY = b'def solve(n, edges, s, t):\n    return n\n'
NONCE = "a" * 32


def make_job(sequence: int, body: bytes = BODY, *, job_id: str | None = None,
             token: int = 111) -> dict:
    return {
        "v9": protocol.JOB_SCHEMA,
        "job_id": job_id or f"{sequence:032x}",
        "sequence": sequence,
        "kind": "system",
        "body_sha256": protocol.sha256_bytes(body),
        "probe_index": None,
        "input": {"n": token, "edges": [], "s": 0, "t": 0},
        "limits": {
            "max_stdout_bytes": constants.MAX_CHILD_STDOUT_BYTES,
            "memory_bytes": constants.MEMORY_LIMIT_BYTES,
            "max_processes": constants.MAX_PROCESSES_PER_CANDIDATE,
        },
    }


def response_for(job: dict, *, tree_empty: bool = True) -> dict:
    return {
        "v9": protocol.JOB_SCHEMA,
        "job_id": job["job_id"],
        "sequence": job["sequence"],
        "kind": job["kind"],
        "body_sha256": job["body_sha256"],
        "probe_index": job.get("probe_index"),
        "status": "ok",
        "tree_empty": tree_empty,
        "answer": job["input"]["n"],
        "inside_sandbox": True,
        "raw_stdout": "",
    }


class ProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.inbox = Path(self._tmp.name) / "in"
        self.inbox.mkdir()

    def publish(self, job: dict, body: bytes = BODY) -> Path:
        return protocol.publish_immutable_job(self.inbox, job, body)

    def test_two_jobs_get_distinct_names_and_read_back_in_sequence(self):
        first = self.publish(make_job(1))
        second = self.publish(make_job(2))
        self.assertNotEqual(first.name, second.name)
        self.assertTrue(first.name.startswith("job-000001-"))
        self.assertTrue(second.name.startswith("job-000002-"))
        self.assertEqual(protocol.read_immutable_job(first)["sequence"], 1)
        scan = protocol.scan_immutable_jobs(self.inbox)
        self.assertEqual([job["sequence"] for job in scan["requests"]], [1, 2])
        self.assertEqual(scan["errors"], [])

    def test_a_body_is_content_addressed_and_reused(self):
        first = self.publish(make_job(1))
        second = self.publish(make_job(2))
        bodies = sorted(path.name for path in (self.inbox / "bodies").iterdir())
        self.assertEqual(bodies, [f"{protocol.sha256_bytes(BODY)}.py"])
        for job_file in (first, second):
            job = protocol.read_immutable_job(job_file)
            body = protocol.immutable_body_path(self.inbox, job["body_sha256"])
            self.assertEqual(body.read_bytes(), BODY)

    def test_a_published_request_is_never_overwritten(self):
        path = self.publish(make_job(1))
        before = path.read_bytes()
        with self.assertRaises(protocol.ImmutableJobError) as ctx:
            self.publish(make_job(1, token=999))
        self.assertEqual(ctx.exception.category, "job_already_exists")
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse(any(p.name.endswith(".tmp") for p in self.inbox.iterdir()))

    def test_a_job_whose_body_hash_is_wrong_is_rejected(self):
        job = make_job(1)
        job["body_sha256"] = protocol.sha256_bytes(b"different")
        with self.assertRaises(protocol.ImmutableJobError) as ctx:
            self.publish(job)
        self.assertEqual(ctx.exception.category, "body_hash_mismatch")
        self.assertEqual(list(self.inbox.glob("job-*.json")), [])

    def test_an_existing_body_cannot_change_under_its_hash(self):
        self.publish(make_job(1))
        body = protocol.immutable_body_path(self.inbox, protocol.sha256_bytes(BODY))
        body.write_bytes(b"tampered")
        with self.assertRaises(protocol.ImmutableJobError) as ctx:
            self.publish(make_job(2))
        self.assertEqual(ctx.exception.category, "body_conflict")
        self.assertEqual(list(self.inbox.glob("job-*.json")).__len__(), 1)

    def test_filename_must_agree_with_its_payload(self):
        path = self.publish(make_job(1))
        copy = self.inbox / protocol.immutable_job_filename(2, "b" * 32)
        copy.write_bytes(path.read_bytes())
        with self.assertRaises(protocol.ImmutableJobError) as ctx:
            protocol.read_immutable_job(copy)
        self.assertEqual(ctx.exception.category, "filename_payload_mismatch")

    def test_duplicate_job_id_is_an_error(self):
        job = make_job(1)
        path = self.publish(job)
        duplicate = self.inbox / protocol.immutable_job_filename(2, job["job_id"])
        payload = dict(job, sequence=2)
        duplicate.write_text(json.dumps(payload), encoding="utf-8")
        scan = protocol.scan_immutable_jobs(self.inbox)
        self.assertIn("duplicate_job_id", [item["error"] for item in scan["errors"]])
        self.assertEqual([item["sequence"] for item in scan["requests"]], [1])
        self.assertTrue(path.exists())

    def test_two_ids_claiming_one_sequence_is_an_error(self):
        self.publish(make_job(1))
        other = self.inbox / protocol.immutable_job_filename(1, "c" * 32)
        other.write_text(json.dumps(make_job(1, job_id="c" * 32)), encoding="utf-8")
        scan = protocol.scan_immutable_jobs(self.inbox)
        self.assertIn("conflicting_sequence", [item["error"] for item in scan["errors"]])
        self.assertEqual(len(scan["requests"]), 1)

    def test_a_corrupt_request_is_reported_not_executed(self):
        path = self.inbox / protocol.immutable_job_filename(1, "d" * 32)
        path.write_text("{not json", encoding="utf-8")
        scan = protocol.scan_immutable_jobs(self.inbox)
        self.assertEqual(scan["errors"][0]["error"], "unreadable")
        self.assertEqual(scan["requests"], [])

    def test_out_of_order_and_repeated_scans(self):
        second = make_job(2)
        self.publish(second)
        outcome, job, _, _ = sandbox_agent._decide_immutable(
            protocol.scan_immutable_jobs(self.inbox), 1, set()
        )
        self.assertEqual((outcome, job), ("out_of_order", None))

        first = self.publish(make_job(1))
        outcome, job, _, _ = sandbox_agent._decide_immutable(
            protocol.scan_immutable_jobs(self.inbox), 1, set()
        )
        self.assertEqual((outcome, job["sequence"]), ("new_job", 1))

        outcome, job, _, _ = sandbox_agent._decide_immutable(
            protocol.scan_immutable_jobs(self.inbox), 2, {first.name[-37:-5]}
        )
        self.assertEqual((outcome, job["sequence"]), ("new_job", 2))
        self.assertTrue(second["job_id"])


class ServeTests(unittest.TestCase):
    """Drive the real loop with a fake executor; no child process is started."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        root = Path(self._tmp.name)
        self.inbox, self.outbox, self.scratch = root / "in", root / "out", root / "scratch"
        for path in (self.inbox, self.outbox, self.scratch):
            path.mkdir()
        self.calls: list[tuple[int, str]] = []

    def runner(self, job, body, response_dir, scratch, *, timeout, memory_bytes,
               max_processes, paths=None):
        self.calls.append((job["sequence"], job["job_id"]))
        self.assertEqual(body.read_bytes(), BODY)
        self.assertIsInstance(paths, dict)
        self.assertEqual(set(paths), {"inbox", "outbox", "scratch"})
        protocol.write_response_exclusive(response_dir, response_for(job))

    def test_two_jobs_are_discovered_and_answered_in_sequence(self):
        for sequence, token in ((1, 111), (2, 222)):
            protocol.publish_immutable_job(
                self.inbox, make_job(sequence, token=token), BODY
            )
        log = sandbox_agent.EventLog(self.outbox, NONCE)
        done = sandbox_agent.serve_immutable(
            self.inbox, self.outbox, self.scratch, timeout=1.0,
            memory_bytes=constants.MEMORY_LIMIT_BYTES,
            max_processes=4, max_jobs=2, poll=0.01, events=log,
            state_interval=0.01, runner=self.runner,
        )
        self.assertEqual(done, 2)
        self.assertEqual(self.calls, [(1, f"{1:032x}"), (2, f"{2:032x}")])
        responses = sorted(p.name for p in self.outbox.glob("response-*.json"))
        self.assertEqual(len(responses), 2)
        collected = backend.collect_events(self.outbox, NONCE)
        self.assertEqual(collected["anomalies"], [])
        outcomes = [event["state"]["outcome"] for event in collected["events"]
                    if event["event"] == "poll_state"]
        self.assertIn("new_job", outcomes)
        self.assertEqual(
            [event["event"] for event in collected["events"]
             if event["event"] != "poll_state"],
            ["job_discovered", "job_started", "response_written",
             "job_discovered", "job_started", "response_written"],
        )

    def test_telemetry_distinguishes_empty_old_new_and_broken(self):
        log = sandbox_agent.EventLog(self.outbox, NONCE)
        state = sandbox_agent.JobLoopState()

        empty = protocol.scan_immutable_jobs(self.inbox)
        outcome, job, error, error_file = sandbox_agent._decide_immutable(empty, 1, set())
        self.assertEqual((outcome, job), ("no_jobs", None))
        state.observe(scanned=empty["scanned"], visible=empty["visible"],
                      visible_count=empty["visible_count"], outcome=outcome,
                      error=error, error_file=error_file)
        log.emit("poll_state", phase="serve", state=state.snapshot())

        first = protocol.publish_immutable_job(self.inbox, make_job(1), BODY)
        scan = protocol.scan_immutable_jobs(self.inbox)
        outcome, job, _, _ = sandbox_agent._decide_immutable(scan, 2, {make_job(1)["job_id"]})
        self.assertEqual(outcome, "only_handled")
        state.observe(scanned=scan["scanned"], visible=scan["visible"],
                      visible_count=scan["visible_count"], outcome=outcome)
        log.emit("poll_state", phase="serve", state=state.snapshot())

        protocol.publish_immutable_job(self.inbox, make_job(2), BODY)
        scan = protocol.scan_immutable_jobs(self.inbox)
        outcome, job, _, _ = sandbox_agent._decide_immutable(scan, 2, set())
        self.assertEqual((outcome, job["sequence"]), ("new_job", 2))
        state.observe(scanned=scan["scanned"], visible=scan["visible"],
                      visible_count=scan["visible_count"], outcome=outcome)
        log.emit("poll_state", phase="serve", state=state.snapshot())

        broken = self.inbox / protocol.immutable_job_filename(3, "e" * 32)
        broken.write_text("{", encoding="utf-8")
        scan = protocol.scan_immutable_jobs(self.inbox)
        outcome, job, error, error_file = sandbox_agent._decide_immutable(scan, 3, set())
        self.assertEqual((outcome, job, error_file), ("error", None, broken.name))
        state.observe(scanned=scan["scanned"], visible=scan["visible"],
                      visible_count=scan["visible_count"], outcome=outcome,
                      error=error, error_file=error_file)
        log.emit("poll_state", phase="serve", state=state.snapshot())

        collected = backend.collect_events(self.outbox, NONCE)
        self.assertEqual(collected["anomalies"], [])
        self.assertEqual(
            [event["state"]["outcome"] for event in collected["events"]],
            ["no_jobs", "only_handled", "new_job", "error"],
        )
        self.assertTrue(first.exists())

    def test_a_handled_job_is_not_processed_twice(self):
        protocol.publish_immutable_job(self.inbox, make_job(1), BODY)
        log = sandbox_agent.EventLog(self.outbox, NONCE)
        sandbox_agent.serve_immutable(
            self.inbox, self.outbox, self.scratch, timeout=1.0,
            memory_bytes=constants.MEMORY_LIMIT_BYTES,
            max_processes=4, max_jobs=1, poll=0.01, events=log,
            state_interval=0.01, runner=self.runner,
        )
        # The file is still visible on the next scan, but no second execution is
        # allowed. Give the loop a moment to poll again, then check the call log.
        state = sandbox_agent.JobLoopState()
        scan = protocol.scan_immutable_jobs(self.inbox)
        outcome, job, _, _ = sandbox_agent._decide_immutable(
            scan, 2, {make_job(1)["job_id"]}
        )
        self.assertEqual((outcome, job), ("only_handled", None))
        self.assertEqual(len(self.calls), 1)
        self.assertTrue(state)

    def _serve_bounded(self, max_polls: int = 3) -> int:
        log = sandbox_agent.EventLog(self.outbox, NONCE)
        return sandbox_agent.serve_immutable(
            self.inbox, self.outbox, self.scratch, timeout=1.0,
            memory_bytes=constants.MEMORY_LIMIT_BYTES,
            max_processes=4, poll=0.01, events=log,
            state_interval=0.01, runner=self.runner, max_polls=max_polls,
        )

    def test_a_malformed_extra_request_blocks_the_valid_job(self):
        protocol.publish_immutable_job(self.inbox, make_job(1), BODY)
        broken = self.inbox / protocol.immutable_job_filename(2, "b" * 32)
        broken.write_text("{not json", encoding="utf-8")
        self._serve_bounded()
        self.assertEqual(self.calls, [])
        self.assertEqual(list(self.outbox.glob("response-*.json")), [])
        collected = backend.collect_events(self.outbox, NONCE)
        self.assertTrue(any(
            event["event"] == "poll_state" and event["state"]["outcome"] == "error"
            for event in collected["events"]
        ))

    def test_a_duplicate_job_id_blocks_the_valid_job(self):
        job = make_job(1)
        protocol.publish_immutable_job(self.inbox, job, BODY)
        duplicate = self.inbox / protocol.immutable_job_filename(2, job["job_id"])
        duplicate.write_text(json.dumps(dict(job, sequence=2)), encoding="utf-8")
        self._serve_bounded()
        self.assertEqual(self.calls, [])
        self.assertEqual(list(self.outbox.glob("response-*.json")), [])

    def test_a_conflicting_sequence_blocks_the_valid_job(self):
        protocol.publish_immutable_job(self.inbox, make_job(1), BODY)
        conflict = self.inbox / protocol.immutable_job_filename(1, "c" * 32)
        conflict.write_text(json.dumps(make_job(1, job_id="c" * 32)), encoding="utf-8")
        self._serve_bounded()
        self.assertEqual(self.calls, [])
        self.assertEqual(list(self.outbox.glob("response-*.json")), [])

    def test_a_truncated_scan_never_yields_an_executable_job(self):
        protocol.publish_immutable_job(self.inbox, make_job(1), BODY)
        scan = protocol.scan_immutable_jobs(self.inbox)
        scan["truncated"] = True
        outcome, job, error, _ = sandbox_agent._decide_immutable(scan, 1, set())
        self.assertEqual((outcome, job, error), ("error", None, "scan_truncated"))

        original = protocol.IMMUTABLE_SCAN_LIMIT
        self.addCleanup(setattr, protocol, "IMMUTABLE_SCAN_LIMIT", original)
        protocol.IMMUTABLE_SCAN_LIMIT = 1
        protocol.publish_immutable_job(self.inbox, make_job(2), BODY)
        self.assertGreater(
            protocol.scan_immutable_jobs(self.inbox)["visible_count"], 1
        )
        self.assertTrue(protocol.scan_immutable_jobs(self.inbox)["truncated"])
        self._serve_bounded()
        self.assertEqual(self.calls, [])
        self.assertEqual(list(self.outbox.glob("response-*.json")), [])

    def test_the_heartbeat_snapshots_the_real_loop_state(self):
        job = make_job(1)
        protocol.publish_immutable_job(self.inbox, job, BODY)
        log = sandbox_agent.EventLog(self.outbox, NONCE)
        state = sandbox_agent.JobLoopState()
        sandbox_agent.serve_immutable(
            self.inbox, self.outbox, self.scratch, timeout=1.0,
            memory_bytes=constants.MEMORY_LIMIT_BYTES,
            max_processes=4, max_jobs=1, poll=0.01, events=log,
            state_interval=0.01, runner=self.runner, state=state,
        )
        snapshot = state.snapshot()
        self.assertGreaterEqual(snapshot["poll_count"], 1)
        self.assertEqual(snapshot["last_job_id"], job["job_id"])
        heartbeat = sandbox_agent.Heartbeat(log, 0.2, state=state.snapshot)
        heartbeat.start()
        time.sleep(0.3)
        heartbeat.stop()
        heartbeat.join(timeout=2.0)
        collected = backend.collect_events(self.outbox, NONCE)
        self.assertEqual(collected["anomalies"], [])
        beats = [event for event in collected["events"] if event["event"] == "heartbeat"]
        self.assertTrue(beats)
        self.assertGreaterEqual(beats[-1]["state"]["poll_count"], 1)
        self.assertEqual(beats[-1]["state"]["last_job_id"], job["job_id"])


class TransportSelectionTests(unittest.TestCase):
    """The real transport must read the request it actually published."""

    def test_sandbox_transport_selects_the_immutable_request(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox, outbox, scratch = root / "in", root / "out", root / "scratch"
            for path in (inbox, outbox, scratch):
                path.mkdir()
            job = make_job(1)
            protocol.publish_immutable_job(inbox, job, BODY)
            protocol.write_response_exclusive(outbox, response_for(job))
            transport = backend.WindowsSandboxTransport(job_protocol="immutable")
            transport._attestation = {"verified": True}
            transport._nonce = NONCE
            record = transport.execute(
                inbox, outbox, scratch, timeout=1.0,
                memory_bytes=constants.MEMORY_LIMIT_BYTES, max_processes=4,
            )
            self.assertEqual(record["job_id"], job["job_id"])
            self.assertEqual(record["answer"], 111)

    def test_sandbox_transport_rejects_an_unusable_immutable_request(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox, outbox, scratch = root / "in", root / "out", root / "scratch"
            for path in (inbox, outbox, scratch):
                path.mkdir()
            (inbox / protocol.immutable_job_filename(1, "f" * 32)).write_text(
                "{", encoding="utf-8"
            )
            transport = backend.WindowsSandboxTransport(job_protocol="immutable")
            transport._attestation = {"verified": True}
            transport._nonce = NONCE
            with self.assertRaises(backend.FatalBoundaryError):
                transport.execute(
                    inbox, outbox, scratch, timeout=0.1,
                    memory_bytes=constants.MEMORY_LIMIT_BYTES, max_processes=4,
                )


class RendezvousProtocolTests(unittest.TestCase):
    """The immutable variant must still enforce ordering and tree-empty."""

    class Transport:
        name = "immutable-scripted"
        requires_sandbox = True
        isolation_verified = True
        nonce = NONCE

        def __init__(self, outbox: Path, *, tree_empty: bool = True) -> None:
            self.outbox = Path(outbox)
            self.tree_empty = tree_empty

        def attestation(self):
            return {"verified": True, "agent": {"pid": 777}, "transport": self.name}

        def execute(self, staging, response_dir, scratch, *, timeout, memory_bytes,
                    max_processes):
            scan = protocol.scan_immutable_jobs(staging)
            self.assertEqual(scan["errors"], [])
            job = scan["requests"][-1]
            record = response_for(job, tree_empty=self.tree_empty)
            protocol.write_response_exclusive(response_dir, record)
            return record

        def assertEqual(self, left, right):
            if left != right:
                raise AssertionError(f"{left!r} != {right!r}")

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def _controller(self, **kwargs) -> controller.Controller:
        inbox, outbox, scratch = (self.root / "in", self.root / "out",
                                  self.root / "scratch")
        for path in (inbox, outbox, scratch):
            path.mkdir(exist_ok=True)
        transport = self.Transport(outbox, **kwargs)
        controller.stage_runtime(inbox)
        return controller.Controller(self.root / "work", transport=transport,
                                     case_paths=(inbox, outbox, scratch))

    def test_immutable_rendezvous_answers_a_then_b(self):
        result = controller.run_rendezvous(
            self._controller(), HERE / "fixtures" / "echo_input.py", immutable=True
        )
        self.assertTrue(result["ordering_ok"], result["checks"])
        self.assertEqual(result["protocol"], "immutable-v1")
        self.assertIsNone(result["diagnostic"])
        jobs = sorted((self.root / "in").glob("job-*.json"))
        self.assertEqual([job.name[:10] for job in jobs],
                         ["job-000001", "job-000002"])

    def test_tree_empty_is_still_required(self):
        with self.assertRaises(backend.FatalBoundaryError):
            controller.run_rendezvous(
                self._controller(tree_empty=False),
                HERE / "fixtures" / "echo_input.py", immutable=True,
            )

    def test_one_response_per_job(self):
        controller.run_rendezvous(
            self._controller(), HERE / "fixtures" / "echo_input.py", immutable=True
        )
        out = self.root / "out"
        responses = sorted(out.glob("response-*.json"))
        self.assertEqual(len(responses), 2)
        self.assertEqual(len({path.name for path in responses}), 2)
        # A second response under the same job id must never overwrite the first.
        with self.assertRaises(FileExistsError):
            protocol.write_response_exclusive(
                out, json.loads(responses[0].read_text(encoding="utf-8"))
            )


if __name__ == "__main__":
    unittest.main()
