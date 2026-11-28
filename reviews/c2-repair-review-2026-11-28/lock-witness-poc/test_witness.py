import multiprocessing
import json
import os
import shutil
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from github_adapter import FakeGitHub, Reconciler, WebhookInbox
from trust import (ExternalCheckpoint, IntegrityError, PolicyAuthority, PolicyError,
                   ReceiptSigner, ReceiptVerifier, canonical, sha)
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


def new_authority(state_path):
    authority = PolicyAuthority(ROOT_KEY, {"LC518-R2-C2": "LC518-R2-C2"}, state_path)
    if not os.path.exists(state_path) and not os.path.exists(state_path + ".head"):
        authority.initialize()
    return authority


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
    authority = new_authority(authority_path)
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


def independent_checkpoint_writer(db_path, local_path, external_path, authority_path,
                                  target, barrier, queue, observed_heads):
    try:
        authority = new_authority(authority_path)
        manifest = authority.issue(POLICY)
        def pre_lock(sequence, _event_hash, previous_hash):
            observed_heads.put((sequence, previous_hash))
            barrier.wait(timeout=20)
        external = ExternalCheckpoint(external_path, POLICY["custodian_id"],
                                      manifest.digest, CUSTODIAN_KEY,
                                      pre_lock_hook=pre_lock)
        verifier = ReceiptVerifier(ROLE_KEYS)
        store = CheckpointStore(db_path, external, manifest, authority, CUSTODIAN_KEY, verifier)
        witness = Witness(local_path, store, manifest, authority, verifier)
        witness.intent(make_request(target=target))
        queue.put((db_path, "accepted", ""))
        witness.db.close(); store.db.close()
    except Exception as exc:
        queue.put((db_path, "rejected", type(exc).__name__))


def authority_issue_worker(state_path, policy, barrier, queue):
    try:
        authority = new_authority(state_path)
        barrier.wait(timeout=20)
        manifest = authority.issue(policy)
        queue.put(("accepted", manifest.digest, policy["experiment_id"]))
    except Exception as exc:
        queue.put(("rejected", type(exc).__name__, policy["experiment_id"]))


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
        reconstructed_authority = new_authority(authority_path)
        self.assertEqual(reconstructed_authority.issue(POLICY).digest, self.manifest.digest)
        with self.assertRaises(PolicyError): reconstructed_authority.issue(alternate)
        # No second manifest means no independently initialized second custodian.
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM claims").fetchone()[0], 0)

    def test_separate_policy_authority_state_paths_can_fork_same_root(self):
        root = Path(self.tmp.name)
        authority_a = new_authority(str(root / "authority-a.jsonl"))
        authority_b = new_authority(str(root / "authority-b.jsonl"))
        manifest_a = authority_a.issue(POLICY)
        alternate = {**POLICY, "experiment_id": "FORKED-EXPERIMENT",
                     "registry_digest": "f" * 64, "custodian_id": "FORKED-CUSTODIAN"}
        manifest_b = authority_b.issue(alternate)
        self.assertNotEqual(manifest_a.digest, manifest_b.digest)
        # This demonstrates a trust-model boundary: each local log enforces one lineage,
        # but two copies of the trusted root with separate state are not globally unique.

    def test_policy_authority_concurrent_same_manifest_issuance_is_serialized(self):
        ctx = multiprocessing.get_context("spawn")
        barrier, queue = ctx.Barrier(4), ctx.Queue()
        authority_path = str(Path(self.tmp.name) / "concurrent-policy.jsonl")
        new_authority(authority_path)
        processes = [ctx.Process(target=authority_issue_worker,
                    args=(authority_path, POLICY, barrier, queue)) for _ in range(4)]
        for proc in processes: proc.start()
        results = [queue.get(timeout=30) for _ in processes]
        for proc in processes:
            proc.join(30)
            self.assertEqual(proc.exitcode, 0)
        self.assertEqual([row[0] for row in results], ["accepted"] * 4, results)
        self.assertEqual({row[1] for row in results}, {self.manifest.digest})
        reconstructed = new_authority(authority_path)
        self.assertEqual(reconstructed.issue(POLICY).digest, self.manifest.digest)

    def test_policy_authority_concurrent_conflicting_manifests_choose_one(self):
        ctx = multiprocessing.get_context("spawn")
        barrier, queue = ctx.Barrier(4), ctx.Queue()
        authority_path = str(Path(self.tmp.name) / "conflicting-policy.jsonl")
        new_authority(authority_path)
        policies = [({**POLICY, "experiment_id": f"FORK-{i}",
                      "registry_digest": str(i) * 64, "custodian_id": f"CUSTODIAN-{i}"})
                    for i in range(4)]
        processes = [ctx.Process(target=authority_issue_worker,
                    args=(authority_path, policy, barrier, queue)) for policy in policies]
        for proc in processes: proc.start()
        results = [queue.get(timeout=30) for _ in processes]
        for proc in processes:
            proc.join(30)
            self.assertEqual(proc.exitcode, 0)
        accepted = [row for row in results if row[0] == "accepted"]
        rejected = [row for row in results if row[0] == "rejected"]
        self.assertEqual(len(accepted), 1, results)
        self.assertEqual(len(rejected), 3, results)
        winner = next(policy for policy in policies if policy["experiment_id"] == accepted[0][2])
        reconstructed = new_authority(authority_path)
        self.assertEqual(reconstructed.issue(winner).digest, accepted[0][1])
        with self.assertRaises(PolicyError): reconstructed.issue(next(p for p in policies if p != winner))

    def test_policy_authority_missing_state_fails_closed_for_live_and_reconstructed_authority(self):
        authority_path = str(Path(self.tmp.name) / "missing-policy.jsonl")
        authority = new_authority(authority_path)
        manifest = authority.issue(POLICY)
        authorization = authority.authorize_initialization(manifest)
        os.remove(authority_path)
        with self.assertRaises(PolicyError): authority.verify(manifest)
        with self.assertRaises(PolicyError): authority.issue(POLICY)
        with self.assertRaises(PolicyError): authority.authorize_initialization(manifest)
        with self.assertRaises(PolicyError): authority.verify_initialization(manifest, authorization)
        with self.assertRaises(PolicyError): PolicyAuthority(
            ROOT_KEY, {"LC518-R2-C2": "LC518-R2-C2"}, authority_path)

    def test_new_policy_authority_requires_explicit_initialization(self):
        authority_path = str(Path(self.tmp.name) / "not-yet-initialized.jsonl")
        authority = PolicyAuthority(ROOT_KEY, {"LC518-R2-C2": "LC518-R2-C2"}, authority_path)
        with self.assertRaises(PolicyError): authority.issue(POLICY)
        self.assertFalse(os.path.exists(authority_path))
        self.assertEqual(authority.initialize(), "created")
        self.assertEqual(authority.issue(POLICY).digest, self.manifest.digest)

    def test_policy_authority_missing_state_after_initialization_and_issuance_fails_closed(self):
        for suffix, prepare in (("initialized", lambda a, m: a.authorize_initialization(m)),
                                ("issued", lambda _a, _m: None)):
            authority_path = str(Path(self.tmp.name) / f"authority-{suffix}.jsonl")
            authority = new_authority(authority_path)
            manifest = authority.issue(POLICY)
            authorization = prepare(authority, manifest)
            if authorization is None:
                authorization = authority.authorize_initialization(manifest)
            os.remove(authority_path)
            with self.assertRaises(PolicyError): authority.verify(manifest)
            with self.assertRaises(PolicyError): authority.issue(POLICY)
            with self.assertRaises(PolicyError): authority.authorize_initialization(manifest)
            with self.assertRaises(PolicyError): authority.verify_initialization(manifest, authorization)
            with self.assertRaises(PolicyError): PolicyAuthority(
                ROOT_KEY, {"LC518-R2-C2": "LC518-R2-C2"}, authority_path)

    def test_policy_authority_truncation_and_corruption_fail_closed_after_reconstruction(self):
        for mode in ("truncate", "corrupt"):
            authority_path = str(Path(self.tmp.name) / f"authority-{mode}.jsonl")
            authority = new_authority(authority_path)
            manifest = authority.issue(POLICY)
            authorization = authority.authorize_initialization(manifest)
            with open(authority_path, "rb") as f:
                data = f.read()
            if mode == "truncate":
                data = data[:data.rfind(b"\n", 0, len(data) - 1) + 1]
            else:
                data = data.replace(b"POLICY_BOUND", b"POLICY_BROKEN", 1)
            with open(authority_path, "wb") as f:
                f.write(data)
            with self.assertRaises(PolicyError): authority.verify(manifest)
            with self.assertRaises(PolicyError): authority.issue(POLICY)
            with self.assertRaises(PolicyError): authority.authorize_initialization(manifest)
            with self.assertRaises(PolicyError): authority.verify_initialization(manifest, authorization)
            with self.assertRaises(PolicyError): PolicyAuthority(
                ROOT_KEY, {"LC518-R2-C2": "LC518-R2-C2"}, authority_path)

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

    def test_genesis_initialization_recovers_at_each_crash_boundary(self):
        for boundary in ("before_external_genesis", "after_external_genesis",
                         "after_metadata_insert", "after_metadata_commit"):
            with self.subTest(boundary=boundary):
                root = Path(self.tmp.name) / boundary
                root.mkdir()
                authority_path = str(root / "authority.jsonl")
                authority = new_authority(authority_path)
                manifest = authority.issue(POLICY)
                authorization = authority.authorize_initialization(manifest)
                external_path = str(root / "checkpoint.jsonl")
                external = ExternalCheckpoint(external_path, POLICY["custodian_id"],
                                              manifest.digest, CUSTODIAN_KEY)
                store = CheckpointStore(str(root / "checkpoint.db"), external, manifest,
                                        authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
                with self.assertRaises(RuntimeError): store.initialize(authorization, failpoint=boundary)
                # Reconstruct all mutable components as after a process crash.
                store.db.close()
                authority = PolicyAuthority(ROOT_KEY, {"LC518-R2-C2": "LC518-R2-C2"}, authority_path)
                external = ExternalCheckpoint(external_path, POLICY["custodian_id"],
                                              manifest.digest, CUSTODIAN_KEY)
                store = CheckpointStore(str(root / "checkpoint.db"), external, manifest,
                                        authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
                result = store.initialize(authorization)
                self.assertIn(result, ("created", "duplicate"))
                self.assertEqual(len(external.records()), 1)
                self.assertEqual(store.verify(), [])
                with self.assertRaises(PolicyError): authority.authorize_initialization(manifest)
                store.db.close()

    def test_mismatched_genesis_fails_closed_during_initialization_recovery(self):
        root = Path(self.tmp.name) / "mismatched-genesis"
        root.mkdir()
        authority_path = str(root / "authority.jsonl")
        authority = new_authority(authority_path)
        manifest = authority.issue(POLICY)
        authorization = authority.authorize_initialization(manifest)
        external_path = str(root / "checkpoint.jsonl")
        external = ExternalCheckpoint(external_path, POLICY["custodian_id"], manifest.digest, CUSTODIAN_KEY)
        store = CheckpointStore(str(root / "checkpoint.db"), external, manifest,
                                authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        with self.assertRaises(RuntimeError): store.initialize(authorization, failpoint="after_external_genesis")
        store.db.close()
        wrong = ExternalCheckpoint(external_path, "OTHER-CUSTODIAN", manifest.digest, CUSTODIAN_KEY)
        record = {"kind": "GENESIS", "sequence": 0, "custodian_id": "OTHER-CUSTODIAN",
                  "manifest_digest": manifest.digest, "previous_hash": "0" * 64,
                  "checkpoint_hash": sha(f"GENESIS|OTHER-CUSTODIAN|{manifest.digest}"), "recorded_ns": 1}
        record["signature"] = wrong._sign(record)
        with open(external_path, "w", encoding="utf-8") as f:
            f.write(canonical(record) + "\n")
        external = ExternalCheckpoint(external_path, POLICY["custodian_id"], manifest.digest, CUSTODIAN_KEY)
        store = CheckpointStore(str(root / "checkpoint.db"), external, manifest,
                                authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        with self.assertRaises(IntegrityError): store.initialize(authorization)
        store.db.close()

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

    def test_external_compare_append_serializes_independent_checkpoint_databases(self):
        ctx = multiprocessing.get_context("spawn")
        barrier, queue = ctx.Barrier(2), ctx.Queue()
        observed_heads = ctx.Queue()
        root = Path(self.tmp.name)
        authority_path = str(root / "policy-authority.jsonl")
        specs = []
        for name, target in (("writer-a", "3" * 40), ("writer-b", "4" * 40)):
            checkpoint_db = str(root / f"{name}-checkpoint.db")
            local_db = str(root / f"{name}-local.db")
            dst = sqlite3.connect(checkpoint_db)
            self.store.db.backup(dst)  # both independent DBs start at identical trusted genesis
            dst.close()
            specs.append((checkpoint_db, local_db, target))
        processes = [ctx.Process(target=independent_checkpoint_writer,
            args=(db, local, self.external_path, authority_path, target, barrier, queue, observed_heads))
            for db, local, target in specs]
        for proc in processes: proc.start()
        submitted_heads = [observed_heads.get(timeout=25) for _ in processes]
        self.assertEqual(submitted_heads[0], submitted_heads[1])  # both prepared against the same head
        results = [queue.get(timeout=25) for _ in processes]
        for proc in processes:
            proc.join(25)
            self.assertEqual(proc.exitcode, 0)
        accepted = [row for row in results if row[1] == "accepted"]
        rejected = [row for row in results if row[1] == "rejected"]
        self.assertEqual(len(accepted), 1, results)
        self.assertEqual(len(rejected), 1, results)
        # The shared external chain remains valid and contains exactly one new head.
        self.assertEqual(len(self.external.records()), 2)  # genesis + one publication
        winner_db = accepted[0][0]
        winner_store = CheckpointStore(winner_db, self.external, self.manifest,
                                       self.authority, CUSTODIAN_KEY, ReceiptVerifier(ROLE_KEYS))
        self.assertEqual(len(winner_store.verify()), 1)
        winner_store.db.close()

    def test_exact_duplicate_and_changed_target(self):
        req = make_request()
        first = self.witness.intent(req)
        self.assertEqual(self.witness.intent(req), (first[0], "duplicate"))
        with self.assertRaises(Conflict): self.witness.intent(make_request(target="e" * 40))

    def test_noop_commit_target_rejected_and_hex_case_normalized(self):
        no_op = make_request(target="d" * 40)
        with self.assertRaises(PolicyError): self.witness.intent(no_op)
        request = make_request(target="e" * 40)
        first = self.witness.intent(request)
        uppercase = {**request, "oac_sha256": request["oac_sha256"].upper(),
                     "base_commit": request["base_commit"].upper(),
                     "target_commit": request["target_commit"].upper()}
        self.assertEqual(self.witness.intent(uppercase), (first[0], "duplicate"))

    def test_duplicate_intent_in_breach_reports_breach_and_receipt_replay_cannot_clear_it(self):
        request, github = make_request(), self.adapter()
        self.witness.intent(request)
        applied_receipt = github.apply_intent(request)
        self.witness.record_adapter_evidence(request, applied_receipt)
        reconciler = self.reconciler(request, github)
        github.force_update("f" * 40)
        self.assertEqual(reconciler.reconcile(), "BREACH")
        self.assertEqual(self.witness.intent(request)[1], "BREACH")
        with self.assertRaises(Conflict): self.witness.record_adapter_evidence(request, applied_receipt)
        self.assertEqual(self.witness.state(), "BREACH")

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

    def test_pending_reconciliation_routes_to_breach_on_external_change(self):
        request = make_request()
        self.witness.intent(request)
        github = self.adapter()
        pending = self.signers["witness_worker"].sign(
            github._receipt(request, "PENDING_RECONCILIATION", None)["payload"])
        self.witness.record_adapter_evidence(request, pending)
        github.force_update("f" * 40)  # external ref mutation after the pending state was recorded

        class RaisingAdapter(FakeGitHub):
            def apply_intent(self, _request):
                raise RuntimeError("simulated GitHub adapter failure")

        raising = RaisingAdapter(POLICY, self.signers["github_adapter"])
        raising.ref, raising.events = github.ref, github.events
        reconciler = self.reconciler(request, raising)
        self.assertEqual(reconciler.apply_once(), "BREACH")
        self.assertEqual(self.witness.state(), "BREACH")

    def test_pending_reconciliation_retries_untouched_ref_to_applied(self):
        request, github = make_request(), self.adapter()
        github.app_allowed = False
        reconciler = self.reconciler(request, github)
        self.assertEqual(reconciler.apply_once(), "PENDING_RECONCILIATION")
        self.assertIsNone(github.read_ref())
        self.assertEqual(github.events, [])
        github.app_allowed = True
        self.assertEqual(reconciler.apply_once(), "GITHUB_APPLIED")
        self.assertEqual(github.read_ref(), request["target_commit"])
        self.assertEqual(github.events, [
            ("create", None, request["base_commit"], "app"),
            ("update", request["base_commit"], request["target_commit"], "app"),
        ])
        with self.assertRaises(Conflict):
            self.witness.intent(make_request(target="e" * 40))

    def test_pending_reconciliation_retries_partial_base_creation_to_applied(self):
        request = make_request()

        class FailAfterBaseCreateAdapter(FakeGitHub):
            def __init__(self, policy, app_signer):
                super().__init__(policy, app_signer)
                self.fail_on_update = True

            def apply_intent(self, req):
                normalized = {**req, "base_commit": req["base_commit"].lower(),
                              "target_commit": req["target_commit"].lower()}
                base, target = normalized["base_commit"], normalized["target_commit"]
                if self.ref is None:
                    self.ref = base
                    self.events.append(("create", None, base, "app"))
                if self.fail_on_update and self.ref == base:
                    raise RuntimeError("simulated outage between base create and B->A update")
                return super().apply_intent(req)

        github = FailAfterBaseCreateAdapter(POLICY, self.signers["github_adapter"])
        reconciler = self.reconciler(request, github)
        self.assertEqual(reconciler.apply_once(), "PENDING_RECONCILIATION")
        self.assertEqual(github.read_ref(), request["base_commit"])
        self.assertEqual(github.events, [("create", None, request["base_commit"], "app")])
        github.fail_on_update = False
        self.assertEqual(reconciler.apply_once(), "GITHUB_APPLIED")
        self.assertEqual(github.read_ref(), request["target_commit"])
        self.assertEqual(github.events, [
            ("create", None, request["base_commit"], "app"),
            ("update", request["base_commit"], request["target_commit"], "app"),
        ])

    def test_pending_reconciliation_progressing_none_to_base_then_applied_without_conflict(self):
        request = make_request()

        class OutageThenBaseFailAdapter(FakeGitHub):
            def __init__(self, policy, app_signer):
                super().__init__(policy, app_signer)
                self.mode = "outage"

            def apply_intent(self, req):
                if self.mode == "outage":
                    raise RuntimeError("transient outage before create")
                if self.mode == "fail_update":
                    base = req["base_commit"].lower()
                    if self.ref is None:
                        self.ref = base
                        self.events.append(("create", None, base, "app"))
                    raise RuntimeError("transient failure after create")
                return super().apply_intent(req)

        github = OutageThenBaseFailAdapter(POLICY, self.signers["github_adapter"])
        reconciler = self.reconciler(request, github)
        self.assertEqual(reconciler.apply_once(), "PENDING_RECONCILIATION")
        github.mode = "fail_update"
        self.assertEqual(reconciler.apply_once(), "PENDING_RECONCILIATION")
        self.assertEqual(github.read_ref(), request["base_commit"])
        github.mode = "ok"
        self.assertEqual(reconciler.apply_once(), "GITHUB_APPLIED")
        self.assertEqual(github.read_ref(), request["target_commit"])

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
