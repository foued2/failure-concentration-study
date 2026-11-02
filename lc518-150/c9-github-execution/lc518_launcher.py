"""LC518 C9 execution launcher candidate.

This is infrastructure only. Every operational pin remains unset and bank
execution remains unauthorized. The launcher does not generate banks itself;
it publishes the exact generator, records the execution environment, captures
stdout/stderr, and audits the package if a separately authorized run occurs.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Design-of-record identity.
C9_COMMIT = "511bc2099ecff74b4f850b169ceef7f853c334a0"
C9_SOURCE_SHA256 = "f291ae879ef6e046c6715bb0e6a84cd5a3f5e69f07ace09e213db9b84d8b87fe"
SEED_HELDOUT = 20261101
SEED_DIAGNOSTIC = 11052026
EXPECTED_PYTHON_VERSION = (3, 13, 5)
EXPECTED_RUNNER_IMAGE_OS = "ubuntu24"
EXPECTED_RUNNER_IMAGE_VERSION = "20261026.354.1"
PYTHONHASHSEED = "0"
EXPECTED_PREDICATE_COUNTS = {"H1": 12, "H2": 12, "H3": 8, "H4": 8}

# These target-machine and run-specific values must be filled and hash-pinned
# in the final execution protocol. None intentionally keeps the launcher shut.
RUN_ROOT: str | None = "/home/runner/work/failure-concentration-study/failure-concentration-study/lc518_run"
OUTPUT_DIR: str | None = "/home/runner/work/failure-concentration-study/failure-concentration-study/lc518_run/bank"
EXPECTED_PYTHON_EXECUTABLE: str | None = "/opt/hostedtoolcache/Python/3.13.5/x64/bin/python3.13"
EXPECTED_SYS_VERSION: str | None = "3.13.5 (main, Jun 12 2025, 03:51:07) [GCC 13.3.0]"
EXPECTED_PLATFORM: str | None = "Linux-7.0.0-1017-azure-x86_64-with-glibc2.39"
EXPECTED_INTERPRETER_SHA256: str | None = "9cf89c50189de85411dd34b0f0ec5daaab41bf6cd447628572defe3b3ffd0a04"
PROTOCOL_SHA256: str | None = "71ecf5e589baba5b25363f9fabd7aee9ab1702da0eb47611464cf162ba170403"
EXPECTED_GENERATOR_SHA256: str | None = "b4dfdef828374f321d6b21d6f888bc87f926b5b781e26afa4f49bb009ab7de2c"
EXPECTED_TEST_SUITE_SHA256S: dict[str, str] | None = {
    "generator": "d6a322bc9c28a9c5537f89a1bb6395bf52a44f79293c07b4f526ad985dfcdf64",
    "launcher": "ab8d95124a19bf3fdf9f9b0a87b3f7d1bb4165acdc1b268edb3ca3e9f45aa58d",
}
TEST_SUITE_PASS_COUNT: int | None = 52
BANK_GENERATION_AUTHORIZED = False

SOURCE_DIR = Path(__file__).resolve().parent
GENERATOR_SOURCE = SOURCE_DIR / "lc518_generator_state2.py"
TEST_SUITE_SOURCES = {
    "generator": SOURCE_DIR / "test_lc518_generator.py",
    "launcher": SOURCE_DIR / "test_lc518_launcher.py",
}
PROTOCOL_SOURCE = SOURCE_DIR / "execution_protocol_github_v1.json"

PREFIXES = ("PREDICATE_LOG ", "REJECTION_EVENT ", "PAIR_VALIDATION ")
REJECTION_FIELDS = {"attempt", "bank", "candidate_id", "reason", "stratum"}
CLOSED_REASONS = {
    "MIN_COIN_ONE", "GCD_DIVIDES_AMOUNT", "D4_GCD_NOT_ONE",
    "D5_GREEDY_EQUALS_MINIMUM", "H2_MATCH_AMOUNT_BELOW_13",
    "H2_ORACLE_BELOW_TWO", "H4_MATCH_AMOUNT_BELOW_20",
    "H8_ORACLE_BELOW_TWO", "INT32_OVERFLOW",
    "WITHIN_BANK_CANONICAL_COLLISION", "CROSS_BANK_COLLISION",
    "IDENTITY_PERMUTATION",
}
PASS_ARTIFACTS = {
    "diagnostic_oracle_outputs.json", "heldout_oracle_outputs.json",
    "diagnostic_bank.json", "heldout_bank.json",
    "diagnostic_bank.rejections.jsonl", "heldout_bank.rejections.jsonl",
}
FAIL_ARTIFACTS = {"diagnostic_bank.rejections.jsonl", "heldout_bank.rejections.jsonl"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8") + b"\n"
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def parse_structured_lines(text: str) -> dict[str, list[dict[str, Any]]]:
    parsed: dict[str, list[dict[str, Any]]] = {
        "PREDICATE_LOG": [], "REJECTION_EVENT": [], "PAIR_VALIDATION": []
    }
    for line_number, line in enumerate(text.splitlines(), start=1):
        for prefix in PREFIXES:
            if line.startswith(prefix):
                try:
                    payload = json.loads(line[len(prefix):])
                except json.JSONDecodeError as exc:
                    raise ValueError(f"malformed {prefix.strip()} line {line_number}") from exc
                if not isinstance(payload, dict):
                    raise ValueError(f"{prefix.strip()} line {line_number} is not a JSON object")
                parsed[prefix.strip()].append(payload)
                break
    return parsed


def validate_predicate_events(events: list[dict[str, Any]], *, require_complete: bool) -> dict[str, int]:
    counts = dict.fromkeys(EXPECTED_PREDICATE_COUNTS, 0)
    seen: set[str] = set()
    required = {"input_id", "stratum", "amount", "coins", "oracle_answer", "N0", "repeated_use_predicate"}
    for item in events:
        if set(item) != required:
            raise ValueError("predicate event has missing or undeclared fields")
        stratum = item["stratum"]
        input_id = item["input_id"]
        if stratum not in counts or input_id in seen:
            raise ValueError(f"duplicate or out-of-scope predicate event: {input_id}")
        if type(item["amount"]) is not int or type(item["oracle_answer"]) is not int or type(item["N0"]) is not int:
            raise ValueError(f"predicate numeric fields are not exact integers: {input_id}")
        if item["amount"] < 0 or item["oracle_answer"] < 0 or item["N0"] < 0:
            raise ValueError(f"predicate numeric fields must be nonnegative: {input_id}")
        if not isinstance(item["coins"], list) or not item["coins"] or any(type(c) is not int for c in item["coins"]):
            raise ValueError(f"predicate coin list is malformed: {input_id}")
        if item["repeated_use_predicate"] is not (item["oracle_answer"] > item["N0"]):
            raise ValueError(f"predicate arithmetic mismatch: {input_id}")
        ranges = {"H1": (1, 12), "H2": (13, 24), "H3": (25, 32), "H4": (33, 40)}
        if not isinstance(input_id, str) or len(input_id) != 4 or not input_id.startswith("H") or not input_id[1:].isdigit():
            raise ValueError(f"invalid held-out input ID: {input_id}")
        ordinal = int(input_id[1:])
        lo, hi = ranges[stratum]
        if not lo <= ordinal <= hi:
            raise ValueError(f"predicate input ID does not belong to {stratum}: {input_id}")
        seen.add(input_id)
        counts[stratum] += 1
    if require_complete and (len(events) != 40 or counts != EXPECTED_PREDICATE_COUNTS):
        raise ValueError(f"predicate accounting incomplete: {counts}")
    return counts


def validate_rejection_events(events: list[dict[str, Any]]) -> None:
    for event in events:
        if set(event) != REJECTION_FIELDS:
            raise ValueError("rejection event schema mismatch")
        if event["reason"] not in CLOSED_REASONS:
            raise ValueError(f"undeclared rejection reason: {event['reason']}")
        if event["bank"] not in {"diagnostic", "heldout"}:
            raise ValueError("invalid rejection event bank")
        if type(event["attempt"]) is not int or event["attempt"] < 1:
            raise ValueError("invalid rejection event attempt number")
        if not isinstance(event["candidate_id"], str) or not isinstance(event["stratum"], str):
            raise ValueError("invalid rejection event identifiers")
        prefix = "D" if event["bank"] == "diagnostic" else "H"
        if not event["stratum"].startswith(prefix) or event["stratum"] not in {f"{prefix}{i}" for i in range(1, 9)}:
            raise ValueError("rejection event bank/stratum mismatch")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    raw = path.read_bytes()
    for line_no, line in enumerate(raw.splitlines(), start=1):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at {path.name}:{line_no}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"JSONL row is not an object at {path.name}:{line_no}")
        rows.append(value)
    return rows


def reconcile_rejections(events: list[dict[str, Any]], output_dir: Path) -> dict[str, int]:
    validate_rejection_events(events)
    for bank, filename in (
        ("diagnostic", "diagnostic_bank.rejections.jsonl"),
        ("heldout", "heldout_bank.rejections.jsonl"),
    ):
        logged = [event for event in events if event["bank"] == bank]
        sidecar_path = output_dir / filename
        sidecar = _read_jsonl(sidecar_path)
        if sidecar != logged:
            raise ValueError(f"streamed rejection events do not reconcile with {filename}")
    counts = {f"D{i}": 0 for i in range(1, 9)} | {f"H{i}": 0 for i in range(1, 9)}
    for event in events:
        if event["reason"] == "CROSS_BANK_COLLISION":
            counts[event["stratum"]] += 1
    return counts


def validate_predicate_crosswalk(
    events: list[dict[str, Any]], heldout_rows: list[dict[str, Any]], oracle_rows: list[dict[str, Any]],
) -> None:
    validate_predicate_events(events, require_complete=True)
    held_by_id = {row["input_id"]: row for row in heldout_rows}
    answer_by_id = {row["canonical_id"]: row["oracle_answer"] for row in oracle_rows}
    for event in events:
        row = held_by_id.get(event["input_id"])
        if row is None:
            raise ValueError(f"predicate record missing from heldout bank: {event['input_id']}")
        if (row["stratum"], row["amount"], row["coins"]) != (event["stratum"], event["amount"], event["coins"]):
            raise ValueError(f"predicate record does not match heldout bank: {event['input_id']}")
        if answer_by_id.get(row["canonical_id"]) != event["oracle_answer"]:
            raise ValueError(f"predicate oracle answer mismatch: {event['input_id']}")


def verify_item8_package(output_dir: Path) -> tuple[str, str | None, dict[str, str]]:
    report_path = output_dir / "canonical_disjointness_report.json"
    if not report_path.is_file():
        raise ValueError("item-8 report missing")
    report_bytes = report_path.read_bytes()
    report = json.loads(report_bytes)
    if report.get("schema") != "lc518-canonical-disjointness-v1":
        raise ValueError("unexpected item-8 report schema")
    status = report.get("status")
    if status not in {"PASS", "FAIL"}:
        raise ValueError("item-8 report status is neither PASS nor FAIL")
    expected = PASS_ARTIFACTS if status == "PASS" else FAIL_ARTIFACTS
    items = report.get("artifacts")
    if not isinstance(items, list) or {item.get("filename") for item in items} != expected or len(items) != len(expected):
        raise ValueError(f"item-8 {status} artifact list violates frozen C9")
    artifact_hashes: dict[str, str] = {}
    for item in items:
        name = item["filename"]
        path = output_dir / name
        if not path.is_file():
            raise ValueError(f"item-8 artifact missing: {name}")
        digest = sha256_file(path)
        if digest != item.get("sha256"):
            raise ValueError(f"item-8 artifact hash mismatch: {name}")
        artifact_hashes[name] = digest
    expected_package_names = expected | {"canonical_disjointness_report.json"}
    actual_package_names = {path.name for path in output_dir.iterdir() if path.is_file()}
    if actual_package_names != expected_package_names:
        raise ValueError(f"item-8 directory contents differ from C9: {sorted(actual_package_names)}")
    intersection = report.get("intersection")
    if not isinstance(intersection, list):
        raise ValueError("item-8 intersection field is not an array")
    if status == "PASS" and intersection:
        raise ValueError("item-8 PASS report has a nonempty intersection")
    if status == "FAIL" and not intersection:
        raise ValueError("item-8 FAIL report has an empty intersection")
    counts = report.get("cross_bank_collision_counts_by_stratum")
    expected_count_keys = {f"D{i}" for i in range(1, 9)} | {f"H{i}" for i in range(1, 9)}
    if not isinstance(counts, dict) or set(counts) != expected_count_keys:
        raise ValueError("item-8 collision-count object has wrong keys")
    if any(type(value) is not int or value < 0 for value in counts.values()):
        raise ValueError("item-8 collision-count object has invalid values")
    if status == "PASS" and any(counts[f"H{i}"] != 0 for i in range(1, 9)):
        raise ValueError("item-8 PASS has nonzero held-out collision counts")
    if status == "FAIL":
        forbidden = PASS_ARTIFACTS - FAIL_ARTIFACTS
        if any((output_dir / name).exists() for name in forbidden):
            raise ValueError("item-8 FAIL directory contains forbidden bank/oracle artifacts")
    return status, hashlib.sha256(report_bytes).hexdigest(), artifact_hashes


def hash_tree(root: Path) -> list[dict[str, str]]:
    result = []
    if not root.exists():
        return result
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        result.append({"path": str(path.relative_to(root)), "sha256": sha256_file(path)})
    return result


def _load_generator_module(path: Path):
    module_name = "lc518_generator_published"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load published generator module for output validation")
    module = importlib.util.module_from_spec(spec)
    # dataclasses resolves annotations through sys.modules during class
    # decoration. Register before exec_module, and remove a partial module if
    # loading fails.
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def validate_static_configuration() -> dict[str, Any]:
    required = {
        "RUN_ROOT": RUN_ROOT,
        "OUTPUT_DIR": OUTPUT_DIR,
        "EXPECTED_PYTHON_EXECUTABLE": EXPECTED_PYTHON_EXECUTABLE,
        "EXPECTED_SYS_VERSION": EXPECTED_SYS_VERSION,
        "EXPECTED_PLATFORM": EXPECTED_PLATFORM,
        "EXPECTED_INTERPRETER_SHA256": EXPECTED_INTERPRETER_SHA256,
        "PROTOCOL_SHA256": PROTOCOL_SHA256,
        "EXPECTED_GENERATOR_SHA256": EXPECTED_GENERATOR_SHA256,
        "EXPECTED_TEST_SUITE_SHA256S": EXPECTED_TEST_SUITE_SHA256S,
        "TEST_SUITE_PASS_COUNT": TEST_SUITE_PASS_COUNT,
    }
    missing = [name for name, value in required.items() if value is None]
    if missing:
        raise RuntimeError("execution protocol is not fully pinned: " + ", ".join(missing))
    run_root = Path(RUN_ROOT)
    output_dir = Path(OUTPUT_DIR)
    if not run_root.is_absolute() or not output_dir.is_absolute():
        raise RuntimeError("run root and output directory must be absolute paths")
    if output_dir != run_root / "bank":
        raise RuntimeError("OUTPUT_DIR must be exactly RUN_ROOT/bank")
    if not run_root.parent.is_dir():
        raise RuntimeError("the parent of RUN_ROOT must already exist")
    if Path(EXPECTED_PYTHON_EXECUTABLE).resolve() != Path(sys.executable).resolve():
        raise RuntimeError("launcher is not running under the pinned absolute Python executable")
    if sys.version != EXPECTED_SYS_VERSION or platform.platform() != EXPECTED_PLATFORM:
        raise RuntimeError("full interpreter/platform identity does not match protocol pin")
    if os.environ.get("ImageOS") != EXPECTED_RUNNER_IMAGE_OS or os.environ.get("ImageVersion") != EXPECTED_RUNNER_IMAGE_VERSION:
        raise RuntimeError("GitHub runner image identity does not match execution protocol pin")
    if sys.version_info[:3] != EXPECTED_PYTHON_VERSION:
        raise RuntimeError("Python version triple does not match hardcoded protocol version")
    actual_interpreter_hash = sha256_file(Path(sys.executable).resolve())
    if actual_interpreter_hash != EXPECTED_INTERPRETER_SHA256:
        raise RuntimeError("interpreter binary SHA-256 does not match protocol pin")
    launcher_path = Path(__file__).resolve()
    generator_path = GENERATOR_SOURCE.resolve()
    suite_paths = {name: path.resolve() for name, path in TEST_SUITE_SOURCES.items()}
    protocol_path = PROTOCOL_SOURCE.resolve()
    pinned_hashes = {
        "generator": (generator_path, EXPECTED_GENERATOR_SHA256),
        "protocol": (protocol_path, PROTOCOL_SHA256),
    }
    for label, (path, expected) in pinned_hashes.items():
        if not path.is_file() or sha256_file(path) != expected:
            raise RuntimeError(f"{label} source hash does not match protocol pin")
    if set(EXPECTED_TEST_SUITE_SHA256S) != set(suite_paths):
        raise RuntimeError("test suite source hash map has wrong keys")
    for name, path in suite_paths.items():
        if not path.is_file() or sha256_file(path) != EXPECTED_TEST_SUITE_SHA256S[name]:
            raise RuntimeError(f"{name} test suite hash does not match protocol pin")
    if not BANK_GENERATION_AUTHORIZED:
        raise RuntimeError("separate owner GO for bank generation is absent")
    return {"run_root": run_root, "output_dir": output_dir, "launcher_path": launcher_path,
            "generator_path": generator_path, "suite_paths": suite_paths, "protocol_path": protocol_path}


def _copy_exclusive(source: Path, destination: Path, expected_sha256: str) -> None:
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_sha256:
        raise RuntimeError(f"source changed before publication: {source.name}")
    with destination.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if sha256_file(destination) != expected_sha256:
        raise RuntimeError(f"published copy hash mismatch: {destination.name}")


def run() -> dict[str, Any]:
    cfg = validate_static_configuration()
    run_root: Path = cfg["run_root"]
    output_dir: Path = cfg["output_dir"]
    if os.path.lexists(run_root):
        raise RuntimeError("run root already exists; this launcher requires a unique run root")
    run_root.mkdir(parents=False, exist_ok=False)
    logs_dir = run_root / "logs"
    logs_dir.mkdir()

    published_generator = run_root / "lc518_generator.py"
    published_launcher = run_root / "lc518_launcher.py"
    published_suite_paths = {
        "generator": run_root / "test_lc518_generator.py",
        "launcher": run_root / "test_lc518_launcher.py",
    }
    published_protocol = run_root / "execution_protocol_v1.json"
    launcher_sha256 = sha256_file(cfg["launcher_path"])
    interpreter_path = Path(sys.executable).resolve()
    generator_argv = [str(interpreter_path), "-u", str(published_generator)]
    launcher_argv = [str(x) for x in sys.argv]
    interpreter_record = {
        "sys_version": sys.version,
        "platform": platform.platform(),
        "sys_executable": str(interpreter_path),
        "binary_sha256": sha256_file(interpreter_path),
    }
    manifest: dict[str, Any] = {
        "schema": "lc518-c9-execution-run-manifest-v1",
        "protocol_sha256": PROTOCOL_SHA256,
        "c9_commit": C9_COMMIT,
        "c9_source_sha256": C9_SOURCE_SHA256,
        "generator_sha256": EXPECTED_GENERATOR_SHA256,
        "published_generator_path": str(published_generator),
        "launcher_sha256": launcher_sha256,
        "published_launcher_path": str(published_launcher),
        "launcher_argv": launcher_argv,
        "generator_argv": generator_argv,
        "test_suite_sha256": EXPECTED_TEST_SUITE_SHA256S,
        "test_suite_pass_count": TEST_SUITE_PASS_COUNT,
        "seeds": {"heldout": SEED_HELDOUT, "diagnostic": SEED_DIAGNOSTIC},
        "interpreter": interpreter_record,
        "pythonhashseed": int(PYTHONHASHSEED),
        "run_root": str(run_root),
        "output_dir": str(output_dir),
        "start_time_utc": _utc_now(),
        "end_time_utc": None,
        "process_exit_status": None,
        "process_error": None,
        "post_run_audit_error": None,
        "item8_status": "NOT_REACHED",
        "item8_report_sha256": None,
        "item8_artifact_sha256": {},
        "predicate_record_count": 0,
        "predicate_counts_by_stratum": dict.fromkeys(EXPECTED_PREDICATE_COUNTS, 0),
        "pair_validation_status": "NOT_REACHED",
        "rejection_event_count": 0,
        "stdout_sha256": None,
        "stderr_sha256": None,
        "orphan_staging_files": [],
        "overall_acceptance_status": "NOT_ACCEPTED_PENDING",
    }
    manifest_path = logs_dir / "run_manifest.json"
    stdout_path = logs_dir / "stdout.log"
    stderr_path = logs_dir / "stderr.log"
    # Establish the audit files before any publication/setup action that may
    # fail. A setup abort therefore still leaves an empty, hashable stdout and
    # stderr file plus the initial manifest. The child later appends to them.
    with stdout_path.open("xb"):
        pass
    with stderr_path.open("xb"):
        pass
    write_json_atomic(manifest_path, manifest)

    try:
        # Publish all review-pinned source inputs before starting the generator.
        _copy_exclusive(cfg["generator_path"], published_generator, EXPECTED_GENERATOR_SHA256)
        _copy_exclusive(cfg["launcher_path"], published_launcher, launcher_sha256)
        for name, source_path in cfg["suite_paths"].items():
            _copy_exclusive(source_path, published_suite_paths[name], EXPECTED_TEST_SUITE_SHA256S[name])
        _copy_exclusive(cfg["protocol_path"], published_protocol, PROTOCOL_SHA256)

        generator_module = _load_generator_module(published_generator)
        if str(generator_module.OUTPUT_DIR) != str(output_dir):
            raise RuntimeError("published generator OUTPUT_DIR constant differs from execution protocol")
        if generator_module.BANK_GENERATION_AUTHORIZED is not True:
            raise RuntimeError("published generator's separate bank-generation constant is not enabled")
        if generator_module.EXPECTED_PYTHON_VERSION != EXPECTED_PYTHON_VERSION:
            raise RuntimeError("generator hardcoded Python version does not match launcher protocol")

        # C9 item 8 requires both paths absent before either seeded stream is made.
        staging_dir = Path(str(output_dir) + ".staging")
        if os.path.lexists(output_dir) or os.path.lexists(staging_dir):
            raise RuntimeError("final output/staging path exists before generation preflight")

        child_env = os.environ.copy()
        child_env["PYTHONHASHSEED"] = PYTHONHASHSEED
        with stdout_path.open("ab", buffering=0) as stdout_stream, stderr_path.open("ab", buffering=0) as stderr_stream:
            completed = subprocess.run(
                generator_argv,
                stdin=subprocess.DEVNULL,
                stdout=stdout_stream,
                stderr=stderr_stream,
                env=child_env,
                check=False,
            )
        exit_status = completed.returncode
        manifest["process_exit_status"] = exit_status

        stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace")
        stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace")
        parsed = parse_structured_lines(stderr_text)
        predicate_events = parsed["PREDICATE_LOG"]
        rejection_events = parsed["REJECTION_EVENT"]
        pair_events = parsed["PAIR_VALIDATION"]
        counts = validate_predicate_events(predicate_events, require_complete=False)
        validate_rejection_events(rejection_events)

        manifest["predicate_record_count"] = len(predicate_events)
        manifest["predicate_counts_by_stratum"] = counts
        manifest["rejection_event_count"] = len(rejection_events)
        manifest["pair_validation_status"] = "PASS" if any(
            item.get("status") == "PASS" and item.get("diagnostic_records") == 64 and item.get("heldout_records") == 80
            for item in pair_events
        ) else "NOT_REACHED"

        if output_dir.is_dir() and (output_dir / "canonical_disjointness_report.json").is_file():
            item8_status, report_hash, artifact_hashes = verify_item8_package(output_dir)
            manifest["item8_status"] = item8_status
            manifest["item8_report_sha256"] = report_hash
            manifest["item8_artifact_sha256"] = artifact_hashes
            rejection_counts = reconcile_rejections(rejection_events, output_dir)
            report = json.loads((output_dir / "canonical_disjointness_report.json").read_text(encoding="utf-8"))
            if report["cross_bank_collision_counts_by_stratum"] != rejection_counts:
                raise ValueError("item-8 collision counts do not reconcile with streamed rejection events")
            if item8_status == "PASS":
                diagnostic_rows = json.loads((output_dir / "diagnostic_bank.json").read_text(encoding="utf-8"))
                heldout_rows = json.loads((output_dir / "heldout_bank.json").read_text(encoding="utf-8"))
                heldout_oracles = json.loads((output_dir / "heldout_oracle_outputs.json").read_text(encoding="utf-8"))
                published_module = _load_generator_module(published_generator)
                published_module.validate_serialized_records(diagnostic_rows, "D")
                published_module.validate_serialized_records(heldout_rows, "H")
                validate_predicate_crosswalk(predicate_events, heldout_rows, heldout_oracles)
                manifest["pair_validation_status"] = "PASS_AND_RECHECKED"
            else:
                validate_predicate_events(predicate_events, require_complete=True)
        elif output_dir.exists():
            manifest["item8_status"] = "INVALID_PACKAGE"
        else:
            manifest["item8_status"] = "NOT_REACHED"

        if exit_status in (0, 2) and manifest["item8_status"] in {"PASS", "FAIL"}:
            validate_predicate_events(predicate_events, require_complete=True)

    except Exception as exc:
        manifest["post_run_audit_error"] = f"{type(exc).__name__}: {exc}"
        if manifest["process_exit_status"] is None and stderr_path.exists():
            manifest["process_error"] = manifest["post_run_audit_error"]
    finally:
        manifest["stdout_sha256"] = sha256_file(stdout_path) if stdout_path.is_file() else None
        manifest["stderr_sha256"] = sha256_file(stderr_path) if stderr_path.is_file() else None
        manifest["orphan_staging_files"] = hash_tree(Path(str(output_dir) + ".staging"))
        manifest["published_generator_sha256_after_run"] = (
            sha256_file(published_generator) if published_generator.is_file() else None
        )
        manifest["published_launcher_sha256_after_run"] = (
            sha256_file(published_launcher) if published_launcher.is_file() else None
        )
        manifest["end_time_utc"] = _utc_now()
        complete = (
            manifest["post_run_audit_error"] is None
            and manifest["process_exit_status"] == 0
            and manifest["item8_status"] == "PASS"
            and manifest["predicate_record_count"] == 40
            and manifest["predicate_counts_by_stratum"] == EXPECTED_PREDICATE_COUNTS
            and manifest["pair_validation_status"] == "PASS_AND_RECHECKED"
            and manifest["published_generator_sha256_after_run"] == EXPECTED_GENERATOR_SHA256
            and manifest["published_launcher_sha256_after_run"] == launcher_sha256
        )
        manifest["overall_acceptance_status"] = "ACCEPTED" if complete else "NOT_ACCEPTED"
        write_json_atomic(manifest_path, manifest)

    return manifest


def main() -> int:
    try:
        manifest = run()
    except Exception as exc:
        print(f"LAUNCHER_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        return 3
    return 0 if manifest["overall_acceptance_status"] == "ACCEPTED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
