"""Test-only trust primitives for pinned policy, external checkpoint, and receipts."""
import hashlib
import hmac
import json
import os
import secrets
from contextlib import contextmanager
from dataclasses import dataclass
import time


class IntegrityError(Exception):
    pass


class PolicyError(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


@contextmanager
def _file_lock(path):
    """Advisory cross-process lock for local shared-filesystem model stores."""
    with open(path + ".lock", "a+b") as lock_file:
        if os.name == "nt":
            import msvcrt
            lock_file.seek(0, os.SEEK_END)
            if lock_file.tell() == 0:
                lock_file.write(b"\0")
                lock_file.flush()
            lock_file.seek(0)
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                lock_file.seek(0)
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


@dataclass(frozen=True)
class SignedPolicy:
    payload_json: str
    signature: str

    @property
    def payload(self):
        return json.loads(self.payload_json)

    @property
    def digest(self):
        return sha(self.payload_json)


class PolicyAuthority:
    """Model of a separately trusted signer for canonical study policy."""
    def __init__(self, root_key, canonical_purposes, state_path=None):
        self._root_key = root_key
        self._canonical_purposes = dict(canonical_purposes)
        self._state_path = state_path
        self._issuance = {}
        self._consumed = set()
        self._purpose_manifests = {}
        self._anchor_path = state_path + ".head" if state_path else None
        if state_path and (os.path.exists(state_path) or os.path.exists(self._anchor_path)):
            with _file_lock(state_path):
                self._load_issuance_log_unlocked()

    def _anchor_signature(self, sequence, event_hash):
        data = canonical({"sequence": sequence, "event_hash": event_hash})
        return hmac.new(self._root_key, data.encode(), hashlib.sha256).hexdigest()

    def _write_anchor_unlocked(self, sequence, event_hash):
        record = {"sequence": sequence, "event_hash": event_hash,
                  "signature": self._anchor_signature(sequence, event_hash)}
        temp_path = self._anchor_path + f".{os.getpid()}.tmp"
        with open(temp_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(canonical(record) + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, self._anchor_path)

    def _initialize_log_unlocked(self):
        if os.path.exists(self._state_path) or os.path.exists(self._anchor_path):
            raise PolicyError("policy-authority state is partially initialized")
        with open(self._state_path, "x", encoding="utf-8", newline="\n") as f:
            f.flush()
            os.fsync(f.fileno())
        self._write_anchor_unlocked(0, "0" * 64)

    def _append_authority_event_unlocked(self, kind, manifest_digest, nonce, scientific_purpose):
        if not self._state_path:
            raise PolicyError("durable policy-authority state path required for genesis authorization")
        rows = self._authority_records_unlocked()
        previous = rows[-1]["event_hash"] if rows else "0" * 64
        record = {"kind": kind, "sequence": len(rows) + 1,
                  "manifest_digest": manifest_digest, "nonce": nonce,
                  "scientific_purpose": scientific_purpose,
                  "previous_hash": previous, "recorded_ns": time.time_ns()}
        record["event_hash"] = sha(canonical(record))
        record["signature"] = hmac.new(self._root_key, canonical(record).encode(), hashlib.sha256).hexdigest()
        with open(self._state_path, "a", encoding="utf-8", newline="\n") as f:
            f.write(canonical(record) + "\n")
            f.flush()
            os.fsync(f.fileno())
        self._write_anchor_unlocked(record["sequence"], record["event_hash"])
        if kind == "INIT_ISSUED":
            self._issuance[manifest_digest] = nonce
        elif kind == "INIT_CONSUMED":
            self._consumed.add(manifest_digest)
        elif kind == "POLICY_BOUND":
            self._purpose_manifests[scientific_purpose] = manifest_digest

    def _authority_records_unlocked(self):
        if not self._state_path or not os.path.exists(self._state_path):
            raise PolicyError("configured policy-authority state log is missing")
        try:
            with open(self._state_path, "rb") as f:
                data = f.read()
            if data and not data.endswith(b"\n"):
                raise PolicyError("policy-authority state log is truncated")
            return [json.loads(line) for line in data.decode("utf-8").splitlines() if line.strip()]
        except Exception as exc:
            if isinstance(exc, PolicyError):
                raise
            raise PolicyError("policy-authority state log unreadable") from exc

    def _load_issuance_log_unlocked(self):
        if not self._state_path or not os.path.exists(self._state_path) or not os.path.exists(self._anchor_path):
            raise PolicyError("policy-authority log or independently retained head anchor is missing")
        self._issuance = {}
        self._consumed = set()
        self._purpose_manifests = {}
        previous = "0" * 64
        records = self._authority_records_unlocked()
        for seq, record in enumerate(records, 1):
            signature = record.pop("signature", None)
            if not signature or not hmac.compare_digest(
                    signature, hmac.new(self._root_key, canonical(record).encode(), hashlib.sha256).hexdigest()):
                raise PolicyError("policy-authority state signature invalid")
            event_hash = record.pop("event_hash", None)
            if (event_hash != sha(canonical(record)) or record.get("sequence") != seq or
                    record.get("previous_hash") != previous):
                raise PolicyError("policy-authority state chain invalid")
            record["event_hash"] = event_hash
            record["signature"] = signature
            previous = event_hash
            digest, nonce = record["manifest_digest"], record["nonce"]
            purpose = record.get("scientific_purpose")
            if record["kind"] == "POLICY_BOUND":
                if not purpose or purpose in self._purpose_manifests or nonce != "":
                    raise PolicyError("scientific purpose already has a manifest lineage")
                self._purpose_manifests[purpose] = digest
            elif record["kind"] == "INIT_ISSUED":
                if self._purpose_manifests.get(purpose) != digest:
                    raise PolicyError("initialization references an unbound manifest lineage")
                if digest in self._issuance:
                    raise PolicyError("duplicate initialization authorization record")
                self._issuance[digest] = nonce
            elif (record["kind"] == "INIT_CONSUMED" and self._issuance.get(digest) == nonce
                  and digest not in self._consumed):
                self._consumed.add(digest)
            else:
                raise PolicyError("invalid policy-authority state transition")

        try:
            with open(self._anchor_path, "r", encoding="utf-8") as f:
                anchor = json.load(f)
        except Exception as exc:
            raise PolicyError("policy-authority head anchor unreadable") from exc
        if not isinstance(anchor, dict):
            raise PolicyError("policy-authority head anchor is invalid")
        anchor_sequence = anchor.get("sequence")
        anchor_hash = anchor.get("event_hash")
        anchor_signature = anchor.get("signature")
        if (not isinstance(anchor_sequence, int) or isinstance(anchor_sequence, bool) or
                not isinstance(anchor_hash, str) or not isinstance(anchor_signature, str)):
            raise PolicyError("policy-authority head anchor is invalid")
        expected_signature = self._anchor_signature(anchor_sequence, anchor_hash)
        if (anchor_sequence < 0 or
                not hmac.compare_digest(anchor_signature, expected_signature) or
                anchor_sequence > len(records)):
            raise PolicyError("policy-authority head anchor is invalid or ahead of its log")
        hash_at_anchor = records[anchor_sequence - 1]["event_hash"] if anchor_sequence else "0" * 64
        if hash_at_anchor != anchor_hash:
            raise PolicyError("policy-authority log differs from its pinned head anchor")
        # Recover a crash after the signed log append but before the sidecar replace.
        if len(records) > anchor_sequence:
            latest_hash = records[-1]["event_hash"] if records else "0" * 64
            self._write_anchor_unlocked(len(records), latest_hash)

    def initialize(self):
        """Explicit trusted bootstrap; issuance never silently recreates missing state."""
        if not self._state_path:
            raise PolicyError("durable policy-authority state path required")
        with _file_lock(self._state_path):
            if not os.path.exists(self._state_path) and not os.path.exists(self._anchor_path):
                self._initialize_log_unlocked()
                return "created"
            if (os.path.exists(self._state_path) and not os.path.exists(self._anchor_path) and
                    os.path.getsize(self._state_path) == 0):
                self._write_anchor_unlocked(0, "0" * 64)
            self._load_issuance_log_unlocked()
            if os.path.getsize(self._state_path) == 0:
                return "duplicate"
            raise PolicyError("policy authority already has an issuance history")

    def _verify_manifest_unlocked(self, manifest):
        expected = hmac.new(self._root_key, manifest.payload_json.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, manifest.signature):
            raise PolicyError("policy manifest signature invalid")
        payload = manifest.payload
        required = {"scientific_purpose", "purpose_key", "experiment_id", "registry_digest", "custodian_id",
                    "repository", "lock_ref", "app_id"}
        if set(payload) != required:
            raise PolicyError("policy manifest fields invalid")
        if self._canonical_purposes.get(payload["scientific_purpose"]) != payload["purpose_key"]:
            raise PolicyError("signed policy purpose key is not canonical")
        if self._purpose_manifests.get(payload["scientific_purpose"]) != manifest.digest:
            raise PolicyError("manifest is not the authorized lineage for this scientific purpose")
        return payload

    def issue(self, policy):
        if self._canonical_purposes.get(policy.get("scientific_purpose")) != policy.get("purpose_key"):
            raise PolicyError("purpose key is not canonical in the trusted policy registry")
        payload = canonical(policy)
        manifest_digest = sha(payload)
        if not self._state_path:
            raise PolicyError("durable policy-authority state path required")
        with _file_lock(self._state_path):
            self._load_issuance_log_unlocked()
            bound_digest = self._purpose_manifests.get(policy["scientific_purpose"])
            if bound_digest is not None and bound_digest != manifest_digest:
                raise PolicyError("scientific purpose already has a different manifest/custodian lineage")
            if bound_digest is None:
                self._append_authority_event_unlocked("POLICY_BOUND", manifest_digest, "", policy["scientific_purpose"])
                self._load_issuance_log_unlocked()
            sig = hmac.new(self._root_key, payload.encode(), hashlib.sha256).hexdigest()
            return SignedPolicy(payload, sig)

    def verify(self, manifest):
        if not self._state_path:
            raise PolicyError("durable policy-authority state path required")
        with _file_lock(self._state_path):
            self._load_issuance_log_unlocked()
            return self._verify_manifest_unlocked(manifest)

    def authorize_initialization(self, manifest):
        if not self._state_path:
            raise PolicyError("durable policy-authority state path required")
        with _file_lock(self._state_path):
            self._load_issuance_log_unlocked()
            self._verify_manifest_unlocked(manifest)
            if manifest.digest in self._issuance or manifest.digest in self._consumed:
                raise PolicyError("genesis initialization authorization already issued/consumed")
            nonce = secrets.token_hex(24)
            self._append_authority_event_unlocked("INIT_ISSUED", manifest.digest, nonce,
                                                  manifest.payload["scientific_purpose"])
            self._load_issuance_log_unlocked()
            authorization = {"action": "initialize-custodian-genesis", "manifest_digest": manifest.digest,
                             "custodian_id": manifest.payload["custodian_id"], "nonce": nonce}
            encoded = canonical(authorization)
            signature = hmac.new(self._root_key, encoded.encode(), hashlib.sha256).hexdigest()
            return encoded, signature

    def verify_initialization(self, manifest, authorization):
        if not self._state_path:
            raise PolicyError("durable policy-authority state path required")
        with _file_lock(self._state_path):
            self._load_issuance_log_unlocked()
            self._verify_manifest_unlocked(manifest)
            self._check_initialization_unlocked(manifest, authorization)

    def _check_initialization_unlocked(self, manifest, authorization):
        encoded, signature = authorization
        expected_sig = hmac.new(self._root_key, encoded.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, signature):
            raise PolicyError("genesis initialization authorization invalid")
        expected_payload = {"action": "initialize-custodian-genesis", "manifest_digest": manifest.digest,
                            "custodian_id": manifest.payload["custodian_id"],
                            "nonce": self._issuance.get(manifest.digest)}
        if json.loads(encoded) != expected_payload or expected_payload["nonce"] is None:
            raise PolicyError("genesis authorization does not match pinned manifest")
        if manifest.digest in self._consumed:
            raise PolicyError("genesis authorization already consumed")

    def consume_initialization(self, manifest, authorization):
        if not self._state_path:
            raise PolicyError("durable policy-authority state path required")
        with _file_lock(self._state_path):
            self._load_issuance_log_unlocked()
            self._verify_manifest_unlocked(manifest)
            # Consumption after a durable matching genesis is idempotent on recovery.
            encoded, signature = authorization
            expected_sig = hmac.new(self._root_key, encoded.encode(), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expected_sig, signature):
                raise PolicyError("genesis initialization authorization invalid")
            payload = json.loads(encoded)
            if payload != {"action": "initialize-custodian-genesis", "manifest_digest": manifest.digest,
                           "custodian_id": manifest.payload["custodian_id"],
                           "nonce": self._issuance.get(manifest.digest)}:
                raise PolicyError("genesis authorization does not match pinned manifest")
            if manifest.digest not in self._consumed:
                self._append_authority_event_unlocked("INIT_CONSUMED", manifest.digest, payload["nonce"],
                                                      manifest.payload["scientific_purpose"])
                self._load_issuance_log_unlocked()


class ExternalCheckpoint:
    """Append-only JSONL checkpoint model outside both SQLite databases.

    The file and HMAC key are still local test fixtures. Production needs a separately
    operated durable service and asymmetric signing keys.
    """
    def __setattr__(self, name, value):
        if getattr(self, "_sealed", False):
            raise AttributeError("ExternalCheckpoint identity and key are immutable after construction")
        object.__setattr__(self, name, value)

    def __init__(self, path, custodian_id, manifest_digest, signing_key, pre_lock_hook=None):
        object.__setattr__(self, "_sealed", False)
        self.path = path
        self.custodian_id = custodian_id
        self.manifest_digest = manifest_digest
        self._key = signing_key
        self._pre_lock_hook = pre_lock_hook
        object.__setattr__(self, "_sealed", True)

    @contextmanager
    def _serialized(self):
        """Cross-process lock around external checkpoint compare-and-append."""
        with _file_lock(self.path):
            yield

    def _sign(self, record):
        return hmac.new(self._key, canonical(record).encode(), hashlib.sha256).hexdigest()

    def initialize(self, authority, manifest, authorization):
        authority.verify(manifest)
        authority.verify_initialization(manifest, authorization)
        if (manifest.payload["custodian_id"], manifest.digest) != (self.custodian_id, self.manifest_digest):
            raise PolicyError("custodian identity or manifest digest mismatch")
        genesis = {"kind": "GENESIS", "sequence": 0, "custodian_id": self.custodian_id,
                   "manifest_digest": self.manifest_digest, "previous_hash": "0" * 64,
                   "checkpoint_hash": sha(f"GENESIS|{self.custodian_id}|{self.manifest_digest}"),
                   "recorded_ns": time.time_ns()}
        genesis["signature"] = self._sign(genesis)
        with self._serialized():
            if os.path.exists(self.path):
                records = self._records_unlocked()
                if len(records) == 1 and records[0] == genesis:
                    return "duplicate"
                if (len(records) == 1 and records[0].get("kind") == "GENESIS" and
                        records[0].get("custodian_id") == self.custodian_id and
                        records[0].get("manifest_digest") == self.manifest_digest):
                    # recorded_ns makes otherwise matching genesis bytes differ.
                    return "duplicate"
                raise PolicyError("external checkpoint contains a mismatched or advanced genesis")
            with open(self.path, "x", encoding="utf-8", newline="\n") as f:
                f.write(canonical(genesis) + "\n")
                f.flush()
                os.fsync(f.fileno())
        return "created"

    def _records_unlocked(self):
        if not os.path.exists(self.path):
            raise IntegrityError("trusted genesis checkpoint missing; explicit initialization required")
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                records = [json.loads(line) for line in f if line.strip()]
        except Exception as exc:
            raise IntegrityError("external checkpoint unreadable") from exc
        if not records:
            raise IntegrityError("empty external checkpoint is not a valid genesis")
        prev = "0" * 64
        for index, record in enumerate(records):
            signature = record.pop("signature", None)
            expected_signature = self._sign(record)
            record["signature"] = signature
            if not signature or not hmac.compare_digest(signature, expected_signature):
                raise IntegrityError("external checkpoint signature invalid")
            if index == 0:
                expected_hash = sha(f"GENESIS|{self.custodian_id}|{self.manifest_digest}")
                if (record.get("kind"), record.get("sequence"), record.get("custodian_id"),
                    record.get("manifest_digest"), record.get("checkpoint_hash")) != (
                    "GENESIS", 0, self.custodian_id, self.manifest_digest, expected_hash):
                    raise IntegrityError("external checkpoint genesis identity mismatch")
            else:
                body = {k: v for k, v in record.items() if k not in ("signature", "checkpoint_hash")}
                expected_hash = sha(canonical(body))
                if (record.get("kind") != "HEAD" or record.get("custodian_id") != self.custodian_id or
                    record.get("sequence") != index or record.get("previous_hash") != prev or
                    record.get("checkpoint_hash") != expected_hash or record.get("manifest_digest") != self.manifest_digest):
                    raise IntegrityError("external checkpoint sequence/hash chain invalid")
            prev = record["checkpoint_hash"]
        return records

    def records(self):
        with self._serialized():
            return self._records_unlocked()

    def _head_unlocked(self):
        records = self._records_unlocked()
        return records[-1]["sequence"], records[-1]["checkpoint_hash"]

    def head(self):
        with self._serialized():
            return self._head_unlocked()

    def publish(self, sequence, event_hash, previous_hash):
        if self._pre_lock_hook is not None:
            self._pre_lock_hook(sequence, event_hash, previous_hash)
        with self._serialized():
            current_sequence, current_hash = self._head_unlocked()
            if sequence != current_sequence + 1 or previous_hash != current_hash:
                raise IntegrityError("external checkpoint compare-and-append failed")
            body = {"kind": "HEAD", "sequence": sequence, "custodian_id": self.custodian_id,
                    "manifest_digest": self.manifest_digest, "previous_hash": previous_hash,
                    "event_hash": event_hash, "recorded_ns": time.time_ns()}
            body["checkpoint_hash"] = sha(canonical(body))
            body["signature"] = self._sign(body)
            with open(self.path, "a", encoding="utf-8", newline="\n") as f:
                f.write(canonical(body) + "\n")
                f.flush()
                os.fsync(f.fileno())


class ReceiptSigner:
    """Separate test credential for adapter/worker/reconciler roles."""
    def __init__(self, role, key):
        self.role = role
        self._key = key

    def sign(self, payload):
        body = {"role": self.role, "payload": payload}
        return {**body, "signature": hmac.new(self._key, canonical(body).encode(), hashlib.sha256).hexdigest()}


class ReceiptVerifier:
    def __init__(self, role_keys):
        self._role_keys = dict(role_keys)

    def verify(self, receipt):
        role = receipt.get("role")
        if role not in self._role_keys:
            raise IntegrityError("receipt signer role is not authorized")
        body = {"role": role, "payload": receipt.get("payload")}
        expected = hmac.new(self._role_keys[role], canonical(body).encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(receipt.get("signature", ""), expected):
            raise IntegrityError("receipt signature invalid")
        return role, receipt["payload"]
