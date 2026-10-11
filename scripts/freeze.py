"""Write FREEZE.md with sha256 hashes and gate evidence. Run only after gates pass."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FROZEN_PATHS = [
    "PROTOCOL.md",
    "specs/instrument_spec.json",
    "specs/generator_spec.json",
    "study/sssp.py",
    "study/families.py",
    "study/probes.py",
    "study/instances.py",
    "study/features.py",
    "study/models.py",
    "scripts/run_gates.py",
    "scripts/run_pilot.py",
    "scripts/freeze.py",
]


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    gates = json.loads((ROOT / "gates" / "gates_report.json").read_text())
    assert gates["all_pass"], "gates not passed; cannot freeze"

    proto_hash = sha256_file(ROOT / "PROTOCOL.md")
    hashes = {rel: sha256_file(ROOT / rel) for rel in FROZEN_PATHS if (ROOT / rel).exists()}

    lines = [
        "# FREEZE — v0.1",
        "",
        f"**Frozen at:** {datetime.now(timezone.utc).isoformat()}",
        f"**Protocol hash (sha256(PROTOCOL.md)):** `{proto_hash}`",
        f"**Confirmatory seed derivation:** `int.from_bytes(sha256(f'{proto_hash[:16]}:confirmatory:{i}')[:4],'big')` for i = 0..N_c-1",
        "",
        "## Gate evidence (must pass before freeze)",
        "",
        f"- G1 partition: {gates['G1']['exact_one']}/{gates['G1']['total']} probes satisfy exactly one declared predicate across seeds {gates['G1']['seeds']}; violations: {len(gates['G1']['violations'])}",
        f"- G2 measurement chain: {len(gates['G2']['checks'])} hand-computed cases passed (k/C values, eligibility boundary, Y labels, crash-as-failure, output identity)",
        f"- G3 oracle chain: reference vs brute force on {gates['G3']['cases']} tiny random graphs; mismatches: {len(gates['G3']['mismatches'])}",
        f"- All gates pass: **{gates['all_pass']}** (report: gates/gates_report.json)",
        "",
        "G1 establishes the declared partition property only — not construct validity (PROTOCOL.md §3).",
        "",
        "## Frozen file hashes (sha256)",
        "",
    ]
    for rel, h in hashes.items():
        lines.append(f"- `{rel}`: `{h}`")
    lines += [
        "",
        "## Terminology (binding, PROTOCOL.md §6 / GPT ratification)",
        "",
        "- An observation is a (solver, instance) pair.",
        "- The binary outcome Y is whether that solver passes all 20 hidden oracle inputs assigned to that instance.",
        "- The 20 hidden inputs are never counted as 20 independent observations.",
        "- Inference concerns unseen problem instances under the fixed generator and solver-pack protocol, not unseen solver-generating models.",
        "",
        "## Scope of any positive result",
        "",
        "Predictive value only, conditional on the frozen instrument, generator, class, and threshold δ = 0.01 nats. Not localization. Not novelty. All outcomes terminal.",
        "",
    ]
    (ROOT / "FREEZE.md").write_text("\n".join(lines))
    print(f"FREEZE.md written; protocol hash {proto_hash[:16]}...")


if __name__ == "__main__":
    main()
