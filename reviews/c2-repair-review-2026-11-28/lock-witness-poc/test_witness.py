import multiprocessing
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path

from github_adapter import FakeGitHub, Reconciler, WebhookInbox
from witness import CheckpointStore, Conflict, IntegrityError, PolicyError, Witness


TEST_POLICY = {
    "purpose_key": "LC518-R2-C2",
    "experiment_id": "TEST-ONLY-REGISTRY-ID",
    "registry_digest": "a" * 64,
}
TEST_KEY = b"test-only-checkpoint-signing-key-not-for-production"


def request(target="b" * 40, **extra):
    result = {
        "experiment_id": TEST_POLICY["experiment_id"],
        "registry_digest": TEST_POLICY["registry_digest"],
        "oac_sha256": "c" * 64,
        "base_commit": "d" * 40,
        "target_commit": target,
    }
    result.update(extra)
    return result


def competing_process(local_path, anchor_path, req, barrier, queue):
    anchor = CheckpointStore(anchor_path, TEST_KEY)
    witness = Witness(local_path, anchor, TEST_POLICY)
    barrier.wait()
    try:
        queue.put((req["target_commit"], witness.intent(req)[1]))
    except Conflict:
        queue.put((req["target_commit"], "rejected"))
    finally:
        witness.db.close()
        anchor.db.close()


class WitnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.local_path = str(root / "witness-local.db")
        self.anchor_path = str(root / "external-custodian.db")
        self.anchor = CheckpointStore(self.anchor_path, TEST_KEY)
        self.witness = Witness(self.local_path, self.anchor, TEST_POLICY)

    def tearDown(self):
        self.witness.db.close()
        self.anchor.db.close()
        self.tmp.cleanup()

    def test_scope_experiment_alias_and_metadata_cannot_create_second_claim(self):
        original = request()
        self.witness.intent(original)
        with self.assertRaises(TypeError): self.witness.policy["purpose_key"] = "LC518-R2-C2-ALIAS"
        with self.assertRaises(AttributeError): self.witness.scope = "LC518-R2-C2-ALIAS"
        changed_experiment = request(experiment_id="LC518-R2-C2-ALIAS")
        with self.assertRaises(PolicyError): self.witness.intent(changed_experiment)
        with self.assertRaises(PolicyError): self.witness.intent(request(scope="LC518-R2-C2-REPLACEMENT"))
        with self.assertRaises(PolicyError): self.witness.intent(request(registry_digest="e" * 64))
        self.assertEqual(self.anchor.db.execute("SELECT COUNT(*) FROM claims").fetchone()[0], 1)
        self.assertEqual(self.anchor.state(TEST_POLICY["purpose_key"]), "INTENT_RECORDED")

    def test_exact_duplicate_is_idempotent_and_changed_request_conflicts(self):
        first = self.witness.intent(request())
        self.assertEqual(self.witness.intent(request()), (first[0], "duplicate"))
        with self.assertRaises(Conflict): self.witness.intent(request(target="e" * 40))

    def test_independent_processes_compete_on_one_external_claim(self):
        ctx = multiprocessing.get_context("spawn")
        barrier, queue = ctx.Barrier(2), ctx.Queue()
        root = Path(self.tmp.name)
        specs = [
            (str(root / "proc-a.db"), request(target="1" * 40)),
            (str(root / "proc-b.db"), request(target="2" * 40)),
        ]
        processes = [ctx.Process(target=competing_process,
                                 args=(local, self.anchor_path, req, barrier, queue))
                     for local, req in specs]
        for proc in processes: proc.start()
        outcomes = [queue.get(timeout=15) for _ in processes]
        for proc in processes:
            proc.join(15)
            self.assertEqual(proc.exitcode, 0)
        self.assertEqual(sorted(result for _, result in outcomes), ["accepted", "rejected"])
        self.assertEqual(self.anchor.db.execute("SELECT COUNT(*) FROM claims").fetchone()[0], 1)

    def test_corrupt_external_signature_fails_closed_before_acceptance(self):
        self.witness.intent(request())
        self.anchor.db.execute("DROP TRIGGER events_no_update")
        self.anchor.db.execute("UPDATE events SET signature='bad' WHERE sequence=1")
        with self.assertRaises(IntegrityError): self.witness.intent(request(target="e" * 40))

    def test_missing_or_rolled_back_external_checkpoint_fails_closed(self):
        self.witness.intent(request())
        empty_anchor_path = str(Path(self.tmp.name) / "stale-anchor.db")
        stale_anchor = CheckpointStore(empty_anchor_path, TEST_KEY)
        witness_with_stale_anchor = Witness(self.local_path, stale_anchor, TEST_POLICY)
        with self.assertRaises(IntegrityError): witness_with_stale_anchor.intent(request(target="e" * 40))
        witness_with_stale_anchor.db.close()
        stale_anchor.db.close()

    def test_anchor_rollback_snapshot_detected_against_local_mirror(self):
        self.witness.intent(request())
        snapshot = str(Path(self.tmp.name) / "anchor-snapshot.db")
        snap = sqlite3.connect(snapshot)
        self.anchor.db.backup(snap)
        snap.close()
        self.witness.transition(request(), "PENDING_RECONCILIATION")
        self.anchor.db.close()
        shutil.copyfile(snapshot, self.anchor_path)
        rolled_back_anchor = CheckpointStore(self.anchor_path, TEST_KEY)
        restarted = Witness(self.local_path, rolled_back_anchor, TEST_POLICY)
        with self.assertRaises(IntegrityError): restarted.intent(request(target="e" * 40))
        restarted.db.close()
        rolled_back_anchor.db.close()
        self.witness.db.close()
        self.anchor = CheckpointStore(self.anchor_path, TEST_KEY)  # safe teardown handle
        self.witness = Witness(self.local_path, self.anchor, TEST_POLICY)

    def test_recovery_state_transitions_are_constrained_and_breach_terminal(self):
        req = request()
        self.assertEqual(self.witness.state(), "UNCLAIMED")
        self.witness.intent(req)
        self.assertEqual(self.witness.state(), "INTENT_RECORDED")
        self.witness.transition(req, "PENDING_RECONCILIATION")
        self.witness.transition(req, "GITHUB_APPLIED")
        self.witness.transition(req, "BREACH")
        with self.assertRaises(Conflict): self.witness.transition(req, "GITHUB_APPLIED")
        with self.assertRaises(Conflict): self.witness.transition(request(target="e" * 40), "INTENT_RECORDED")

    def test_crash_before_github_call_recovers_same_intent_only(self):
        req, github = request(), FakeGitHub()
        self.witness.intent(req)  # crash boundary: record exists; adapter has not been called
        self.witness.db.close()
        self.anchor.db.close()
        self.anchor = CheckpointStore(self.anchor_path, TEST_KEY)
        self.witness = Witness(self.local_path, self.anchor, TEST_POLICY)
        self.assertEqual(self.witness.state(), "INTENT_RECORDED")
        self.assertEqual(github.events, [])
        self.assertEqual(Reconciler(self.witness, req, github).apply_once(), "GITHUB_APPLIED")
        with self.assertRaises(Conflict): self.witness.intent(request(target="e" * 40))

    def test_github_applied_lost_response_restart_and_same_intent_reconciliation(self):
        req, github = request(), FakeGitHub()
        reconciler = Reconciler(self.witness, req, github)
        self.assertEqual(reconciler.apply_once(lose_response=True), "GITHUB_APPLIED")
        self.assertEqual(self.witness.state(), "GITHUB_APPLIED")
        self.assertEqual(github.events, [("create", None, req["base_commit"], "app"),
                                         ("update", req["base_commit"], req["target_commit"], "app")])
        self.assertEqual(reconciler.apply_once(), "GITHUB_APPLIED")
        with self.assertRaises(Conflict): self.witness.intent(request(target="e" * 40))

    def test_webhook_duplicate_missing_and_reordered_arrivals_do_not_define_state(self):
        req, github = request(), FakeGitHub()
        github.apply_intent(req["base_commit"], req["target_commit"])
        inbox = WebhookInbox()
        # Update arrives before creation; duplicate update is acknowledged but not reprocessed.
        self.assertEqual(inbox.deliver("delivery-update", {"kind": "push", "after": req["target_commit"]}), "accepted")
        self.assertEqual(inbox.deliver("delivery-create", {"kind": "create", "after": req["base_commit"]}), "accepted")
        self.assertEqual(inbox.deliver("delivery-update", {"kind": "push", "after": req["target_commit"]}), "duplicate")
        self.assertEqual([d for d, _ in inbox.arrivals], ["delivery-update", "delivery-create"])
        self.witness.intent(req)
        # Creation webhook is absent; current ref plus adapter event journal is reconciled.
        missing_inbox = WebhookInbox()
        missing_inbox.deliver("only-update", {"kind": "push", "after": req["target_commit"]})
        self.assertEqual([event[1]["kind"] for event in missing_inbox.arrivals], ["push"])
        self.assertEqual(Reconciler(self.witness, req, github).reconcile(), "GITHUB_APPLIED")
        self.assertEqual(self.witness.state(), "GITHUB_APPLIED")

    def test_ref_deletion_is_reconciled_as_breach(self):
        req, github = request(), FakeGitHub()
        reconciler = Reconciler(self.witness, req, github)
        self.assertEqual(reconciler.apply_once(), "GITHUB_APPLIED")
        github.delete()
        self.assertEqual(reconciler.reconcile(), "BREACH")
        self.assertEqual(self.witness.state(), "BREACH")

    def test_ref_deletion_then_same_name_recreation_is_breach_even_at_target_sha(self):
        req, github = request(), FakeGitHub()
        reconciler = Reconciler(self.witness, req, github)
        reconciler.apply_once()
        github.delete()
        github.recreate(req["target_commit"])
        self.assertEqual(github.read_ref(), req["target_commit"])
        self.assertEqual(reconciler.reconcile(), "BREACH")  # complete adapter journal exposes lifecycle

    def test_force_update_is_reconciled_as_breach(self):
        req, github = request(), FakeGitHub()
        reconciler = Reconciler(self.witness, req, github)
        reconciler.apply_once()
        github.force_update("f" * 40)
        self.assertEqual(reconciler.reconcile(), "BREACH")

    def test_admin_ruleset_change_before_write_is_pending_and_same_intent_can_resume(self):
        req, github = request(), FakeGitHub()
        github.app_allowed = False
        reconciler = Reconciler(self.witness, req, github)
        self.assertEqual(reconciler.apply_once(), "PENDING_RECONCILIATION")
        self.assertEqual(self.witness.state(), "PENDING_RECONCILIATION")
        github.app_allowed = True
        self.assertEqual(reconciler.apply_once(), "GITHUB_APPLIED")
        with self.assertRaises(Conflict): self.witness.intent(request(target="e" * 40))


if __name__ == "__main__": unittest.main()
