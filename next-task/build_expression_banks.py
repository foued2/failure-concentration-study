"""Build the frozen-candidate expression diagnostic and evaluation banks."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from expression_task import FAMILY_NAMES, FAMILY_ORDER, evaluate, evaluate_ast, validate_bank

ROOT = Path(__file__).resolve().parent
BANKS = ROOT / "banks"

DIAGNOSTIC = {
    "F1": ["2+3*4", "5+2*3", "6+1*4", "9+1*2", "2*3+4*5"],
    "F2": ["9-3-2", "8-1-2-3", "7-2-2", "9-4-2-1", "6-1-2-3"],
    "F3": ["9-(3-2)", "8-(1+2)", "9-(1+1)", "8-(2-1)", "9-(3-(1+1))"],
    "F4": ["-3+5", "-2-4", "-4+1", "-3+0", "-2-9"],
    "F5": ["12+3", "10-4", "99+1", "25-5", "100+20"],
    "F6": [" 2 + 3 ", "4 + 5", "1+ 2", " 9 - 2 ", "3 + 0"],
}

EVALUATION = {
    "F1": ["3+4*2", "4+5*2", "3*4+5*2", "8+2*2", "7+2*3"],
    "F2": ["8-2-3", "9-1-1-1", "6-2-3", "8-3-2-1", "7-1-2-2"],
    "F3": ["8-(3-1)", "7-(1+1)", "9-(2+2)", "6-(1-(1+1))", "8-(3-(1+1))"],
    "F4": ["-5+2", "-3-3", "-1+4", "-4+0", "-2-8"],
    "F5": ["13+4", "11-5", "98+2", "30-4", "200+30"],
    "F6": [" 3 + 4 ", "5 + 6", "2+ 3", " 8 - 1 ", "4 + 0"],
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_records(spec: dict[str, list[str]], id_field: str, id_prefix: str) -> list[dict]:
    records: list[dict] = []
    for family in FAMILY_ORDER:
        for index, expr in enumerate(spec[family]):
            expected = evaluate(expr)
            if evaluate_ast(expr) != expected:
                raise RuntimeError(f"oracle disagreement for {expr!r}")
            records.append({
                id_field: f"{id_prefix}{family[1:]}_{index}",
                "family": family,
                "family_name": FAMILY_NAMES[family],
                "expr": expr,
                "expected": expected,
            })
    return records


def main() -> None:
    if BANKS.exists():
        raise FileExistsError(BANKS)
    diagnostic = build_records(DIAGNOSTIC, "probe_id", "F")
    evaluation = build_records(EVALUATION, "hid", "E")
    validate_bank(diagnostic, 5)
    validate_bank(evaluation, 5)
    diagnostic_exprs = {record["expr"] for record in diagnostic}
    evaluation_exprs = {record["expr"] for record in evaluation}
    if diagnostic_exprs & evaluation_exprs:
        raise RuntimeError("diagnostic and evaluation expressions overlap")
    if len(diagnostic_exprs) != 30 or len(evaluation_exprs) != 30:
        raise RuntimeError("bank size is not 30")
    BANKS.mkdir()
    write_json(BANKS / "diagnostic.json", {
        "schema": 1,
        "task_id": "expression_eval_v1",
        "bank": "diagnostic",
        "family_order": FAMILY_ORDER,
        "family_names": FAMILY_NAMES,
        "records": diagnostic,
    })
    write_json(BANKS / "evaluation.json", {
        "schema": 1,
        "task_id": "expression_eval_v1",
        "bank": "evaluation",
        "family_order": FAMILY_ORDER,
        "family_names": FAMILY_NAMES,
        "records": evaluation,
    })
    family_counts = {
        family: sum(record["family"] == family for record in diagnostic)
        for family in FAMILY_ORDER
    }
    evaluation_family_counts = {
        family: sum(record["family"] == family for record in evaluation)
        for family in FAMILY_ORDER
    }
    write_json(BANKS / "BUILD_MANIFEST.json", {
        "schema": 1,
        "task_id": "expression_eval_v1",
        "status": "BUILT_NOT_FROZEN",
        "no_model_calls": True,
        "diagnostic": {
            "path": "diagnostic.json",
            "sha256": sha256_file(BANKS / "diagnostic.json"),
            "records": len(diagnostic),
            "family_counts": family_counts,
        },
        "evaluation": {
            "path": "evaluation.json",
            "sha256": sha256_file(BANKS / "evaluation.json"),
            "records": len(evaluation),
            "family_counts": evaluation_family_counts,
        },
        "graph_or_expression_overlap": False,
        "oracle": "recursive-descent and independent AST evaluator agree on every record",
        "disjointness": "exact expression strings are disjoint across banks",
    })
    print(json.dumps({
        "diagnostic_records": len(diagnostic),
        "evaluation_records": len(evaluation),
        "family_counts": family_counts,
        "evaluation_family_counts": evaluation_family_counts,
        "diagnostic_sha256": sha256_file(BANKS / "diagnostic.json"),
        "evaluation_sha256": sha256_file(BANKS / "evaluation.json"),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
