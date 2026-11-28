"""Policy-bound lock witness backed by an independently pinned checkpoint model.

The external checkpoint and receipt credentials here are test stand-ins. They are
not independent production services or GitHub-authenticated evidence.
"""
import hashlib
import hmac
import json
import sqlite3
import time
from types import MappingProxyType

from trust import IntegrityError, PolicyError, canonical, sha


class Conflict(Exception):
    pass


ALLOWED_TRANSITIONS = {
    "UNCLAIMED": {"INTENT_RECORDED"},
    "INTENT_RECORDED": {"GITHUB_APPLIED", "PENDING_RECONCILIATION", "BREACH"},
    "PENDING_RECONCILIATION": {"GITHUB_APPLIED", "BREACH"},
    "GITHUB_APPLIED": {"BREACH"},
    "BREACH": set(),
}


def validate_request(request, policy):
    required = {"experiment_id", "registry_digest", "oac_sha256", "base_commit", "target_commit"}
    if not isinstance(request, dict) or set(request) != required:
        raise PolicyError("request fields must exactly match pinned schema")
    if request["experiment_id"] != policy["experiment_id"] or request["registry_digest"] != policy["registry_digest"]:
        raise PolicyError("experiment/registry identity differs from signed policy")
    if len(request["oac_sha256"]) != 64 or any(c not in "0123456789abcdef" for c in request["oac_sha256"].lower()):
        raise PolicyError("invalid OAC SHA-256")
    for field in ("base_commit", "target_commit"):
        if len(request[field]) not in (40, 64) or any(c not in "0123456789abcdef" for c in request[field].lower()):
            raise PolicyError(f"invalid {field}")
    return sha(canonical(request))


class CheckpointStore:
    """SQLite mirror checked against an append-only checkpoint file outside SQLite."""
    def __setattr__(self, name, value):
        if getattr(self, "_sealed", False):
            raise AttributeError("CheckpointStore policy and dependencies are immutable after construction")
        object.__setattr__(self, name, value)

    def __init__(self, path, external_checkpoint, manifest, policy_authority, signing_key, receipt_verifier):
        object.__setattr__(self, "_sealed", False)
        self.external = external_checkpoint
        self.manifest = manifest
        self.authority = policy_authority
        self.key = signing_key
        self.receipt_verifier = receipt_verifier
        self.policy = MappingProxyType(self.authority.verify(manifest))
        if (self.external.custodian_id != self.policy["custodian_id"] or
                self.external.manifest_digest != manifest.digest):
            raise PolicyError("checkpoint identity is not pinned by policy manifest")
        self.db = sqlite3.connect(path, timeout=10, isolation_level=None)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
          CREATE TABLE IF NOT EXISTS metadata(
            singleton INTEGER PRIMARY KEY CHECK(singleton=1), custodian_id TEXT NOT NULL,
            manifest_digest TEXT NOT NULL, genesis_hash TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS events(
            sequence INTEGER PRIMARY KEY, scope TEXT NOT NULL, experiment_id TEXT NOT NULL,
            request_hash TEXT NOT NULL, state TEXT NOT NULL, previous_hash TEXT NOT NULL,
            event_hash TEXT NOT NULL UNIQUE, signature TEXT NOT NULL, recorded_ns INTEGER NOT NULL,
            receipt_digest TEXT);
          CREATE TABLE IF NOT EXISTS claims(
            scope TEXT PRIMARY KEY, experiment_id TEXT NOT NULL, request_hash TEXT NOT NULL,
            state TEXT NOT NULL, sequence INTEGER NOT NULL, receipt_digest TEXT);
          CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events
            BEGIN SELECT RAISE(ABORT, 'append-only event log'); END;
          CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events
            BEGIN SELECT RAISE(ABORT, 'append-only event log'); END;
          CREATE TRIGGER IF NOT EXISTS claims_no_delete BEFORE DELETE ON claims
            BEGIN SELECT RAISE(ABORT, 'claims cannot be deleted'); END;
        """)
        object.__setattr__(self, "_sealed", True)

    def initialize(self, authorization):
        """Explicit one-time bootstrap; never called implicitly by construction."""
        if self.db.execute("SELECT 1 FROM metadata").fetchone():
            raise PolicyError("checkpoint database already initialized")
        self.external.initialize(self.authority, self.manifest, authorization)
        genesis_hash = self.external.head()[1]
        self.db.execute("INSERT INTO metadata VALUES(1,?,?,?)",
                        (self.policy["custodian_id"], self.manifest.digest, genesis_hash))
        self.db.execute("PRAGMA wal_checkpoint(FULL)")

    @staticmethod
    def _event_body(seq, scope, exp, req_hash, state, prev, recorded_ns, receipt_digest):
        return canonical({"sequence": seq, "scope": scope, "experiment_id": exp,
                          "request_hash": req_hash, "state": state,
                          "previous_hash": prev, "recorded_ns": recorded_ns,
                          "receipt_digest": receipt_digest})

    def verify(self):
        rows = self.db.execute("SELECT sequence,scope,experiment_id,request_hash,state,previous_hash,event_hash,signature,recorded_ns,receipt_digest FROM events ORDER BY sequence").fetchall()
        metadata = self.db.execute("SELECT custodian_id,manifest_digest,genesis_hash FROM metadata WHERE singleton=1").fetchone()
        if metadata is None:
            raise IntegrityError("checkpoint database lacks explicitly authorized genesis")
        external_records = self.external.records()  # missing/empty/unidentified pin fails closed
        if metadata[:2] != (self.policy["custodian_id"], self.manifest.digest):
            raise IntegrityError("checkpoint database custodian or policy identity mismatch")
        genesis = external_records[0]["checkpoint_hash"]
        if metadata[2] != genesis or len(external_records) != len(rows) + 1:
            raise IntegrityError("database reset, stale head, or missing checkpoint event")
        previous = genesis
        latest = {}
        for expected, row in enumerate(rows, 1):
            seq, scope, exp, req_hash, state, prev, event_hash, signature, recorded_ns, receipt_digest = row
            payload = self._event_body(seq, scope, exp, req_hash, state, prev, recorded_ns, receipt_digest)
            calculated = sha(payload)
            signed = hmac.new(self.key, calculated.encode(), hashlib.sha256).hexdigest()
            ext = external_records[expected]
            if (seq != expected or scope != self.policy["purpose_key"] or
                exp != self.policy["experiment_id"] or prev != previous or calculated != event_hash or
                not hmac.compare_digest(signature, signed) or
                ext.get("sequence") != seq or ext.get("event_hash") != event_hash):
                raise IntegrityError("checkpoint chain, signature, policy scope, or external pin mismatch")
            previous = event_hash
            latest[scope] = (exp, req_hash, state, seq, receipt_digest)
        claims = {row[0]: row[1:] for row in self.db.execute(
            "SELECT scope,experiment_id,request_hash,state,sequence,receipt_digest FROM claims")}
        if claims != latest:
            raise IntegrityError("checkpoint claims do not match append-only event head")
        return rows

    def _append(self, scope, experiment_id, request_hash, state, receipt_digest=None):
        if scope != self.policy["purpose_key"] or experiment_id != self.policy["experiment_id"]:
            raise PolicyError("custodian rejects noncanonical purpose or experiment identity")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            rows = self.verify()
            existing = self.db.execute("SELECT experiment_id,request_hash,state,sequence,receipt_digest FROM claims WHERE scope=?", (scope,)).fetchone()
            if state == "INTENT_RECORDED":
                if existing:
                    if existing[0] != experiment_id or existing[1] != request_hash:
                        raise Conflict("canonical purpose is already claimed by another intent")
                    self.db.execute("COMMIT")
                    return existing[3], "duplicate"
                current_state = "UNCLAIMED"
            else:
                if not existing:
                    raise Conflict("cannot transition an unclaimed purpose")
                if existing[0] != experiment_id or existing[1] != request_hash:
                    raise Conflict("transition does not match the claimed intent")
                current_state = existing[2]
                if state == current_state:
                    if receipt_digest == existing[4]:
                        self.db.execute("COMMIT")
                        return existing[3], "duplicate"
                    raise Conflict("conflicting receipt replay for current state")
            if state not in ALLOWED_TRANSITIONS[current_state]:
                raise Conflict(f"transition {current_state} -> {state} is forbidden")
            seq = len(rows) + 1
            prev = rows[-1][6] if rows else self.external.head()[1]
            recorded_ns = time.time_ns()
            payload = self._event_body(seq, scope, experiment_id, request_hash, state, prev,
                                       recorded_ns, receipt_digest)
            event_hash = sha(payload)
            signature = hmac.new(self.key, event_hash.encode(), hashlib.sha256).hexdigest()
            self.db.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?)",
                            (seq, scope, experiment_id, request_hash, state, prev, event_hash,
                             signature, recorded_ns, receipt_digest))
            self.db.execute("INSERT INTO claims VALUES(?,?,?,?,?,?) ON CONFLICT(scope) DO UPDATE SET "
                            "experiment_id=excluded.experiment_id,request_hash=excluded.request_hash,"
                            "state=excluded.state,sequence=excluded.sequence,receipt_digest=excluded.receipt_digest",
                            (scope, experiment_id, request_hash, state, seq, receipt_digest))
            # The external checkpoint append is outside SQLite. It is published before
            # acceptance returns; if it fails, the local DB is ahead and all later
            # acceptance fails closed until operator recovery of this exact event.
            checkpoint_previous = self.external.head()[1]
            self.external.publish(seq, event_hash, checkpoint_previous)
            self.db.execute("COMMIT")
            return seq, "accepted"
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def accept_intent(self, request):
        request_hash = validate_request(request, self.policy)
        return self._append(self.policy["purpose_key"], self.policy["experiment_id"],
                            request_hash, "INTENT_RECORDED", None)

    def record_receipt(self, request, receipt):
        request_hash = validate_request(request, self.policy)
        role, payload = self.receipt_verifier.verify(receipt)
        expected = {"purpose_key": self.policy["purpose_key"],
                    "experiment_id": self.policy["experiment_id"],
                    "request_hash": request_hash, "repository": self.policy["repository"],
                    "lock_ref": self.policy["lock_ref"], "app_id": self.policy["app_id"]}
        if any(payload.get(k) != v for k, v in expected.items()):
            raise IntegrityError("receipt is not bound to the pinned purpose and request")
        outcome = payload.get("outcome")
        allowed_role = {"GITHUB_APPLIED": "github_adapter",
                        "PENDING_RECONCILIATION": "witness_worker",
                        "BREACH": "independent_reconciler"}
        if allowed_role.get(outcome) != role:
            raise IntegrityError("receipt role is not authorized for this state")
        if outcome == "GITHUB_APPLIED" and payload.get("observed_sha") != request["target_commit"]:
            raise IntegrityError("adapter receipt does not attest the intended target")
        receipt_digest = sha(canonical(receipt))
        return self._append(self.policy["purpose_key"], self.policy["experiment_id"],
                            request_hash, outcome, receipt_digest)

    def state(self, scope):
        row = self.db.execute("SELECT state FROM claims WHERE scope=?", (scope,)).fetchone()
        return row[0] if row else "UNCLAIMED"


class Witness:
    """Immutable policy binding, intent acceptance, and signed adapter-evidence gate."""
    __slots__ = ("_anchor", "_manifest", "_policy", "_authority", "_receipt_verifier", "_db", "_sealed")

    def __init__(self, local_path, checkpoint_store, manifest, policy_authority, receipt_verifier):
        object.__setattr__(self, "_sealed", False)
        policy = policy_authority.verify(manifest)
        if checkpoint_store.manifest.digest != manifest.digest:
            raise PolicyError("witness policy differs from genesis-pinned custodian policy")
        object.__setattr__(self, "_anchor", checkpoint_store)
        object.__setattr__(self, "_manifest", manifest)
        object.__setattr__(self, "_policy", MappingProxyType(dict(policy)))
        object.__setattr__(self, "_authority", policy_authority)
        object.__setattr__(self, "_receipt_verifier", receipt_verifier)
        db = sqlite3.connect(local_path, timeout=10, isolation_level=None)
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
        db.execute("CREATE TABLE IF NOT EXISTS mirror(sequence INTEGER PRIMARY KEY,event_hash TEXT NOT NULL)")
        object.__setattr__(self, "_db", db)
        object.__setattr__(self, "_sealed", True)

    def __setattr__(self, name, value):
        if getattr(self, "_sealed", False):
            raise AttributeError("Witness policy and dependencies are immutable after construction")
        object.__setattr__(self, name, value)

    @property
    def policy(self): return self._policy
    @property
    def scope(self): return self._policy["purpose_key"]
    @property
    def experiment_id(self): return self._policy["experiment_id"]
    @property
    def registry_digest(self): return self._policy["registry_digest"]
    @property
    def db(self): return self._db

    def _request_hash(self, request):
        return validate_request(request, self._policy)

    def _sync_and_verify(self):
        anchored = self._anchor.verify()  # signed manifest, genesis, external pin and DB chain
        local = self._db.execute("SELECT sequence,event_hash FROM mirror ORDER BY sequence").fetchall()
        if len(local) > len(anchored):
            raise IntegrityError("external checkpoint is stale or rolled back")
        for seq, digest in local:
            if seq < 1 or anchored[seq - 1][6] != digest:
                raise IntegrityError("local mirror and external checkpoint diverge")
        self._db.execute("BEGIN IMMEDIATE")
        try:
            for row in anchored[len(local):]:
                self._db.execute("INSERT INTO mirror VALUES(?,?)", (row[0], row[6]))
            self._db.execute("COMMIT")
        except Exception:
            self._db.execute("ROLLBACK")
            raise

    def intent(self, request):
        request_hash = self._request_hash(request)
        self._sync_and_verify()
        result = self._anchor.accept_intent(request)
        self._sync_and_verify()
        return result

    def record_adapter_evidence(self, request, receipt):
        request_hash = self._request_hash(request)
        role, payload = self._receipt_verifier.verify(receipt)
        expected = {"purpose_key": self.scope, "experiment_id": self.experiment_id,
                    "request_hash": request_hash, "repository": self._policy["repository"],
                    "lock_ref": self._policy["lock_ref"], "app_id": self._policy["app_id"]}
        if any(payload.get(k) != v for k, v in expected.items()):
            raise IntegrityError("adapter evidence is for a different policy/intent")
        outcome = payload.get("outcome")
        allowed_role = {"GITHUB_APPLIED": "github_adapter",
                        "PENDING_RECONCILIATION": "witness_worker",
                        "BREACH": "independent_reconciler"}
        if allowed_role.get(outcome) != role:
            raise IntegrityError("receipt signer is not authorized for this state transition")
        if outcome == "GITHUB_APPLIED" and payload.get("observed_sha") != request["target_commit"]:
            raise IntegrityError("adapter receipt does not attest the intended target")
        self._sync_and_verify()
        result = self._anchor.record_receipt(request, receipt)
        self._sync_and_verify()
        return result

    def state(self):
        self._sync_and_verify()
        return self._anchor.state(self.scope)
