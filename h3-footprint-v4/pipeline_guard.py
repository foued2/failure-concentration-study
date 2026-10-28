from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parent
FREEZE_PATH = ROOT / "FREEZE.json"
AUTH_PATH = ROOT / "EVALUATION_AUTHORIZATION.json"

REQUIRED_ARTIFACTS = (
    ".github/workflows/h3-v4-footprint-gate.yml",
    "h3-footprint-v4/generate.py",
    "h3-footprint-v4/run_gate.py",
    "h3-footprint-v4/container_eval.py",
    "h3-footprint-v4/container-image/Dockerfile",
    "h3-footprint-v4/container-image/sandbox_worker.py",
    "h3-footprint-v4/instrument.py",
    "h3-footprint-v4/expected_values.json",
    "h3-footprint-v4/isolation_battery.py",
    "h3-footprint-v4/validate_controls.py",
    "h3-footprint-v4/coherence_review.json",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"required authorization artifact is missing: {path.name}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def validate() -> dict:
    freeze = load_json(FREEZE_PATH)
    review = load_json(ROOT / "coherence_review.json")
    auth = load_json(AUTH_PATH)

    if freeze.get("status") != "FROZEN_V4_FOOTPRINT_ONLY":
        raise ValueError("generation blocked: FREEZE.json is not a frozen V4 footprint-only protocol")
    if review.get("status") != "APPROVED":
        raise ValueError("generation blocked: V4 protocol coherence review is not APPROVED")
    if review.get("version") != 4:
        raise ValueError("generation blocked: coherence review is not version 4")

    population = freeze.get("model_population") or {}
    expected_endpoint = "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/chat/completions"
    if population.get("model") != "gpt-oss-120b":
        raise ValueError("generation blocked: frozen model differs from V4 anonymous endpoint model")
    if population.get("endpoint") != expected_endpoint:
        raise ValueError("generation blocked: frozen endpoint differs from reviewed V4 endpoint")
    if population.get("provider") != "OVHcloud AI Endpoints anonymous lane":
        raise ValueError("generation blocked: frozen provider differs from reviewed V4 provider")

    policy = freeze.get("policy") or {}
    if policy.get("hard_cap_batches") != 400 or policy.get("bodies_per_batch") != 8:
        raise ValueError("generation blocked: frozen batch budget is not the reviewed 400 x 8 policy")
    if policy.get("eligible_k") != [2, 24] or policy.get("futility_checkpoints") != {"100": 10, "200": 20, "300": 30}:
        raise ValueError("generation blocked: frozen eligibility/futility rules do not match V4 proposal")

    if auth.get("status") != "AUTHORIZED":
        raise ValueError("generation blocked: EVALUATION_AUTHORIZATION.json is not AUTHORIZED")
    if auth.get("authorize_footprint_only_generation_and_scoring") is not True:
        raise ValueError("generation blocked: explicit V4 footprint-only authorization is false")
    if auth.get("freeze_sha256") != sha256(FREEZE_PATH):
        raise ValueError("generation blocked: authorization is bound to a different FREEZE.json")
    if auth.get("model") != population.get("model") or auth.get("endpoint") != population.get("endpoint"):
        raise ValueError("generation blocked: authorization model/endpoint differs from the frozen population")

    pinned = freeze.get("artifact_hashes_sha256")
    if not isinstance(pinned, dict):
        raise ValueError("generation blocked: freeze has no artifact_hashes_sha256 mapping")
    missing = [path for path in REQUIRED_ARTIFACTS if path not in pinned]
    if missing:
        raise ValueError("generation blocked: freeze omits required artifacts: " + ", ".join(missing))
    mismatches = []
    for relative in REQUIRED_ARTIFACTS:
        path = REPO / relative
        if not path.is_file():
            mismatches.append(relative + " (missing)")
        elif sha256(path) != pinned[relative]:
            mismatches.append(relative + " (hash mismatch)")
    if mismatches:
        raise ValueError("generation blocked: frozen code or protocol changed: " + "; ".join(mismatches))

    return {
        "authorized": True,
        "version": 4,
        "model": population["model"],
        "endpoint": population["endpoint"],
        "freeze_sha256": sha256(FREEZE_PATH),
        "artifact_count": len(REQUIRED_ARTIFACTS),
        "note": "This gate authorizes only the frozen V4 footprint-only run; it does not authorize held-out scoring or broader H3 claims.",
    }


def main() -> int:
    try:
        result = validate()
    except ValueError as exc:
        print(json.dumps({"authorized": False, "reason": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
