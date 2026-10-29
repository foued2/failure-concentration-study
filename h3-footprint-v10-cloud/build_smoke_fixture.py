"""Build a public-input-only fixture for cloud executor plumbing tests.

This imports V3 probe definitions, serializes only input fields, and never calls
or exports instrument.expected_values(). The fixed solver below is a hand-written
harness control, not a generated candidate and not part of the H3 experiment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "h3-footprint-v3"
if str(V3) not in sys.path:
    sys.path.insert(0, str(V3))

import instrument


SMOKE_BODY = """def solve(n, edges, s, t):
    import heapq

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    distances = [float("inf")] * n
    distances[s] = 0
    queue = [(0, s)]
    while queue:
        distance, node = heapq.heappop(queue)
        if distance != distances[node]:
            continue
        if node == t:
            return distance
        for nxt, weight in graph[node]:
            candidate = distance + weight
            if candidate < distances[nxt]:
                distances[nxt] = candidate
                heapq.heappush(queue, (candidate, nxt))
    return -1
"""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_probe_payloads() -> list[dict]:
    payloads = []
    for probe in instrument.PROBES:
        payload = {
            "probe_id": probe["probe_id"],
            "n": probe["n"],
            "edges": [list(edge) for edge in probe["edges"]],
            "s": probe["s"],
            "t": probe["t"],
        }
        if set(payload) != {"probe_id", "n", "edges", "s", "t"}:
            raise AssertionError("unexpected probe payload fields")
        payloads.append(payload)

    ids = [item["probe_id"] for item in payloads]
    if len(payloads) != 30 or len(set(ids)) != 30:
        raise AssertionError("expected exactly 30 uniquely identified V3 probes")
    return payloads


def write_fixture(out_dir: Path) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payloads = build_probe_payloads()
    body = SMOKE_BODY.encode("utf-8")
    probes = (json.dumps(payloads, sort_keys=True, indent=2) + "\n").encode("utf-8")
    canonical_payloads = json.dumps(payloads, sort_keys=True, separators=(",", ":")).encode("utf-8")
    body_path = out_dir / "smoke-body.py"
    probes_path = out_dir / "probes.json"
    body_path.write_bytes(body)
    probes_path.write_bytes(probes)

    manifest = {
        "version": 1,
        "kind": "fixed_harness_control",
        "source_instrument": "h3-footprint-v3/instrument.py",
        "source_instrument_sha256": sha256((V3 / "instrument.py").read_bytes()),
        "probe_count": 30,
        "probe_ids": [item["probe_id"] for item in payloads],
        "probe_payload_sha256": sha256(canonical_payloads),
        "body_sha256": sha256(body),
        "probes_sha256": sha256(probes),
        "expected_answers_in_fixture": False,
        "model_generated": False,
        "candidate_generation_performed": False,
        "candidate_evaluation_performed": False,
        "scoring_performed": False,
        "purpose": "test hosted execution plumbing only; not an H3 experiment",
    }
    manifest_path = out_dir / "fixture-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sums = (
        sha256(body) + "  smoke-body.py\n"
        + sha256(probes) + "  probes.json\n"
        + sha256(manifest_path.read_bytes()) + "  fixture-manifest.json\n"
    )
    (out_dir / "SHA256SUMS").write_text(sums, encoding="ascii")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    manifest = write_fixture(Path(args.out_dir))
    print(json.dumps({
        "status": "PASS",
        "kind": manifest["kind"],
        "probe_count": manifest["probe_count"],
        "probe_ids": manifest["probe_ids"],
        "expected_answers_in_fixture": False,
        "candidate_generation_performed": False,
        "scoring_performed": False,
        "body_sha256": manifest["body_sha256"],
        "probes_sha256": manifest["probes_sha256"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
