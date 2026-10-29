#!/usr/bin/env python3
"""GLM-agent H3 exploratory pilot - generation stage.

Bounded, keyless generation through the z-ai CLI already available in this
sandbox (no separate API key, no paid API, no Copilot). Mirrors the structure
of h3-footprint-v10-cloud/copilot_auto_pilot.py:
  - identical fixed schedule of 12 requests (4 x direct, 4 x menu, 4 x simple,
    interleaved) taken verbatim from the trusted module's prompts();
  - identical extraction/dedup rules via the trusted normalize_candidate();
  - no retries: a request that fails, times out, or yields an invalid response
    is recorded and never re-attempted. (--from/--to chunking only skips
    requests already recorded in state; it never re-runs an attempted one.)

This is NOT the frozen three-generator H3 gate and no confirmatory batches
are started. The generator differs from the frozen generator list by design;
the point of this screen is feasibility of the GLM-agent route.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

REPO_PILOT = Path("/home/z/my-project/fcs-verify/h3-footprint-v10-cloud/copilot_auto_pilot.py")
OUT_DIR = Path("/home/z/my-project/scripts/h3/pilot-run")
REQUEST_TIMEOUT_SECONDS = 120
MAX_REQUESTS = 12
PROVIDER_ROUTE = "z-ai CLI chat (platform-provided GLM access in analysis sandbox)"


def load_trusted_module():
    spec = importlib.util.spec_from_file_location("copilot_auto_pilot", REPO_PILOT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def call_zai(prompt: str, raw_path: Path) -> dict:
    """One generation request. No retries. Returns attempt metadata."""
    started = time.monotonic()
    started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        proc = subprocess.run(
            ["z-ai", "chat", "--prompt", prompt, "--output", str(raw_path)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=REQUEST_TIMEOUT_SECONDS,
            check=False,
        )
        rc, err = proc.returncode, proc.stderr.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return {"exit_code": 124, "stderr_sha256": None, "stderr_excerpt": "timeout",
                "started_utc": started_utc,
                "elapsed_seconds": round(time.monotonic() - started, 2)}
    return {
        "exit_code": rc,
        "stderr_sha256": sha256_bytes(err.encode("utf-8")),
        "stderr_excerpt": err[-300:],
        "started_utc": started_utc,
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="frm", type=int, default=1)
    parser.add_argument("--to", dest="to", type=int, default=MAX_REQUESTS)
    args = parser.parse_args()

    trusted = load_trusted_module()
    schedule = trusted.prompts()
    assert len(schedule) == MAX_REQUESTS, "trusted schedule must be 12 requests"
    variants = [v for _, v, _ in schedule]
    assert variants.count("direct") == 4 and variants.count("menu") == 4 and variants.count("simple") == 4

    (OUT_DIR / "responses").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "bodies").mkdir(exist_ok=True)
    state_path = OUT_DIR / "generation-state.json"
    state: dict[str, Any] = {"requests": {}, "schedule": [
        {"request_id": rid, "prompt_variant": v} for rid, v, _ in schedule]}
    if state_path.exists():
        state.update(json.loads(state_path.read_text(encoding="utf-8")))

    for request_id, variant, prompt in schedule:
        idx = int(request_id.split("-")[1])
        if not (args.frm <= idx <= args.to):
            continue
        if request_id in state["requests"]:
            print(f"{request_id}: already attempted (skipping; no retries)", flush=True)
            continue

        raw_path = OUT_DIR / "responses" / f"{request_id}.raw.json"
        att = call_zai(prompt, raw_path)
        rec: dict[str, Any] = {
            "request_id": request_id,
            "provenance_group": request_id,
            "prompt_variant": variant,
            "provider_route": PROVIDER_ROUTE,
            "model_requested": "platform-default",
            "actual_model_identity_verified": False,
            "attempt": att,
            "retry_count": 0,
        }
        if att["exit_code"] != 0:
            rec.update({"status": "request_failed",
                        "error_category": "timeout" if att["exit_code"] == 124 else "cli_error"})
            state["requests"][request_id] = rec
            print(f"{request_id}: request_failed ({rec['error_category']})", flush=True)
            state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
            continue

        raw_bytes = raw_path.read_bytes()
        rec["raw_response_sha256"] = sha256_bytes(raw_bytes)
        rec["raw_response_bytes"] = len(raw_bytes)
        try:
            raw = json.loads(raw_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            rec.update({"status": "invalid_response", "error_category": "response_not_utf8_json"})
            state["requests"][request_id] = rec
            print(f"{request_id}: invalid_response (response_not_utf8_json)", flush=True)
            state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
            continue

        # record every identity/usage field the endpoint exposed, verbatim
        rec["endpoint_reported_model"] = raw.get("model")
        rec["endpoint_request_id"] = raw.get("request_id")
        rec["endpoint_completion_id"] = raw.get("id")
        rec["endpoint_usage"] = raw.get("usage")
        rec["finish_reason"] = (raw.get("choices") or [{}])[0].get("finish_reason")
        content = (raw.get("choices") or [{}])[0].get("message", {}).get("content")
        if not isinstance(content, str) or not content.strip():
            rec.update({"status": "invalid_response", "error_category": "empty_content"})
            state["requests"][request_id] = rec
            print(f"{request_id}: invalid_response (empty_content)", flush=True)
            state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
            continue

        source, invalid_reason = trusted.normalize_candidate(content)
        if invalid_reason:
            rec.update({"status": "invalid_response", "error_category": invalid_reason})
            state["requests"][request_id] = rec
            print(f"{request_id}: invalid_response ({invalid_reason})", flush=True)
            state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
            continue

        body_bytes = source.encode("utf-8")
        body_hash = sha256_bytes(body_bytes)
        body_path = OUT_DIR / "bodies" / f"{request_id}.py"
        body_path.write_bytes(body_bytes)
        rec.update({
            "status": "candidate_ready",
            "body_sha256": body_hash,
            "body_bytes": len(body_bytes),
            "body_path": str(Path("bodies") / body_path.name),
        })
        state.setdefault("first_hash_request", {})
        first = state["first_hash_request"]
        rec["duplicate_of"] = first.get(body_hash)
        if body_hash not in first:
            first[body_hash] = request_id
        state["requests"][request_id] = rec
        print(f"{request_id}: candidate_ready duplicate_of={rec['duplicate_of']} "
              f"model={rec['endpoint_reported_model']}", flush=True)
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")

    # index (same schema family as the trusted manifest)
    reqs = [state["requests"].get(rid) for rid, _, _ in schedule]
    reqs = [r for r in reqs if r]
    manifest = {
        "schema_version": 1,
        "kind": "glm_agent_single_provider_exploratory_footprint_screen",
        "fixed_request_cap": MAX_REQUESTS,
        "requests_attempted": len(reqs),
        "retry_policy": "no retries",
        "prompt_schedule": {"direct": 4, "menu": 4, "simple": 4, "interleaved": True,
                            "source": "verbatim from copilot_auto_pilot.prompts()"},
        "provider_route": PROVIDER_ROUTE,
        "model_requested": "platform-default",
        "endpoint_reported_models": sorted({str(r.get("endpoint_reported_model")) for r in reqs
                                            if r.get("endpoint_reported_model")}),
        "actual_model_identity_verified": False,
        "candidate_count_before_deduplication": sum(r.get("status") == "candidate_ready" for r in reqs),
        "unique_candidate_body_count": len({r["body_sha256"] for r in reqs
                                            if r.get("status") == "candidate_ready"}),
        "H3_confirmatory_batches_started": False,
        "held_out_evaluation_performed": False,
        "H3_scientific_result": False,
        "requests": reqs,
    }
    (OUT_DIR / "candidate-index.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in (
        "requests_attempted", "candidate_count_before_deduplication",
        "unique_candidate_body_count", "endpoint_reported_models")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
