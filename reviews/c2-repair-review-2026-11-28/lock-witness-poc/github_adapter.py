"""GitHub adapter boundary plus explicit fake used only by local tests."""


class FakeGitHub:
    """Models a ref and a complete event journal; it is not GitHub integration."""
    def __init__(self, ref=None):
        self.ref = ref
        self.events = []
        self.app_allowed = True

    def apply_intent(self, base, target):
        if not self.app_allowed:
            raise PermissionError("modeled ruleset rejects the App")
        if self.ref is None:
            self.ref = base
            self.events.append(("create", None, base, "app"))
        if self.ref == base:
            self.ref = target
            self.events.append(("update", base, target, "app"))
            return
        if self.ref == target:
            return  # idempotent exact retry after ambiguous response
        raise RuntimeError("ref is neither expected base nor intended target")

    def delete(self, actor="admin"):
        before, self.ref = self.ref, None
        self.events.append(("delete", before, None, actor))

    def recreate(self, sha, actor="admin"):
        before, self.ref = self.ref, sha
        self.events.append(("create", before, sha, actor))

    def force_update(self, sha, actor="admin"):
        before, self.ref = self.ref, sha
        self.events.append(("force_update", before, sha, actor))

    def read_ref(self):
        return self.ref


class Reconciler:
    """Reconcile against adapter ref and its event history; journal completeness is assumed."""
    def __init__(self, witness, request, adapter):
        self.witness = witness
        self.request = request
        self.adapter = adapter

    def reconcile(self):
        state = self.witness.state()
        if state not in ("INTENT_RECORDED", "PENDING_RECONCILIATION", "GITHUB_APPLIED", "BREACH"):
            raise RuntimeError("cannot reconcile an unclaimed purpose")
        if state == "BREACH":
            return state
        base, target = self.request["base_commit"], self.request["target_commit"]
        events = self.adapter.events
        expected = [("create", None, base, "app"), ("update", base, target, "app")]
        if self.adapter.read_ref() == target and events == expected:
            if state != "GITHUB_APPLIED":
                self.witness.transition(self.request, "GITHUB_APPLIED")
            return "GITHUB_APPLIED"
        # Exact partial prefix is retryable; every deletion/recreation/force or unknown
        # event is a breach in this adapter model.
        if self.adapter.read_ref() == base and events == expected[:1]:
            if state == "INTENT_RECORDED":
                self.witness.transition(self.request, "PENDING_RECONCILIATION")
            return "PENDING_RECONCILIATION"
        if self.adapter.read_ref() is None and not events:
            if state == "INTENT_RECORDED":
                self.witness.transition(self.request, "PENDING_RECONCILIATION")
            return "PENDING_RECONCILIATION"  # no GitHub mutation; exact intent can resume
        self.witness.transition(self.request, "BREACH")
        return "BREACH"

    def apply_once(self, lose_response=False):
        state = self.witness.state()
        if state == "UNCLAIMED":
            self.witness.intent(self.request)
        elif state in ("GITHUB_APPLIED", "BREACH"):
            return state
        try:
            self.adapter.apply_intent(self.request["base_commit"], self.request["target_commit"])
        except Exception:
            if self.witness.state() == "INTENT_RECORDED":
                self.witness.transition(self.request, "PENDING_RECONCILIATION")
            return self.reconcile()
        if lose_response:
            self.witness.transition(self.request, "PENDING_RECONCILIATION")
            return self.reconcile()
        return self.reconcile()


class WebhookInbox:
    """Delivery simulator; webhook order is retained only as arrival history."""
    def __init__(self):
        self.seen = set()
        self.arrivals = []

    def deliver(self, delivery_id, event):
        if delivery_id in self.seen:
            return "duplicate"
        self.seen.add(delivery_id)
        self.arrivals.append((delivery_id, event))
        return "accepted"
