from __future__ import annotations

import collections
import hashlib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.model import expected_answer, family_index, independent_answer  # noqa: E402

D = json.loads((ROOT / "banks" / "diagnostic.json").read_text(encoding="utf-8"))["probes"]
E = json.loads((ROOT / "banks" / "evaluation.json").read_text(encoding="utf-8"))["probes"]
ALL = json.loads((ROOT / "banks" / "domain.json").read_text(encoding="utf-8"))["inputs"]
SIZES = tuple(sum(1 for p in E if p["family_index"] == family) for family in range(6))


def stats(text: str) -> dict[str, int]:
    balance = 0
    minimum = 0
    maximum = 0
    for char in text:
        balance += 1 if char == "(" else -1
        minimum = min(minimum, balance)
        maximum = max(maximum, balance)
    return {
        "close": text.count(")"),
        "open": text.count("("),
        "rev": text.count(")("),
        "pair": text.count("()"),
        "min": minimum,
        "max": maximum,
        "bal": balance,
        "opens_prefix": len(text) - len(text.lstrip("(")),
        "closes_prefix": len(text) - len(text.lstrip(")")),
        "opens_suffix": len(text) - len(text.rstrip("(")),
        "closes_suffix": len(text) - len(text.rstrip(")")),
        "first_close": text.find(")") if ")" in text else 7,
        "last_open": text.rfind("(") if "(" in text else -1,
    }


STATS = {probe["text"]: stats(probe["text"]) for probe in [*D, *E, *ALL]}


def add_if(predicate):
    def solve(text: str) -> int:
        return expected_answer(text) + (1 if predicate(text) else 0)

    return solve


def min_tail(text: str, count: int) -> int:
    balance = 0
    minimum = 0
    for index, char in enumerate(text):
        balance += 1 if char == "(" else -1
        if index < len(text) - count:
            minimum = min(minimum, balance)
    return balance - 2 * minimum


def min_init(text: str, value: int) -> int:
    balance = 0
    minimum = value
    for char in text:
        balance += 1 if char == "(" else -1
        minimum = min(minimum, balance)
    return balance - 2 * minimum


def omit_empty(text: str, count: int) -> int:
    stack = 0
    missing = 0
    ignored = 0
    for char in text:
        if char == "(":
            stack += 1
        elif stack:
            stack -= 1
        elif ignored < count:
            ignored += 1
        else:
            missing += 1
    return missing + stack


def push_empty(text: str, cap: int) -> int:
    stack = 0
    missing = 0
    for char in text:
        if char == "(":
            stack += 1
        elif stack:
            stack -= 1
        elif stack < cap:
            stack += 1
        else:
            missing += 1
    return missing + stack


def truncated(text: str, count: int, side: str) -> int:
    if side == "prefix":
        return expected_answer(text[count:])
    return expected_answer(text[: len(text) - count] if count else text)


def min_update(text: str, mode: str) -> int:
    balance = 0
    minimum = 0
    for char in text:
        balance += 1 if char == "(" else -1
        if mode == "close" and char == ")":
            minimum = min(minimum, balance)
        elif mode == "open" and char == "(":
            minimum = min(minimum, balance)
        elif mode == "after" and balance < 0:
            minimum = min(minimum, balance)
    return balance - 2 * minimum


def sign_error(text: str) -> int:
    balance = 0
    minimum = 0
    for char in text:
        balance += 1 if char == "(" else -1
        minimum = min(minimum, balance)
    return balance + 2 * minimum


def candidates():
    for count in range(7):
        yield f"min_tail(r={count})", lambda text, count=count: min_tail(text, count)
    for value in range(-2, 4):
        yield f"min_init(v={value})", lambda text, value=value: min_init(text, value)
    for count in range(4):
        yield f"omit_empty(r={count})", lambda text, count=count: omit_empty(text, count)
    for cap in range(4):
        yield f"push_empty(cap={cap})", lambda text, cap=cap: push_empty(text, cap)
    for count in range(1, 6):
        yield f"truncate_prefix(r={count})", lambda text, count=count: truncated(text, count, "prefix")
        yield f"truncate_suffix(r={count})", lambda text, count=count: truncated(text, count, "suffix")
    for mode in ("close", "open", "after"):
        yield f"min_update({mode})", lambda text, mode=mode: min_update(text, mode)
    yield "sign_error", sign_error
    for feature in STATS[D[0]["text"]]:
        values = sorted({STATS[probe["text"]][feature] for probe in D})
        for operator in ("eq", "ge", "le"):
            for threshold in values:
                if operator == "eq":
                    predicate = lambda text, feature=feature, threshold=threshold: STATS[text][feature] == threshold
                elif operator == "ge":
                    predicate = lambda text, feature=feature, threshold=threshold: STATS[text][feature] >= threshold
                else:
                    predicate = lambda text, feature=feature, threshold=threshold: STATS[text][feature] <= threshold
                yield f"{feature}_{operator}({threshold})", add_if(predicate)


def evaluate(name: str, solve) -> dict[str, object] | None:
    failures = set()
    for probe in ALL:
        try:
            value = solve(probe["text"])
        except Exception:
            return None
        if type(value) is not int:
            return None
        if value != independent_answer(probe["text"]):
            failures.add(probe["text"])
    diagnostic = [0] * 6
    evaluation = [0] * 6
    for probe in D:
        if probe["text"] in failures:
            diagnostic[probe["family_index"]] += 1
    for probe in E:
        if probe["text"] in failures:
            evaluation[probe["family_index"]] += 1
    family_accuracy = [
        (SIZES[family] - evaluation[family]) / SIZES[family] for family in range(6)
    ]
    return {
        "name": name,
        "family": name.split("(")[0],
        "diagnostic_profile": diagnostic,
        "k": sum(diagnostic),
        "C": max(diagnostic) / sum(diagnostic) if sum(diagnostic) else None,
        "evaluation_failures": evaluation,
        "evaluation_score_raw": 1 - sum(evaluation) / 98,
        "evaluation_score_equal_family": sum(family_accuracy) / 6,
        "failure_set_sha256": hashlib.sha256(
            "\n".join(sorted(failures)).encode("utf-8")
        ).hexdigest(),
        "failure_count": len(failures),
        "failures": sorted(failures),
    }


def main() -> int:
    records = []
    for name, solve in candidates():
        record = evaluate(name, solve)
        if record is not None:
            records.append(record)
    k5 = [record for record in records if record["k"] == 5]
    by_family = collections.defaultdict(list)
    for record in k5:
        by_family[record["family"]].append(record)
    multi = {
        family: [
            {
                "name": record["name"],
                "profile": record["diagnostic_profile"],
                "C": record["C"],
            }
            for record in items
        ]
        for family, items in by_family.items()
        if len({tuple(record["diagnostic_profile"]) for record in items}) > 1
    }
    matches = []
    for left, right in itertools.combinations(k5, 2):
        if left["diagnostic_profile"] != right["diagnostic_profile"]:
            continue
        if left["family"] == right["family"]:
            continue
        matches.append(
            {
                "profile": left["diagnostic_profile"],
                "C": left["C"],
                "left": left["name"],
                "right": right["name"],
                "left_score_raw": left["evaluation_score_raw"],
                "right_score_raw": right["evaluation_score_raw"],
                "left_score_equal_family": left["evaluation_score_equal_family"],
                "right_score_equal_family": right["evaluation_score_equal_family"],
                "same_failure_set": left["failure_set_sha256"] == right["failure_set_sha256"],
            }
        )
    distinct_matches = [match for match in matches if not match["same_failure_set"]]
    result = {
        "schema": 1,
        "status": "NEGATIVE_NO_SEPARATION_DEMONSTRATED",
        "candidate_count": len(records),
        "k5_candidate_count": len(k5),
        "families_with_multiple_k5_profiles": multi,
        "matched_profiles": matches,
        "distinct_mechanism_matches": distinct_matches,
        "k5_records": [
            {
                key: record[key]
                for key in (
                    "name",
                    "diagnostic_profile",
                    "C",
                    "evaluation_failures",
                    "evaluation_score_raw",
                    "evaluation_score_equal_family",
                    "failure_count",
                )
            }
            for record in k5
        ],
    }
    output = ROOT / "audit" / "construction_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "candidate_count": result["candidate_count"],
        "k5_candidate_count": result["k5_candidate_count"],
        "multi_profile_families": len(result["families_with_multiple_k5_profiles"]),
        "matched_profiles": len(result["matched_profiles"]),
        "distinct_mechanism_matches": len(result["distinct_mechanism_matches"]),
    }, indent=2))
    return 0 if not result["distinct_mechanism_matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
