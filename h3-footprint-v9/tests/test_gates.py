"""The execution gate must fail closed.

Every test here builds a *synthetic* state tree, so a passing case proves the
gate is capable of passing when the evidence really is complete. The last test
runs the gate against this repository and asserts that it refuses.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import gates  # noqa: E402
import backend  # noqa: E402

V9 = HERE.parent
GATE_IDS = (
    "sandbox_agent_acceptance",
    "sandbox_rendezvous_ordering",
    "sandbox_isolation_report",
    "memory_and_process_caps",
    "verdict_and_support_cells",
)


def blocker_ids(report: dict) -> set[str]:
    return {item["id"] for item in report["blockers"]}


class GateTree:
    """A repository-shaped tree whose one failing property a test can set."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.evidence = {
            "evidence/preflight.json": {
                "ok": True,
                "evaluation_attempted": False,
                "preflight": {"attestation": {"verified": True}, "jobs_published": 0},
            },
            "evidence/rendezvous.json": {"ordering_ok": True},
            "evidence/isolation.json": {"ok": True, "blocked": []},
            "evidence/verdict.json": {"ok": True},
        }
        self.caps_source = "# resource caps\n"
        self.rules_source = "# verdict and support-cell rules\n"
        self.statuses = {gate_id: "PASS" for gate_id in GATE_IDS}
        self.authorization: dict | None = {
            "v9": 1,
            "evaluation_authorized": True,
            "operator": "operator",
            "authorized_at": "2026-10-28T00:00:00Z",
            "scope": "unit test",
        }
        self.write()

    # -- writers -----------------------------------------------------------
    def write_evidence(self) -> None:
        for relative, payload in self.evidence.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        (self.root / "winjob.py").write_text(self.caps_source, encoding="utf-8")
        (self.root / "verdict_rules.py").write_text(self.rules_source, encoding="utf-8")

    def write_policy(self, pins: dict | None = None) -> None:
        policy = {
            "v9": 1,
            "required_gates": [
                {
                    "id": "sandbox_agent_acceptance",
                    "evidence": ["evidence/preflight.json"],
                    "require_json": {
                        "ok": True,
                        "evaluation_attempted": False,
                        "preflight.attestation.verified": True,
                        "preflight.jobs_published": 0,
                    },
                },
                {
                    "id": "sandbox_rendezvous_ordering",
                    "evidence": ["evidence/rendezvous.json"],
                    "require_json": {"ordering_ok": True},
                },
                {
                    "id": "sandbox_isolation_report",
                    "evidence": ["evidence/isolation.json"],
                    "require_json": {"ok": True},
                },
                {"id": "memory_and_process_caps", "evidence": ["winjob.py"]},
                {
                    "id": "verdict_and_support_cells",
                    "evidence": ["evidence/verdict.json"],
                    "require_json": {"ok": True},
                },
            ],
            "evidence_pins": pins if pins is not None else {
                relative: gates.canonical_sha256(self.root / relative)
                for relative in ("evidence/preflight.json",
                                 "evidence/rendezvous.json",
                                 "evidence/isolation.json",
                                 "evidence/verdict.json", "winjob.py")
            },
            "verdict_rules": {
                "path": "verdict_rules.py",
                "sha256": gates.canonical_sha256(self.root / "verdict_rules.py"),
            },
            "authorization": {"path": "EVALUATION_AUTHORIZATION.json"},
        }
        (self.root / "EXECUTION_PREREQUISITES.json").write_text(
            json.dumps(policy, indent=2) + "\n", encoding="utf-8")

    def write_status(self) -> None:
        status = {
            "version": 9,
            "gates": [{"id": gate_id, "status": status}
                      for gate_id, status in self.statuses.items()],
        }
        (self.root / "STATUS.json").write_text(
            json.dumps(status, indent=2) + "\n", encoding="utf-8")

    def write_authorization(self) -> None:
        path = self.root / "EVALUATION_AUTHORIZATION.json"
        if self.authorization is None:
            if path.exists():
                path.unlink()
            return
        grant = dict(self.authorization)
        grant.setdefault("policy_sha256",
                         gates.canonical_sha256(self.root / "EXECUTION_PREREQUISITES.json"))
        grant.setdefault("status_sha256",
                         gates.canonical_sha256(self.root / "STATUS.json"))
        path.write_text(json.dumps(grant, indent=2) + "\n", encoding="utf-8")

    def write(self) -> None:
        self.write_evidence()
        self.write_policy()
        self.write_status()
        self.write_authorization()

    def check(self) -> dict:
        return gates.check(root=self.root)


class GatePolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tree = GateTree(Path(self._tmp.name))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_a_fully_satisfied_tree_is_authorized(self):
        report = self.tree.check()
        self.assertTrue(report["ok"], report["blockers"])
        self.assertEqual(report["blockers"], [])
        self.assertTrue(report["authorization"]["ok"])
        self.assertTrue(report["verdict_rules"]["ok"])

    def test_require_authorized_returns_the_report_when_clean(self):
        self.assertTrue(gates.require_authorized(root=self.tree.root)["ok"])

    def test_require_authorized_raises_the_boundary_error_family(self):
        self.assertTrue(issubclass(gates.ExecutionNotAuthorized,
                                   backend.BoundaryNotEstablished))

    # -- one failing gate at a time ---------------------------------------
    def test_failed_gate_blocks(self):
        self.tree.statuses["sandbox_rendezvous_ordering"] = "FAIL"
        self.tree.write()
        self.assertIn("gate_not_passing:sandbox_rendezvous_ordering",
                      blocker_ids(self.tree.check()))

    def test_not_run_gate_blocks(self):
        self.tree.statuses["sandbox_isolation_report"] = "NOT_RUN"
        self.tree.write()
        self.assertIn("gate_not_passing:sandbox_isolation_report",
                      blocker_ids(self.tree.check()))

    def test_not_implemented_gate_blocks(self):
        self.tree.statuses["verdict_and_support_cells"] = "NOT_IMPLEMENTED"
        self.tree.write()
        self.assertIn("gate_not_passing:verdict_and_support_cells",
                      blocker_ids(self.tree.check()))

    def test_partial_gate_blocks(self):
        self.tree.statuses["memory_and_process_caps"] = "PARTIAL"
        self.tree.write()
        self.assertIn("gate_not_passing:memory_and_process_caps",
                      blocker_ids(self.tree.check()))

    def test_missing_gate_blocks(self):
        del self.tree.statuses["sandbox_isolation_report"]
        self.tree.write()
        self.assertIn("gate_missing:sandbox_isolation_report",
                      blocker_ids(self.tree.check()))

    # -- evidence ----------------------------------------------------------
    def test_missing_evidence_blocks(self):
        (self.tree.root / "evidence" / "rendezvous.json").unlink()
        self.assertIn("evidence_missing:evidence/rendezvous.json",
                      blocker_ids(self.tree.check()))

    def test_tampered_evidence_blocks(self):
        path = self.tree.root / "evidence" / "preflight.json"
        altered = json.loads(path.read_text(encoding="utf-8"))
        altered["preflight"]["jobs_published"] = 3
        path.write_text(json.dumps(altered), encoding="utf-8")
        self.assertIn("evidence_tampered:evidence/preflight.json",
                      blocker_ids(self.tree.check()))

    def test_unpinned_evidence_blocks(self):
        pins = {
            "evidence/rendezvous.json":
                gates.canonical_sha256(self.tree.root / "evidence/rendezvous.json"),
            "winjob.py": gates.canonical_sha256(self.tree.root / "winjob.py"),
        }
        self.tree.write_policy(pins=pins)
        self.tree.write_authorization()
        self.assertIn("evidence_unpinned:evidence/preflight.json",
                      blocker_ids(self.tree.check()))

    def test_pinned_but_unreferenced_file_is_a_commitment(self):
        (self.tree.root / "evidence" / "extra.json").write_text('{"ok": true}', encoding="utf-8")
        pins = {
            relative: gates.canonical_sha256(self.tree.root / relative)
            for relative in ("evidence/preflight.json", "evidence/rendezvous.json",
                             "evidence/isolation.json", "evidence/verdict.json",
                             "winjob.py")
        }
        pins["evidence/extra.json"] = "0" * 64
        self.tree.write_policy(pins=pins)
        self.tree.write_authorization()
        self.assertIn("pinned_file_tampered:evidence/extra.json",
                      blocker_ids(self.tree.check()))

    def test_forged_status_cannot_override_the_evidence(self):
        """The gate PASS is not enough: the pinned report must agree."""
        self.tree.evidence["evidence/rendezvous.json"] = {"ordering_ok": False}
        self.tree.write()  # statuses PASS, pins refreshed to the failing report
        ids = blocker_ids(self.tree.check())
        self.assertIn("evidence_assertion_failed:sandbox_rendezvous_ordering:ordering_ok", ids)

    # -- verdict rules -----------------------------------------------------
    def test_missing_verdict_rules_block(self):
        (self.tree.root / "verdict_rules.py").unlink()
        self.assertIn("verdict_rules_missing", blocker_ids(self.tree.check()))

    def test_tampered_verdict_rules_block(self):
        (self.tree.root / "verdict_rules.py").write_text("# rewritten\n", encoding="utf-8")
        self.assertIn("verdict_rules_tampered", blocker_ids(self.tree.check()))

    # -- separate authorization -------------------------------------------
    def test_absent_authorization_blocks(self):
        self.tree.authorization = None
        self.tree.write()
        self.assertIn("authorization_missing", blocker_ids(self.tree.check()))

    def test_authorization_must_be_explicit(self):
        self.tree.authorization = {
            "v9": 1, "evaluation_authorized": "yes",
            "operator": "operator", "authorized_at": "2026-10-28T00:00:00Z",
            "scope": "unit test",
        }
        self.tree.write()
        self.assertIn("authorization_invalid", blocker_ids(self.tree.check()))

    def test_authorization_is_bound_to_the_policy(self):
        self.tree.authorization = {
            "v9": 1, "evaluation_authorized": True, "policy_sha256": "0" * 64,
            "operator": "operator", "authorized_at": "2026-10-28T00:00:00Z",
            "scope": "unit test",
        }
        self.tree.write()
        report = self.tree.check()
        self.assertIn("authorization_invalid", blocker_ids(report))
        self.assertTrue(any("policy_sha256" in b["detail"] for b in report["blockers"]))

    def test_authorization_is_bound_to_the_status_ledger(self):
        self.tree.write()
        status = json.loads((self.tree.root / "STATUS.json").read_text(encoding="utf-8"))
        status["gates"][0]["detail"] = "edited after authorization"
        (self.tree.root / "STATUS.json").write_text(json.dumps(status), encoding="utf-8")
        report = self.tree.check()
        self.assertIn("authorization_invalid", blocker_ids(report))
        self.assertTrue(any("status_sha256" in b["detail"] for b in report["blockers"]))


class RealRepositoryGateTests(unittest.TestCase):
    """This revision cannot authorize anything, and says why."""

    def test_this_repository_refuses_authorized_evaluation(self):
        report = gates.check(root=V9)
        self.assertFalse(report["ok"])
        ids = blocker_ids(report)
        for expected in (
            "gate_not_passing:sandbox_rendezvous_ordering",
            "gate_not_passing:sandbox_isolation_report",
            "gate_not_passing:memory_and_process_caps",
            "gate_not_passing:verdict_and_support_cells",
            "verdict_rules_missing",
            "authorization_missing",
        ):
            self.assertIn(expected, ids)

    def test_no_authorization_file_is_committed(self):
        self.assertFalse((V9 / "EVALUATION_AUTHORIZATION.json").exists())

    def test_the_policy_pins_the_failed_rendezvous_report(self):
        policy = json.loads((V9 / "EXECUTION_PREREQUISITES.json").read_text(encoding="utf-8"))
        relative = "evidence/rendezvous-sandbox-2026-10-28.json"
        self.assertIn(relative, policy["evidence_pins"])
        self.assertEqual(policy["evidence_pins"][relative],
                         gates.canonical_sha256(V9 / relative))


if __name__ == "__main__":
    unittest.main()
