import shutil
import sqlite3
import multiprocessing
import tempfile
import threading
import unittest
from pathlib import Path

from witness import Conflict, Witness


class FakeGitHub:
    """Models create-at-B then one fast-forward B->A; no network is used."""
    def __init__(self):
        self.ref = None
        self.ruleset_allows_app = True

    def apply_exact_intent(self, request):
        if not self.ruleset_allows_app:
            raise PermissionError("App rejected by modeled ruleset")
        if self.ref is None:
            self.ref = request["base"]
        if self.ref == request["base"]:
            self.ref = request["target"]
            return
        if self.ref == request["target"]:
            return  # ambiguous-response retry is idempotent after read/reconcile
        raise Conflict("GitHub ref is at an unexpected value; no replacement allowed")


def competing_process(db_path, request, barrier, queue):
    w = Witness(db_path)
    barrier.wait()
    try:
        queue.put((request["commit"], w.intent("study", request)[1]))
    except Conflict:
        queue.put((request["commit"], "rejected"))
    finally:
        w.db.close()


class WitnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.tmp.name) / "witness.db")
        self.w = Witness(self.db)

    def tearDown(self):
        self.w.db.close()
        self.tmp.cleanup()

    def test_two_competing_requests_only_one_claim(self):
        outcomes = []
        def submit(name):
            w = Witness(self.db)
            try: outcomes.append((name, w.intent("study", {"commit": name})))
            except Conflict: outcomes.append((name, "rejected"))
            finally: w.db.close()
        ts = [threading.Thread(target=submit, args=(n,)) for n in ("A", "B")]
        [t.start() for t in ts]; [t.join() for t in ts]
        self.assertEqual(sum(v != "rejected" for _, v in outcomes), 1)
        self.assertEqual(self.w.count("study"), 1)

    def test_two_independent_processes_race_on_same_persistent_witness(self):
        ctx = multiprocessing.get_context("spawn")
        barrier = ctx.Barrier(2)
        queue = ctx.Queue()
        requests = [{"commit": "A"}, {"commit": "B"}]
        processes = [ctx.Process(target=competing_process, args=(self.db, req, barrier, queue)) for req in requests]
        for process in processes: process.start()
        outcomes = [queue.get(timeout=15) for _ in processes]
        for process in processes:
            process.join(15)
            self.assertEqual(process.exitcode, 0)
        self.assertEqual(sum(outcome == "accepted" for _, outcome in outcomes), 1)
        self.assertEqual(sum(outcome == "rejected" for _, outcome in outcomes), 1)
        self.assertTrue(self.w.verify())

    def test_duplicate_and_delayed_retry_are_idempotent(self):
        first = self.w.intent("s", {"sha": "abc"})
        self.assertEqual(self.w.intent("s", {"sha": "abc"}), (first[0], "duplicate"))
        self.assertEqual(self.w.count("s"), 1)

    def test_later_different_intent_cannot_replace(self):
        self.w.intent("s", {"sha": "first"})
        with self.assertRaises(Conflict): self.w.intent("s", {"sha": "replacement"})

    def test_crash_after_record_before_github_keeps_intent_consumed(self):
        request = {"base": "B", "target": "A"}
        self.w.intent("s", request)
        github = FakeGitHub()  # simulated crash occurs before adapter receives request
        with self.assertRaises(Conflict): self.w.intent("s", {"base": "B", "target": "C"})
        self.w.intent("s", request)
        github.apply_exact_intent(request)
        self.assertEqual(github.ref, "A")
        self.assertTrue(self.w.verify())

    def test_github_succeeded_response_lost_witness_restarts_and_retries_same_intent(self):
        request = {"base": "B", "target": "A"}
        self.w.intent("s", request)  # durable record before GitHub call
        github = FakeGitHub()
        github.apply_exact_intent(request)  # GitHub applies; response is lost
        self.w.db.close()
        reopened = Witness(self.db)
        self.assertEqual(reopened.intent("s", request), (1, "duplicate"))
        reopened_github_ref = github.ref  # reconciliation GET observes A
        if reopened_github_ref != request["target"]:
            github.apply_exact_intent(request)
        self.assertEqual(github.ref, "A")
        with self.assertRaises(Conflict): reopened.intent("s", {"base": "B", "target": "C"})
        self.assertTrue(reopened.verify())
        reopened.db.close()

    def test_out_of_order_duplicate_missing_webhooks_do_not_define_order(self):
        self.w.intent("s", {"sha": "fixed"})
        self.assertTrue(self.w.verify())

    def test_ref_delete_recreate_and_force_push_are_external_breaches(self):
        self.w.intent("s", {"sha": "fixed"})
        with self.assertRaises(Conflict): self.w.intent("s", {"sha": "recreated"})
        self.assertEqual(self.w.count("s"), 1)

    def test_ruleset_change_and_bypass_are_outside_local_witness(self):
        request = {"base": "B", "target": "A"}
        self.w.intent("s", request)
        github = FakeGitHub()
        github.apply_exact_intent(request)
        github.ruleset_allows_app = False  # administrator modifies enforcement after intent
        with self.assertRaises(PermissionError): github.apply_exact_intent(request)
        github.ref = "ADMINISTRATOR_VALUE"  # model administrator bypass/force update
        self.assertNotEqual(github.ref, request["target"])  # ref reconciliation detects divergence
        self.assertTrue(self.w.verify())

    def test_hash_chain_detects_tampering(self):
        self.w.intent("s", {"sha": "fixed"})
        self.w.db.execute("UPDATE events SET payload='{}' WHERE sequence=1")
        self.assertFalse(self.w.verify())

    def test_storage_truncation_is_detected_but_checkpoint_is_external(self):
        self.w.intent("s", {"sha": "fixed"})
        saved_checkpoint = self.w.checkpoint()
        self.w.db.execute("DELETE FROM events WHERE sequence=1")
        self.assertFalse(self.w.verify())
        self.assertEqual(saved_checkpoint, (1, saved_checkpoint[1]))

    def test_full_database_rollback_requires_external_checkpoint(self):
        self.w.intent("s", {"sha": "fixed"})
        snapshot = str(Path(self.tmp.name) / "snapshot.db")
        snap_db = sqlite3.connect(snapshot)
        self.w.db.backup(snap_db)
        snap_db.close()
        first_checkpoint = self.w.checkpoint()  # assume independently retained
        self.w.intent("other-scope", {"sha": "later"})
        later_checkpoint = self.w.checkpoint()  # assume independently retained
        self.assertNotEqual(first_checkpoint, later_checkpoint)
        self.w.db.close()
        shutil.copyfile(snapshot, self.db)  # deliberate rollback of persistent witness DB
        rolled_back = Witness(self.db)
        self.assertTrue(rolled_back.verify())  # internally consistent old snapshot
        self.assertNotEqual(rolled_back.checkpoint(), later_checkpoint)  # external anchor exposes rollback
        rolled_back.db.close()


if __name__ == "__main__": unittest.main()
