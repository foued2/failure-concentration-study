from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.model import (  # noqa: E402
    FAMILY_COUNT,
    FAMILY_ORDER,
    PROBES_PER_FAMILY,
    Probe,
    all_texts,
    expected_answer,
    family_index,
    is_palindrome,
    validate_family_partition,
    validate_oracles,
)

BANKS = ROOT / "banks"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def select_diagnostic() -> list[Probe]:
    domain = all_texts()
    by_family: list[list[str]] = [[] for _ in range(FAMILY_COUNT)]
    for text in domain:
        by_family[family_index(text)].append(text)
    selected: list[Probe] = []
    for index in range(FAMILY_COUNT):
        palindromes = sorted((text for text in by_family[index] if is_palindrome(text)), key=sha256_text)
        non_palindromes = sorted((text for text in by_family[index] if not is_palindrome(text)), key=sha256_text)
        if index < 5:
            if not palindromes:
                raise AssertionError(f"family {FAMILY_ORDER[index]} has no palindrome")
            chosen = [palindromes[0], *non_palindromes[: PROBES_PER_FAMILY - 1]]
        else:
            chosen = non_palindromes[:PROBES_PER_FAMILY]
        if len(chosen) != PROBES_PER_FAMILY or len(set(chosen)) != PROBES_PER_FAMILY:
            raise AssertionError(f"diagnostic selection failed for family {index}")
        for number, text in enumerate(chosen):
            selected.append(
                Probe(
                    probe_id=f"D{index}_{number:02d}",
                    family_index=index,
                    text=text,
                    expected=expected_answer(text),
                )
            )
    if len(selected) != FAMILY_COUNT * PROBES_PER_FAMILY:
        raise AssertionError("diagnostic bank has the wrong size")
    return selected


def main() -> None:
    validate_oracles()
    partition = validate_family_partition()
    diagnostic = select_diagnostic()
    diagnostic_texts = {probe.text for probe in diagnostic}
    evaluation = [
        Probe(
            probe_id=f"E{number:03d}",
            family_index=family_index(text),
            text=text,
            expected=expected_answer(text),
        )
        for number, text in enumerate(
            sorted((text for text in all_texts() if text not in diagnostic_texts), key=lambda text: (sha256_text(text), text))
        )
    ]
    if len(evaluation) != 128 - len(diagnostic):
        raise AssertionError("evaluation bank has the wrong size")
    if diagnostic_texts & {probe.text for probe in evaluation}:
        raise AssertionError("diagnostic/evaluation input overlap")

    BANKS.mkdir(parents=True, exist_ok=True)
    domain_record = [
        {
            "text": text,
            "family": FAMILY_ORDER[family_index(text)],
            "family_index": family_index(text),
            "expected": expected_answer(text),
        }
        for text in all_texts()
    ]
    write_json(BANKS / "domain.json", {
        "schema": 1,
        "task": "paren7_min_insertions",
        "length": 7,
        "input_count": len(domain_record),
        "inputs": domain_record,
    })
    write_json(BANKS / "diagnostic.json", {
        "schema": 1,
        "task": "paren7_min_insertions",
        "family_order": list(FAMILY_ORDER),
        "probe_count": len(diagnostic),
        "probes": [probe.to_record() for probe in diagnostic],
    })
    write_json(BANKS / "evaluation.json", {
        "schema": 1,
        "task": "paren7_min_insertions",
        "family_order": list(FAMILY_ORDER),
        "probe_count": len(evaluation),
        "probes": [probe.to_record() for probe in evaluation],
    })

    eval_family_counts = {name: 0 for name in FAMILY_ORDER}
    for probe in evaluation:
        eval_family_counts[FAMILY_ORDER[probe.family_index]] += 1

    manifest = {
        "schema": 1,
        "task": "paren7_min_insertions",
        "status": "STAGE_B_BANKS_FROZEN_FOR_GATE1_ONLY",
        "model_calls": 0,
        "generated_solvers": 0,
        "declared_domain": "all 128 strings of length 7 over ( and )",
        "domain_input_count": 128,
        "diagnostic_probe_count": len(diagnostic),
        "evaluation_probe_count": len(evaluation),
        "diagnostic_per_family": PROBES_PER_FAMILY,
        "diagnostic_evaluation_overlap": 0,
        "family_domain_counts": partition,
        "evaluation_family_counts": eval_family_counts,
        "selection_rule": (
            "For families 0-4, one palindrome and four non-palindromes by ascending SHA-256 of the input; "
            "for family 5, five non-palindromes by ascending SHA-256. Evaluation is the exhaustive complement."
        ),
        "diagnostic_ids": [probe.probe_id for probe in diagnostic],
        "evaluation_ids": [probe.probe_id for probe in evaluation],
        "oracles": {
            "primary": "balance - 2 * minimum_prefix",
            "independent": "unmatched closes from left plus unmatched opens from right",
            "agreement": "all 128 domain inputs",
        },
        "files": {
            "domain.json": sha256_file(BANKS / "domain.json"),
            "diagnostic.json": sha256_file(BANKS / "diagnostic.json"),
            "evaluation.json": sha256_file(BANKS / "evaluation.json"),
            "core/model.py": sha256_file(ROOT / "core" / "model.py"),
            "build_banks.py": sha256_file(Path(__file__).resolve()),
            "03_TASK_SPEC.md": sha256_file(ROOT / "03_TASK_SPEC.md"),
        },
    }
    write_json(BANKS / "MANIFEST.json", manifest)
    freeze = {
        "schema": 1,
        "status": "FROZEN_FOR_GATE1_ONLY",
        "manifest_sha256": sha256_file(BANKS / "MANIFEST.json"),
        "file_hashes": manifest["files"],
        "diagnostic_probe_count": len(diagnostic),
        "evaluation_probe_count": len(evaluation),
        "model_calls": 0,
    }
    write_json(BANKS / "FREEZE.json", freeze)
    print(json.dumps({
        "manifest": str(BANKS / "MANIFEST.json"),
        "freeze": str(BANKS / "FREEZE.json"),
        "diagnostic": len(diagnostic),
        "evaluation": len(evaluation),
        "family_domain_counts": partition,
        "evaluation_family_counts": eval_family_counts,
    }, indent=2))


if __name__ == "__main__":
    main()
