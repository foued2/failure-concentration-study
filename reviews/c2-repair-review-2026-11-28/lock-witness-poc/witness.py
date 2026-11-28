"""Local model of a policy-bound witness backed by a separate checkpoint custodian.

This is a proof of concept: SQLite files and an HMAC key do not provide production
independence. Production would replace CheckpointStore with a separately operated,
linearizable append-only service and asymmetric signatures.
"""
import hashlib
import hmac
import json
import sqlite3
import time
from types import MappingProxyType


class Conflict(Exception):
    pass


class IntegrityError(Exception):
    pass


class PolicyError(Exception):
    pass


ALLOWED_TRANSITIONS = {
    "UNCLAIMED": {"INTENT_RECORDED"},
    "INTENT_RECORDED": {"GITHUB_APPLIED", "PENDING_RECONCILIATION", "BREACH"},
    "PENDING_RECONCILIATION": {"GITHUB_APPLIED", "BREACH"},
    "GITHUB_APPLIED": {"BREACH"},
    "BREACH": set(),
}


class CheckpointStore:
    """Separate custodian model: signed append-only event log and unique purpose claim."""
    def __init__(self, path, signing_key):
        self.key = signing_key
        self.db = sqlite3.connect(path, timeout=10, isolation_level=None)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
          CREATE TABLE IF NOT EXISTS events(
            sequence INTEGER PRIMARY KEY, scope TEXT NOT NULL, experiment_id TEXT NOT NULL,
            request_hash TEXT NOT NULL, state TEXT NOT NULL, previous_hash TEXT NOT NULL,
            event_hash TEXT NOT NULL UNIQUE, signature TEXT NOT NULL, recorded_ns INTEGER NOT NULL);
          CREATE TABLE IF NOT EXISTS claims(
            scope TEXT PRIMARY KEY, experiment_id TEXT NOT NULL, request_hash TEXT NOT NULL,
            state TEXT NOT NULL, sequence INTEGER NOT NULL);
          CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events
            BEGIN SELECT RAISE(ABORT, 'append-only event log'); END;
          CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events
            BEGIN SELECT RAISE(ABORT, 'append-only event log'); END;
          CREATE TRIGGER IF NOT EXISTS claims_no_delete BEFORE DELETE ON claims
            BEGIN SELECT RAISE(ABORT, 'claims cannot be deleted'); END;
        """)

    @staticmethod
    def _canonical(value):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def _sha(value):
        return hashlib.sha256(value.encode()).hexdigest()

    def verify(self):
        previous = "0" * 64
        latest = {}
        rows = self.db.execute("SELECT sequence,scope,experiment_id,request_hash,state,previous_hash,event_hash,signature,recorded_ns FROM events ORDER BY sequence").fetchall()
        for expected, row in enumerate(rows, 1):
            seq, scope, exp, request_hash, state, prev, event_hash, signature, recorded_ns = row
            payload = self._canonical({"sequence": seq, "scope": scope, "experiment_id": exp,
                                       "request_hash": request_hash, "state": state,
                                       "previous_hash": prev, "recorded_ns": recorded_ns})
            calculated = self._sha(payload)
            signed = hmac.new(self.key, calculated.encode(), hashlib.sha256).hexdigest()
            if seq != expected or prev != previous or calculated != event_hash or not hmac.compare_digest(signature, signed):
                raise IntegrityError("checkpoint chain/signature invalid or incomplete")
            previous = event_hash
            latest[scope] = (exp, request_hash, state, seq)
        claims = {row[0]: row[1:] for row in self.db.execute(
            "SELECT scope,experiment_id,request_hash,state,sequence FROM claims")}
        if claims != latest:
            raise IntegrityError("checkpoint claims do not match append-only event head")
        return rows

    def _append(self, scope, experiment_id, request_hash, state):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            # Verify under the same write lock before deciding the next transition.
            rows = self.verify()
            existing = self.db.execute("SELECT experiment_id,request_hash,state,sequence FROM claims WHERE scope=?", (scope,)).fetchone()
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
                if state == current_state and state == "PENDING_RECONCILIATION":
                    self.db.execute("COMMIT")
                    return existing[3], "duplicate"
            if state not in ALLOWED_TRANSITIONS[current_state]:
                raise Conflict(f"transition {current_state} -> {state} is forbidden")
            seq = len(rows) + 1
            prev = rows[-1][6] if rows else "0" * 64
            recorded_ns = time.time_ns()
            payload = self._canonical({"sequence": seq, "scope": scope, "experiment_id": experiment_id,
                                       "request_hash": request_hash, "state": state,
                                       "previous_hash": prev, "recorded_ns": recorded_ns})
            event_hash = self._sha(payload)
            signature = hmac.new(self.key, event_hash.encode(), hashlib.sha256).hexdigest()
            self.db.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?)",
                            (seq, scope, experiment_id, request_hash, state, prev, event_hash, signature, recorded_ns))
            self.db.execute("INSERT INTO claims VALUES(?,?,?,?,?) ON CONFLICT(scope) DO UPDATE SET "
                            "experiment_id=excluded.experiment_id,request_hash=excluded.request_hash,"
                            "state=excluded.state,sequence=excluded.sequence",
                            (scope, experiment_id, request_hash, state, seq))
            self.db.execute("COMMIT")
            return seq, "accepted"
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def append_intent(self, scope, experiment_id, request_hash):
        return self._append(scope, experiment_id, request_hash, "INTENT_RECORDED")

    def transition(self, scope, experiment_id, request_hash, state):
        return self._append(scope, experiment_id, request_hash, state)

    def state(self, scope):
        row = self.db.execute("SELECT state FROM claims WHERE scope=?", (scope,)).fetchone()
        return row[0] if row else "UNCLAIMED"


class Witness:
    """Policy-bound intent endpoint and local mirror of the external checkpoint."""
    def __init__(self, local_path, checkpoint_store, policy):
        self.anchor = checkpoint_store
        if set(policy) != {"purpose_key", "experiment_id", "registry_digest"}:
            raise PolicyError("policy must pin purpose, experiment ID, and registry digest")
        self.policy = MappingProxyType(dict(policy))
        self.db = sqlite3.connect(local_path, timeout=10, isolation_level=None)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("CREATE TABLE IF NOT EXISTS mirror(sequence INTEGER PRIMARY KEY,event_hash TEXT NOT NULL)")

    @property
    def scope(self):
        return self.policy["purpose_key"]

    @property
    def experiment_id(self):
        return self.policy["experiment_id"]

    @property
    def registry_digest(self):
        return self.policy["registry_digest"]

    def _request_hash(self, request):
        required = {"experiment_id", "registry_digest", "oac_sha256", "base_commit", "target_commit"}
        if set(request) != required:
            raise PolicyError("request fields must exactly match the pinned schema")
        if request["experiment_id"] != self.experiment_id or request["registry_digest"] != self.registry_digest:
            raise PolicyError("experiment/registry identity differs from pinned policy")
        for field in ("oac_sha256",):
            if len(request[field]) != 64 or any(c not in "0123456789abcdef" for c in request[field].lower()):
                raise PolicyError(f"invalid {field}")
        for field in ("base_commit", "target_commit"):
            if len(request[field]) not in (40, 64) or any(c not in "0123456789abcdef" for c in request[field].lower()):
                raise PolicyError(f"invalid {field}")
        return CheckpointStore._sha(CheckpointStore._canonical(request))

    def _sync_and_verify(self):
        anchored = self.anchor.verify()  # missing/corrupt checkpoint raises before accepting anything
        local = self.db.execute("SELECT sequence,event_hash FROM mirror ORDER BY sequence").fetchall()
        if len(local) > len(anchored):
            raise IntegrityError("external checkpoint is stale or rolled back")
        for seq, digest in local:
            if seq < 1 or anchored[seq - 1][6] != digest:
                raise IntegrityError("local mirror and external checkpoint diverge")
        # Recover a crash after external append but before local mirror update.
        self.db.execute("BEGIN IMMEDIATE")
        try:
            for row in anchored[len(local):]:
                self.db.execute("INSERT INTO mirror VALUES(?,?)", (row[0], row[6]))
            self.db.execute("COMMIT")
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def intent(self, request):
        request_hash = self._request_hash(request)
        self._sync_and_verify()
        result = self.anchor.append_intent(self.scope, self.experiment_id, request_hash)
        self._sync_and_verify()
        return result

    def transition(self, request, state):
        request_hash = self._request_hash(request)
        self._sync_and_verify()
        result = self.anchor.transition(self.scope, self.experiment_id, request_hash, state)
        self._sync_and_verify()
        return result

    def state(self):
        self._sync_and_verify()
        return self.anchor.state(self.scope)
