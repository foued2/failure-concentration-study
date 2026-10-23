from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.model import FAMILY_COUNT, FAMILY_ORDER  # noqa: E402

CONTROLS = ROOT / "controls"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def common_source() -> str:
    return '''def _answer(text):
    balance = 0
    minimum = 0
    for char in text:
        balance += 1 if char == "(" else -1
        minimum = min(minimum, balance)
    return balance - 2 * minimum


def _family(text):
    balance = 0
    minimum = 0
    for char in text:
        balance += 1 if char == "(" else -1
        minimum = min(minimum, balance)
    answer = balance - 2 * minimum
    if answer == 1:
        return 0 if balance == -1 else 1
    if answer == 3:
        return 2 if balance < 0 else 3
    if answer == 5:
        return 4
    if answer == 7:
        return 5
    raise ValueError("outside domain")
'''


def reference_source() -> str:
    return common_source() + '''

def solve(text):
    return _answer(text)
'''


def family_source(index: int) -> str:
    return common_source() + f'''

def solve(text):
    answer = _answer(text)
    if _family(text) == {index}:
        return answer + 1
    return answer
'''


def palindrome_source() -> str:
    return common_source() + '''

def solve(text):
    answer = _answer(text)
    if text == text[::-1]:
        return answer + 1
    return answer
'''


def main() -> None:
    CONTROLS.mkdir(parents=True, exist_ok=True)
    records = []
    reference = reference_source()
    (CONTROLS / "reference.py").write_text(reference, encoding="utf-8")
    records.append({
        "control_id": "reference",
        "path": "controls/reference.py",
        "source_sha256": sha256_text(reference),
        "target_id": None,
        "expected_diagnostic_vector": [0] * FAMILY_COUNT,
    })
    for index in range(FAMILY_COUNT):
        source = family_source(index)
        path = CONTROLS / f"localized_offbyone_{index}_{FAMILY_ORDER[index].lower()}.py"
        path.write_text(source, encoding="utf-8")
        profile = [0] * FAMILY_COUNT
        profile[index] = 5
        records.append({
            "control_id": f"localized_offbyone_{index}",
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": sha256_text(source),
            "target_id": f"T{index}_{FAMILY_ORDER[index]}",
            "expected_diagnostic_vector": profile,
        })
    spread = palindrome_source()
    spread_path = CONTROLS / "spread_palindrome.py"
    spread_path.write_text(spread, encoding="utf-8")
    records.append({
        "control_id": "spread_palindrome",
        "path": "controls/spread_palindrome.py",
        "source_sha256": sha256_text(spread),
        "target_id": "T6_SPREAD",
        "expected_diagnostic_vector": [1, 1, 1, 1, 1, 0],
    })
    manifest = {
        "schema": 1,
        "status": "HAND_BUILT_CALIBRATION_CONTROLS_ONLY",
        "model_calls": 0,
        "generated_solvers": 0,
        "description": (
            "The six localized controls add one to the correct answer only in one structural family. "
            "The spread control adds one only on palindromic inputs. These are calibration controls, "
            "not generated solvers and not evidence for H1a."
        ),
        "controls": records,
    }
    write_json(CONTROLS / "MANIFEST.json", manifest)
    print(json.dumps({"controls": len(records), "manifest": str(CONTROLS / "MANIFEST.json")}, indent=2))


if __name__ == "__main__":
    main()
