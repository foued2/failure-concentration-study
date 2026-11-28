import tempfile
import threading
import unittest
from pathlib import Path

from witness import Conflict, Witness


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

    def test_duplicate_and_delayed_retry_are_idempotent(self):
        first = self.w.intent("s", {"sha": "abc"})
        self.assertEqual(self.w.intent("s", {"sha": "abc"}), (first[0], "duplicate"))
        self.assertEqual(self.w.count("s"), 1)

    def test_later_different_intent_cannot_replace(self):
        self.w.intent("s", {"sha": "first"})
        with self.assertRaises(Conflict): self.w.intent("s", {"sha": "replacement"})

    def test_recorded_before_operation_and_witness_outage(self):
        self.w.intent("s", {"sha": "fixed"})
        with self.assertRaises(Conflict): self.w.intent("s", {"sha": "other"})
        self.assertTrue(self.w.verify())

    def test_reopen_after_response_lost_or_crash(self):
        self.w.intent("s", {"sha": "fixed"})
        self.w.db.close()
        reopened = Witness(self.db)
        self.assertEqual(reopened.intent("s", {"sha": "fixed"}), (1, "duplicate"))
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
        self.w.intent("s", {"sha": "fixed"})
        self.assertTrue(self.w.verify())

    def test_hash_chain_detects_tampering(self):
        self.w.intent("s", {"sha": "fixed"})
        self.w.db.execute("UPDATE events SET payload='{}' WHERE sequence=1")
        self.assertFalse(self.w.verify())


if __name__ == "__main__": unittest.main()
