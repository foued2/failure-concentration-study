"""Adapter contract and fake GitHub implementation used only by local tests."""
from trust import canonical, sha
from witness import normalized_request


class FakeGitHub:
    """Models GitHub ref calls and complete event history; not a GitHub integration."""
    def __init__(self, policy, app_signer):
        self.policy = dict(policy)
        self.app_signer = app_signer
        self.ref = None
        self.events = []
        self.app_allowed = True

    def _receipt(self, request, outcome, observed_sha=None):
        normalized = normalized_request(request)
        payload = {"purpose_key": self.policy["purpose_key"],
                   "experiment_id": self.policy["experiment_id"],
                   "request_hash": sha(canonical(normalized)),
                   "repository": self.policy["repository"], "lock_ref": self.policy["lock_ref"],
                   "app_id": self.policy["app_id"], "outcome": outcome,
                   "observed_sha": observed_sha, "event_count": len(self.events)}
        return self.app_signer.sign(payload)

    def apply_intent(self, request):
        if not self.app_allowed:
            raise PermissionError("modeled ruleset rejects the App")
        request = normalized_request(request)
        base, target = request["base_commit"], request["target_commit"]
        if self.ref is None:
            self.ref = base
            self.events.append(("create", None, base, "app"))
        if self.ref == base:
            self.ref = target
            self.events.append(("update", base, target, "app"))
        elif self.ref != target:
            raise RuntimeError("ref is neither expected base nor intended target")
        return self._receipt(request, "GITHUB_APPLIED", self.ref)

    def delete(self, actor="admin"):
        before, self.ref = self.ref, None
        self.events.append(("delete", before, None, actor))

    def recreate(self, sha_value, actor="admin"):
        before, self.ref = self.ref, sha_value
        self.events.append(("create", before, sha_value, actor))

    def force_update(self, sha_value, actor="admin"):
        before, self.ref = self.ref, sha_value
        self.events.append(("force_update", before, sha_value, actor))

    def read_ref(self):
        return self.ref

    def attest_applied(self, request):
        return self._receipt(request, "GITHUB_APPLIED", self.ref)


class Reconciler:
    """Worker that validates observed adapter state and submits signed evidence."""
    def __init__(self, witness, request, adapter, worker_signer, reconciler_signer):
        self.witness = witness
        self.request = normalized_request(request)
        self.adapter = adapter
        self.worker_signer = worker_signer
        self.reconciler_signer = reconciler_signer

    def _worker_receipt(self):
        return self.worker_signer.sign(self.adapter._receipt(
            self.request, "PENDING_RECONCILIATION", self.adapter.read_ref())["payload"])

    def _breach_receipt(self):
        payload = self.adapter._receipt(self.request, "BREACH", self.adapter.read_ref())["payload"]
        return self.reconciler_signer.sign(payload)

    def reconcile(self):
        state = self.witness.state()
        if state not in ("INTENT_RECORDED", "PENDING_RECONCILIATION", "GITHUB_APPLIED", "BREACH"):
            raise RuntimeError("cannot reconcile an unclaimed purpose")
        if state == "BREACH":
            return state
        base, target = self.request["base_commit"], self.request["target_commit"]
        expected = [("create", None, base, "app"), ("update", base, target, "app")]
        if self.adapter.read_ref() == target and self.adapter.events == expected:
            if state == "GITHUB_APPLIED":
                return state
            receipt = self.adapter.attest_applied(self.request)
            self.witness.record_adapter_evidence(self.request, receipt)
            return self.witness.state()
        if self.adapter.read_ref() == base and self.adapter.events == expected[:1]:
            self.witness.record_adapter_evidence(self.request, self._worker_receipt())
            return self.witness.state()
        if self.adapter.read_ref() is None and not self.adapter.events:
            self.witness.record_adapter_evidence(self.request, self._worker_receipt())
            return self.witness.state()
        self.witness.record_adapter_evidence(self.request, self._breach_receipt())
        return self.witness.state()

    def apply_once(self):
        state = self.witness.state()
        if state == "UNCLAIMED":
            self.witness.intent(self.request)
        elif state == "PENDING_RECONCILIATION":
            return self.reconcile()
        elif state in ("GITHUB_APPLIED", "BREACH"):
            return state
        try:
            receipt = self.adapter.apply_intent(self.request)
        except Exception:
            self.witness.record_adapter_evidence(self.request, self._worker_receipt())
            return self.reconcile()
        self.witness.record_adapter_evidence(self.request, receipt)
        return self.witness.state()


class WebhookInbox:
    """Delivery simulator: deduplicates IDs but records arrival, never event order."""
    def __init__(self):
        self.seen = set()
        self.arrivals = []

    def deliver(self, delivery_id, event):
        if delivery_id in self.seen:
            return "duplicate"
        self.seen.add(delivery_id)
        self.arrivals.append((delivery_id, event))
        return "accepted"
