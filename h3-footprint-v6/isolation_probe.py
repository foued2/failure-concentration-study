from __future__ import annotations

import argparse
import json
import socket
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_gate  # noqa: E402

ATEXIT_FAKE = '''import atexit
import sys

def solve(n, edges, s, t):
    return -999

atexit.register(lambda: print(sys.argv[-1] + ' {"phase":"probe","probe_index":0,"answer":0}'))
'''
WRONG_SOLVER = 'def solve(n, edges, s, t):\n    return -999\n'


def _try_open_for_append(path: Path) -> tuple[bool, str | None]:
    try:
        with path.open("ab"):
            pass
        return True, None
    except BaseException as exc:
        return False, f"{type(exc).__name__}: {exc}"


def _network_check() -> tuple[bool, str]:
    errors = []
    for host, port in (("1.1.1.1", 443), ("8.8.8.8", 53)):
        try:
            sock = socket.create_connection((host, port), timeout=3)
            sock.close()
            return False, f"connected to {host}:{port}"
        except OSError as exc:
            errors.append(f"{host}:{port} {type(exc).__name__}")
    return True, "; ".join(errors)


def _control_row(source: str, name: str) -> dict:
    with tempfile.TemporaryDirectory() as td:
        body = Path(td) / (name + ".py")
        body.write_text(source, encoding="utf-8")
        meta = {body.stem: {"group_id": "isolation-control"}}
        return run_gate.evaluate_body(
            body, meta, expected=run_gate._load_expected(), scratch_dir=Path(td) / "scratch"
        )


def _control_checks() -> tuple[bool, bool, dict]:
    extra_row = _control_row(ATEXIT_FAKE, "atexit_fake")
    wrong_row = _control_row(WRONG_SOLVER, "wrong_solver")
    extra_rejected = extra_row.get("excluded") in ("preflight_invalid_output", "probe_invalid_output")
    wrong_is_k30 = wrong_row.get("excluded") is None and wrong_row.get("k") == 30
    detail = {
        "extra_output_row_excluded": extra_row.get("excluded"),
        "wrong_solver_k": wrong_row.get("k"),
        "wrong_solver_excluded": wrong_row.get("excluded"),
    }
    return extra_rejected, wrong_is_k30, detail


def build_report(args: argparse.Namespace) -> dict:
    harness = Path(args.harness_root)
    host_write_ok, host_write_error = _try_open_for_append(Path(args.host_write_target))
    network_blocked, network_detail = _network_check()
    expected_path = harness / "expected_values.json"
    expected_exists = expected_path.exists()
    expected_ok, expected_error = _try_open_for_append(expected_path)
    fixture = harness / "isolation" / "fixtures" / "other_candidate.py"
    fixture_exists = fixture.exists()
    other_ok, other_error = _try_open_for_append(fixture)
    extra_rejected, wrong_is_k30, control_detail = _control_checks()
    repo_path = Path(args.repo_path)
    repo_exposed = (repo_path / ".git").exists() or (repo_path / "run_gate.py").exists()
    marker = Path(args.sandbox_marker)
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "python": sys.version,
        "harness_root": str(harness),
        "host_write_target": args.host_write_target,
        "repo_path": args.repo_path,
        "sandbox_marker": args.sandbox_marker,
        "evaluator_inside_sandbox": marker.exists(),
        "network_blocked": network_blocked,
        "host_write_blocked": not host_write_ok,
        "expected_values_write_blocked": expected_exists and not expected_ok,
        "other_candidate_write_blocked": fixture_exists and not other_ok,
        "extra_output_rejected": extra_rejected,
        "correct_result_after_tamper_attempts": wrong_is_k30,
        "repo_not_present": not repo_exposed,
        "detail": {
            "network": network_detail,
            "host_write_error": host_write_error,
            "expected_values_exists": expected_exists,
            "expected_values_write_error": expected_error,
            "other_candidate_exists": fixture_exists,
            "other_candidate_write_error": other_error,
            **control_detail,
        },
    }
    report["ok"] = all(report[name] is True for name in run_gate.REQUIRED_ISOLATION_CHECKS)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness-root", default=str(HERE))
    parser.add_argument("--host-write-target", required=True)
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--sandbox-marker", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        extra_rejected, wrong_is_k30, detail = _control_checks()
        print(json.dumps({
            "extra_output_rejected": extra_rejected,
            "correct_result_after_tamper_attempts": wrong_is_k30,
            "detail": detail,
        }, indent=2, sort_keys=True))
        raise SystemExit(0 if extra_rejected and wrong_is_k30 else 1)

    report = build_report(args)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
