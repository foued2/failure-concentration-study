"""Bounded one-request-per-route smoke test for API access; never generates candidates.

The script stores no prompt response text. It records a digest and length, then
reports whether the route returned a usable short response. API keys are read
from the environment and never serialized.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from providers import ProviderError, ROUTES, call_chat

PROMPT = "Reply with exactly H3_PROVIDER_SMOKE_OK and no other text."
EXPECTED = "H3_PROVIDER_SMOKE_OK"


def run(routes: list[str], timeout: float) -> dict:
    results = []
    for route_id in routes:
        if route_id not in ROUTES:
            raise ValueError(f"unknown route_id: {route_id}")
        route = ROUTES[route_id]
        credential_present = bool(os.environ.get(route.key_env, "").strip())
        started = time.time()
        try:
            result = call_chat(
                route_id,
                PROMPT,
                max_tokens=32,
                temperature=0.0,
                timeout=timeout,
            )
            response = result["content"]
            results.append({
                "route_id": route_id,
                "original_alias": result["original_alias"],
                "provider": result["provider"],
                "api_url": result["api_url"],
                "api_model": result["api_model"],
                "status": (
                    "PASS" if response.strip() == EXPECTED
                    else ("REACHABLE_PROMPT_MISMATCH" if response.strip() else "EMPTY_RESPONSE")
                ),
                "credential_configured": credential_present,
                "request_attempted": result.get("request_attempted", True),
                "http_response_received": result.get("http_response_received", True),
                "http_status": result["http_status"],
                "provider_request_id": result["provider_request_id"],
                "finish_reason": result["finish_reason"],
                "usage": result["usage"],
                "safe_rate_headers": result["safe_rate_headers"],
                "elapsed_seconds": result["elapsed_seconds"],
                "response_characters": len(response),
                "response_sha256": hashlib.sha256(response.encode("utf-8")).hexdigest(),
                "exact_token_match": response.strip() == EXPECTED,
                "raw_response_stored": False,
                "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            })
        except ProviderError as exc:
            results.append({
                "route_id": route_id,
                "original_alias": ROUTES[route_id].original_alias,
                "provider": ROUTES[route_id].provider,
                "api_url": ROUTES[route_id].api_url,
                "api_model": ROUTES[route_id].api_model,
                "status": "BLOCKED",
                "credential_configured": credential_present,
                "request_attempted": exc.request_attempted,
                "http_response_received": exc.http_response_received,
                "http_status": exc.status,
                "error_category": exc.category,
                "retry_after": exc.retry_after,
                "error": str(exc),
                "raw_response_stored": False,
                "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            })
    return {
        "version": 1,
        "kind": "provider_access_smoke_only",
        "candidate_generation_performed": False,
        "candidate_evaluation_performed": False,
        "outcome": "PASS" if results and all(r["status"] == "PASS" for r in results) else "BLOCKED",
        "route_count": len(results),
        "request_attempt_count": sum(1 for item in results if item["request_attempted"]),
        "http_response_count": sum(1 for item in results if item["http_response_received"]),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--routes", nargs="+", choices=sorted(ROUTES), default=sorted(ROUTES))
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.timeout <= 0 or args.timeout > 180:
        parser.error("--timeout must be between 0 and 180 seconds")
    report = run(args.routes, args.timeout)
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "outcome": report["outcome"],
        "route_count": report["route_count"],
        "request_attempt_count": report["request_attempt_count"],
        "http_response_count": report["http_response_count"],
        "routes": [{"route_id": r["route_id"], "status": r["status"],
                    "request_attempted": r["request_attempted"],
                    "http_response_received": r["http_response_received"],
                    "http_status": r.get("http_status"), "error_category": r.get("error_category"),
                    "provider_request_id": r.get("provider_request_id"),
                    "elapsed_seconds": r.get("elapsed_seconds")} for r in report["results"]],
        "report": str(path),
        "raw_response_stored": False,
        "candidate_generation_performed": False,
        "candidate_evaluation_performed": False,
    }, indent=2))
    return 0 if report["outcome"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
