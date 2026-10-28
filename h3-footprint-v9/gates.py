"""Fail-closed prerequisite gate for authorized candidate evaluation.

A verified Sandbox handshake proves one thing only: an agent running as
``WDAGUtilityAccount`` echoed a host nonce from inside the guest. It does not
prove that the job broker is ordered, that the isolation probes passed, that
the resource caps are enforced, or that the verdict rules exist. Treating the
handshake as sufficient was the control gap in revision 6.

This module is the single decision point, and it fails closed. For authorized
evaluation to run, all of the following must hold:

  1. every prerequisite gate recorded in ``STATUS.json`` is ``PASS``;
  2. every evidence file named for those gates is listed in the committed
     policy with a matching SHA-256 (hashes are canonicalised to LF line
     endings, exactly like ``MANIFEST.json``, so a Windows checkout does not
     change them);
  3. the hash-pinned evidence still *says* what the gate claims -- a gate
     flipped to PASS cannot override a rendezvous report that records
     ``ordering_ok: false``;
  4. the verdict/support-cell rules exist and match their pinned hash;
  5. a separate authorization file exists and pins both the policy and the
     status ledger, so an old authorization cannot be replayed against a new
     state.

No authorization file is committed in this revision. Evaluation stays blocked,
and so does every caller that tries to skip this gate.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from backend import BoundaryNotEstablished

HERE = Path(__file__).resolve().parent

POLICY_FILENAME = "EXECUTION_PREREQUISITES.json"
STATUS_FILENAME = "STATUS.json"
AUTHORIZATION_FILENAME = "EVALUATION_AUTHORIZATION.json"
REQUIRED_STATUS = "PASS"
_HEX64 = re.compile(r"[0-9a-f]{64}")


class ExecutionNotAuthorized(BoundaryNotEstablished):
    """Authorized evaluation was requested before its prerequisites passed."""


def canonical_sha256(path: Path | str) -> str:
    """Hash the way ``MANIFEST.json`` does: CRLF and LF are the same content."""
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dig(record: Any, dotted: str) -> Any:
    current = record
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted)
        current = current[part]
    return current


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check(*, root: Path | str | None = None,
          policy_path: Path | str | None = None,
          status_path: Path | str | None = None,
          authorization_path: Path | str | None = None) -> dict[str, Any]:
    """Return the gate verdict and every blocker. Never raises on bad state."""
    base = Path(root) if root is not None else HERE
    policy_path = Path(policy_path) if policy_path is not None else base / POLICY_FILENAME
    status_path = Path(status_path) if status_path is not None else base / STATUS_FILENAME
    authorization_path = (Path(authorization_path) if authorization_path is not None
                          else base / AUTHORIZATION_FILENAME)

    blockers: list[dict[str, str]] = []

    def block(identifier: str, detail: str) -> None:
        blockers.append({"id": identifier, "detail": detail})

    # -- policy -------------------------------------------------------------
    policy: dict[str, Any] | None = None
    if not policy_path.is_file():
        block("policy_missing", f"{policy_path.name} does not exist")
    else:
        try:
            loaded = _read_json(policy_path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            block("policy_invalid", f"cannot read {policy_path.name}: {type(exc).__name__}")
        else:
            if isinstance(loaded, dict):
                policy = loaded
            else:
                block("policy_invalid", f"{policy_path.name} is not a JSON object")

    # -- status ledger ------------------------------------------------------
    status: dict[str, Any] | None = None
    gates_by_id: dict[str, dict[str, Any]] = {}
    if not status_path.is_file():
        block("status_missing", f"{status_path.name} does not exist")
    else:
        try:
            loaded = _read_json(status_path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            block("status_invalid", f"cannot read {status_path.name}: {type(exc).__name__}")
        else:
            if not isinstance(loaded, dict):
                block("status_invalid", f"{status_path.name} is not a JSON object")
            else:
                status = loaded
                ledger = loaded.get("gates")
                if not isinstance(ledger, list) or not ledger:
                    block("status_invalid", f"{status_path.name} has no gates ledger")
                else:
                    for entry in ledger:
                        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                            gates_by_id[entry["id"]] = entry

    policy_sha = (canonical_sha256(policy_path) if policy_path.is_file() else None)
    status_sha = (canonical_sha256(status_path) if status_path.is_file() else None)

    pins: dict[str, str] = {}
    checked_gates: list[dict[str, Any]] = []
    covered_evidence: set[str] = set()

    if policy is not None:
        raw_pins = policy.get("evidence_pins")
        if not isinstance(raw_pins, dict):
            block("policy_invalid", "evidence_pins must be an object")
        else:
            pins = {k: v for k, v in raw_pins.items() if isinstance(k, str)}

        required = policy.get("required_gates")
        if not isinstance(required, list) or not required:
            block("policy_invalid", "required_gates must be a non-empty list")
            required = []

        for entry in required:
            if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
                block("policy_invalid", f"malformed required_gates entry: {entry!r}")
                continue
            gate_id = entry["id"]
            gate = gates_by_id.get(gate_id)
            record: dict[str, Any] = {
                "id": gate_id,
                "status": gate.get("status") if gate else None,
                "evidence_verified": [],
                "assertions_ok": None,
            }
            checked_gates.append(record)

            if gate is None:
                block(f"gate_missing:{gate_id}",
                      f"{gate_id} is not recorded in {status_path.name}")
                continue
            if gate.get("status") != REQUIRED_STATUS:
                block(f"gate_not_passing:{gate_id}",
                      f"{gate_id} is {gate.get('status')!r}; authorized evaluation "
                      f"requires {REQUIRED_STATUS}")

            evidence = entry.get("evidence") or []
            if not isinstance(evidence, list) or not all(isinstance(p, str) for p in evidence):
                block(f"policy_invalid:{gate_id}", "evidence must be a list of paths")
                evidence = []

            if gate.get("status") == REQUIRED_STATUS and not evidence:
                block(f"gate_without_pinned_evidence:{gate_id}",
                      f"{gate_id} is PASS but the policy names no hash-pinned evidence")

            verified: list[str] = []
            for relative in evidence:
                covered_evidence.add(relative)
                candidate = base / relative
                if not candidate.is_file():
                    block(f"evidence_missing:{relative}", f"{relative} does not exist")
                    continue
                if relative not in pins:
                    block(f"evidence_unpinned:{relative}",
                          f"{relative} is not pinned in {policy_path.name}")
                    continue
                actual = canonical_sha256(candidate)
                if pins[relative] != actual:
                    block(f"evidence_tampered:{relative}",
                          f"{relative} does not match its pinned SHA-256")
                    continue
                verified.append(relative)
            record["evidence_verified"] = verified

            assertions = entry.get("require_json") or {}
            if assertions and not isinstance(assertions, dict):
                block(f"policy_invalid:{gate_id}", "require_json must be an object")
            elif assertions and verified:
                try:
                    document = _read_json(base / verified[0])
                except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                    block(f"evidence_unreadable:{verified[0]}", type(exc).__name__)
                    document = None
                if document is not None:
                    failed = False
                    for dotted, expected in assertions.items():
                        try:
                            actual = _dig(document, dotted)
                        except KeyError:
                            block(f"evidence_assertion_missing:{gate_id}:{dotted}",
                                  f"{verified[0]} has no {dotted!r}")
                            failed = True
                            continue
                        if actual != expected:
                            block(f"evidence_assertion_failed:{gate_id}:{dotted}",
                                  f"{verified[0]} records {dotted}={actual!r}, "
                                  f"gate requires {expected!r}")
                            failed = True
                    record["assertions_ok"] = not failed

        # Pins are a commitment: a pinned file that is missing or changed is a
        # blocker even when no required gate happens to reference it.
        for relative, expected in sorted(pins.items()):
            if relative in covered_evidence:
                continue
            candidate = base / relative
            if not candidate.is_file():
                block(f"pinned_file_missing:{relative}", f"{relative} does not exist")
            elif canonical_sha256(candidate) != expected:
                block(f"pinned_file_tampered:{relative}",
                      f"{relative} does not match its pinned SHA-256")

    # -- verdict rules ------------------------------------------------------
    verdict_report: dict[str, Any] = {"path": None, "sha256": None, "ok": False}
    if policy is not None:
        rules = policy.get("verdict_rules")
        if not isinstance(rules, dict) or not _nonempty(rules.get("path")):
            block("verdict_rules_unpinned",
                  "the policy does not name a verdict/support-cell rules file")
        else:
            verdict_report["path"] = rules["path"]
            rules_path = base / rules["path"]
            expected = rules.get("sha256")
            if not rules_path.is_file():
                block("verdict_rules_missing",
                      f"{rules['path']} does not exist; the verdict/support-cell "
                      "layer is not implemented")
            elif not isinstance(expected, str) or not _HEX64.fullmatch(expected):
                block("verdict_rules_unpinned",
                      f"{rules['path']} exists but has no pinned SHA-256")
            else:
                actual = canonical_sha256(rules_path)
                verdict_report["sha256"] = actual
                if actual != expected:
                    block("verdict_rules_tampered",
                          f"{rules['path']} does not match its pinned SHA-256")
                else:
                    verdict_report["ok"] = True

    # -- separate authorization --------------------------------------------
    authorization: dict[str, Any] = {
        "path": authorization_path.name, "present": False, "ok": False,
    }
    if not authorization_path.is_file():
        block("authorization_missing",
              f"{authorization_path.name} is absent; authorized evaluation needs a "
              "separate, explicit authorization")
    else:
        authorization["present"] = True
        try:
            grant = _read_json(authorization_path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            block("authorization_invalid", f"cannot read the authorization: {type(exc).__name__}")
        else:
            if not isinstance(grant, dict):
                block("authorization_invalid", "the authorization is not a JSON object")
            else:
                problems = []
                if grant.get("v9") != 1:
                    problems.append("v9 must be 1")
                if grant.get("evaluation_authorized") is not True:
                    problems.append("evaluation_authorized must be true")
                if policy_sha is None or grant.get("policy_sha256") != policy_sha:
                    problems.append("policy_sha256 does not match the current policy")
                if status_sha is None or grant.get("status_sha256") != status_sha:
                    problems.append("status_sha256 does not match the current status ledger")
                for key in ("operator", "authorized_at", "scope"):
                    if not _nonempty(grant.get(key)):
                        problems.append(f"{key} must be a non-empty string")
                if problems:
                    block("authorization_invalid", "; ".join(problems))
                else:
                    authorization["ok"] = True

    return {
        "ok": not blockers,
        "blockers": blockers,
        "policy": str(policy_path),
        "policy_sha256": policy_sha,
        "status": str(status_path),
        "status_sha256": status_sha,
        "authorization": authorization,
        "verdict_rules": verdict_report,
        "gates": checked_gates,
    }


def require_authorized(**kwargs: Any) -> dict[str, Any]:
    """Raise unless every prerequisite is satisfied. The only way to proceed."""
    report = check(**kwargs)
    if report["ok"]:
        return report
    sample = "; ".join(
        f"{item['id']} ({item['detail']})" for item in report["blockers"][:6]
    )
    more = "" if len(report["blockers"]) <= 6 else f"; +{len(report['blockers']) - 6} more"
    raise ExecutionNotAuthorized(
        f"authorized evaluation is not permitted: {len(report['blockers'])} "
        f"prerequisite blocker(s): {sample}{more}"
    )
