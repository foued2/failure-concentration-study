import multiprocessing
import os
import shutil
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from github_adapter import FakeGitHub, Reconciler, WebhookInbox
from trust import ExternalCheckpoint, IntegrityError, PolicyAuthority, PolicyError, ReceiptSigner, ReceiptVerifier
from witness import CheckpointStore, Conflict, Witness


ROOT_KEY = b"test-only-policy-root-key"
CUSTODIAN_KEY = b"test-only-custodian-key"
ROLE_KEYS = {
    "github_adapter": b"test-only-app-adapter-key",
    "witness_worker": b"test-only-worker-key",
    "independent_reconciler": b"test-only-reconciler-key",
}
POLICY = {
    "scientific_purpose": "LC518-R2-C2",
    "purpose_key": "LC518-R2-C2",
    "experiment_id": "TEST-ONLY-REGISTRY-ID",
    "registry_digest": "a" * 64,
    "custodian_id": "TEST-CUSTODIAN-01",
    "repository": "example/lock-test",
    "lock_ref": "refs/heads/test-lock",
    "app_id": 54321,
}


def make_request(target="b" * 40, **extra):
    request = {
        "experiment_id": POLICY["experiment_id"],
        "registry_digest": POLICY["registry_digest"],
        "oac_sha256": "c" * 64,
        "base_commit": "d" * 40,
        "target_commit": target,
    }
    request.update(extra)
    return request


def make_fixture(local_path, db_path, external_path, manifest_payload=POLICY):
    authority_path = str(Path(local_path).parent / "policy-authority.jsonl")
    authority = PolicyAuthority(ROOT_KEY, {"LC518-R2-C2": "LC518-R2-C2"}, authority_path)
    manifest = authority.issue(manifest_payload)
    external = ExternalCheckpoint(external_path, manifest_payload["custodian_id"],
                                  manifest.digest, CUSTODIAN_KEY)
    verifier = ReceiptVerifier(ROLE_KEYS)
    store = CheckpointStore(db_path, external, manifest, authority, CUSTODIAN_KEY, verifier)
    if not os.path.exists(external_path):
        store.initialize(authority.authorize_initialization(manifest))
    witness = Witness(local_path, store, manifest, authority, verifier)
    signers = {role: ReceiptSigner(role, key) for role, key in ROLE_KEYS.items()}
    return authority, manifest, external, store, witness, signers


def racing_process(local_path, db_path, external_path, target, barrier, queue):
    try:
        _, _, _, store, witness, _ = make_fixture(local_path, db_path, external_path)
        barrier.wait()
        queue.put((target, witness.intent(make_request(target=target))[1]))
        witness.db.close()
        store.db.close()
    except Exception as exc:
        queue.put((target, f"rejected:{type(exc).__name__}"))


class WitnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.local_path = str(root / "witness-mirror.db")
        self.db_path = str(root / "checkpoint-mirror.db")
        self.external_path = str(root / "independent-checkpoint.jsonl")
        (self.authority, self.manifest, self.external, self.store,
         self.witness, self.signers) = make_fixture(self.local_path, self.db_path, self.external_path)

    def tearDown(self):
        self.witness.db.close()
        self.store.db.close()
        self.tmp.cleanup()

    def adapter(self):
        return FakeGitHub(POLICY, self.signers["github_adapter"])

    def reconciler(self, request, adapter, witness=None):
        return Reconciler(witness or self.witness, request, adapter,
                          self.signers["witness_worker"], self.signers["independent_reconciler"])

    def test_object_policy_reassignment_and_mapping_mutation_are_rejected(self):
        with self.assertRaises(AttributeError): self.witness.policy = {**POLICY, "purpose_key": "ALIAS"}
        with self.assertRaises(TypeError): self.witness.policy["purpose_key"] = "ALIAS"
        with self.assertRaises(AttributeError): self.witness._policy = {**POLICY, "purpose_key": "ALIAS"}
        with self.assertRaises(AttributeError): self.store.policy = {**POLICY, "purpose_key": "ALIAS"}
        with self.assertRaises(AttributeError): self.external.custodian_id = "ALIAS-CUSTODIAN"

    def test_request_alias_and_alternate_witness_manifest_are_rejected(self):
        with self.assertRaises(PolicyError): self.witness.intent(make_request(experiment_id="ALIAS-ID"))
        with self.assertRaises(PolicyError): self.witness.intent(make_request(scope="LC518-R2-C2-ALIAS"))
        alias_policy = {**POLICY, "purpose_key": "LC518-R2-C2-ALIAS"}
        with self.assertRaises(PolicyError): self.authority.issue(alias_policy)
        forged = replace(self.manifest, payload_json=self.manifest.payload_json.replace(
            "LC518-R2-C2", "LC518-R2-C2-ALIAS"))
        with self.assertRaises(PolicyError):
            Witness(str(Path(self.tmp.name) / "forged-local.db"), self.store,
                    forged, self.authority, ReceiptVerifier(ROLE_KEYS))
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM claims").fetchone()[0], 0)

    def test_second_manifest_for_same_purpose_rejected_after_authority_reconstruction(self):
        self.assertEqual(self.authority.issue(POLICY).digest, self.manifest.digest)
        alternate = {**POLICY, "experiment_id": "SECOND-EXPERIMENT",
                     "registry_digest": "e" * 64, "custodian_id": "SECOND-CUSTODIAN"}
        with self.assertRaises(PolicyError): self.authority.issue(alternate)
        authority_path = str(Path(self.local_path).parent / "policy-authority.jsonl")
        reconstructed_authority = PolicyAuthority(
            ROOT_KEY, {"LC518-R2-C2": "LC518-R2-C2"}, authority_path)
        self.assertEqual(reconstructed_authority.issue(POLICY).digest, self.manifest.digest)
        with self.assertRaises(PolicyError): reconstructed_authority.issue(alternate)
        # No second manifest means no independently initialized second custodian.
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM claims").fetchone()[0], 0)

    def test_new_empty_or_different_custodian_checkpoint_fails_closed(self):
        empty_external_path = str(Path(self.tmp.name) / "empty-checkpoint.jsonl")
        empty_db = str(Path(self.tmp.name) / "empty-checkpoint.db")
        empty_local = str(Path(self.tmp.name) / "empty-local.db")
        empty_external = ExternalCheckpoint(empty_external_path, POLICY["custodian_id"],
                                            self.manifest.digest, CUSTODIAN_KEY)
        empty_store = CheckpointStore(empty_db, empty_external, self.manifest,
                                      self.authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        empty_witness = Witness(empty_local, empty_store, self.manifest,
                                self.authority, ReceiptVerifier(ROLE_KEYS))
        with self.assertRaises(IntegrityError): empty_witness.intent(make_request())
        empty_witness.db.close(); empty_store.db.close()
        other_external = ExternalCheckpoint(str(Path(self.tmp.name) / "other.jsonl"),
                                            "UNPINNED-CUSTODIAN", self.manifest.digest, CUSTODIAN_KEY)
        with self.assertRaises(PolicyError):
            CheckpointStore(str(Path(self.tmp.name) / "other.db"), other_external,
                            self.manifest, self.authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))

    def test_explicit_genesis_initialization_is_one_time_and_signed(self):
        with self.assertRaises(PolicyError): self.authority.authorize_initialization(self.manifest)
        forged_authorization = ('{"action":"initialize-custodian-genesis"}', "0" * 64)
        with self.assertRaises(PolicyError): self.store.authority.verify_initialization(
            self.manifest, forged_authorization)
        self.assertEqual(self.external.head()[0], 0)

    def test_resetting_both_sqlite_databases_fails_against_external_pin(self):
        self.witness.intent(make_request())
        self.witness.db.close(); self.store.db.close()
        for db_path in (self.local_path, self.db_path):
            for suffix in ("", "-wal", "-shm"):
                path = db_path + suffix
                if os.path.exists(path): os.remove(path)
        _, _, external, store, witness, _ = make_fixture(
            self.local_path, self.db_path, self.external_path)
        with self.assertRaises(IntegrityError): witness.intent(make_request(target="e" * 40))
        witness.db.close(); store.db.close()
        self.external = external
        self.store = CheckpointStore(self.db_path, external, self.manifest,
                                     self.authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        self.witness = Witness(self.local_path, self.store, self.manifest,
                               self.authority, ReceiptVerifier(ROLE_KEYS))

    def test_external_checkpoint_corruption_and_rollback_fail_closed(self):
        self.witness.intent(make_request())
        # Corrupt tail record, not merely the SQLite mirror.
        with open(self.external_path, "a", encoding="utf-8") as f:
            f.write('{"kind":"GENESIS"}\n')
        with self.assertRaises(IntegrityError): self.witness.intent(make_request(target="e" * 40))

    def test_external_checkpoint_rollback_fails_even_when_both_sqlite_mirrors_match(self):
        genesis_snapshot = str(Path(self.tmp.name) / "genesis-checkpoint.jsonl")
        shutil.copyfile(self.external_path, genesis_snapshot)
        self.witness.intent(make_request())
        # Roll back the independently pinned append-only file while leaving both DBs advanced.
        shutil.copyfile(genesis_snapshot, self.external_path)
        with self.assertRaises(IntegrityError): self.witness.intent(make_request(target="e" * 40))

    def test_independent_processes_race_on_pinned_custodian(self):
        ctx = multiprocessing.get_context("spawn")
        barrier, queue = ctx.Barrier(2), ctx.Queue()
        processes = []
        for name, target in (("a", "1" * 40), ("b", "2" * 40)):
            local = str(Path(self.tmp.name) / f"{name}-local.db")
            processes.append(ctx.Process(target=racing_process,
                args=(local, self.db_path, self.external_path, target, barrier, queue)))
        for process in processes: process.start()
        outcomes = [queue.get(timeout=20) for _ in processes]
        for process in processes:
            process.join(20)
            self.assertEqual(process.exitcode, 0)
        self.assertEqual(sum(result == "accepted" for _, result in outcomes), 1)
        self.assertEqual(sum(result.startswith("rejected") for _, result in outcomes), 1)

    def test_exact_duplicate_and_changed_target(self):
        req = make_request()
        first = self.witness.intent(req)
        self.assertEqual(self.witness.intent(req), (first[0], "duplicate"))
        with self.assertRaises(Conflict): self.witness.intent(make_request(target="e" * 40))

    def test_states_require_signed_evidence_and_forged_applied_is_rejected(self):
        req = make_request()
        self.witness.intent(req)
        self.assertFalse(hasattr(self.witness, "transition"))
        self.assertFalse(hasattr(self.store, "transition"))
        self.assertFalse(hasattr(self.store, "append_intent"))
        forged = self.signers["witness_worker"].sign({
            "purpose_key": POLICY["purpose_key"], "experiment_id": POLICY["experiment_id"],
            "request_hash": "0" * 64, "repository": POLICY["repository"],
            "lock_ref": POLICY["lock_ref"], "app_id": POLICY["app_id"],
            "outcome": "GITHUB_APPLIED", "observed_sha": req["target_commit"]})
        with self.assertRaises(IntegrityError): self.witness.record_adapter_evidence(req, forged)
        with self.assertRaises(IntegrityError): self.store.record_receipt(req, forged)
        with self.assertRaises(IntegrityError): self.witness.record_adapter_evidence(req, {"role": "github_adapter", "payload": {}, "signature": "bad"})
        valid = self.adapter().apply_intent(req)
        self.assertEqual(self.witness.record_adapter_evidence(req, valid)[1], "accepted")
        self.assertEqual(self.witness.state(), "GITHUB_APPLIED")

    def test_crash_after_intent_before_github_call_restarts_same_request(self):
        req = make_request()
        github = self.adapter()
        self.witness.intent(req)  # simulated crash boundary: no adapter call has happened
        self.witness.db.close(); self.store.db.close()
        external = ExternalCheckpoint(self.external_path, POLICY["custodian_id"],
                                      self.manifest.digest, CUSTODIAN_KEY)
        store = CheckpointStore(self.db_path, external, self.manifest,
                                self.authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        witness = Witness(self.local_path, store, self.manifest,
                          self.authority, ReceiptVerifier(ROLE_KEYS))
        self.assertEqual(witness.state(), "INTENT_RECORDED")
        self.assertEqual(github.events, [])
        reconciler = self.reconciler(req, github, witness)
        self.assertEqual(reconciler.apply_once(), "GITHUB_APPLIED")
        with self.assertRaises(Conflict): witness.intent(make_request(target="e" * 40))
        witness.db.close(); store.db.close()
        self.external = external
        self.store = CheckpointStore(self.db_path, external, self.manifest,
                                     self.authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        self.witness = Witness(self.local_path, self.store, self.manifest,
                               self.authority, ReceiptVerifier(ROLE_KEYS))

    def test_pending_requires_worker_receipt_and_breach_requires_reconciler_receipt(self):
        req = make_request()
        self.witness.intent(req)
        fake = self.adapter()
        pending = self.signers["witness_worker"].sign(fake._receipt(req, "PENDING_RECONCILIATION")["payload"])
        self.witness.record_adapter_evidence(req, pending)
        breach = self.signers["independent_reconciler"].sign(fake._receipt(req, "BREACH")["payload"])
        self.witness.record_adapter_evidence(req, breach)
        self.assertEqual(self.witness.state(), "BREACH")
        with self.assertRaises(Conflict): self.witness.record_adapter_evidence(req, pending)

    def test_lost_response_recovery_reconstructs_all_local_components(self):
        req, github = make_request(), self.adapter()
        self.witness.intent(req)
        github.apply_intent(req)  # remote ref moves to A; deliberately discard its response
        pending = self.signers["witness_worker"].sign(github._receipt(
            req, "PENDING_RECONCILIATION", github.read_ref())["payload"])
        self.witness.record_adapter_evidence(req, pending)
        self.assertEqual(self.witness.state(), "PENDING_RECONCILIATION")

        # Actual local restart: close and reconstruct witness, checkpoint DB, and reconciler.
        self.witness.db.close(); self.store.db.close()
        external = ExternalCheckpoint(self.external_path, POLICY["custodian_id"],
                                      self.manifest.digest, CUSTODIAN_KEY)
        store = CheckpointStore(self.db_path, external, self.manifest,
                                self.authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        witness = Witness(self.local_path, store, self.manifest,
                          self.authority, ReceiptVerifier(ROLE_KEYS))
        reconciler = self.reconciler(req, github, witness)
        self.assertEqual(reconciler.reconcile(), "GITHUB_APPLIED")
        with self.assertRaises(Conflict): witness.intent(make_request(target="e" * 40))
        witness.db.close(); store.db.close()
        self.external = external
        self.store = CheckpointStore(self.db_path, external, self.manifest,
                                     self.authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        self.witness = Witness(self.local_path, self.store, self.manifest,
                               self.authority, ReceiptVerifier(ROLE_KEYS))

    def test_applied_receipt_replay_after_lost_ack_is_idempotent_after_restart(self):
        req, github = make_request(), self.adapter()
        self.witness.intent(req)
        receipt = github.apply_intent(req)
        self.assertEqual(self.witness.record_adapter_evidence(req, receipt)[1], "accepted")
        # The state acknowledgement is lost; reconstruct every local checkpoint component.
        self.witness.db.close(); self.store.db.close()
        external = ExternalCheckpoint(self.external_path, POLICY["custodian_id"],
                                      self.manifest.digest, CUSTODIAN_KEY)
        store = CheckpointStore(self.db_path, external, self.manifest,
                                self.authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        witness = Witness(self.local_path, store, self.manifest,
                          self.authority, ReceiptVerifier(ROLE_KEYS))
        self.assertEqual(witness.record_adapter_evidence(req, receipt)[1], "duplicate")
        altered_payload = {**receipt["payload"], "event_count": receipt["payload"]["event_count"] + 1}
        conflicting = self.signers["github_adapter"].sign(altered_payload)
        with self.assertRaises(Conflict): witness.record_adapter_evidence(req, conflicting)
        self.assertEqual(witness.state(), "GITHUB_APPLIED")
        witness.db.close(); store.db.close()
        self.external = external
        self.store = CheckpointStore(self.db_path, external, self.manifest,
                                     self.authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        self.witness = Witness(self.local_path, self.store, self.manifest,
                               self.authority, ReceiptVerifier(ROLE_KEYS))

    def test_webhooks_duplicate_missing_and_out_of_order_are_not_authority(self):
        req, github = make_request(), self.adapter()
        github.apply_intent(req)
        inbox = WebhookInbox()
        self.assertEqual(inbox.deliver("update", {"kind": "push"}), "accepted")
        self.assertEqual(inbox.deliver("create", {"kind": "create"}), "accepted")
        self.assertEqual(inbox.deliver("update", {"kind": "push"}), "duplicate")
        self.assertEqual([key for key, _ in inbox.arrivals], ["update", "create"])
        missing = WebhookInbox(); missing.deliver("only-update", {"kind": "push"})
        self.witness.intent(req)
        self.assertEqual(self.reconciler(req, github).reconcile(), "GITHUB_APPLIED")

    def test_ref_delete_recreate_and_force_update_reconcile_to_breach(self):
        req, github = make_request(), self.adapter()
        reconciler = self.reconciler(req, github)
        self.assertEqual(reconciler.apply_once(), "GITHUB_APPLIED")
        github.delete(); github.recreate(req["target_commit"])
        self.assertEqual(reconciler.reconcile(), "BREACH")

    def test_force_update_after_applied_is_breach(self):
        req, github = make_request(), self.adapter()
        reconciler = self.reconciler(req, github)
        reconciler.apply_once(); github.force_update("f" * 40)
        self.assertEqual(reconciler.reconcile(), "BREACH")


if __name__ == "__main__": unittest.main()
