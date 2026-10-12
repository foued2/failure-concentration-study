"""Write FREEZE_V02.md and hash v0.2 + reused v0.1 instrument. Run after gates pass."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V02 = ROOT / "v02"

REUSED_V01 = [
    "study/sssp.py", "study/families.py", "study/probes.py",
    "study/instances.py", "study/features.py", "study/models.py",
    "specs/instrument_spec.json",
]
V02_FILES = [
    "v02/PROTOCOL_V02.md", "v02/spec_v02.json", "v02/models_v02.py",
    "v02/run_gates_v02.py", "v02/run_pilot_v02.py", "v02/run_confirmatory_v02.py",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    gates = json.loads((ROOT / "gates" / "gates_report_v02.json").read_text(encoding="utf-8"))
    assert gates["all_pass"], "v0.2 gates not passed"
    proto_hash = sha(V02 / "PROTOCOL_V02.md")
    lines = [
        "# FREEZE — v0.2", "",
        f"**Frozen at:** {datetime.now(timezone.utc).isoformat()}",
        f"**v0.2 protocol hash:** `{proto_hash}`",
        "**Confirmatory seeds:** `int.from_bytes(sha256(f'" + proto_hash[:16] + ":confirmatory:{i}')[:4],'big')` for i = 0..39, asserted distinct from pilot seeds 101-103",
        "", "## Gate evidence", "",
        f"- G1: {gates['G1']['exact_one']}/{gates['G1']['total']} probes exact-one predicate (reused instrument)",
        f"- G2: {len(gates['G2']['checks'])} v0.2 chain checks (soft labels, instance weights, LOIO, shared relabel)",
        f"- G3: {gates['G3']['hidden_inputs_checked']} hidden inputs checked vs brute force, {len(gates['G3']['mismatches'])} mismatches",
        f"- All pass: **{gates['all_pass']}**", "",
        "## v0.2 file hashes", "",
    ]
    for rel in V02_FILES:
        p = ROOT / rel
        if p.exists():
            lines.append(f"- `{rel}`: `{sha(p)}`")
    lines += ["", "## Reused v0.1 instrument hashes (imported unchanged)", ""]
    for rel in REUSED_V01:
        lines.append(f"- `{rel}`: `{sha(ROOT / rel)}`")
    lines += ["",
        "Post-freeze: G3 re-run on all 40 confirmatory hidden sets before pack execution; recorded in confirmatory log.",
        "Outcome rules and pilot gate as frozen in v02/PROTOCOL_V02.md §§5-6.", ""]
    (ROOT / "v02" / "FREEZE_V02.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"FREEZE_V02.md written; protocol hash {proto_hash[:16]}...")


if __name__ == "__main__":
    main()
