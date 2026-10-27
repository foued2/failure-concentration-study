"""Audit-only diagnostic: quantify the extract() prelude-drop defect.

This script does NOT produce a gate result. It evaluates bodies that are
already frozen on the gate branch, after restoring module imports that the
frozen extractor discarded. Its output is diagnostic evidence about the
harness defect, not a replacement verdict for H3.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import tempfile
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
BODIES = ROOT / "generated" / "bodies"
RAW = ROOT / "generated" / "raw"
WORKER = ROOT / "probe_worker.py"
REPORT = ROOT / "results" / "footprint.json"
OUT = ROOT / "audit" / "extractor_defect.json"

FENCE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.S | re.I)
DEF_RE = re.compile(r"(?m)^def\s+solve\s*\(")
IMPORT_RE = re.compile(r"(?m)^\s*(?:from\s+\S+\s+import|import\s+\S+)")


def raw_prelude_stats() -> dict:
    blocks = with_prelude = prelude_import = 0
    for path in sorted(RAW.glob("*.txt")):
        texts = []
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "text":
                texts.append(event.get("part", {}).get("text", ""))
        text = "\n".join(texts)
        for block in FENCE.findall(text):
            if "def solve" not in block:
                continue
            blocks += 1
            match = DEF_RE.search(block)
            prelude = block[: match.start()] if match else ""
            if prelude.strip():
                with_prelude += 1
            if IMPORT_RE.search(prelude):
                prelude_import += 1
    return {
        "code_blocks_with_def_solve": blocks,
        "blocks_with_nonempty_prelude": with_prelude,
        "blocks_with_import_in_prelude": prelude_import,
    }


def needed_imports(source: str) -> list[str]:
    found = re.findall(
        r"(?m)^\s*(?:from\s+([\w.]+)\s+import\s+([\w, ]+)|import\s+([\w.]+))", source
    )
    names = set()
    for module, imported, direct in found:
        if direct:
            names.add(direct.split(".")[-1])
        for part in imported.split(","):
            names.add(part.strip().split(".")[-1])
    out = []
    if re.search(r"\bheapq\.", source) and "heapq" not in names:
        out.append("import heapq")
    if re.search(r"\bdeque\(", source) and "deque" not in names:
        out.append("from collections import deque")
    if re.search(r"\bdefaultdict\(", source) and "defaultdict" not in names:
        out.append("from collections import defaultdict")
    if re.search(r"(?<![.\w])Counter\(", source) and "Counter" not in names:
        out.append("from collections import Counter")
    return out


def evaluate(source: str) -> tuple[list[bool], str | None]:
    handle = tempfile.NamedTemporaryFile(
        "w", suffix=".py", delete=False, encoding="utf-8", newline="\n"
    )
    try:
        handle.write(source)
        handle.close()
        proc = subprocess.run(
            [sys.executable, "-I", str(WORKER), handle.name],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=5,
            encoding="utf-8",
            errors="replace",
        )
        data = json.loads(proc.stdout.strip().splitlines()[-1])
        return data["fails"], data.get("load_error")
    except Exception as exc:  # noqa: BLE001 - audit diagnostic
        return [True] * 30, f"{type(exc).__name__}: {exc}"
    finally:
        pathlib.Path(handle.name).unlink(missing_ok=True)


def family_counts(fails: list[bool]) -> dict[str, int]:
    sys.path.insert(0, str(ROOT))
    import instrument  # noqa: E402

    return instrument.family_counts(fails)


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    rows = report["rows"]
    transitions = Counter()
    before_after = []
    corrected_counts = Counter()
    corrected_all_or_none_terms = 0
    corrected_family_total = 0
    importer_bodies = 0

    for row in rows:
        source = (BODIES / f"{row['body_hash']}.py").read_text(encoding="utf-8")
        imports = needed_imports(source)
        before = row["k"]
        if imports:
            importer_bodies += 1
            fails, load_error = evaluate("\n".join(imports) + "\n\n" + source)
        else:
            fails, load_error = row["fails"], row.get("load_error")
        counts = family_counts(fails)
        after = sum(counts.values())
        corrected_counts[after] += 1
        corrected_all_or_none_terms += sum(1 for v in counts.values() if v in (0, 5))
        corrected_family_total += 6
        transitions[(before, after)] += 1
        if before != after:
            before_after.append(
                {
                    "body_hash": row["body_hash"],
                    "restored_imports": imports,
                    "k_before": before,
                    "k_after": after,
                    "load_error": load_error,
                }
            )

    distribution = dict(sorted(corrected_counts.items()))
    eligible = sum(v for k, v in corrected_counts.items() if 2 <= k <= 24)
    result = {
        "status": "INVALID_RUN_DIAGNOSTIC_ONLY",
        "note": (
            "Import restoration is diagnostic evidence about the harness defect. "
            "It is not a result from the frozen harness and does not establish any "
            "H3 conclusion."
        ),
        "frozen_report": "results/footprint.json",
        "raw_prelude_stats": raw_prelude_stats(),
        "bodies_in_frozen_report": len(rows),
        "bodies_with_restored_imports": importer_bodies,
        "bodies_with_changed_k": len(before_after),
        "k_30_before_to_below_30_after": sum(
            1 for b in before_after if b["k_before"] == 30 and b["k_after"] < 30
        ),
        "transitions": [
            {"k_before": a, "k_after": b, "count": n}
            for (a, b), n in sorted(transitions.items())
        ],
        "corrected_k_distribution": distribution,
        "corrected_total_bodies": sum(distribution.values()),
        "corrected_eligible_k_2_to_24": eligible,
        "corrected_all_or_none_fraction": round(
            corrected_all_or_none_terms / corrected_family_total, 6
        )
        if corrected_family_total
        else 1.0,
        "denominator_reconciliation": {
            "total": len(rows),
            "k_zero": corrected_counts.get(0, 0),
            "eligible_k_2_to_24": eligible,
            "k_25": corrected_counts.get(25, 0),
            "k_29": corrected_counts.get(29, 0),
            "k_30": corrected_counts.get(30, 0),
            "sum": sum(distribution.values()),
            "resolved": sum(distribution.values()) == len(rows),
        },
        "changed_rows": before_after,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "changed_rows"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
